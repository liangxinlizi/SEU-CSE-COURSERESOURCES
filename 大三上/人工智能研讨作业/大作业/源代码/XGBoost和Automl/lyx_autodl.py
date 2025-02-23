# H2O的autoDL算法

import pandas as pd
import h2o
from h2o.automl import H2OAutoML
from sklearn.model_selection import train_test_split

# 1. 启动 H2O 服务
h2o.init()

# 2. 加载数据
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

print(f"训练集大小: {len(train_data)}")
print(f"测试集大小: {len(test_data)}")

# 3. 划分训练集和验证集 (9:1)
X = train_data.drop(columns=['id', 'NObeyesdad'])  # 特征
y = train_data['NObeyesdad']  # 标签

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)
print(f"训练数据大小: {len(X_train)}, 验证数据大小: {len(X_val)}")

# 4. 转换数据为 H2O 格式
train_h2o = h2o.H2OFrame(pd.concat([X_train, y_train], axis=1))
val_h2o = h2o.H2OFrame(pd.concat([X_val, y_val], axis=1))
test_h2o = h2o.H2OFrame(test_data.drop(columns=['id']))

# 设置标签列
target = "NObeyesdad"
features = X_train.columns.tolist()

train_h2o[target] = train_h2o[target].asfactor()  # 转换标签为分类
val_h2o[target] = val_h2o[target].asfactor()

# 5. 使用 H2O AutoML 训练模型
aml = H2OAutoML(max_models=20, seed=42, balance_classes=True)  # 设置自动化训练参数
aml.train(x=features, y=target, training_frame=train_h2o, validation_frame=val_h2o)

# 6. 查看最佳模型
lb = aml.leaderboard
print("模型排行榜：")
print(lb)

# 7. 使用最佳模型生成预测结果
predictions = aml.leader.predict(test_h2o)

# 8. 提取预测值并保存到文件
test_data['NObeyesdad'] = predictions.as_data_frame().iloc[:, 0]
output = test_data[['id', 'NObeyesdad']]
output.to_csv("submission.csv", index=False)

print("预测结果已保存为 submission.csv！")
print("最佳模型：")
print(aml.leader)
print("最佳模型的超参数：")
print(aml.leader.params)
print(aml.leaderboard)


# 关闭 H2O 服务
h2o.shutdown(prompt=False)