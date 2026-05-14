"""RSI 超买超卖策略"""
from typing import Optional
from .base import BaseStrategy


class RSIStrategy(BaseStrategy):
    """RSI 指标策略：RSI < 超卖线买入，RSI > 超买线卖出"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.oversold = config.get("oversold", 30)      # 超卖线
        self.overbought = config.get("overbought", 70)  # 超买线
        self.rsi_period = config.get("rsi_period", 14)  # RSI 周期
        self._last_rsi = None

    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        if not klines:
            return None

        current_price = klines[-1]["close"]
        rsi = indicators.get("rsi")

        if rsi is None:
            return {"action": "hold", "price": current_price, "amount": 0,
                    "reason": "RSI 数据不足"}

        signal = {"action": "hold", "price": current_price, "amount": 0, "reason": "无信号"}

        # RSI 从超卖区回升 → 买入
        if self._last_rsi and self._last_rsi <= self.oversold and rsi > self.oversold:
            amount = self.config.get("trade_amount", 0.001)
            signal = {"action": "buy", "price": current_price, "amount": amount,
                      "reason": f"RSI 超卖回升: {self._last_rsi:.1f} → {rsi:.1f} (超卖线 {self.oversold})"}

        # RSI 从超买区回落 → 卖出
        elif self._last_rsi and self._last_rsi >= self.overbought and rsi < self.overbought:
            amount = self.config.get("trade_amount", 0.001)
            signal = {"action": "sell", "price": current_price, "amount": amount,
                      "reason": f"RSI 超买回落: {self._last_rsi:.1f} → {rsi:.1f} (超买线 {self.overbought})"}

        self._last_rsi = rsi
        return signal
