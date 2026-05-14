#!/usr/bin/env python3
"""
CryptoQuant — 加密货币量化交易系统
后端入口：FastAPI + WebSocket 实时推送
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from config import load_config, save_config, set_exchange_keys, set_llm_keys, is_first_run
from database import init_db
from auth import (
    hash_password, verify_password, set_initial_password,
    create_access_token, verify_token, check_first_run
)
from market import (
    get_all_tickers, get_ticker, get_klines, get_orderbook,
    calculate_indicators, SYMBOLS_LIST
)
from strategies import list_strategies, get_strategy, STRATEGY_META
from engine import engine
from risk_manager import risk_manager
from database import (
    save_strategy, get_strategies, update_strategy,
    delete_strategy, get_orders, get_trade_logs,
    get_portfolio, log_trade
)

app = FastAPI(title="CryptoQuant", version="1.0.0")

# 安全认证
security = HTTPBearer(auto_error=False)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 数据模型 ===

class LoginRequest(BaseModel):
    username: str
    password: str

class SetPasswordRequest(BaseModel):
    password: str

class ExchangeKeyRequest(BaseModel):
    apiKey: str
    secret: str
    password: Optional[str] = ""
    testnet: Optional[bool] = True

class LLMKeyRequest(BaseModel):
    provider: str
    apiKey: str
    model: str

class StrategyRequest(BaseModel):
    name: str
    type: str
    symbol: str
    side: Optional[str] = "both"
    config: dict = {}

class StrategyUpdateRequest(BaseModel):
    enabled: Optional[int] = None
    config: Optional[dict] = None

# === 认证中间件 ===

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="请先登录")
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    return payload

# === 路由 ===

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "CryptoQuant"}


# ----- 认证 -----

@app.get("/api/setup-status")
def setup_status():
    """检查是否首次使用"""
    return {"firstRun": check_first_run()}


@app.post("/api/setup-password")
def setup_password(req: SetPasswordRequest):
    """首次设置密码"""
    if not check_first_run():
        raise HTTPException(status_code=400, detail="密码已设置")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少 6 位")
    set_initial_password(req.password)
    return {"ok": True, "message": "密码设置成功"}


@app.post("/api/login")
def login(req: LoginRequest):
    """登录"""
    cfg = load_config()
    stored_hash = cfg.get("app", {}).get("password_hash", "")
    if not stored_hash:
        raise HTTPException(status_code=400, detail="请先设置密码")

    if not verify_password(req.password, stored_hash):
        raise HTTPException(status_code=401, detail="密码错误")

    token = create_access_token(req.username)
    return {"ok": True, "token": token, "username": req.username}


# ----- 交易所配置 -----

@app.get("/api/exchange/status", dependencies=[Depends(require_auth)])
def exchange_status():
    """交易所连接状态"""
    cfg = load_config()
    ex = cfg.get("exchange", {})
    if ex.get("apiKey"):
        return {"configured": True, "exchange": ex.get("name"), "testnet": ex.get("testnet", True)}
    return {"configured": False}


@app.post("/api/exchange/keys", dependencies=[Depends(require_auth)])
def set_keys(req: ExchangeKeyRequest):
    """设置交易所 API Key"""
    set_exchange_keys(req.apiKey, req.secret, req.password, req.testnet)
    return {"ok": True, "message": "API Key 已保存"}


# ----- LLM 配置 -----

@app.post("/api/llm/keys", dependencies=[Depends(require_auth)])
def set_llm(req: LLMKeyRequest):
    """设置 LLM API Key"""
    set_llm_keys(req.provider, req.apiKey, req.model)
    return {"ok": True, "message": "LLM API Key 已保存"}


@app.get("/api/llm/status", dependencies=[Depends(require_auth)])
def llm_status():
    """LLM 配置状态"""
    cfg = load_config()
    llm = cfg.get("llm", {})
    if llm.get("apiKey"):
        return {
            "configured": True,
            "provider": llm.get("provider"),
            "model": llm.get("model"),
        }
    return {"configured": False}


# ----- 行情数据 -----

@app.get("/api/market/tickers")
def all_tickers():
    """获取所有币种行情"""
    return get_all_tickers()


@app.get("/api/market/ticker/{symbol}")
def single_ticker(symbol: str):
    """获取单个币种行情"""
    return get_ticker(symbol.upper())


@app.get("/api/market/klines/{symbol}")
def klines(symbol: str, timeframe: str = "1h", limit: int = 100):
    """获取 K 线数据"""
    return get_klines(symbol.upper(), timeframe, limit)


@app.get("/api/market/orderbook/{symbol}")
def orderbook(symbol: str, limit: int = 10):
    """获取订单簿"""
    return get_orderbook(symbol.upper(), limit)


@app.get("/api/market/indicators/{symbol}")
def indicators(symbol: str, timeframe: str = "1h", limit: int = 100):
    """获取技术指标"""
    klines_data = get_klines(symbol.upper(), timeframe, limit)
    if isinstance(klines_data, dict) and "error" in klines_data:
        return klines_data
    return calculate_indicators(klines_data)


@app.get("/api/market/symbols")
def symbols():
    """获取支持的币种列表"""
    return {"symbols": SYMBOLS_LIST}


# ----- 策略管理 -----

@app.get("/api/strategies/list-available")
def available_strategies():
    """可用的策略类型"""
    return {"strategies": STRATEGY_META}


@app.post("/api/strategies", dependencies=[Depends(require_auth)])
def create_strategy(req: StrategyRequest):
    """创建策略"""
    sid = save_strategy(req.name, req.type, req.symbol, req.side, req.config)
    return {"ok": True, "id": sid}


@app.get("/api/strategies", dependencies=[Depends(require_auth)])
def list_user_strategies():
    """获取用户的所有策略"""
    return {"strategies": get_strategies()}


@app.put("/api/strategies/{sid}", dependencies=[Depends(require_auth)])
def edit_strategy(sid: int, req: StrategyUpdateRequest):
    """更新策略"""
    kwargs = {}
    if req.enabled is not None:
        kwargs["enabled"] = req.enabled
    if req.config is not None:
        kwargs["config"] = req.config
    if kwargs:
        update_strategy(sid, **kwargs)
    return {"ok": True}


@app.delete("/api/strategies/{sid}", dependencies=[Depends(require_auth)])
def remove_strategy(sid: int):
    """删除策略"""
    delete_strategy(sid)
    return {"ok": True}


@app.post("/api/strategies/{sid}/toggle", dependencies=[Depends(require_auth)])
def toggle_strategy(sid: int):
    """启动/停止策略"""
    strategies = get_strategies()
    target = next((s for s in strategies if s["id"] == sid), None)
    if not target:
        raise HTTPException(status_code=404, detail="策略不存在")

    new_enabled = 0 if target["enabled"] else 1
    update_strategy(sid, enabled=new_enabled)

    if new_enabled:
        import json
        config = json.loads(target["config"]) if isinstance(target["config"], str) else target["config"]
        config["name"] = target["name"]
        config["symbol"] = target["symbol"]
        config["side"] = target["side"]
        engine.start_strategy(sid, target["type"], config)
        log_trade(sid, target["symbol"], "start", "策略已启动")
    else:
        engine.stop_strategy(sid)
        log_trade(sid, target["symbol"], "stop", "策略已停止")

    return {"ok": True, "enabled": bool(new_enabled)}


@app.post("/api/strategies/{sid}/run", dependencies=[Depends(require_auth)])
def run_strategy_once(sid: int):
    """手动执行一次策略"""
    result = engine.run_strategy_once(sid)
    return result


# ----- 持仓 & 订单 -----

@app.get("/api/portfolio", dependencies=[Depends(require_auth)])
def portfolio():
    """获取持仓"""
    return {"portfolio": get_portfolio()}


@app.get("/api/orders", dependencies=[Depends(require_auth)])
def orders(limit: int = 50):
    """获取订单历史"""
    return {"orders": get_orders(limit)}


@app.get("/api/trade-logs", dependencies=[Depends(require_auth)])
def trade_logs(limit: int = 100):
    """获取交易日志"""
    return {"logs": get_trade_logs(limit)}


# ----- 系统 -----

@app.get("/api/engine/status", dependencies=[Depends(require_auth)])
def engine_status():
    """引擎状态"""
    return engine.get_status()


@app.get("/api/risk/status", dependencies=[Depends(require_auth)])
def risk_status():
    """风控状态"""
    return risk_manager.get_status()


# ----- 前端静态文件 -----

import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


# === 启动 ===

if __name__ == "__main__":
    init_db()
    port = load_config().get("app", {}).get("port", 8888)
    print(f"🚀 CryptoQuant 启动成功！ http://localhost:{port}")
    print(f"📊 支持 {len(SYMBOLS_LIST)} 个主流币种")
    print(f"🤖 策略: 网格 / 均线 / RSI / MACD / AI 智能分析")
    uvicorn.run(app, host="0.0.0.0", port=port)
