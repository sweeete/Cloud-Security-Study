"""行情数据模块 — 只获取 10 个主流币种，快速返回"""
import ccxt
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime

SYMBOLS = {
    "BTC":  "BTC/USDT", "ETH":  "ETH/USDT", "SOL":  "SOL/USDT",
    "BNB":  "BNB/USDT", "XRP":  "XRP/USDT", "DOGE": "DOGE/USDT",
    "ADA":  "ADA/USDT", "AVAX": "AVAX/USDT", "LINK": "LINK/USDT",
    "DOT":  "DOT/USDT",
}

SYMBOLS_LIST = [
    {"id": "BTC",  "name": "Bitcoin",      "pair": "BTC/USDT"},
    {"id": "ETH",  "name": "Ethereum",     "pair": "ETH/USDT"},
    {"id": "SOL",  "name": "Solana",       "pair": "SOL/USDT"},
    {"id": "BNB",  "name": "BNB",          "pair": "BNB/USDT"},
    {"id": "XRP",  "name": "Ripple",       "pair": "XRP/USDT"},
    {"id": "DOGE", "name": "Dogecoin",     "pair": "DOGE/USDT"},
    {"id": "ADA",  "name": "Cardano",      "pair": "ADA/USDT"},
    {"id": "AVAX", "name": "Avalanche",    "pair": "AVAX/USDT"},
    {"id": "LINK", "name": "Chainlink",    "pair": "LINK/USDT"},
    {"id": "DOT",  "name": "Polkadot",     "pair": "DOT/USDT"},
]

TIMEFRAMES = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h", "1d": "1d"}

# ===== 缓存 =====
_cache = {"tickers": None, "tickers_time": 0, "klines": {}, "klines_time": {}}
CACHE_TTL = 15
_lock = threading.Lock()


def _get_exchange():
    """使用 OKX 作为数据源（国内服务器可访问）"""
    exchange = ccxt.okx({
        "enableRateLimit": True,
        "timeout": 5000,
        "options": {"defaultType": "spot"},
    })
    return exchange


def get_all_tickers() -> list:
    """只获取 10 个币种的行情"""
    global _cache

    # 检查缓存
    if _cache["tickers"] and _cache["tickers_time"] > time.time() - CACHE_TTL:
        return _cache["tickers"]

    with _lock:
        # 双重检查
        if _cache["tickers"] and _cache["tickers_time"] > time.time() - CACHE_TTL:
            return _cache["tickers"]

        results = []
        failed_count = 0

        try:
            exchange = _get_exchange()

            for coin in SYMBOLS_LIST:
                try:
                    t = exchange.fetch_ticker(coin["pair"])
                    if t and t.get("last"):
                        results.append({
                            "symbol": coin["id"],
                            "name": coin["name"],
                            "last": t["last"],
                            "bid": t["bid"],
                            "ask": t["ask"],
                            "high": t["high"],
                            "low": t["low"],
                            "volume": t["baseVolume"],
                            "change": t.get("percentage", 0),
                            "timestamp": t["timestamp"],
                        })
                    else:
                        failed_count += 1
                        results.append({
                            "symbol": coin["id"], "name": coin["name"],
                            "last": None, "change": 0,
                        })
                except Exception as e:
                    failed_count += 1
                    results.append({
                        "symbol": coin["id"], "name": coin["name"],
                        "last": None, "change": 0,
                    })

            # 如果超过一半失败，直接用模拟数据
            if failed_count > 5:
                print(f"[market] {failed_count}/10 failed, using fallback data")
                results = _generate_fallback_data()

            _cache["tickers"] = results
            _cache["tickers_time"] = time.time()
            return results

        except Exception as e:
            print(f"[market] exchange completely failed: {e}")
            fallback = _generate_fallback_data()
            _cache["tickers"] = fallback
            _cache["tickers_time"] = time.time()
            return fallback


def _generate_fallback_data():
    """模拟数据（API 不可用时展示）"""
    base_prices = {
        "BTC": 65000, "ETH": 3200, "SOL": 150, "BNB": 580,
        "XRP": 0.55, "DOGE": 0.12, "ADA": 0.45, "AVAX": 35,
        "LINK": 15, "DOT": 7,
    }
    results = []
    for coin in SYMBOLS_LIST:
        base = base_prices.get(coin["id"], 100)
        results.append({
            "symbol": coin["id"], "name": coin["name"],
            "last": base, "bid": base * 0.999, "ask": base * 1.001,
            "high": base * 1.02, "low": base * 0.98,
            "volume": 50000, "change": 0.5,
            "timestamp": int(time.time() * 1000),
        })
    return results


def get_ticker(symbol: str) -> dict:
    """单个币种行情"""
    pair = SYMBOLS.get(symbol.upper(), symbol)
    try:
        exchange = _get_exchange()
        t = exchange.fetch_ticker(pair)
        return {"symbol": symbol, "last": t["last"], "change": t.get("percentage", 0)}
    except:
        return {"symbol": symbol, "last": None, "change": 0}


def get_klines(symbol: str, timeframe: str = "1h", limit: int = 100) -> list:
    """K 线数据"""
    pair = SYMBOLS.get(symbol.upper(), symbol)
    tf = TIMEFRAMES.get(timeframe, "1h")
    cache_key = f"{pair}_{tf}_{limit}"

    if cache_key in _cache.get("klines", {}) and _cache.get("klines_time", {}).get(cache_key, 0) > time.time() - 30:
        return _cache["klines"][cache_key]

    try:
        exchange = _get_exchange()
        ohlcv = exchange.fetch_ohlcv(pair, tf, limit=limit)
        result = [{"time": i[0]//1000, "open": float(i[1]), "high": float(i[2]),
                    "low": float(i[3]), "close": float(i[4]), "volume": float(i[5])} for i in ohlcv]

        if "klines" not in _cache:
            _cache["klines"] = {}
            _cache["klines_time"] = {}
        _cache["klines"][cache_key] = result
        _cache["klines_time"][cache_key] = time.time()
        return result
    except Exception as e:
        return {"error": str(e)}


def calculate_indicators(klines: list) -> dict:
    """计算技术指标"""
    if not klines or isinstance(klines, dict):
        return {}

    df = pd.DataFrame(klines)
    if len(df) < 5:
        return {}

    # MA
    df["ma7"] = df["close"].rolling(window=min(7, len(df)), min_periods=1).mean()
    df["ma25"] = df["close"].rolling(window=min(25, len(df)), min_periods=1).mean()
    df["ma99"] = df["close"].rolling(window=min(99, len(df)), min_periods=1).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=min(14, len(df)), min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df)), min_periods=1).mean()
    rs = gain / loss.replace(0, float('nan'))
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, min_periods=1).mean()
    ema26 = df["close"].ewm(span=26, min_periods=1).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, min_periods=1).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    # Bollinger
    bp = min(20, len(df))
    df["bb_mid"] = df["close"].rolling(window=bp, min_periods=1).mean()
    bb_std = df["close"].rolling(window=bp, min_periods=1).std()
    df["bb_upper"] = df["bb_mid"] + 2 * bb_std
    df["bb_lower"] = df["bb_mid"] - 2 * bb_std

    def sv(v):
        import math
        if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
            return None
        return round(float(v), 2)

    l = df.iloc[-1]
    return {
        "ma7": sv(l["ma7"]), "ma25": sv(l["ma25"]), "ma99": sv(l["ma99"]),
        "rsi": sv(l["rsi"]), "macd": round(float(l["macd"]), 6) if not (pd.isna(l["macd"]) or np.isinf(l["macd"])) else None,
        "macd_signal": round(float(l["macd_signal"]), 6) if not (pd.isna(l["macd_signal"]) or np.isinf(l["macd_signal"])) else None,
        "macd_hist": round(float(l["macd_hist"]), 6) if not (pd.isna(l["macd_hist"]) or np.isinf(l["macd_hist"])) else None,
        "bb_upper": sv(l["bb_upper"]), "bb_lower": sv(l["bb_lower"]),
    }
