import pandas as pd
import numpy as np
import math
import time
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理 (8:1:1 划分)
# ==========================================
def load_and_preprocess_data(dga_file, alexa_file, sample_size=200000):
    print(f"正在读取纯域名数据集 (各取前 {sample_size} 条)...")

    # 1. 读取纯域名文件 (每行一个域名)
    # 针对你提供的 cleaned 格式，直接按行读取即可
    dga_list = pd.read_csv(dga_file, header=None, names=['domain'], nrows=sample_size).dropna()
    alexa_list = pd.read_csv(alexa_file, header=None, names=['domain'], nrows=sample_size).dropna()

    # 清洗：转小写、去空格、去重
    dga_list = dga_list['domain'].astype(str).str.lower().str.strip().unique()
    alexa_list = alexa_list['domain'].astype(str).str.lower().str.strip().unique()

    # 构建 DataFrame
    df_dga = pd.DataFrame({'domain': dga_list, 'label': 1})
    df_alexa = pd.DataFrame({'domain': alexa_list, 'label': 0})
    df = pd.concat([df_dga, df_alexa], ignore_index=True)

    # 2. 划分数据集 (固定随机种子 42, 分层抽样)
    print("执行 8:1:1 严谨划分 (Train:Val:Test)...")
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    print(f"数据就绪: 训练集({len(train_df)}), 验证集({len(val_df)}), 测试集({len(test_df)})")
    return train_df, val_df, test_df


# ==========================================
# 第二部分：特征工程 (统计特征提取)
# ==========================================
def calculate_entropy(text):
    """计算域名的香农熵"""
    if not text or not isinstance(text, str): return 0
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def extract_features(df):
    """提取 6 类核心统计特征"""
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
# 第三部分：模型训练、评估与结果打印
# ==========================================
def run_experiment():
    # 1. 加载与准备数据 (请确保文件名与你的本地文件名一致)
    train_df, val_df, test_df = load_and_preprocess_data('dga_cleaned.txt', 'alexa_cleaned.txt')

    print("提取统计特征中...")
    X_train = extract_features(train_df)
    X_val = extract_features(val_df)
    X_test = extract_features(test_df)

    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']

    # 2. 初始化模型 (默认参数)
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.3,
        n_jobs=-1,
        random_state=42,
        eval_metric='logloss'
    )

    # 3. 训练
    print("开始 XGBoost 默认参数训练...")
    start_time = time.time()
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    train_duration = time.time() - start_time

    # 4. 评估
    print("执行性能评估...")
    inf_start = time.time()
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    # 5. 格式化输出 (统一风格)
    print("\n" + "=" * 45)
    print(f"{'实验结果: 二分类统计特征组 (默认参数)':^45}")
    print("=" * 45)
    print(f"准确率 (Accuracy):   {accuracy_score(y_test, y_pred):.4f}")
    print(f"精确率 (Precision):  {precision_score(y_test, y_pred):.4f}")
    print(f"召回率 (Recall):     {recall_score(y_test, y_pred):.4f}")
    print(f"F1 值 (F1-Score):    {f1_score(y_test, y_pred):.4f}")
    print(f"AUC 曲线下面积:      {roc_auc_score(y_test, y_prob):.4f}")
    print("-" * 45)
    print(f"训练总耗时:          {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 45)


if __name__ == "__main__":
    run_experiment()