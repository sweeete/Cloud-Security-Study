#!/bin/bash
# CryptoQuant 启动脚本

echo "🚀 启动 CryptoQuant 量化交易系统..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 请先安装 Python 3.9+"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt -q

# 初始化数据库
echo "🗄️  初始化数据库..."
cd backend
python3 -c "from database import init_db; init_db()"

# 启动
echo "🌐 启动 Web 服务..."
echo "   访问地址: http://localhost:8888"
echo "   首次使用需设置登录密码"
python3 main.py
