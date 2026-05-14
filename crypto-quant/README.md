# CryptoQuant — 加密货币量化交易系统

> 个人专用的加密货币量化交易平台，支持传统策略和 AI 智能分析。

## 功能

- 🔐 **密码登录** — 本地存储，安全可控
- 📊 **行情看板** — 10 个主流币种实时行情 + K 线图
- 📈 **技术指标** — MA、RSI、MACD、布林带自动计算
- ⚙️ **量化策略** — 网格交易、均线金叉死叉、RSI、MACD
- 🤖 **AI 智能策略** — 接入 DeepSeek/OpenAI 等大模型，AI 分析行情自动交易
- 💰 **持仓管理** — 实时查看持仓盈亏
- 📋 **订单日志** — 完整交易记录

## 支持的币种

| # | 币种 | 交易对 |
|---|------|--------|
| 1 | Bitcoin | BTC/USDT |
| 2 | Ethereum | ETH/USDT |
| 3 | Solana | SOL/USDT |
| 4 | BNB | BNB/USDT |
| 5 | XRP | XRP/USDT |
| 6 | Dogecoin | DOGE/USDT |
| 7 | Cardano | ADA/USDT |
| 8 | Avalanche | AVAX/USDT |
| 9 | Chainlink | LINK/USDT |
| 10 | Polkadot | DOT/USDT |

## 支持的策略

| 策略 | 类型 | 说明 |
|------|------|------|
| 网格交易 | 传统 | 在价格区间内自动低买高卖，适合震荡行情 |
| 均线金叉死叉 | 传统 | 短期均线上穿长期买入，下穿卖出 |
| RSI 超买超卖 | 传统 | RSI<30 买入，RSI>70 卖出 |
| MACD 指标 | 传统 | MACD 金叉买入，死叉卖出 |
| AI 智能分析 | 🤖 AI | 接入大模型 API，分析行情后自动交易 |

## 安装与运行

```bash
# 1. 安装依赖
cd crypto-quant
pip install -r requirements.txt

# 2. 启动
cd backend
python3 main.py
```

访问 http://localhost:8888，首次使用设置密码即可登录。

## AI 策略配置

在「设置」中配置以下任意一种 LLM API Key：

| 提供商 | API 地址 | 模型示例 |
|--------|---------|---------|
| DeepSeek | https://api.deepseek.com | deepseek-chat |
| OpenAI | https://api.openai.com | gpt-4o-mini |

## 安全提示

- 交易使用 **交易所 API Key**（Binance/OKX），只开交易权限，不开提现
- 默认使用 **测试网 (testnet)** 模拟交易
- 所有数据存储在本地 SQLite，不上传任何服务器
- **绝对不要**把钱包私钥输入到任何地方
