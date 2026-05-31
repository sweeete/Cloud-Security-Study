"""交易执行器。

没有交易所 API Key 时使用 paper 模式，只写本地订单和持仓。
配置 API Key 后通过 ccxt 提交市价单；测试网开关由配置控制。
"""
import ccxt

from config import get_exchange_config


class TradeExecutionError(RuntimeError):
    """交易所下单失败。"""


class TradeExecutor:
    def __init__(self):
        self._exchange = None
        self._cache_key = None

    def _get_exchange(self):
        cfg = get_exchange_config()
        api_key = cfg.get("apiKey", "")
        secret = cfg.get("secret", "")
        password = cfg.get("password", "")
        exchange_name = cfg.get("name", "binance")
        testnet = bool(cfg.get("testnet", True))

        if not api_key or not secret:
            return None

        cache_key = (exchange_name, api_key, secret, password, testnet)
        if self._exchange is not None and self._cache_key == cache_key:
            return self._exchange

        if not hasattr(ccxt, exchange_name):
            raise TradeExecutionError(f"不支持的交易所: {exchange_name}")

        exchange_cls = getattr(ccxt, exchange_name)
        params = {
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True,
            "timeout": 10000,
            "options": {"defaultType": "spot"},
        }
        if password:
            params["password"] = password

        exchange = exchange_cls(params)
        if testnet and hasattr(exchange, "set_sandbox_mode"):
            exchange.set_sandbox_mode(True)

        self._exchange = exchange
        self._cache_key = cache_key
        return exchange

    def execute_market_order(self, symbol: str, side: str, amount: float, fallback_price: float) -> dict:
        exchange = self._get_exchange()
        if exchange is None:
            return {
                "mode": "paper",
                "order_id": "",
                "status": "filled",
                "price": fallback_price,
                "amount": amount,
                "cost": fallback_price * amount,
                "raw": {},
            }

        try:
            order = exchange.create_market_order(symbol, side, amount)
        except Exception as e:
            raise TradeExecutionError(str(e)) from e

        filled = float(order.get("filled") or 0)
        price = float(order.get("average") or order.get("price") or fallback_price)
        cost = float(order.get("cost") or price * filled)
        status = order.get("status") or "submitted"

        return {
            "mode": "exchange",
            "order_id": str(order.get("id") or ""),
            "status": status,
            "price": price,
            "amount": filled,
            "cost": cost,
            "raw": order,
        }


trade_executor = TradeExecutor()
