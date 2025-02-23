from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# 假设你已经有一个处理过的数据集 data
data = pd.read_csv("processed_data.csv")

# 特征和目标变量
X = data.drop('NObeyesdad', axis=1)  # 特征
y = data['NObeyesdad']  # 目标变量

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 拆分数据集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 参数网格
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['rbf'],
    'gamma': ['scale', 'auto', 0.1, 1]
}

# 使用 GridSearchCV 调优超参数
grid_search = GridSearchCV(SVC(), param_grid, cv=5, verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

y_pred = grid_search.best_estimator_.predict(X_test)

# 评估模型
print("Accuracy:", accuracy_score(y_test, y_pred))

X_new = pd.read_csv('processed_test.csv')

y_pred_new = grid_search.best_estimator_.predict(X_new)

X_new['NObeyesdad'] = y_pred_new
X_new.to_csv("predicted_results.csv", index=True)