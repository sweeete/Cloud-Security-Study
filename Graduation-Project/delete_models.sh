#!/bin/bash
# =============================================
# 删除所有已训练的模型文件
#
# 用法：
#   bash delete_models.sh
#
# 效果：清空 models/ 目录下的所有文件
#       下次运行 predict.py 前需要重新训练
# =============================================

MODELS_DIR="$(dirname "$0")/models"

if [ ! -d "$MODELS_DIR" ]; then
    echo "📂 models/ 目录不存在，无需删除"
    exit 0
fi

FILE_COUNT=$(ls -A "$MODELS_DIR" 2>/dev/null | wc -l)

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "📂 models/ 目录已为空"
    exit 0
fi

echo "⚠️  即将删除 models/ 目录中的 $FILE_COUNT 个文件..."
echo ""
echo "  文件列表:"
ls -1 "$MODELS_DIR" | while read f; do echo "    - $f"; done
echo ""

# 确认提示
read -p "  确认删除? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 已取消"
    exit 1
fi

rm -f "$MODELS_DIR"/*
echo "✅ 已删除 $FILE_COUNT 个模型文件"
