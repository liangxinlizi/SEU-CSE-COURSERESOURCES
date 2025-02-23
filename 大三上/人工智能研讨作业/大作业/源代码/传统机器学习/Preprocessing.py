import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

# 读取数据
data = pd.read_csv("train.csv")

# 删除 id 列
data.drop("id", axis=1, inplace=True)

# 编码二元变量
binary_vars = ['Gender', 'family_history_with_overweight', 'FAVC', 'SMOKE', 'SCC']
binary_map = {'yes': 1, 'no': 0, 'Male': 1, 'Female': 0}
data[binary_vars] = data[binary_vars].replace(binary_map)

# 多类型变量独热编码
multi_class_vars = ['CAEC', 'CALC', 'MTRANS']
data = pd.get_dummies(data, columns=multi_class_vars, drop_first=False)

# 目标变量编码
label_encoder = LabelEncoder()
data['NObeyesdad'] = label_encoder.fit_transform(data['NObeyesdad'])

# 数值变量标准化
numeric_vars = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
scaler = StandardScaler()
data[numeric_vars] = scaler.fit_transform(data[numeric_vars])

# 保存数据
data.to_csv("processed_data.csv", index=False)