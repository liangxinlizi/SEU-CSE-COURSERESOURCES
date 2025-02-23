import os
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# 设置pandas显示选项以显示所有列
pd.set_option('display.max_columns', None)

# 数据集定义
class ObesityDataset(Dataset):
    def __init__(self, data, labels=None):
        self.data = torch.tensor(data.values, dtype=torch.float32)
        self.labels = labels
        if self.labels is not None:
            self.labels = torch.tensor(labels.values, dtype=torch.long)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if self.labels is not None:
            return self.data[idx], self.labels[idx]
        else:
            return self.data[idx]

# 模型定义
class ResidualBlock(nn.Module):
    def __init__(self, in_features, out_features):
        super(ResidualBlock, self).__init__()
        self.fc1 = nn.Linear(in_features, out_features)
        self.fc2 = nn.Linear(out_features, out_features)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

        if in_features != out_features:
            self.shortcut = nn.Linear(in_features, out_features)
        else:
            self.shortcut = nn.Identity()

    def forward(self, x):
        residual = self.shortcut(x)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        x += residual
        x = self.relu(x)
        return x

class SimplifiedObesityClassifier(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SimplifiedObesityClassifier, self).__init__()
        self.res_block1 = ResidualBlock(input_dim, 64)
        self.res_block2 = ResidualBlock(64, 32)
        self.fc_final = nn.Linear(32, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.fc_final(x)
        return x

# 读取训练数据
train_data = pd.read_csv('train.csv')

# 提取特征和标签
train_features = train_data.drop(columns=['id', 'NObeyesdad'])  # 删除ID和标签列
train_labels = train_data['NObeyesdad']

# 类别编码
le = LabelEncoder()
train_labels = le.fit_transform(train_labels)  # 将标签转换为数值

# 检查并处理 CALC 字段
calc_values = train_features['CALC'].unique()
if 'Always' not in calc_values:
    # 如果 'Always' 不在 CALC 的值中，手动添加并进行独热编码
    train_features.loc[len(train_features)] = ['Always'] + [None] * (len(train_features.columns) - 1)
    train_features = pd.get_dummies(train_features, columns=['CALC'], drop_first=True)
    # 移除临时添加的行
    train_features = train_features[:-1]
else:
    # 如果 'Always' 存在于 CALC 中，直接进行独热编码
    train_features = pd.get_dummies(train_features, columns=['CALC'], drop_first=True)

# 确保 CALC_Always 列存在
if 'CALC_Always' not in train_features.columns:
    train_features['CALC_Always'] = 0

# 编码分类特征
train_features = pd.get_dummies(train_features, drop_first=True)  # One-Hot编码

# 打印独热编码后的输入特征的前几行
print("One-hot encoded features:")
print(train_features.head())

# 特征标准化
scaler = StandardScaler()
train_features_scaled = scaler.fit_transform(train_features)

# 数据集划分
X_train, X_val, y_train, y_val = train_test_split(train_features_scaled, train_labels, test_size=0.2, random_state=42)

# 转换为PyTorch数据集
train_dataset = ObesityDataset(pd.DataFrame(X_train, columns=train_features.columns), pd.Series(y_train))
val_dataset = ObesityDataset(pd.DataFrame(X_val, columns=train_features.columns), pd.Series(y_val))

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# 初始化设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 模型保存路径
model_path = 'obesity_classifier3.pth'

# 加载模型或重新训练
if os.path.exists(model_path):
    print(f"Loading model from {model_path}")
    model = SimplifiedObesityClassifier(input_dim=X_train.shape[1], output_dim=len(le.classes_)).to(device)
    model.load_state_dict(torch.load(model_path))
else:
    print("Training new model...")
    model = SimplifiedObesityClassifier(input_dim=X_train.shape[1], output_dim=len(le.classes_)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=0.001)  # 添加L2正则化

    # 训练模型并每隔1个epoch计算一次准确率
    num_epochs = 1000
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

        # 验证集评估
        model.eval()
        val_loss = 0.0
        correct, total = 0, 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()
                val_loss += criterion(outputs, targets).item()

        val_loss /= len(val_loader)
        print(f"Validation Loss after Epoch [{epoch+1}]: {val_loss:.4f}")
        print(f"Validation Accuracy after Epoch [{epoch+1}]: {100 * correct / total:.2f}%")

    # 训练结束后保存模型
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")


# 读取测试数据
test_data = pd.read_csv('test.csv')
test_ids = test_data['id']
test_features = test_data.drop(columns=['id'])

# 检查并处理 CALC 字段
calc_values = test_features['CALC'].unique()
if 'Always' not in calc_values:
    # 如果 'Always' 不在 CALC 的值中，手动添加并进行独热编码
    test_features.loc[len(test_features)] = ['Always'] + [None] * (len(test_features.columns) - 1)
    test_features = pd.get_dummies(test_features, columns=['CALC'], drop_first=True)
    # 移除临时添加的行
    test_features = test_features[:-1]
else:
    # 如果 'Always' 存在于 CALC 中，直接进行独热编码
    test_features = pd.get_dummies(test_features, columns=['CALC'], drop_first=True)

# 确保 CALC_Always 列存在
if 'CALC_Always' not in test_features.columns:
    test_features['CALC_Always'] = 0

# 编码分类特征
test_features = pd.get_dummies(test_features, drop_first=True)  # One-Hot编码

# 确保测试集特征与训练集特征一致
missing_cols = set(train_features.columns) - set(test_features.columns)
for col in missing_cols:
    test_features[col] = 0

extra_cols = set(test_features.columns) - set(train_features.columns)
test_features = test_features[train_features.columns]

# 特征标准化
test_features_scaled = scaler.transform(test_features)

# 转换为PyTorch数据集
test_dataset = ObesityDataset(pd.DataFrame(test_features_scaled, columns=train_features.columns))
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# 在测试集上进行预测
model.eval()
predictions = []
with torch.no_grad():
    for inputs in test_loader:
        inputs = inputs.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        predictions.extend(predicted.cpu().numpy())

# 解码预测结果
predicted_classes = le.inverse_transform(predictions)

# 创建提交文件
submission_df = pd.DataFrame({
    'id': test_ids,
    'NObeyesdad': predicted_classes
})

submission_df.to_csv('submission.csv', index=False)
print("Submission file generated successfully.")