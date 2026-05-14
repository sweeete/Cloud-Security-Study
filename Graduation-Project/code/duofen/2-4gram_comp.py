import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier


# ==========================================
# 第一部分：数据加载与预处理
# ==========================================
def load_multiclass_data(file_path):
    print(f"正在读取多分类数据集: {file_path}...")
    # 针对 domain family 格式，使用空格分隔
    df = pd.read_csv(file_path, sep='\\s+')

    # 标签编码
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['family'])

    print(f"检测到家族数量: {len(le.classes_)}")

    # 8:1:1 随机抽取 (分层抽样)
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    return train_df, val_df, test_df, le.classes_


# ==========================================
# 第二部分：4-gram 特征工程与运行
# ==========================================
def run_4gram_multiclass_exp():
    # 1. 加载数据
    train_df, val_df, test_df, class_names = load_multiclass_data('dga_sampled_8k.txt')

    print("\n开始执行 4-gram 特征向量化...")
    # 提取 4-gram 字符特征
    # 加入 min_df=5 以对齐实验基准，过滤掉只出现过极少数次的随机噪声组合
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(4, 4), min_df=5)

    # 核心：fit 只能在训练集上做
    X_train = vectorizer.fit_transform(train_df['domain'])
    X_val = vectorizer.transform(val_df['domain'])
    X_test = vectorizer.transform(test_df['domain'])

    y_train, y_val, y_test = train_df['label'], val_df['label'], test_df['label']

    print(f"特征提取完成！特征维度: {X_train.shape[1]}")

    # 2. XGBoost 默认参数训练 (多分类)
    print(f"使用 XGBoost 默认参数进行多分类训练 (4-gram)...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.3,
        objective='multi:softprob',
        num_class=len(class_names),
        n_jobs=-1,
        random_state=42,
        eval_metric='mlogloss'
    )

    start_time = time.time()
    # 纯默认参数训练，不开启 Early Stopping
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    train_duration = time.time() - start_time

    # 3. 评估指标
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')

    # 4. 输出结果
    print("\n" + "=" * 45)
    print("多分类实验：4-gram 特征组 (默认参数)")
    print("=" * 45)
    print(f"特征维度:           {X_train.shape[1]}")
    print(f"准确率 (Accuracy):  {acc:.4f}")
    print(f"宏平均 F1 (Macro-F1): {macro_f1:.4f}")
    print(f"训练总耗时:         {train_duration:.2f} 秒")
    print("-" * 45)

    # 建议打印报告，观察 34% 究竟是哪些家族分错了
    print("各家族详细分类报告:")
    print(classification_report(y_test, y_pred, target_names=class_names))
    print("=" * 45)


if __name__ == "__main__":
    run_4gram_multiclass_exp()