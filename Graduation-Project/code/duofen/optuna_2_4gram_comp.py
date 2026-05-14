import pandas as pd
import numpy as np
import time
import optuna
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

    # 分层抽样 8:1:1
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df, le

# ==========================================
# 第二部分：特征工程 (预提取 2-4 gram 锁定维度)
# ==========================================
# 加载数据
train_df, val_df, test_df, le = load_multiclass_data('dga_sampled_8k.txt')

print("\n执行 2-4 gram 特征向量化 (混合 2/3/4 位特征，min_df=5)...")
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4), min_df=5)

# 统一在训练集上 fit，确保特征维度锁定，避免调参过程重复计算
X_train = vectorizer.fit_transform(train_df['domain'])
X_val = vectorizer.transform(val_df['domain'])
X_test = vectorizer.transform(test_df['domain'])

y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']
feat_dim = X_train.shape[1]
print(f"复合特征维度锁定为: {feat_dim}")

# ==========================================
# 第三部分：Optuna 贝叶斯寻优
# ==========================================
def objective(trial):
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 5),
        # 固定参数
        'objective': 'multi:softprob',
        'num_class': len(le.classes_),
        'n_jobs': -1,
        'random_state': 42,
        'eval_metric': 'mlogloss'
    }

    model = XGBClassifier(**param)
    model.fit(X_train, y_train)

    # 使用验证集评估 (Macro-F1 对各家族公平评价)
    preds = model.predict(X_val)
    return f1_score(y_val, preds, average='macro')

print(f"\n--- 开始多分类 2-4 gram 贝叶斯调参 (类别数: {len(le.classes_)}) ---")
tune_start = time.time()
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20) # 建议视机器性能可提升至 30-50
tune_duration = time.time() - tune_start

# ==========================================
# 第四部分：最终评估
# ==========================================
print(f"\n调参完成！最优 Macro-F1: {study.best_value:.4f}")
best_params = study.best_params

print("\n使用最优参数在测试集上进行最终评估...")
final_model = XGBClassifier(**best_params, random_state=42, n_jobs=-1, eval_metric='mlogloss')

start_time = time.time()
final_model.fit(X_train, y_train)
train_duration = time.time() - start_time

# 推理性能评估
inf_start = time.time()
y_pred = final_model.predict(X_test)
inference_time_avg = (time.time() - inf_start) / len(test_df)

# 格式化输出 (统一视觉风格)
print("\n" + "=" * 50)
print(f"{'实验结果: 多分类 2-4 gram 贝叶斯调参版':^50}")
print("=" * 50)
print(f"混合特征总维度:      {feat_dim}")
print(f"最优参数组合:        {best_params}")
print(f"调参总耗时:          {tune_duration:.2f} 秒")
print("-" * 50)
print(f"准确率 (Accuracy):   {accuracy_score(y_test, y_pred):.4f}")
print(f"宏平均 F1 (Macro-F1): {f1_score(y_test, y_pred, average='macro'):.4f}")
print(f"训练总耗时:          {train_duration:.2f} 秒")
print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
print("=" * 50)

print("\n各家族详细分类报告 (最终模型):")
print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))