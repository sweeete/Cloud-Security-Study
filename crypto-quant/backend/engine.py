"""策略引擎 — 定时执行策略并管理交易"""
import time
import threading
from datetime import datetime
from market import get_klines, calculate_indicators, MarketDataError
from strategies import get_strategy
from database import save_order, log_trade, update_portfolio, get_portfolio
from risk_manager import risk_manager
from executor import trade_executor, TradeExecutionError


class StrategyEngine:
    """策略引擎：管理所有运行中的策略"""

    def __init__(self):
        self._strategies = {}  # strategy_id -> strategy_instance
        self._running = False
        self._thread = None

    def start_strategy(self, strategy_id: int, strategy_type: str, config: dict):
        """启动一个策略"""
        strategy = get_strategy(strategy_type, config)
        if strategy:
            self._strategies[strategy_id] = strategy
            return True
        return False

    def stop_strategy(self, strategy_id: int):
        """停止一个策略"""
        if strategy_id in self._strategies:
            del self._strategies[strategy_id]

    def run_strategy_once(self, strategy_id: int) -> dict:
        """手动运行一次策略"""
        strategy = self._strategies.get(strategy_id)
        if not strategy:
            return {"error": "策略未运行"}

        try:
            symbol = strategy.symbol
            interval = strategy.interval

            # 获取行情数据
            klines = get_klines(symbol, interval, limit=100)

            # 计算指标
            indicators = calculate_indicators(klines)

            # 策略分析
            signal = strategy.analyze(klines, indicators)
            if not signal:
                return {"action": "hold", "reason": "无信号"}

            return signal

        except MarketDataError as e:
            log_trade(strategy_id, strategy.symbol, "error", str(e))
            return {"error": str(e)}
        except Exception as e:
            log_trade(strategy_id, strategy.symbol, "error", str(e))
            return {"error": str(e)}

    def _run_loop(self):
        """策略主循环"""
        while self._running:
            for sid, strategy in list(self._strategies.items()):
                try:
                    signal = self.run_strategy_once(sid)
                    if signal and signal.get("action") in ("buy", "sell"):
                        self._execute_signal(sid, strategy, signal)
                except Exception as e:
                    log_trade(sid, strategy.symbol, "error", str(e))

            time.sleep(60)  # 每分钟检查一次

    def _execute_signal(self, strategy_id: int, strategy, signal: dict):
        """执行交易信号"""
        action = signal["action"]
        price = signal["price"]
        amount = signal["amount"]
        reason = signal.get("reason", "")

        if amount <= 0:
            return

        cost = price * amount

        ok, risk_reason = risk_manager.can_trade(action, amount, price)
        if not ok:
            log_trade(strategy_id, strategy.symbol, "blocked", f"风控拒绝: {risk_reason}")
            return

        if action == "sell":
            portfolio = get_portfolio()
            current = next((p for p in portfolio if p["symbol"] == strategy.symbol), None)
            available = current["amount"] if current else strategy.position
            if available <= 0:
                log_trade(strategy_id, strategy.symbol, "blocked", "无可卖持仓")
                return
            amount = min(amount, available)
            cost = price * amount

        try:
            execution = trade_executor.execute_market_order(strategy.symbol, action, amount, price)
        except TradeExecutionError as e:
            log_trade(strategy_id, strategy.symbol, "error", f"下单失败: {e}")
            return

        fill_price = execution["price"]
        fill_amount = execution["amount"]
        fill_cost = execution["cost"]

        # 记录订单
        save_order(
            strategy_id=strategy_id,
            symbol=strategy.symbol,
            side=action,
            type_="market",
            price=fill_price,
            amount=fill_amount,
            cost=fill_cost,
            status=execution["status"],
            order_id=execution["order_id"],
        )

        if fill_amount <= 0:
            log_trade(strategy_id, strategy.symbol, "submitted", f"{reason} | 订单已提交但未确认成交")
            return

        # 更新策略持仓
        strategy.on_trade(action, fill_price, fill_amount)

        # 更新数据库持仓
        portfolio = get_portfolio()
        current = next((p for p in portfolio if p["symbol"] == strategy.symbol), None)
        if current:
            new_amount = current["amount"] + (fill_amount if action == "buy" else -fill_amount)
            new_avg = current["avg_price"]
            if action == "buy" and current["amount"] > 0:
                new_avg = (current["avg_price"] * current["amount"] + fill_cost) / new_amount if new_amount != 0 else 0
            elif new_amount <= 0:
                new_avg = 0
            update_portfolio(strategy.symbol, max(0, new_amount), new_avg)
        else:
            if action == "buy":
                update_portfolio(strategy.symbol, fill_amount, fill_price)

        risk_manager.record_trade(action, fill_cost)

        # 记录日志
        log_trade(strategy_id, strategy.symbol, action, f"{reason} | {execution['mode']} | 价格: {fill_price:.2f}, 数量: {fill_amount:.6f}, 金额: {fill_cost:.2f}")

    def start(self):
        """启动引擎（后台线程）"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """停止引擎"""
        self._running = False

    def get_status(self) -> dict:
        return {
            "running": self._running,
            "active_strategies": len(self._strategies),
            "strategies": {str(sid): s.get_status() for sid, s in self._strategies.items()},
        }


# 全局引擎实例
engine = StrategyEngine()
