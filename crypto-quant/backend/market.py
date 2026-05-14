"""行情数据模块 — 使用 CCXT 从交易所获取实时数据"""
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

# 10 个主流加密货币的交易对
SYMBOLS = {
    "BTC":  "BTC/USDT",
    "ETH":  "ETH/USDT",
    "SOL":  "SOL/USDT",
    "BNB":  "BNB/USDT",
    "XRP":  "XRP/USDT",
    "DOGE": "DOGE/USDT",
    "ADA":  "ADA/USDT",
    "AVAX": "AVAX/USDT",
    "LINK": "LINK/USDT",
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

TIMEFRAMES = {
    "1m":  "1m",
    "5m":  "5m",
    "15m": "15m",
    "1h":  "1h",
    "4h":  "4h",
    "1d":  "1d",
}

_exchange = None


def _get_exchange():
    """获取或创建交易所实例（公开数据，无需 API Key）"""
    global _exchange
    if _exchange is None:
        _exchange = ccxt.binance({
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        })
    return _exchange


def get_ticker(symbol: str) -> dict:
    """获取单个币种的最新行情"""
    ex = _get_exchange()
    pair = SYMBOLS.get(symbol.upper(), symbol)
    try:
        ticker = ex.fetch_ticker(pair)
        return {
            "symbol": symbol,
            "last": ticker["last"],
            "bid": ticker["bid"],
            "ask": ticker["ask"],
            "high": ticker["high"],
            "low": ticker["low"],
            "volume": ticker["baseVolume"],
            "change": ticker.get("percentage", 0),
            "timestamp": ticker["timestamp"],
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def get_all_tickers() -> list:
    """获取所有 10 个币种的行情"""
    results = []
    for coin in SYMBOLS_LIST:
        data = get_ticker(coin["id"])
        data["name"] = coin["name"]
        results.append(data)
    return results


def get_klines(symbol: str, timeframe: str = "1h", limit: int = 100) -> list:
    """获取 K 线数据"""
    ex = _get_exchange()
    pair = SYMBOLS.get(symbol.upper(), symbol)

    tf = TIMEFRAMES.get(timeframe, "1h")
    try:
        ohlcv = ex.fetch_ohlcv(pair, tf, limit=limit)
        result = []
        for item in ohlcv:
            result.append({
                "time": item[0] // 1000,  # 秒级时间戳
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
            })
        return result
    except Exception as e:
        return {"error": str(e)}


def get_orderbook(symbol: str, limit: int = 10) -> dict:
    """获取订单簿"""
    ex = _get_exchange()
    pair = SYMBOLS.get(symbol.upper(), symbol)
    try:
        ob = ex.fetch_order_book(pair, limit)
        return {
            "bids": ob["bids"][:limit],
            "asks": ob["asks"][:limit],
            "timestamp": ob["timestamp"],
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_indicators(klines: list) -> dict:
    """计算常用技术指标"""
    if not klines or isinstance(klines, dict):
        return {}

    df = pd.DataFrame(klines)

    # MA
    df["ma7"] = df["close"].rolling(window=7).mean()
    df["ma25"] = df["close"].rolling(window=25).mean()
    df["ma99"] = df["close"].rolling(window=99).mean()

    # RSI (14)
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12).mean()
    ema26 = df["close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    # Bollinger Bands
    df["bb_mid"] = df["close"].rolling(window=20).mean()
    bb_std = df["close"].rolling(window=20).std()
    df["bb_upper"] = df["bb_mid"] + 2 * bb_std
    df["bb_lower"] = df["bb_mid"] - 2 * bb_std

    latest = df.iloc[-1]
    return {
        "ma7": round(float(latest["ma7"]), 2) if not pd.isna(latest["ma7"]) else None,
        "ma25": round(float(latest["ma25"]), 2) if not pd.isna(latest["ma25"]) else None,
        "ma99": round(float(latest["ma99"]), 2) if not pd.isna(latest["ma99"]) else None,
        "rsi": round(float(latest["rsi"]), 2) if not pd.isna(latest["rsi"]) else None,
        "macd": round(float(latest["macd"]), 6) if not pd.isna(latest["macd"]) else None,
        "macd_signal": round(float(latest["macd_signal"]), 6) if not pd.isna(latest["macd_signal"]) else None,
        "macd_hist": round(float(latest["macd_hist"]), 6) if not pd.isna(latest["macd_hist"]) else None,
        "bb_upper": round(float(latest["bb_upper"]), 2) if not pd.isna(latest["bb_upper"]) else None,
        "bb_lower": round(float(latest["bb_lower"]), 2) if not pd.isna(latest["bb_lower"]) else None,
    }
