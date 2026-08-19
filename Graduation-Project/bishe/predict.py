#!/usr/bin/env python3
"""
DGA 域名检测 — 交互式预测工具
===================================

功能：
  1. 二分类：输入域名，判断是「良性域名」还是「恶意域名（DGA）」
  2. 多分类：输入域名，判断它属于哪个 DGA 家族（如 Kraken、Shiotob 等）

底层模型：
  - 二分类 → erfen_optuna_feature+2_gram_comp.py 训练
  - 多分类 → duofen_optuna_feature+2_gram_comp.py 训练
  两个模型都是「统计特征 + 2-gram 融合 + Optuna 贝叶斯优化」

用法：
  python3 predict.py

首次使用前，必须先训练模型（只需跑一次）：
  cd code/ronghe
  python3 erfen_optuna_feature+2_gram_comp.py
  python3 duofen_optuna_feature+2_gram_comp.py
"""

import os, sys, math, pickle, json
from collections import Counter
from scipy.sparse import hstack    # 用于水平拼接稀疏矩阵（N-gram）+ 稠密矩阵（统计特征）
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier


# ===== 路径定义 =====
# BASE_DIR 是 predict.py 所在的目录（Graduation-Project/）
# MODEL_DIR 是 models/ 子目录，训练好的模型文件都保存在这里
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ============================================================
# 特征工程函数
# 与训练脚本（code/ronghe/ 下的文件）中的函数保持一致
# 训练时是在整个数据集上批量提取特征
# 预测时是逐条提取，逻辑完全相同
# ============================================================

def calculate_entropy(text):
    """
    计算域名的信息熵（香农熵）
    
    信息熵衡量字符串的随机程度：
      - 正常域名（如 google）：熵值较低，字符分布有规律
      - DGA 域名（如 xkz9f2a）：熵值较高，字符随机分布
    这是区分恶意/良性域名的关键统计特征之一。
    """
    if not text or not isinstance(text, str):
        return 0
    # 统计每个字符出现的频率
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    # 香农熵公式: H = -Σ p(x) * log₂(p(x))
    return -sum(p * math.log2(p) for p in probs)


def extract_stat_features_single(domain):
    """
    提取单个域名的 6 维统计特征
    
    这 6 个特征从不同角度描述域名的结构特性：
      1. f_len:          域名长度 — DGA 域名通常较长
      2. f_digit_ratio:  数字占比 — DGA 常含随机数字
      3. f_vowel_ratio:  元音占比 — 正常域名可读性强，元音多
      4. f_unique_chars: 唯一字符数 — DGA 字符集更大
      5. f_hyphen_ratio: 连字符占比 — 某些 DGA 含特殊字符
      6. f_entropy:      信息熵 — 随机字符串熵值高
    
    返回格式：shape=(1, 6) 的 numpy 数组，可与 N-gram 稀疏矩阵拼接
    """
    domain = domain.lower().strip()
    
    f_len = len(domain)
    # 数字占比：统计所有数字字符（0-9）的比例
    f_digit_ratio = sum(c.isdigit() for c in domain) / len(domain) if len(domain) > 0 else 0
    # 元音占比：统计 aeiou 的比例（不区分大小写，已转小写）
    f_vowel_ratio = sum(c in 'aeiou' for c in domain) / len(domain) if len(domain) > 0 else 0
    # 唯一字符数：set 去重后统计不同字符个数
    f_unique_chars = len(set(domain))
    # 连字符占比：统计 '-' 的比例
    f_hyphen_ratio = domain.count('-') / len(domain) if len(domain) > 0 else 0
    # 信息熵
    f_entropy = calculate_entropy(domain)
    
    # 返回形状为 (1, 6) 的二维数组
    return np.array([[f_len, f_digit_ratio, f_vowel_ratio,
                      f_unique_chars, f_hyphen_ratio, f_entropy]])


# ============================================================
# 模型加载函数
# ============================================================

def load_model(model_type):
    """
    从 models/ 目录加载训练好的模型和相关组件
    
    参数：
      model_type: "binary" 或 "multiclass"
    
    返回：
      (model, vectorizer, metrics)
      - model:      训练好的 XGBoost 分类器
      - vectorizer: 训练好的 CountVectorizer（用于将域名转为 N-gram 特征向量）
      - metrics:    模型在测试集上的评估指标（准确率、F1 等）
    
    如果模型文件不存在，会提示用户先运行训练脚本。
    """
    # 根据模式选择对应的文件路径
    if model_type == "binary":
        model_path = os.path.join(MODEL_DIR, "erfen_fusion_model.json")
        vec_path = os.path.join(MODEL_DIR, "erfen_vectorizer.pkl")
        metrics_path = os.path.join(MODEL_DIR, "erfen_metrics.json")
    else:  # multiclass
        model_path = os.path.join(MODEL_DIR, "duofen_fusion_model.json")
        vec_path = os.path.join(MODEL_DIR, "duofen_vectorizer.pkl")
        metrics_path = os.path.join(MODEL_DIR, "duofen_metrics.json")

    # 检查所有必需文件是否存在
    for p in [model_path, vec_path, metrics_path]:
        if not os.path.exists(p):
            print(f"❌ 模型文件不存在: {p}")
            print("   请先运行训练脚本生成模型！")
            print("   cd code/ronghe")
            print("   python3 erfen_optuna_feature+2_gram_comp.py   (二分类)")
            print("   python3 duofen_optuna_feature+2_gram_comp.py  (多分类)")
            return None, None, None

    # 加载 XGBoost 模型（使用原生 save_model/load_model 接口，保存为 JSON 格式）
    model = XGBClassifier()
    model.load_model(model_path)

    # 加载 CountVectorizer（保存了词汇表、停用词等状态）
    # 必须使用训练时拟合好的 vectorizer，否则特征维度会不一致
    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)

    # 加载评估指标（JSON 格式）
    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    return model, vectorizer, metrics


# ============================================================
# 预测函数
# ============================================================

def predict_binary(domain, model, vectorizer, metrics):
    """
    二分类预测：判断域名是「良性」还是「恶意（DGA）」
    
    流程：
      1. 用 CountVectorizer 将域名转为 N-gram 稀疏特征向量
      2. 手动提取 6 维统计特征
      3. 水平拼接两种特征（hstack）
      4. 用 XGBoost 模型预测概率
      5. 输出结果（label + confidence）
    """
    # ---------- 特征提取 ----------
    # N-gram 特征：使用训练好的 vectorizer 做 transform（不是 fit_transform！）
    X_ngram = vectorizer.transform([domain.lower().strip()])
    
    # 统计特征（6维）
    X_stat = extract_stat_features_single(domain)
    
    # 特征融合：hstack 将稀疏矩阵（N-gram）和稠密矩阵（统计特征）拼接
    X = hstack([X_ngram, X_stat])

    # ---------- 预测 ----------
    # predict_proba 返回两个概率值：[良性概率, DGA概率]
    prob = model.predict_proba(X)[0]
    # predict 返回 0（良性）或 1（DGA）
    pred = model.predict(X)[0]

    prob_dga = prob[1]      # DGA 域名概率
    prob_benign = prob[0]   # 良性域名概率

    label = "恶意域名 (DGA)" if pred == 1 else "良性域名"
    confidence = prob_dga if pred == 1 else prob_benign

    # ---------- 结果输出 ----------
    print(f"\n{'='*50}")
    print("  二分类检测结果")
    print(f"{'='*50}")
    print(f"  域名:       {domain}")
    print(f"  判定结果:   {label}")
    print(f"  置信度:     {confidence*100:.2f}%")
    print(f"  DGA 概率:   {prob_dga*100:.2f}%")
    print(f"  良性概率:   {prob_benign*100:.2f}%")
    print(f"{'-'*50}")
    # 显示训练时得到的模型整体性能指标
    print(f"  模型准确率: {metrics['accuracy']*100:.2f}%")
    print(f"  模型 F1:    {metrics['f1']*100:.2f}%")
    print(f"  模型 AUC:   {metrics['auc']:.4f}")
    print(f"{'='*50}")


def predict_multiclass(domain, model, vectorizer, metrics):
    """
    多分类预测：判定域名属于哪个 DGA 家族
    
    流程：
      1. 加载 LabelEncoder（将家族名称和数字标签互相映射）
      2. 与二分类相同的特征提取 + 融合流程
      3. 用多分类模型预测概率分布（softmax 输出）
      4. 显示概率最高的前 5 个家族及概率
    
    与二分类的区别：
      - 输出不是 0/1，而是 n 个类别的概率分布
      - 多了 LabelEncoder 来解析家族名称
      - 显示 Top-5 概率排名
    """
    # 加载标签编码器（保存了 family_name → label_id 的映射关系）
    le_path = os.path.join(MODEL_DIR, "duofen_label_encoder.pkl")
    with open(le_path, "rb") as f:
        le = pickle.load(f)

    # ---------- 特征提取（与二分类相同） ----------
    X_ngram = vectorizer.transform([domain.lower().strip()])
    X_stat = extract_stat_features_single(domain)
    X = hstack([X_ngram, X_stat])

    # ---------- 预测 ----------
    # predict_proba 返回所有类别的概率向量，和为 1
    prob = model.predict_proba(X)[0]
    # predict 返回概率最高的类别 index
    pred = model.predict(X)[0]

    # 取概率最高的前 5 个家族（如果家族总数不足 5 个则全取）
    top_n = min(5, len(le.classes_))
    # argsort 按概率排序，[::-1] 逆序取最高的
    top_indices = np.argsort(prob)[::-1][:top_n]

    # 将预测的 index 转换为家族名称
    pred_family = le.classes_[pred]

    # ---------- 结果输出 ----------
    print(f"\n{'='*50}")
    print("  多分类检测结果")
    print(f"{'='*50}")
    print(f"  域名:           {domain}")
    print(f"  判定家族:       {pred_family}")
    print(f"  置信度:         {prob[pred]*100:.2f}%")
    print(f"{'-'*50}")
    print("  各家族概率排名:")
    # 用 ASCII 条形图直观显示概率大小
    for idx in top_indices:
        bar = "█" * int(prob[idx] * 30)
        print(f"    {le.classes_[idx]:<20s} {prob[idx]*100:>5.2f}% {bar}")
    print(f"{'-'*50}")
    # 显示训练时得到的模型整体性能指标
    print(f"  模型准确率:     {metrics['accuracy']*100:.2f}%")
    print(f"  模型 Macro F1:  {metrics['macro_f1']*100:.2f}%")
    print(f"{'='*50}")


# ============================================================
# 主交互逻辑
# ============================================================

def main():
    """
    主程序入口：循环等待用户输入域名，
    提供二分类 / 多分类两种检测模式。
    
    交互流程：
      Step 1: 用户输入域名
      Step 2: 选择检测模式（1=二分类, 2=多分类）
      Step 3: 加载对应模型
      Step 4: 执行预测并输出结果
      Step 5: 回到 Step 1（输入 q 退出）
    """
    print("=" * 50)
    print("  DGA 域名检测系统 — 交互式预测")
    print("=" * 50)

    while True:
        print()
        # 获取用户输入的域名
        domain = input("请输入域名 (输入 q 退出): ").strip().lower()

        if domain == 'q':
            print("再见！")
            break

        if not domain:
            continue

        # 选择检测模式
        print()
        print("  请选择检测模式:")
        print("    1. 二分类 (判断恶意/良性)")
        print("    2. 多分类 (判定 DGA 家族)")
        mode = input("  请输入 1 或 2: ").strip()

        if mode == '1':
            # 二分类模式
            model, vectorizer, metrics = load_model("binary")
            if model is None:
                continue  # 模型未训练，提示后重新输入
            predict_binary(domain, model, vectorizer, metrics)

        elif mode == '2':
            # 多分类模式
            model, vectorizer, metrics = load_model("multiclass")
            if model is None:
                continue
            # 多分类还需要加载 LabelEncoder（在 predict_multiclass 内部加载）
            predict_multiclass(domain, model, vectorizer, metrics)

        else:
            print("  无效输入，请输入 1 或 2")


if __name__ == "__main__":
    main()
