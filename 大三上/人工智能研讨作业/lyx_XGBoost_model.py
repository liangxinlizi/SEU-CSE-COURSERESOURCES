# XGBoost的模型选择

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
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

# 列出要比较的模型
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
}

# 完善模型比较
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    results[name] = acc
    print(f"\n{name} Validation Report:\n")
    print(classification_report(y_val, y_pred))

# 比较每个模型的出现
print("\nModel Comparison:")
for name, acc in results.items():
    print(f"{name}: Accuracy = {acc:.4f}")

# 选择最佳模型
best_model_name = max(results, key=results.get)
best_model = models[best_model_name]
print(f"\nBest Model: {best_model_name} with Accuracy = {results[best_model_name]:.4f}")

# 将选择的模型应用于测试集预测
best_model.fit(X_train, y_train)
y_test_pred = best_model.predict(test_data)

# 将预测结果映射回原始标签
y_test_pred = label_encoder.inverse_transform(y_test_pred)

# 保存预测结果
test_ids = pd.read_csv("test.csv")['id']  # 从原始测试集加载 ID
output = pd.DataFrame({'id': test_ids, 'NObeyesdad': y_test_pred})
output.to_csv("submission.csv", index=False)

print("\u9884\u6d4b\u7ed3\u679c\u5df2\u4fdd\u5b58\u4e3a submission.csv！")