#!/bin/bash
# ============================================================
# 一键运行所有实验脚本
# 按顺序执行：二分类 → 多分类 → 融合特征
# 输出保存到 experiments.log
# ============================================================

set -e  # 出错即停（可改为 set +e 跳过错误继续）

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$BASE_DIR/experiments.log"
START_TIME=$(date +%s)

echo "==========================================" | tee -a "$LOG_FILE"
echo "  DGA 检测实验 — 全自动运行" | tee -a "$LOG_FILE"
echo "  开始时间: $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 计数器
TOTAL=0
PASSED=0
FAILED=0

run_experiment() {
    local dir="$1"
    local script="$2"
    local label="$3"
    
    TOTAL=$((TOTAL + 1))
    SCRIPT_PATH="$BASE_DIR/code/$dir/$script"
    
    if [ ! -f "$SCRIPT_PATH" ]; then
        echo "  ⚠️  文件不存在: $SCRIPT_PATH" | tee -a "$LOG_FILE"
        return
    fi
    
    echo "" | tee -a "$LOG_FILE"
    echo "──────────────────────────────────────────" | tee -a "$LOG_FILE"
    echo "  [$TOTAL] $label" | tee -a "$LOG_FILE"
    echo "  脚本: $dir/$script" | tee -a "$LOG_FILE"
    echo "──────────────────────────────────────────" | tee -a "$LOG_FILE"
    
    # 记录开始时间
    SCRIPT_START=$(date +%s)
    
    # 运行脚本，同时输出到屏幕和日志
    cd "$BASE_DIR/code/$dir"
    if python3 "$script" 2>&1 | tee -a "$LOG_FILE"; then
        PASSED=$((PASSED + 1))
        SCRIPT_END=$(date +%s)
        DURATION=$((SCRIPT_END - SCRIPT_START))
        echo "" | tee -a "$LOG_FILE"
        echo "  ✅ 完成 ($DURATION 秒)" | tee -a "$LOG_FILE"
    else
        FAILED=$((FAILED + 1))
        SCRIPT_END=$(date +%s)
        DURATION=$((SCRIPT_END - SCRIPT_START))
        echo "" | tee -a "$LOG_FILE"
        echo "  ❌ 失败 ($DURATION 秒)" | tee -a "$LOG_FILE"
    fi
    
    cd "$BASE_DIR"
}

# ============================================================
# 第一阶段：二分类实验 (erfen)
# 顺序：统计默认 → 2-gram默认 → 2-4gram默认 → 统计Optuna → 2-gram Optuna → 2-4gram Optuna
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"
echo "  第一阶段：二分类 (Binary Classification)" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"

run_experiment "erfen" "feature_comp.py"       "二分类 | 统计特征 | 默认参数"
run_experiment "erfen" "2-gram_comp.py"         "二分类 | 2-gram   | 默认参数"
run_experiment "erfen" "2-4gram_comp.py"        "二分类 | 2-4gram  | 默认参数"
run_experiment "erfen" "optuna_feature_comp.py" "二分类 | 统计特征 | Optuna 调参 (50次)"
run_experiment "erfen" "optuna_2-gram_comp.py"  "二分类 | 2-gram   | Optuna 调参 (30次)"
run_experiment "erfen" "optuna_2-4gram_comp.py" "二分类 | 2-4gram  | Optuna 调参 (30次)" || true

# ============================================================
# 第二阶段：多分类实验 (duofen)
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"
echo "  第二阶段：多分类 (Multi Classification)" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"

run_experiment "duofen" "feature_comp.py"         "多分类 | 统计特征 | 默认参数"
run_experiment "duofen" "2-gram_comp.py"           "多分类 | 2-gram   | 默认参数"
run_experiment "duofen" "2-4gram_comp.py"          "多分类 | 2-4gram  | 默认参数"
run_experiment "duofen" "optuna_feature_comp.py"   "多分类 | 统计特征 | Optuna 调参 (50次)"
run_experiment "duofen" "optuna_2-gram_comp.py"    "多分类 | 2-gram   | Optuna 调参 (30次)"
run_experiment "duofen" "optuna_2_4gram_comp.py"   "多分类 | 2-4gram  | Optuna 调参 (30次)"

# ============================================================
# 第三阶段：融合特征实验 (ronghe)
# 注：ronghe 目录下有 erfen_ 和 duofen_ 两种前缀
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"
echo "  第三阶段：融合特征 (Fusion)" | tee -a "$LOG_FILE"
echo "══════════════════════════════════════════════" | tee -a "$LOG_FILE"

# 二分类融合
run_experiment "ronghe" "erfen_feature+2-gram_comp.py"           "融合二分类 | 统计+2-gram   | 默认参数"
run_experiment "ronghe" "erfen_feature_2-4gram_comp.py"          "融合二分类 | 统计+2-4gram  | 默认参数"
run_experiment "ronghe" "erfen_optuna_feature+2_gram_comp.py"    "融合二分类 | 统计+2-gram   | Optuna (30次)"
run_experiment "ronghe" "erfen_optuna_feature+2-4gram_comp.py"   "融合二分类 | 统计+2-4gram  | Optuna (30次)"

# 多分类融合
run_experiment "ronghe" "duofen_feature+2_gram_comp.py"          "融合多分类 | 统计+2-gram   | 默认参数"
run_experiment "ronghe" "duofen_feature+2-4gram_comp.py"         "融合多分类 | 统计+2-4gram  | 默认参数"
run_experiment "ronghe" "duofen_optuna_feature+2_gram_comp.py"   "融合多分类 | 统计+2-gram   | Optuna (30次)"
run_experiment "ronghe" "duofen_optuna_feature+2-4gram_comp.py"  "融合多分类 | 统计+2-4gram  | Optuna (30次)"

# ============================================================
# 完成
# ============================================================
END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo "" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "  全部实验结束" | tee -a "$LOG_FILE"
echo "  完成时间: $(date)" | tee -a "$LOG_FILE"
echo "  总耗时: $((TOTAL_DURATION / 60)) 分 $((TOTAL_DURATION % 60)) 秒" | tee -a "$LOG_FILE"
echo "  总实验数: $TOTAL | 通过: $PASSED | 失败: $FAILED" | tee -a "$LOG_FILE"
echo "  日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
