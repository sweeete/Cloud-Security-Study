"""均线金叉死叉策略"""
from typing import Optional
from .base import BaseStrategy


class MACrossStrategy(BaseStrategy):
    """均线交叉策略：短期均线上穿长期均线 = 买入信号，下穿 = 卖出信号"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.fast_period = config.get("fast_period", 7)     # 短期均线周期
        self.slow_period = config.get("slow_period", 25)    # 长期均线周期
        self._prev_fast = None
        self._prev_slow = None

    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        if not klines or len(klines) < self.slow_period + 1:
            return None

        current_price = klines[-1]["close"]
        fast_ma = indicators.get("ma7")
        slow_ma = indicators.get("ma25")

        if fast_ma is None or slow_ma is None:
            return {"action": "hold", "price": current_price, "amount": 0,
                    "reason": "指标数据不足"}

        signal = {"action": "hold", "price": current_price, "amount": 0, "reason": "无信号"}

        if self._prev_fast and self._prev_slow:
            # 金叉：短线上穿长线
            if self._prev_fast <= self._prev_slow and fast_ma > slow_ma:
                amount = self.config.get("trade_amount", 0.001)
                signal = {"action": "buy", "price": current_price, "amount": amount,
                          "reason": f"金叉信号: MA{self.fast_period}={fast_ma:.2f} 上穿 MA{self.slow_period}={slow_ma:.2f}"}
            # 死叉：短线下穿长线
            elif self._prev_fast >= self._prev_slow and fast_ma < slow_ma:
                amount = self.config.get("trade_amount", 0.001)
                signal = {"action": "sell", "price": current_price, "amount": amount,
                          "reason": f"死叉信号: MA{self.fast_period}={fast_ma:.2f} 下穿 MA{self.slow_period}={slow_ma:.2f}"}

        self._prev_fast = fast_ma
        self._prev_slow = slow_ma
        return signal
