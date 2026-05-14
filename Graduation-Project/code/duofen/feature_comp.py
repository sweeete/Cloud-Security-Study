import pandas as pd
import numpy as np
import math
import time
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理 (8:1:1 划分)
# ==========================================
def load_multiclass_data(file_path):
    print(f"正在读取多分类数据集: {file_path}...")
    # 统一读取：假设表头为 family domain
    df = pd.read_csv(file_path, sep='\\s+')

    # 标签编码
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['family'])

    # 打印家族分布简报
    dist = df['family'].value_counts()
    print(f"检测到 {len(le.classes_)} 个家族，样本总量: {len(df)}")
    print(f"家族样本量区间: [{dist.min()}, {dist.max()}]")

    # 分层抽样划分 8:1:1
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df, le


# ==========================================
# 第二部分：特征工程 (6 维统计特征)
# ==========================================
def calculate_entropy(text):
    if not text or not isinstance(text, str): return 0
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def extract_features(df):
    domains = df['domain'].astype(str)
    features = pd.DataFrame()
    features['f_len'] = domains.apply(len)
    features['f_digit_ratio'] = domains.apply(lambda x: sum(c.isdigit() for c in x) / len(x) if len(x) > 0 else 0)
    features['f_vowel_ratio'] = domains.apply(lambda x: sum(c in 'aeiou' for c in x) / len(x) if len(x) > 0 else 0)
    features['f_unique_chars'] = domains.apply(lambda x: len(set(x)))
    features['f_hyphen_ratio'] = domains.apply(lambda x: x.count('-') / len(x) if len(x) > 0 else 0)
    features['f_entropy'] = domains.apply(calculate_entropy)
    return features


# ==========================================
# 第三部分：模型训练与评估
# ==========================================
def run_experiment():
    # 1. 准备数据
    train_df, val_df, test_df, le = load_multiclass_data('dga_sampled_8k.txt')

    print("\n正在提取 6 维统计特征...")
    X_train = extract_features(train_df)
    X_val = extract_features(val_df)
    X_test = extract_features(test_df)

    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']

    # 2. 初始化多分类模型
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

    # 3. 训练
    print(f"开始 XGBoost 多分类训练 (类别数: {len(le.classes_)})...")
    start_time = time.time()
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    train_duration = time.time() - start_time

    # 4. 预测与评估指标
    inf_start = time.time()
    y_pred = model.predict(X_test)
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')

    # 5. 格式化输出 (统一风格)
    print("\n" + "=" * 45)
    print(f"{'实验结果: 多分类统计特征组 (默认参数)':^45}")
    print("=" * 45)
    print(f"类别总数:           {len(le.classes_)}")
    print(f"准确率 (Accuracy):   {acc:.4f}")
    print(f"宏平均 F1 (Macro-F1): {macro_f1:.4f}")
    print("-" * 45)
    print(f"训练总耗时:          {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 45)

    # 打印详细分类报告，以便分析具体家族的识别情况
    print("\n各家族详细分类报告:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))


if __name__ == "__main__":
    run_experiment()