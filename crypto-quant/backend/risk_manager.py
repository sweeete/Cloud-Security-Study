"""风控模块"""
import time
from datetime import datetime


class RiskManager:
    """风险管理器"""

    def __init__(self):
        self.max_drawdown = 0.15          # 最大回撤 15%
        self.max_position_size = 0.3      # 单币仓位不超过总资金的 30%
        self.daily_loss_limit = 0.10      # 每日最大亏损 10%
        self.max_orders_per_min = 5       # 每分钟最多 5 笔订单
        self._order_timestamps = []
        self._daily_pnl = 0
        self._initial_balance = 0
        self._current_balance = 0
        self._last_reset_day = datetime.now().day

    def set_balance(self, balance: float):
        """设置当前账户余额"""
        if self._initial_balance == 0:
            self._initial_balance = balance
        self._current_balance = balance
        self._check_daily_reset()

    def _check_daily_reset(self):
        """每日重置"""
        today = datetime.now().day
        if today != self._last_reset_day:
            self._daily_pnl = 0
            self._last_reset_day = today

    def check_order_rate(self) -> bool:
        """检查下单频率"""
        now = time.time()
        self._order_timestamps = [t for t in self._order_timestamps if now - t < 60]
        return len(self._order_timestamps) < self.max_orders_per_min

    def check_drawdown(self) -> tuple[bool, str]:
        """检查回撤"""
        if self._initial_balance == 0:
            return True, ""

        drawdown = (self._initial_balance - self._current_balance) / self._initial_balance
        if drawdown > self.max_drawdown:
            return False, f"最大回撤 {drawdown:.2%} 超过限制 {self.max_drawdown:.0%}"
        return True, ""

    def check_daily_loss(self) -> tuple[bool, str]:
        """检查日亏损限制"""
        if self._initial_balance == 0:
            return True, ""

        daily_loss_pct = abs(min(0, self._daily_pnl)) / self._initial_balance
        if daily_loss_pct > self.daily_loss_limit:
            return False, f"今日亏损 {daily_loss_pct:.2%} 超过限制 {self.daily_loss_limit:.0%}"
        return True, ""

    def can_trade(self, action: str, amount: float, price: float) -> tuple[bool, str]:
        """综合检查是否可以交易"""
        # 频率检查
        if not self.check_order_rate():
            return False, "下单频率过高"

        # 回撤检查
        ok, msg = self.check_drawdown()
        if not ok:
            return False, msg

        # 日亏损检查
        ok, msg = self.check_daily_loss()
        if not ok:
            return False, msg

        return True, "OK"

    def record_trade(self, action: str, cost: float):
        """记录交易"""
        self._order_timestamps.append(time.time())

        if action == "buy":
            self._daily_pnl -= cost
        elif action == "sell":
            self._daily_pnl += cost

    def get_status(self) -> dict:
        drawdown = 0
        if self._initial_balance > 0:
            drawdown = (self._initial_balance - self._current_balance) / self._initial_balance

        return {
            "initial_balance": round(self._initial_balance, 2),
            "current_balance": round(self._current_balance, 2),
            "drawdown": round(drawdown * 100, 2),
            "daily_pnl": round(self._daily_pnl, 2),
            "max_drawdown": self.max_drawdown,
            "daily_loss_limit": self.daily_loss_limit,
        }


risk_manager = RiskManager()
