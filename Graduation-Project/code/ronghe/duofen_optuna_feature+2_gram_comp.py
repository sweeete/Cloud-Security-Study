import pandas as pd
import numpy as np
import math, time, os, json, pickle
import optuna
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
# 第二部分：特征工程 (统计特征 + 2-gram)
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
# 第三部分：实验运行与贝叶斯寻优
# ==========================================
def run_fusion_tuning_experiment():
    # 1. 加载数据
    train_df, val_df, test_df, le = load_multiclass_data('dga_sampled_8k.txt')
    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']
    num_classes = len(le.classes_)

    # 2. 预提取融合特征
    print("\n提取 2-gram 字符特征...")
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    X_train_ngram = vectorizer.fit_transform(train_df['domain'])
    X_val_ngram = vectorizer.transform(val_df['domain'])
    X_test_ngram = vectorizer.transform(test_df['domain'])

    print("提取 6 维统计特征...")
    X_train_stat = extract_stat_features(train_df)
    X_val_stat = extract_stat_features(val_df)
    X_test_stat = extract_stat_features(test_df)

    print("执行特征空间融合 (Fusion)...")
    X_train = hstack([X_train_ngram, X_train_stat])
    X_val = hstack([X_val_ngram, X_val_stat])
    X_test = hstack([X_test_ngram, X_test_stat])

    feat_dim = X_train.shape[1]
    print(f"特征维度锁定: {feat_dim}")

    # 3. 定义寻优目标 (以 Macro-F1 为核心指标)
    def objective(trial):
        param = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 600),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 3),
            'objective': 'multi:softprob',
            'num_class': num_classes,
            'n_jobs': -1,
            'random_state': 42,
            'eval_metric': 'mlogloss'
        }
        model = XGBClassifier(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return f1_score(y_val, preds, average='macro')

    # 4. 执行调参
    print(f"\n--- 开始多分类融合组 (2-gram) 贝叶斯寻优 ---")
    tune_start = time.time()
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=30)
    tune_duration = time.time() - tune_start

    # 5. 最终模型训练与评估
    print(f"\n最优参数组合: {study.best_params}")
    best_model = XGBClassifier(**study.best_params, random_state=42, n_jobs=-1, eval_metric='mlogloss')

    start_train = time.time()
    best_model.fit(X_train, y_train)
    train_duration = time.time() - start_train

    inf_start = time.time()
    y_pred = best_model.predict(X_test)
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    # 6. 统一输出
    print("\n" + "=" * 55)
    print(f"{'实验结果: 多分类融合组 (统计+2-gram) 贝叶斯版':^55}")
    print("=" * 55)
    print(f"融合特征总维度:      {feat_dim}")
    print(f"调参总耗时:          {tune_duration:.2f} 秒")
    print("-" * 55)
    print(f"准确率 (Accuracy):   {accuracy_score(y_test, y_pred):.4f}")
    print(f"宏平均 F1 (Macro-F1): {f1_score(y_test, y_pred, average='macro'):.4f}")
    print(f"最终训练耗时:         {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 55)

    print("\n各家族详细分类报告 (调参后最终模型):")
    print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))

    # ===== 保存模型及相关组件 =====
    model_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models")
    os.makedirs(model_dir, exist_ok=True)

    # 保存模型
    model_path = os.path.join(model_dir, "duofen_fusion_model.json")
    best_model.save_model(model_path)
 
    # 保存向量化器
    vec_path = os.path.join(model_dir, "duofen_vectorizer.pkl")
    with open(vec_path, "wb") as f:
        pickle.dump(vectorizer, f)

    # 保存标签编码器
    le_path = os.path.join(model_dir, "duofen_label_encoder.pkl")
    with open(le_path, "wb") as f:
        pickle.dump(le, f)

    # 保存准确率信息
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    metrics = {
        "type": "multiclass",
        "accuracy": round(acc, 4),
        "macro_f1": round(macro_f1, 4),
        "num_classes": num_classes,
        "class_names": le.classes_.tolist(),
        "best_params": study.best_params
    }
    metrics_path = os.path.join(model_dir, "duofen_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n✅ 模型已保存: {model_path}")
    print(f"✅ 向量化器已保存: {vec_path}")
    print(f"✅ 标签编码器已保存: {le_path}")
    print(f"✅ 评估指标已保存: {metrics_path}")


if __name__ == "__main__":
    run_fusion_tuning_experiment()