import pandas as pd
import numpy as np
import math, time
import optuna
from collections import Counter
from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理 (双文件 8:1:1)
# ==========================================
def load_and_preprocess_data(dga_file, alexa_file, sample_size=200000):
    print(f"正在读取纯域名数据集 (目标各取: {sample_size} 条)...")
    dga_list = pd.read_csv(dga_file, header=None, names=['domain'], nrows=sample_size).dropna()
    alexa_list = pd.read_csv(alexa_file, header=None, names=['domain'], nrows=sample_size).dropna()

    dga_list = dga_list['domain'].astype(str).str.lower().str.strip().unique()
    alexa_list = alexa_list['domain'].astype(str).str.lower().str.strip().unique()

    df_dga = pd.DataFrame({'domain': dga_list, 'label': 1})
    df_alexa = pd.DataFrame({'domain': alexa_list, 'label': 0})
    df = pd.concat([df_dga, df_alexa], ignore_index=True)

    print("执行 8:1:1 严谨划分 (Train:Val:Test)...")
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df


# ==========================================
# 第二部分：特征工程 (统计特征提取)
# ==========================================
def calculate_entropy(text):
    if not text or not isinstance(text, str): return 0
    counter = Counter(text)
    probs = [count / len(text) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def extract_stat_features(df):
    domains = df['domain'].astype(str)
    feat = pd.DataFrame()
    feat['f_len'] = domains.apply(len)
    feat['f_digit_ratio'] = domains.apply(lambda x: sum(c.isdigit() for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_vowel_ratio'] = domains.apply(lambda x: sum(c in 'aeiou' for c in x) / len(x) if len(x) > 0 else 0)
    feat['f_unique_chars'] = domains.apply(lambda x: len(set(x)))
    feat['f_hyphen_ratio'] = domains.apply(lambda x: x.count('-') / len(x) if len(x) > 0 else 0)
    feat['f_entropy'] = domains.apply(calculate_entropy)
    return feat.values


# ==========================================
# 第三部分：贝叶斯调参实验
# ==========================================
def run_tuning_experiment():
    # 1. 准备数据
    train_df, val_df, test_df = load_and_preprocess_data('dga_cleaned.txt', 'alexa_cleaned.txt')
    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']

    # 2. 预提取融合特征 (避免调参循环内重复计算)
    print("\n提取 N-gram 与统计特征并融合...")
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    X_train_ngram = vectorizer.fit_transform(train_df['domain'])
    X_val_ngram = vectorizer.transform(val_df['domain'])
    X_test_ngram = vectorizer.transform(test_df['domain'])

    X_train_stat = extract_stat_features(train_df)
    X_val_stat = extract_stat_features(val_df)
    X_test_stat = extract_stat_features(test_df)

    X_train = hstack([X_train_ngram, X_train_stat])
    X_val = hstack([X_val_ngram, X_val_stat])
    X_test = hstack([X_test_ngram, X_test_stat])

    feat_dim = X_train.shape[1]
    print(f"融合特征锁定完成！总维度: {feat_dim}")

    # 3. 定义 Optuna 寻优目标
    def objective(trial):
        param = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 600),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 3),
            'objective': 'binary:logistic',
            'n_jobs': -1,
            'random_state': 42,
            'eval_metric': 'logloss'
        }
        model = XGBClassifier(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return f1_score(y_val, preds)

    # 4. 执行调参
    print(f"\n--- 开始二分类融合组贝叶斯调参 (Trials=20) ---")
    tune_start = time.time()
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20)
    tune_duration = time.time() - tune_start

    # 5. 最终模型评估
    print(f"\n最优参数: {study.best_params}")
    best_model = XGBClassifier(**study.best_params, random_state=42, n_jobs=-1, eval_metric='logloss')

    start_train = time.time()
    best_model.fit(X_train, y_train)
    train_duration = time.time() - start_train

    inf_start = time.time()
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    # 6. 统一输出
    print("\n" + "=" * 50)
    print(f"{'实验结果: 二分类特征融合 (统计+2-gram) 贝叶斯版':^50}")
    print("=" * 50)
    print(f"融合总维度:          {feat_dim}")
    print(f"调参耗时:            {tune_duration:.2f} 秒")
    print("-" * 50)
    print(f"准确率 (Accuracy):   {accuracy_score(y_test, y_pred):.4f}")
    print(f"精确率 (Precision):  {precision_score(y_test, y_pred):.4f}")
    print(f"召回率 (Recall):     {recall_score(y_test, y_pred):.4f}")
    print(f"F1 值 (F1-Score):    {f1_score(y_test, y_pred):.4f}")
    print(f"AUC 曲线下面积:      {roc_auc_score(y_test, y_prob):.4f}")
    print("-" * 50)
    print(f"最终训练耗时:         {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 50)


if __name__ == "__main__":
    run_tuning_experiment()