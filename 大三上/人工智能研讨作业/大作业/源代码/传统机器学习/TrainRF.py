import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("processed_data.csv")

param_grid = {
    'n_estimators': [100, 200],       # 决策树的数量，减少到 2 个选项
    'max_depth': [None, 10],           # 树的最大深度，减少到 2 个选项
    'min_samples_split': [2, 5],       # 最小拆分样本数，保持 2 个选项
    'min_samples_leaf': [1, 2],        # 最小叶子节点样本数，减少到 2 个选项
    'max_features': ['auto', 'sqrt'],  # 特征选择策略，保持 2 个选项
    'bootstrap': [True, False],        # 是否使用自助法采样，保持 2 个选项
    'class_weight': ['balanced', None] # 类别权重，保持 2 个选项
}

# 特征和目标变量
X = data.drop('NObeyesdad', axis=1)  # 特征
X['CALC_Always'] = False
y = data['NObeyesdad']  # 目标变量

# 数据拆分：80% 训练集，20% 测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化随机森林分类器
model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                           cv=5, n_jobs=-1, verbose=2, scoring='accuracy')

# 训练模型
grid_search.fit(X_train, y_train)

# 打印最佳超参数
print("Best parameters found: ", grid_search.best_params_)

# 使用最佳参数训练的模型
best_rf = grid_search.best_estimator_

y_pred = best_rf.predict(X_test)

# 获取特征重要性
feature_importance = best_rf.feature_importances_
feature_names = X.columns

X_new = pd.read_csv('processed_test.csv')

y_pred_new = best_rf.predict(X_new)

X_new['NObeyesdad'] = y_pred_new
X_new.to_csv("predicted_results.csv", index=True)

print(X_new[['Predicted_NObeyesdad']].head())  # 打印预测结果的前几行