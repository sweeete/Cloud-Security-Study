#!/bin/bash
# =============================================
# 训练模型 — 依次运行两个训练脚本
#
# 用法：
#   bash train_models.sh
#
# 训练完成后，models/ 目录下会生成：
#   erfen_fusion_model.json       二分类模型
#   erfen_vectorizer.pkl          二分类向量化器
#   erfen_metrics.json            二分类评估指标
#   duofen_fusion_model.json      多分类模型
#   duofen_vectorizer.pkl         多分类向量化器
#   duofen_label_encoder.pkl      多分类标签编码器
#   duofen_metrics.json           多分类评估指标
#
# 预计耗时：二分类约 1 分钟，多分类约 2 分钟
# =============================================

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
TRAIN_DIR="$BASE_DIR/code/ronghe"
START_TIME=$(date +%s)

echo "=========================================="
echo "  开始训练 DGA 检测模型"
echo "=========================================="
echo ""
echo "📁 训练脚本目录: $TRAIN_DIR"
echo "📁 模型保存目录: $BASE_DIR/models/"
echo ""

# ---------- 二分类模型 ----------
echo "══════════════════════════════════════════"
echo "  Step 1/2: 训练二分类模型"
echo "  (统计特征 + 2-gram + Optuna)"
echo "══════════════════════════════════════════"
echo ""

cd "$TRAIN_DIR"
python3 erfen_optuna_feature+2_gram_comp.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 二分类模型训练失败！"
    exit 1
fi
echo ""
echo "✅ 二分类模型训练完成"
echo ""

# ---------- 多分类模型 ----------
echo "══════════════════════════════════════════"
echo "  Step 2/2: 训练多分类模型"
echo "  (统计特征 + 2-gram + Optuna)"
echo "══════════════════════════════════════════"
echo ""

python3 duofen_optuna_feature+2_gram_comp.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 多分类模型训练失败！"
    exit 1
fi
echo ""
echo "✅ 多分类模型训练完成"
echo ""

# ---------- 完成 ----------
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

cd "$BASE_DIR"
echo "=========================================="
echo "  🎉 全部模型训练完成！"
echo "  总耗时: $((DURATION / 60)) 分 $((DURATION % 60)) 秒"
echo "=========================================="
echo ""
echo "  生成的模型文件:"
ls -lh "$BASE_DIR/models/" | tail -n +2 | while read line; do
    echo "    $line"
done
echo ""
echo "  现在可以运行预测工具了："
echo "    python3 predict.py"
echo ""
