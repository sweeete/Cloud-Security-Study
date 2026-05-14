"""AI 智能分析策略 — 接入大模型 API 分析行情并自动交易"""
import json
import re
from typing import Optional
from openai import OpenAI
from .base import BaseStrategy


class LLMStrategy(BaseStrategy):
    """
    AI 策略：将行情数据 + 技术指标发给大模型，让 AI 决定买卖
    支持 OpenAI / DeepSeek / 任何兼容 OpenAI API 的模型
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.provider = config.get("provider", "deepseek")
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "deepseek-chat")
        self.base_url = config.get("base_url", "https://api.deepseek.com")
        self.prompt_template = config.get("prompt_template", self._default_prompt())
        self._client = None
        self._trade_history = []

    def _get_client(self) -> Optional[OpenAI]:
        if not self.api_key:
            return None
        if self._client is None:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

    def _default_prompt(self) -> str:
        return """你是一位专业的加密货币量化交易分析师。请根据以下市场数据和分析指标，给出交易建议。

当前持仓情况：
- 持仓数量: {position}
- 入场均价: {entry_price}
- 累计盈亏: {pnl}

最新行情：
- 当前价格: {current_price}
- 24h 最高: {high}
- 24h 最低: {low}
- 24h 成交量: {volume}

技术指标：
- MA7: {ma7}
- MA25: {ma25}
- MA99: {ma99}
- RSI(14): {rsi}
- MACD: {macd}
- MACD Signal: {macd_signal}
- MACD Histogram: {macd_histogram}
- Bollinger Upper: {bb_upper}
- Bollinger Lower: {bb_lower}

近期交易记录：
{trade_history}

请分析当前市场状况，并严格按以下 JSON 格式输出决策：
{
  "action": "buy" 或 "sell" 或 "hold",
  "reason": "详细分析理由（中文）",
  "confidence": 0-100 的置信度分数,
  "suggested_amount": "建议交易数量（占可用资金的百分比，0-100）"
}

注意：只输出 JSON，不要输出其他内容。"""

    def _build_prompt(self, klines: list, indicators: dict) -> str:
        if not klines:
            return ""

        last = klines[-1]
        current_price = last["close"]

        # 近期交易记录（最近 5 条）
        recent_trades = self._trade_history[-5:] if self._trade_history else []
        trade_str = "\n".join([
            f"- {t['time']}: {t['action'].upper()} {t['amount']}@{t['price']} ({t.get('reason', '')})"
            for t in recent_trades
        ]) if recent_trades else "暂无交易记录"

        return self.prompt_template.format(
            position=self.position,
            entry_price=self.entry_price or 0,
            pnl=round(self.pnl, 2),
            current_price=current_price,
            high=last.get("high", "N/A"),
            low=last.get("low", "N/A"),
            volume=last.get("volume", "N/A"),
            ma7=indicators.get("ma7", "N/A"),
            ma25=indicators.get("ma25", "N/A"),
            ma99=indicators.get("ma99", "N/A"),
            rsi=indicators.get("rsi", "N/A"),
            macd=indicators.get("macd", "N/A"),
            macd_signal=indicators.get("macd_signal", "N/A"),
            macd_histogram=indicators.get("macd_hist", "N/A"),
            bb_upper=indicators.get("bb_upper", "N/A"),
            bb_lower=indicators.get("bb_lower", "N/A"),
            trade_history=trade_str,
        )

    def analyze(self, klines: list, indicators: dict) -> Optional[dict]:
        if not klines:
            return None

        client = self._get_client()
        if not client:
            return {"action": "hold", "price": klines[-1]["close"], "amount": 0,
                    "reason": "❌ AI 策略：未配置 LLM API Key，请在设置中配置"}

        prompt = self._build_prompt(klines, indicators)
        current_price = klines[-1]["close"]

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位加密货币量化交易专家，严格按 JSON 格式输出交易决策。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
            )

            content = response.choices[0].message.content.strip()

            # 提取 JSON
            json_match = re.search(r'\{.*?\}', content, re.DOTALL)
            if not json_match:
                return {"action": "hold", "price": current_price, "amount": 0,
                        "reason": f"AI 响应格式异常: {content[:100]}"}

            decision = json.loads(json_match.group())

            action = decision.get("action", "hold")
            reason = decision.get("reason", "AI 未提供理由")
            confidence = decision.get("confidence", 50)
            suggested_pct = decision.get("suggested_amount", 0)

            if action not in ("buy", "sell", "hold"):
                action = "hold"

            # 根据置信度调整
            if confidence < 60:
                action = "hold"
                reason += f" [置信度 {confidence}%，低于 60% 阈值，自动保持]"

            amount = 0
            if action in ("buy", "sell"):
                base_amount = self.config.get("base_amount", 0.001)
                amount = round(base_amount * (suggested_pct / 100) if suggested_pct > 0 else base_amount, 6)

            # 记录交易历史
            from datetime import datetime
            self._trade_history.append({
                "time": datetime.now().strftime("%H:%M"),
                "action": action,
                "price": current_price,
                "amount": amount,
                "reason": reason,
            })

            return {
                "action": action,
                "price": current_price,
                "amount": amount,
                "reason": f"🤖 AI 分析: {reason}",
                "confidence": confidence,
            }

        except Exception as e:
            return {"action": "hold", "price": current_price, "amount": 0,
                    "reason": f"❌ AI 分析出错: {str(e)}"}
