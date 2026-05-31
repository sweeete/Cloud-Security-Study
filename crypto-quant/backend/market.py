"""真实行情数据模块。

此模块只返回交易所真实数据。外部数据源不可用时抛出 MarketDataError，
由 API 层返回失败；不要生成或返回模拟行情。
"""
import ccxt
import httpx
import pandas as pd
import numpy as np
import time
import threading

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
CRYPTOCOMPARE_BASE_URL = "https://min-api.cryptocompare.com/data"

# ===== 缓存 =====
_cache = {"tickers": None, "tickers_time": 0, "klines": {}, "klines_time": {}}
CACHE_TTL = 15
_lock = threading.Lock()


class MarketDataError(RuntimeError):
    """行情源不可用或返回无效数据。"""


def _get_exchange():
    """使用 OKX 作为数据源（国内服务器可访问）"""
    exchange = ccxt.okx({
        "enableRateLimit": True,
        "timeout": 5000,
        "options": {"defaultType": "spot"},
    })
    return exchange


def _cryptocompare_get(path: str, params: dict) -> dict:
    url = f"{CRYPTOCOMPARE_BASE_URL}/{path}"
    with httpx.Client(timeout=8.0) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    if data.get("Response") == "Error":
        raise MarketDataError(data.get("Message", "CryptoCompare 返回错误"))
    return data


def _get_all_tickers_cryptocompare() -> list:
    fsyms = ",".join(coin["id"] for coin in SYMBOLS_LIST)
    data = _cryptocompare_get("pricemultifull", {"fsyms": fsyms, "tsyms": "USDT"})
    raw = data.get("RAW", {})
    results = []
    failures = []

    for coin in SYMBOLS_LIST:
        item = raw.get(coin["id"], {}).get("USDT")
        if not item or item.get("PRICE") is None:
            failures.append(f"{coin['id']}: empty ticker")
            continue
        results.append({
            "symbol": coin["id"],
            "name": coin["name"],
            "last": float(item["PRICE"]),
            "bid": None,
            "ask": None,
            "high": float(item.get("HIGH24HOUR") or 0),
            "low": float(item.get("LOW24HOUR") or 0),
            "volume": float(item.get("VOLUME24HOUR") or 0),
            "change": float(item.get("CHANGEPCT24HOUR") or 0),
            "timestamp": int(item.get("LASTUPDATE", time.time()) * 1000),
            "source": "cryptocompare",
        })

    if failures:
        raise MarketDataError("CryptoCompare 行情获取失败：" + "; ".join(failures))
    return results


def _get_ticker_cryptocompare(symbol: str) -> dict:
    data = _cryptocompare_get("pricemultifull", {"fsyms": symbol.upper(), "tsyms": "USDT"})
    item = data.get("RAW", {}).get(symbol.upper(), {}).get("USDT")
    if not item or item.get("PRICE") is None:
        raise MarketDataError(f"{symbol} 行情为空")
    return {
        "symbol": symbol.upper(),
        "last": float(item["PRICE"]),
        "change": float(item.get("CHANGEPCT24HOUR") or 0),
        "source": "cryptocompare",
    }


def _cryptocompare_history_params(symbol: str, timeframe: str, limit: int) -> tuple[str, dict]:
    if timeframe == "1m":
        path, aggregate = "v2/histominute", 1
    elif timeframe == "5m":
        path, aggregate = "v2/histominute", 5
    elif timeframe == "15m":
        path, aggregate = "v2/histominute", 15
    elif timeframe == "4h":
        path, aggregate = "v2/histohour", 4
    elif timeframe == "1d":
        path, aggregate = "v2/histoday", 1
    else:
        path, aggregate = "v2/histohour", 1

    return path, {
        "fsym": symbol.upper(),
        "tsym": "USDT",
        "limit": max(1, min(int(limit), 2000)),
        "aggregate": aggregate,
    }


def _get_klines_cryptocompare(symbol: str, timeframe: str, limit: int) -> list:
    path, params = _cryptocompare_history_params(symbol, timeframe, limit)
    data = _cryptocompare_get(path, params)
    rows = data.get("Data", {}).get("Data", [])
    result = [
        {
            "time": int(i["time"]),
            "open": float(i["open"]),
            "high": float(i["high"]),
            "low": float(i["low"]),
            "close": float(i["close"]),
            "volume": float(i.get("volumefrom") or 0),
        }
        for i in rows
        if i.get("close") is not None
    ]
    if not result:
        raise MarketDataError(f"{symbol} K 线为空")
    return result


def get_all_tickers() -> list:
    """只获取 10 个币种的真实行情。"""
    global _cache

    # 检查缓存
    if _cache["tickers"] and _cache["tickers_time"] > time.time() - CACHE_TTL:
        return _cache["tickers"]

    with _lock:
        # 双重检查
        if _cache["tickers"] and _cache["tickers_time"] > time.time() - CACHE_TTL:
            return _cache["tickers"]

        try:
            try:
                results = _get_all_tickers_cryptocompare()
            except Exception as first_error:
                exchange = _get_exchange()
                results = []
                failures = []
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
                                "source": "okx",
                            })
                        else:
                            failures.append(f"{coin['id']}: empty ticker")
                    except Exception as e:
                        failures.append(f"{coin['id']}: {e}")

                if failures:
                    raise MarketDataError(
                        f"CryptoCompare 失败: {first_error}; OKX 失败: " + "; ".join(failures)
                    )

            _cache["tickers"] = results
            _cache["tickers_time"] = time.time()
            return results

        except Exception as e:
            raise MarketDataError(str(e)) from e


def get_ticker(symbol: str) -> dict:
    """单个币种真实行情。"""
    pair = SYMBOLS.get(symbol.upper(), symbol)
    try:
        try:
            return _get_ticker_cryptocompare(symbol.upper())
        except Exception as first_error:
            try:
                exchange = _get_exchange()
                t = exchange.fetch_ticker(pair)
                if not t or not t.get("last"):
                    raise MarketDataError(f"{symbol} 行情为空")
                return {"symbol": symbol, "last": t["last"], "change": t.get("percentage", 0), "source": "okx"}
            except Exception as second_error:
                raise MarketDataError(f"CryptoCompare 失败: {first_error}; OKX 失败: {second_error}") from second_error
    except Exception as e:
        raise MarketDataError(str(e)) from e


def get_klines(symbol: str, timeframe: str = "1h", limit: int = 100) -> list:
    """真实 K 线数据。"""
    pair = SYMBOLS.get(symbol.upper(), symbol)
    tf = TIMEFRAMES.get(timeframe, "1h")
    cache_key = f"{pair}_{tf}_{limit}"

    if cache_key in _cache.get("klines", {}) and _cache.get("klines_time", {}).get(cache_key, 0) > time.time() - 30:
        return _cache["klines"][cache_key]

    try:
        try:
            result = _get_klines_cryptocompare(symbol.upper(), timeframe, limit)
        except Exception as first_error:
            try:
                exchange = _get_exchange()
                ohlcv = exchange.fetch_ohlcv(pair, tf, limit=limit)
                if not ohlcv:
                    raise MarketDataError(f"{symbol} K 线为空")
                result = [{"time": i[0]//1000, "open": float(i[1]), "high": float(i[2]),
                            "low": float(i[3]), "close": float(i[4]), "volume": float(i[5])} for i in ohlcv]
            except Exception as second_error:
                raise MarketDataError(f"CryptoCompare 失败: {first_error}; OKX 失败: {second_error}") from second_error

        if "klines" not in _cache:
            _cache["klines"] = {}
            _cache["klines_time"] = {}
        _cache["klines"][cache_key] = result
        _cache["klines_time"][cache_key] = time.time()
        return result
    except Exception as e:
        raise MarketDataError(str(e)) from e


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
