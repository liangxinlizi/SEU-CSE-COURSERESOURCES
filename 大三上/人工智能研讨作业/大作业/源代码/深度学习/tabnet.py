import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.metrics import accuracy_score
import torch

# 设置pandas显示选项以显示所有列
pd.set_option('display.max_columns', None)

# 数据加载
train_data = pd.read_csv('train.csv')

# 提取特征和标签
train_features = train_data.drop(columns=['id', 'NObeyesdad'])  # 删除ID和标签列
train_labels = train_data['NObeyesdad']

# 类别编码
le = LabelEncoder()
train_labels = le.fit_transform(train_labels)  # 将标签转换为数值

# 独热编码和特征工程
train_features = pd.get_dummies(train_features, drop_first=True)

# 标准化特征
scaler = StandardScaler()
train_features_scaled = scaler.fit_transform(train_features)

# 数据集划分
X_train, X_val, y_train, y_val = train_test_split(train_features_scaled, train_labels, test_size=0.1, random_state=42)

# 转换为 numpy 格式
X_train = np.array(X_train)
X_val = np.array(X_val)
y_train = np.array(y_train)
y_val = np.array(y_val)

# TabNet 模型初始化
clf = TabNetClassifier(
    n_d=8,  # 定义 TabNet 解码器中每个决策步骤的维度
    n_a=8,  # 定义 TabNet 解码器的注意力网络的维度
    n_steps=3,  # 决策步骤数量
    gamma=1.5,  # 注意力更新的加权系数
    lambda_sparse=1e-3,  # 稀疏正则化系数
    optimizer_fn=torch.optim.Adam,
    optimizer_params=dict(lr=2e-3),
    scheduler_params={"step_size":10, "gamma":0.9},
    scheduler_fn=torch.optim.lr_scheduler.StepLR,
    mask_type="entmax",  # “sparsemax” 或 “entmax”
    verbose=1
)

# 训练 TabNet 模型
clf.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_name=["val"],
    eval_metric=["accuracy"],
    max_epochs=1000,
    patience=100,
    batch_size=256,
    virtual_batch_size=128
)

# 测试数据加载和处理
test_data = pd.read_csv('test.csv')
test_ids = test_data['id']
test_features = test_data.drop(columns=['id'])

# 独热编码和标准化测试数据
test_features = pd.get_dummies(test_features, drop_first=True)
missing_cols = set(train_features.columns) - set(test_features.columns)
for col in missing_cols:
    test_features[col] = 0
test_features = test_features[train_features.columns]

test_features_scaled = scaler.transform(test_features)
X_test = np.array(test_features_scaled)

# 测试集预测
test_predictions = clf.predict(X_test)

# 解码预测结果
predicted_classes = le.inverse_transform(test_predictions)

# 创建提交文件
submission_df = pd.DataFrame({
    'id': test_ids,
    'NObeyesdad': predicted_classes
})
submission_df.to_csv('submission.csv', index=False)
print("Submission file generated successfully.")
