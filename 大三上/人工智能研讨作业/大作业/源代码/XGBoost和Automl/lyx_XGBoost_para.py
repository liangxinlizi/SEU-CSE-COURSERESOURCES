# XGBoost的k折交叉验证与网格调参
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

# 加载数据
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# 查看数据集的列名
print("Train columns:", train_data.columns)
print("Test columns:", test_data.columns)

# 合并训练集和测试集进行统一处理
combined_data = pd.concat([train_data, test_data], ignore_index=True)

# 确定需要独点编码和分类编码的列
categorical_columns = ['Gender', 'family_history_with_overweight', 'FAVC', 
                       'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']
target_column = 'NObeyesdad'  # 目标变量

# 独点编码指定列
combined_data = pd.get_dummies(combined_data, columns=categorical_columns, drop_first=True)

# 使用 LabelEncoder 对目标变量进行分类编码
label_encoder = LabelEncoder()
combined_data[target_column] = label_encoder.fit_transform(combined_data[target_column])

# 分割回训练集和测试集
train_data = combined_data.iloc[:len(train_data)]
test_data = combined_data.iloc[len(train_data):]

# 标准化数值特征
scaler = StandardScaler()
numeric_columns = ['Age', 'Height', 'Weight']
train_data[numeric_columns] = scaler.fit_transform(train_data[numeric_columns])
test_data[numeric_columns] = scaler.transform(test_data[numeric_columns])

# 定义特征和标签
X = train_data.drop(columns=['id', target_column])
y = train_data[target_column]

# 确保测试集特征与训练集一致
test_data = test_data.drop(columns=['id'], errors='ignore')
missing_cols = set(X.columns) - set(test_data.columns)
for col in missing_cols:
    test_data[col] = 0
test_data = test_data[X.columns]

# 划分训练集和验证集
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# 使用 XGBoost 应用于测试集预测
xgb_model = XGBClassifier(eval_metric='mlogloss', random_state=42)

# 定义 K 折交叉验证
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 网格搜索调优参数一：分类器个数
param_grid_n_estimators = {'n_estimators': [50, 100, 200, 300, 500]}
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid_n_estimators, cv=cv, scoring='accuracy', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 最佳参数：分类器个数
best_n_estimators = grid_search.best_params_['n_estimators']
print(f"Best n_estimators: {best_n_estimators}")

# 调优参数二：模型最大深度
xgb_model.set_params(n_estimators=best_n_estimators)
param_grid_max_depth = {'max_depth': [3, 5, 10, 15, 20]}
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid_max_depth, cv=cv, scoring='accuracy', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 最佳参数：最大深度
best_max_depth = grid_search.best_params_['max_depth']
print(f"Best max_depth: {best_max_depth}")

# 调优参数三：min_samples_split 和 min_samples_leaf
xgb_model.set_params(max_depth=best_max_depth)
param_grid_samples = {
    'min_child_weight': [1, 2, 5, 10],
    'gamma': [0, 0.1, 0.2, 0.5]
}
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid_samples, cv=cv, scoring='accuracy', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 最佳参数： min_child_weight 和 gamma
best_params = grid_search.best_params_
print(f"Best Parameters: {best_params}")

# 将最佳参数设置到 XGBoost 模型
xgb_model.set_params(**best_params)
xgb_model.fit(X_train, y_train)

# 验证集表现
y_pred = xgb_model.predict(X_val)
print("\nValidation Report:")
print(classification_report(y_val, y_pred))

# 将最佳模型应用于测试集预测
y_test_pred = xgb_model.predict(test_data)

# 将预测结果映射回原始标签
y_test_pred = label_encoder.inverse_transform(y_test_pred)

# 保存预测结果
test_ids = pd.read_csv("test.csv")['id']  # 从原始测试集加载 ID
output = pd.DataFrame({'id': test_ids, 'NObeyesdad': y_test_pred})
output.to_csv("submission.csv", index=False)

print("\u9884\u6d4b\u7ed3\u679c\u5df2\u4fdd\u5b58\u4e3a submission.csv！")