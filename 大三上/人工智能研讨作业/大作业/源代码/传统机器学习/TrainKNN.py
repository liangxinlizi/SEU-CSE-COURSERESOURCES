from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

data = pd.read_csv("processed_data.csv")

# 特征和目标变量
X = data.drop('NObeyesdad', axis=1)  # 特征
y = data['NObeyesdad']  # 目标变量

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化 KNeighborsClassifier 模型
knn = KNeighborsClassifier(n_neighbors=5)  # n_neighbors 控制 K 值

# 训练模型
knn.fit(X_train, y_train)
# 预测
y_pred = knn.predict(X_test)

# 评估模型
print("Accuracy:", accuracy_score(y_test, y_pred))

X_new = pd.read_csv('processed_test.csv')

y_pred_new = knn.predict(X_new)

X_new['NObeyesdad'] = y_pred_new
X_new.to_csv("predicted_results.csv", index=True)