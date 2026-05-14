"""MACD 指标策略"""
from typing import Optional
from .base import BaseStrategy


class MACDStrategy(BaseStrategy):
    """MACD 策略：MACD 线上穿信号线（金叉）买入，下穿（死叉）卖出"""

    def __init__(self, config: dict):
        super().__init__(config)
        self._prev_macd = None
        self._prev_signal = None

    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        if not klines:
            return None

        current_price = klines[-1]["close"]
        macd = indicators.get("macd")
        macd_signal = indicators.get("macd_signal")
        macd_hist = indicators.get("macd_hist")

        if macd is None or macd_signal is None:
            return {"action": "hold", "price": current_price, "amount": 0,
                    "reason": "MACD 数据不足"}

        signal = {"action": "hold", "price": current_price, "amount": 0, "reason": "无信号"}

        if self._prev_macd is not None and self._prev_signal is not None:
            # MACD 金叉：MACD 线上穿信号线
            if self._prev_macd <= self._prev_signal and macd > macd_signal:
                amount = self.config.get("trade_amount", 0.001)
                signal = {"action": "buy", "price": current_price, "amount": amount,
                          "reason": f"MACD 金叉: {self._prev_macd:.4f} → {macd:.4f} 上穿信号线 {macd_signal:.4f}"}

            # MACD 死叉：MACD 线下穿信号线
            elif self._prev_macd >= self._prev_signal and macd < macd_signal:
                amount = self.config.get("trade_amount", 0.001)
                signal = {"action": "sell", "price": current_price, "amount": amount,
                          "reason": f"MACD 死叉: {self._prev_macd:.4f} → {macd:.4f} 下穿信号线 {macd_signal:.4f}"}

        self._prev_macd = macd
        self._prev_signal = macd_signal
        return signal
