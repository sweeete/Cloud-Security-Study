"""网格交易策略"""
import math
from typing import Optional
from .base import BaseStrategy


class GridStrategy(BaseStrategy):
    """网格交易：在价格区间内挂买单和卖单，吃震荡收益"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.lower_price = config.get("lower_price", 0.9)   # 网格下限（相对当前价的比例）
        self.upper_price = config.get("upper_price", 1.1)   # 网格上限
        self.grid_count = config.get("grid_count", 10)       # 网格数量
        self.investment = config.get("investment", 100)      # 总投资额 USDT
        self._grids = []
        self._init_grids()

    def _init_grids(self):
        """初始化网格价格"""
        self._grids = []
        step = (self.upper_price - self.lower_price) / self.grid_count
        for i in range(self.grid_count + 1):
            price = self.lower_price + i * step
            self._grids.append(round(price, 4))

    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        if not klines:
            return None

        current_price = klines[-1]["close"]

        if current_price < self.lower_price or current_price > self.upper_price:
            return {"action": "hold", "price": current_price, "amount": 0,
                    "reason": f"价格 {current_price:.2f} 超出网格范围 [{self.lower_price:.2f}, {self.upper_price:.2f}]"}

        signal = self._check_grid(current_price)
        return signal

    def _check_grid(self, price: float) -> dict:
        """检查是否触发网格交易"""
        for i, grid_price in enumerate(self._grids):
            if abs(price - grid_price) / grid_price < 0.001:
                mid_idx = len(self._grids) // 2
                per_grid_amount = self.investment / self.grid_count
                amount = per_grid_amount / price

                if i < mid_idx:
                    return {"action": "buy", "price": price, "amount": round(amount, 6),
                            "reason": f"网格买入（触发价 {price:.2f}，网格 {i+1}/{self.grid_count}）"}
                else:
                    return {"action": "sell", "price": price, "amount": round(amount, 6),
                            "reason": f"网格卖出（触发价 {price:.2f}，网格 {i+1}/{self.grid_count}）"}

        return {"action": "hold", "price": price, "amount": 0, "reason": "未触发网格"}

    def adjust_grid(self, current_price: float):
        """根据当前价格调整网格中心"""
        self.lower_price = current_price * self.config.get("lower_price", 0.9)
        self.upper_price = current_price * self.config.get("upper_price", 1.1)
        self._init_grids()
