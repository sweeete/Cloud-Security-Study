import pandas as pd
import numpy as np
import math, time
from collections import Counter
from scipy.sparse import hstack  # 用于水平拼接稀疏矩阵与稠密矩阵
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理 (8:1:1 划分)
# ==========================================
def load_and_preprocess_data(dga_file, alexa_file, sample_size=200000):
    print(f"正在读取纯域名数据集 (目标各取: {sample_size} 条)...")

    # 1. 读取文件
    dga_list = pd.read_csv(dga_file, header=None, names=['domain'], nrows=sample_size).dropna()
    alexa_list = pd.read_csv(alexa_file, header=None, names=['domain'], nrows=sample_size).dropna()

    # 清洗：小写、去空、去重
    dga_list = dga_list['domain'].astype(str).str.lower().str.strip().unique()
    alexa_list = alexa_list['domain'].astype(str).str.lower().str.strip().unique()

    # 构建 DataFrame
    df_dga = pd.DataFrame({'domain': dga_list, 'label': 1})
    df_alexa = pd.DataFrame({'domain': alexa_list, 'label': 0})
    df = pd.concat([df_dga, df_alexa], ignore_index=True)

    # 2. 划分数据集 (8:1:1 分层采样)
    print("执行 8:1:1 严谨划分 (Train:Val:Test)...")
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    print(f"数据就绪: 训练集({len(train_df)}), 验证集({len(val_df)}), 测试集({len(test_df)})")
    return train_df, val_df, test_df


# ==========================================
# 第二部分：特征工程核心逻辑
# ==========================================
def calculate_entropy(text):
    """计算香农熵"""
    if not text or not isinstance(text, str): return 0
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def extract_stat_features(df):
    """提取本文设计的 6 维稠密统计特征"""
    domains = df['domain'].astype(str)
    feat = pd.DataFrame()
    # 1. 长度 2. 数字占比 3. 元音占比 4. 唯一字符数 5. 连字符占比 6. 熵
    feat['f_len'] = domains.apply(len)
    feat['f_digit_ratio'] = domains.apply(lambda x: sum(c.isdigit() for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_vowel_ratio'] = domains.apply(lambda x: sum(c in 'aeiou' for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_unique_chars'] = domains.apply(lambda x: len(set(x)))
    feat['f_hyphen_ratio'] = domains.apply(lambda x: x.count('-') / len(x) if len(x) > 0 else 0)
    feat['f_entropy'] = domains.apply(calculate_entropy)
    return feat.values


# ==========================================
# 第三部分：融合实验运行 (统计 + 2-4 gram)
# ==========================================
def run_fusion_experiment():
    # 1. 加载数据
    train_df, val_df, test_df = load_and_preprocess_data('dga_cleaned.txt', 'alexa_cleaned.txt')

    # 2. 提取 N-gram 特征 (稀疏矩阵)
    print("\n[Step 1] 提取 2-4 gram 字符特征 (多尺度局部模式)...")
    # ngram_range=(2, 4) 捕捉 2-4 位序列，min_df=5 过滤低频噪声
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4), min_df=5)
    X_train_ngram = vectorizer.fit_transform(train_df['domain'])
    X_val_ngram = vectorizer.transform(val_df['domain'])
    X_test_ngram = vectorizer.transform(test_df['domain'])

    # 3. 提取统计特征 (稠密矩阵)
    print("[Step 2] 提取 6 维全局统计特征 (宏观结构)...")
    X_train_stat = extract_stat_features(train_df)
    X_val_stat = extract_stat_features(val_df)
    X_test_stat = extract_stat_features(test_df)

    # 4. 特征水平融合 (Fusion)
    # 将稀疏的 N-gram 矩阵与稠密的统计特征矩阵进行拼接
    X_train = hstack([X_train_ngram, X_train_stat])
    X_val = hstack([X_val_ngram, X_val_stat])
    X_test = hstack([X_test_ngram, X_test_stat])

    feat_dim = X_train.shape[1]
    print(f"特征融合完成！总特征维度: {feat_dim}")

    # 5. 初始化并训练模型 (默认参数)
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.3,
        objective='binary:logistic',
        n_jobs=-1,
        random_state=42,
        eval_metric='logloss'
    )

    print("模型训练中 (XGBoost 融合特征组)...")
    start_time = time.time()
    model.fit(X_train, train_df['label'], eval_set=[(X_val, val_df['label'])], verbose=False)
    train_duration = time.time() - start_time

    # 6. 预测与评估
    print("执行性能分析...")
    inf_start = time.time()
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    # 7. 格式化输出
    print("\n" + "=" * 45)
    print(f"{'实验结果: 二分类特征融合 (统计+2-4gram)':^45}")
    print("=" * 45)
    print(f"融合特征总维度:      {feat_dim}")
    print(f"准确率 (Accuracy):   {accuracy_score(test_df['label'], y_pred):.4f}")
    print(f"精确率 (Precision):  {precision_score(test_df['label'], y_pred):.4f}")
    print(f"召回率 (Recall):     {recall_score(test_df['label'], y_pred):.4f}")
    print(f"F1 值 (F1-Score):    {f1_score(test_df['label'], y_pred):.4f}")
    print(f"AUC 曲线下面积:      {roc_auc_score(test_df['label'], y_prob):.4f}")
    print("-" * 45)
    print(f"训练总耗时:          {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 45)


if __name__ == "__main__":
    run_fusion_experiment()