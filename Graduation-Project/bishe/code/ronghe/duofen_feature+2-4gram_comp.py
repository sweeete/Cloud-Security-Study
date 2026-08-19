import pandas as pd
import numpy as np
import math, time
from collections import Counter
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理 (8:1:1 划分)
# ==========================================
def load_multiclass_data(file_path):
    print(f"正在读取多分类数据集: {file_path}...")
    df = pd.read_csv(file_path, sep='\\s+')

    le = LabelEncoder()
    df['label'] = le.fit_transform(df['family'])

    # 分层抽样划分
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df, le


# ==========================================
# 第二部分：特征工程 (统计特征 + N-gram)
# ==========================================
def calculate_entropy(text):
    if not text or not isinstance(text, str): return 0
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def extract_stat_features(df):
    """提取 6 维稠密统计特征"""
    domains = df['domain'].astype(str)
    feat = pd.DataFrame()
    feat['f_len'] = domains.apply(len)
    feat['f_digit_ratio'] = domains.apply(lambda x: sum(c.isdigit() for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_vowel_ratio'] = domains.apply(lambda x: sum(c in 'aeiou' for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_unique_chars'] = domains.apply(lambda x: len(set(x)))
    feat['f_hyphen_ratio'] = domains.apply(lambda x: x.count('-') / len(x) if len(x) > 0 else 0)
    feat['f_entropy'] = domains.apply(calculate_entropy)
    return feat.values


def run_fusion_experiment():
    # 1. 准备数据
    train_df, val_df, test_df, le = load_multiclass_data('../duofen/dga_sampled_8k.txt')

    # 2. 提取 N-gram 特征 (稀疏)
    print("\n提取 2-4 gram 特征 (稀疏矩阵)...")
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4), min_df=5)
    X_train_ngram = vectorizer.fit_transform(train_df['domain'])
    X_val_ngram = vectorizer.transform(val_df['domain'])
    X_test_ngram = vectorizer.transform(test_df['domain'])

    # 3. 提取统计特征 (稠密)
    print("提取 6 维统计特征 (稠密矩阵)...")
    X_train_stat = extract_stat_features(train_df)
    X_val_stat = extract_stat_features(val_df)
    X_test_stat = extract_stat_features(test_df)

    # 4. 特征水平拼接 (Fusion)
    # 使用 hstack 将稀疏矩阵与稠密数组组合成新的稀疏矩阵
    X_train = hstack([X_train_ngram, X_train_stat])
    X_val = hstack([X_val_ngram, X_val_stat])
    X_test = hstack([X_test_ngram, X_test_stat])

    feat_dim = X_train.shape[1]
    print(f"融合完成！最终特征维度: {feat_dim} (N-gram + 6 统计特征)")

    # 5. 模型训练 (默认参数)
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.3,
        objective='multi:softprob',
        num_class=len(le.classes_),
        n_jobs=-1,
        random_state=42,
        eval_metric='mlogloss'
    )

    print(f"开始 XGBoost 融合模型训练...")
    start_time = time.time()
    model.fit(X_train, train_df['label'], eval_set=[(X_val, val_df['label'])], verbose=False)
    train_duration = time.time() - start_time

    # 6. 最终评估
    inf_start = time.time()
    y_pred = model.predict(X_test)
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    acc = accuracy_score(test_df['label'], y_pred)
    macro_f1 = f1_score(test_df['label'], y_pred, average='macro')

    # 7. 格式化输出
    print("\n" + "=" * 50)
    print(f"{'实验结果: 多分类特征融合组 (统计+2-4gram)':^50}")
    print("=" * 50)
    print(f"融合后总维度:        {feat_dim}")
    print(f"准确率 (Accuracy):   {acc:.4f}")
    print(f"宏平均 F1 (Macro-F1): {macro_f1:.4f}")
    print("-" * 50)
    print(f"训练总耗时:          {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 50)

    print("\n各家族详细分类报告:")
    print(classification_report(test_df['label'], y_pred, target_names=le.classes_, digits=4))


if __name__ == "__main__":
    run_fusion_experiment()