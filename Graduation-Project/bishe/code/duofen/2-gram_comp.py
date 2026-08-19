import pandas as pd
import numpy as np
import time
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
    # 统一读取格式：假设包含 family domain 列
    df = pd.read_csv(file_path, sep='\\s+')

    le = LabelEncoder()
    df['label'] = le.fit_transform(df['family'])

    print(f"检测到家族数量: {len(le.classes_)}")

    # 分层抽样划分 8:1:1
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df, le


# ==========================================
# 第二部分：特征工程与模型训练 (2-gram)
# ==========================================
def run_experiment():
    # 1. 准备数据
    train_df, val_df, test_df, le = load_multiclass_data('dga_sampled_8k.txt')

    print("\n开始执行 2-gram 特征向量化...")
    # 提取字符级 2-gram
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))

    X_train = vectorizer.fit_transform(train_df['domain'])
    X_val = vectorizer.transform(val_df['domain'])
    X_test = vectorizer.transform(test_df['domain'])

    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']
    feat_dim = X_train.shape[1]
    print(f"特征提取完成！特征维度: {feat_dim}")

    # 2. 初始化多分类模型 (默认参数)
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
    print(f"开始 XGBoost 多分类训练 (2-gram 组)...")
    start_time = time.time()
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    train_duration = time.time() - start_time

    # 4. 评估
    inf_start = time.time()
    y_pred = model.predict(X_test)
    inference_time_avg = (time.time() - inf_start) / len(test_df)

    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')

    # 5. 格式化输出 (统一风格)
    print("\n" + "=" * 45)
    print(f"{'实验结果: 多分类 2-gram 特征组 (默认参数)':^45}")
    print("=" * 45)
    print(f"特征总维度:         {feat_dim}")
    print(f"准确率 (Accuracy):   {acc:.4f}")
    print(f"宏平均 F1 (Macro-F1): {macro_f1:.4f}")
    print("-" * 45)
    print(f"训练总耗时:          {train_duration:.2f} 秒")
    print(f"单条推理平均延时:     {inference_time_avg * 1000:.6f} 毫秒")
    print("=" * 45)

    # 详细报告对多分类家族识别深度分析至关重要
    print("\n各家族详细分类报告:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))


if __name__ == "__main__":
    run_experiment()