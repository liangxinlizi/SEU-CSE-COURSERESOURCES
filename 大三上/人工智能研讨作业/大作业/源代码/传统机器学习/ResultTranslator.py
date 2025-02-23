import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

# 读取数据
data = pd.read_csv("train.csv")

# 目标变量编码
label_encoder = LabelEncoder()
data['NObeyesdad'] = label_encoder.fit_transform(data['NObeyesdad'])

# 读取结果文件
predicted_data = pd.read_csv("predicted_results.csv")

predicted_data['NObeyesdad'] = label_encoder.inverse_transform(predicted_data['NObeyesdad'])

# 打印或保存解码后的结果
predicted_data.to_csv("decoded_predicted_results.csv", index=False)
