"""策略基类"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseStrategy(ABC):
    """所有量化策略的基类"""

    def __init__(self, config: dict):
        self.config = config
        self.name = config.get("name", "Unnamed")
        self.symbol = config.get("symbol", "BTC/USDT")
        self.side = config.get("side", "both")  # long / short / both
        self.interval = config.get("interval", "1h")
        self.position = 0  # 当前持仓数量
        self.entry_price = 0  # 入场价格
        self.pnl = 0  # 累计盈亏

    @abstractmethod
    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        """
        分析市场数据，返回交易信号
        返回: {"action": "buy"|"sell"|"hold", "price": float, "amount": float, "reason": str}
        """
        pass

    def on_trade(self, action: str, price: float, amount: float):
        """成交回调，更新持仓"""
        if action == "buy":
            total_cost = self.position * self.entry_price + amount * price
            self.position += amount
            self.entry_price = total_cost / self.position if self.position > 0 else price
        elif action == "sell":
            self.pnl += (price - self.entry_price) * min(amount, self.position)
            self.position -= min(amount, self.position)
            if self.position <= 0:
                self.position = 0
                self.entry_price = 0

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "position": self.position,
            "entry_price": self.entry_price,
            "pnl": round(self.pnl, 4),
            "config": self.config,
        }
