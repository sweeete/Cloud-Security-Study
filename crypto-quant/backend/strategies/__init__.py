from .base import BaseStrategy
from .grid import GridStrategy
from .ma_cross import MACrossStrategy
from .rsi import RSIStrategy
from .macd_strat import MACDStrategy
from .llm_strategy import LLMStrategy

STRATEGY_REGISTRY = {
    "grid":       GridStrategy,
    "ma_cross":   MACrossStrategy,
    "rsi":        RSIStrategy,
    "macd":       MACDStrategy,
    "llm":        LLMStrategy,
}

STRATEGY_META = [
    {"id": "grid",     "name": "网格交易",       "desc": "在价格区间内自动低买高卖，适合震荡行情"},
    {"id": "ma_cross", "name": "均线金叉死叉",    "desc": "短期均线上穿长期均线买入，下穿卖出"},
    {"id": "rsi",      "name": "RSI 超买超卖",    "desc": "RSI < 30 超卖买入，RSI > 70 超买卖出"},
    {"id": "macd",     "name": "MACD 指标策略",   "desc": "MACD 金叉买入，死叉卖出"},
    {"id": "llm",      "name": "AI 智能分析",     "desc": "接入大模型 API，AI 分析行情自动交易（需 LLM Key）"},
]


def get_strategy(strategy_type: str, config: dict):
    cls = STRATEGY_REGISTRY.get(strategy_type)
    if cls:
        return cls(config)
    return None


def list_strategies():
    return STRATEGY_META
