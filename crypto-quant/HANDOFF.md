# CryptoQuant 项目交接文档

> 此文档供 AI 助手接手继续开发 CryptoQuant 量化交易系统。

## 一、项目概况

CryptoQuant 是一个个人使用的加密货币量化交易系统，包含：
- **后端**：Python FastAPI，端口 8888
- **前端**：Web UI（HTML + JS + lightweight-charts）
- **桌面客户端**：Python tkinter（Windows）

## 二、当前问题

### 问题 1：行情数据无法获取真实价格（已处理）

- 服务器在中国，`ccxt.binance()` 的 API 无法访问（或被墙）
- 已尝试改为 `ccxt.okx()`，但价格仍显示 `$—`
- 已改为优先使用 CryptoCompare 真实行情源，OKX 作为真实备选源
- 全部真实源失败时接口直接返回失败，不再返回模拟数据

**涉及的代码：**
- `backend/market.py` — 行情获取模块
- `_get_exchange()` 函数决定用哪个交易所

### 问题 2：K 线图不显示

- 前端 K 线图使用 `lightweight-charts` 库
- 日志显示 K 线数据 API 已返回 200（后端正常）
- 但浏览器中图表区域空白
- CDN 已从 unpkg 改为 jsdelivr
- **需要**：排查前端 chart 渲染问题

**涉及的代码：**
- `frontend/dashboard/index.html` — 引入 lightweight-charts
- `frontend/js/app.js` — `loadChart()` 函数

### 问题 3：Windows 桌面客户端 Token 获取

- Windows 客户端需要 Token 才能连接服务器
- 目前需要用户先打开浏览器登录，再从开发者工具取 Token
- **可以优化**：提供一个更简单的获取方式

## 三、项目结构

```
crypto-quant/
├── backend/
│   ├── main.py                 # FastAPI 入口 + 所有 API 路由
│   ├── auth.py                 # 密码登录 + JWT 认证
│   ├── config.py               # 配置管理
│   ├── database.py             # SQLite 数据库
│   ├── market.py               # 行情数据（CCXT）
│   ├── engine.py               # 策略引擎
│   ├── risk_manager.py         # 风控模块
│   └── strategies/
│       ├── __init__.py         # 策略注册
│       ├── base.py             # 策略基类
│       ├── grid.py             # 网格交易
│       ├── ma_cross.py         # 均线金叉死叉
│       ├── rsi.py              # RSI 超买超卖
│       ├── macd_strat.py       # MACD 策略
│       └── llm_strategy.py     # AI 智能分析（需 LLM Key）
├── frontend/
│   ├── index.html              # 登录页
│   ├── dashboard/index.html    # 主界面
│   ├── css/style.css           # 样式
│   └── js/
│       ├── api.js              # API 客户端
│       └── app.js              # 主逻辑
├── client/
│   └── crypto_quant_client.py  # Windows 桌面客户端
├── requirements.txt
├── start.sh
├── README.md
└── HANDOFF.md                  # ← 本文档
```

## 四、API 接口清单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/setup-status` | 是否首次使用 |
| POST | `/api/setup-password` | 设置密码 |
| POST | `/api/login` | 登录，返回 JWT Token |
| GET | `/api/market/tickers` | 10 个币种实时行情 |
| GET | `/api/market/ticker/{symbol}` | 单个币种行情 |
| GET | `/api/market/klines/{symbol}` | K 线数据 |
| GET | `/api/market/indicators/{symbol}` | 技术指标 |
| GET | `/api/market/symbols` | 支持的币种列表 |
| GET | `/api/strategies` | 策略列表 |
| POST | `/api/strategies` | 创建策略 |
| POST | `/api/strategies/{id}/toggle` | 启动/停止 |
| POST | `/api/strategies/{id}/run` | 执行一次 |
| DELETE | `/api/strategies/{id}` | 删除策略 |
| GET | `/api/portfolio` | 持仓 |
| GET | `/api/orders` | 订单历史 |
| GET | `/api/trade-logs` | 交易日志 |
| GET | `/api/engine/status` | 引擎状态 |
| GET | `/api/risk/status` | 风控状态 |
| POST | `/api/exchange/keys` | 设置交易所 API Key |
| POST | `/api/llm/keys` | 设置 LLM API Key |

## 五、需要优先处理的任务

### P0 - 紧急
1. [x] **修复行情数据源** — 让 `market.py` 能从国内服务器拉到真实价格
2. [ ] **修复 K 线图渲染** — 让浏览器页面能正常显示 K 线图

### P1 - 重要
3. [ ] 验证策略引擎能不能正常工作
4. [ ] AI 策略（`llm_strategy.py`）需要对接 DeepSeek API

### P2 - 优化
5. [ ] Windows 客户端的 Token 获取流程简化
6. [ ] 添加 binance 测试网支持（spot testnet）
7. [ ] 添加止损止盈风控

## 六、测试方式

启动后端：
```bash
cd ~/Cloud-Security-Study/crypto-quant/backend
python3 main.py
```

访问 `http://服务器IP:8888` 登录后测试。

## 七、当前服务器情况

- **服务器 IP**: 114.55.170.210
- **系统**: Linux, Python 3.10.12
- **项目路径**: `~/Cloud-Security-Study/crypto-quant/`
- **Git 仓库**: `https://github.com/sweeete/Cloud-Security-Study`
- **飞书已配置**: ✅ 可以推送消息
- **LLM 可用**: ✅ DeepSeek V4 Flash
