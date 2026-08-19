import pandas as pd
import numpy as np
import math
import time
import optuna
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
    # 统一读取：假设文件包含 family domain 且有表头
    df = pd.read_csv(file_path, sep='\\s+')

    le = LabelEncoder()
    df['label'] = le.fit_transform(df['family'])

    # 分层抽样划分
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
# 第三部分：实验运行与贝叶斯寻优
# ==========================================
def run_experiment():
    # 1. 准备数据并预提取特征
    train_df, val_df, test_df, le = load_multiclass_data('dga_sampled_8k.txt')

    print("\n预提取统计特征以加速调参过程...")
    X_train = extract_features(train_df)
    X_val = extract_features(val_df)
    X_test = extract_features(test_df)
    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']

    num_classes = len(le.classes_)

    # 2. 定义 Optuna 优化目标
    def objective(trial):
        param = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 800),
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'objective': 'multi:softprob',
            'num_class': num_classes,
            'n_jobs': -1,
            'random_state': 42,
            'eval_metric': 'mlogloss'
        }
        model = XGBClassifier(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        # 多分类调参核心：使用宏平均 F1 (Macro-F1)
        return f1_score(y_val, preds, average='macro')

    # 3. 开始执行寻优
    print(f"\n--- 开始多分类统计特征组贝叶斯调参 (类别数: {num_classes}) ---")
    tune_start = time.time()
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=30)
    tune_duration = time.time() - tune_start

    # 4. 使用最优参数训练最终模型
    print(f"\n调参完成！最优 Macro-F1: {study.best_value:.4f}")
    best_params = study.best_params
    best_model = XGBClassifier(**best_params, random_state=42, n_jobs=-1, eval_metric='mlogloss')

    start_train = time.time()
    best_model.fit(X_train, y_train)
    train_duration = time.time() - start_train

    # 5. 最终评估
    inf_start = time.time()
    y_pred = best_model.predict(X_test)
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')

    # 6. 格式化输出 (统一风格)
    print("\n" + "=" * 45)
    print(f"{'实验结果: 多分类统计特征组 (贝叶斯调参版)':^45}")
    print("=" * 45)
    print(f"最优参数组合:        {best_params}")
    print(f"准确率 (Accuracy):   {acc:.4f}")
    print(f"宏平均 F1 (Macro-F1): {macro_f1:.4f}")
    print("-" * 45)
    print(f"调参总耗时:          {tune_duration:.2f} 秒")
    print(f"最终模型训练耗时:     {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 45)

    print("\n各家族详细分类报告 (最终模型):")
    print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))


if __name__ == "__main__":
    run_experiment()