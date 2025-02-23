import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 读取图像并将像素值归一化到 [0, 1] 范围
def load_image(image_path):
    image = Image.open(image_path)  # 打开图像文件
    return np.array(image) / 255.0  # 将像素值归一化到 [0, 1]

# 幂律变换函数，gamma 是控制对比度的参数
def power_law_transform(image, gamma):
    # 对每个像素值执行幂运算，调整亮度与对比度
    return np.power(image, gamma)

# 指定两张输入图像的文件路径
image1 = load_image('E:\digital_image_Pro\Project2\photo1_1.png')  # 加载并归一化图像1
image2 = load_image('E:\digital_image_Pro\Project2\photo1_2.jpg')  # 加载并归一化图像2

# 定义不同的 gamma 值列表，控制图像对比度
gamma_values = [0.4, 1.0, 2.5]

# 创建子图结构，每个 gamma 值对应两列（每张图像一列）
fig, axes = plt.subplots(len(gamma_values), 2, figsize=(10, 10))

# 遍历每个 gamma 值，对两张图像分别应用幂律变换
for i, gamma in enumerate(gamma_values):
    # 对图像1应用幂律变换并显示结果
    transformed_image1 = power_law_transform(image1, gamma)  # 对图像1进行变换
    axes[i, 0].imshow(transformed_image1, cmap='gray')  # 使用灰度图显示
    axes[i, 0].set_title(f'Image 1 - Gamma: {gamma}')  # 设置图像标题
    axes[i, 0].axis('off')  # 隐藏坐标轴

    # 对图像2应用幂律变换并显示结果
    transformed_image2 = power_law_transform(image2, gamma)  # 对图像2进行变换
    axes[i, 1].imshow(transformed_image2, cmap='gray')  # 使用灰度图显示
    axes[i, 1].set_title(f'Image 2 - Gamma: {gamma}')  # 设置图像标题
    axes[i, 1].axis('off')  # 隐藏坐标轴

# 调整图像布局，防止子图之间重叠
plt.tight_layout()

# 将结果保存为图像文件
plt.savefig('gamma_transform.png')

# 显示最终的图像结果
plt.show()