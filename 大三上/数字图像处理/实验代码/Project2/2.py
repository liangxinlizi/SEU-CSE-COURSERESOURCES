import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 读取图像并将其转换为灰度图，同时将像素值归一化到 [0, 1] 范围
def load_image(image_path):
    image = Image.open(image_path).convert('L')  # 打开并转换为灰度图
    return np.array(image) / 255.0  # 归一化像素值至 [0, 1]

# 实现直方图均衡化，并返回均衡化后的图像和归一化的CDF
def histogram_equalization(image):
    # 计算图像的直方图，统计每个灰度级的像素数量
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 1])

    # 计算累积分布函数 (CDF)，即直方图的累加
    cdf = hist.cumsum()  # 逐步累加每个灰度级的像素数量

    # 归一化 CDF，将它缩放到 [0, 255]，并对新像素值进行四舍五入
    cdf_normalized = (cdf - cdf.min()) / (cdf.max() - cdf.min()) * 255
    sk = np.round(cdf_normalized).astype('uint8')  # 转换为 uint8 类型表示像素值

    # 将原图像的归一化灰度值转换回 [0, 255]，以便进行映射
    img_flat = (image * 255).astype('uint8')  # 恢复像素值到 [0, 255]
    equalized_image = sk[img_flat]  # 使用CDF映射原始像素值到新的均衡化值

    return equalized_image / 255.0, cdf_normalized / 255.0  # 返回归一化的图像和 CDF

# 显示图像及其对应的直方图
def plot_image_and_hist(image, equalized_image, cdf, index):
    # 分别计算原图和均衡化图像的直方图
    hist_orig, bins_orig = np.histogram(image.flatten(), bins=256, range=[0, 1])
    hist_eq, bins_eq = np.histogram(equalized_image.flatten(), bins=256, range=[0, 1])

    # 创建子图，用于显示原图、处理后的图像及其直方图
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # 显示原始图像
    axes[0, 0].imshow(image * 255, cmap='gray', vmin=0, vmax=255)  # 恢复到灰度值范围
    axes[0, 0].set_title(f'Original Image {index}')  # 设置标题
    axes[0, 0].axis('off')  # 隐藏坐标轴

    # 显示均衡化后的图像
    axes[0, 1].imshow(equalized_image, cmap='gray')  # 显示归一化后的图像
    axes[0, 1].set_title(f'Equalized Image {index}')
    axes[0, 1].axis('off')

    # 显示原图的直方图
    axes[1, 0].bar(bins_orig[:-1], hist_orig, width=0.005, color='gray')  # 绘制直方图
    axes[1, 0].set_title('Original Histogram')

    # 显示均衡化后的直方图
    axes[1, 1].bar(bins_eq[:-1], hist_eq, width=0.005, color='gray')
    axes[1, 1].set_title('Equalized Histogram')

    # 调整布局并保存图像
    plt.tight_layout()
    plt.savefig(f'image_histogram_{index}.png')  # 保存图像
    plt.close()  # 关闭当前窗口以节省内存

# 图像路径列表，用于批量处理
image_paths = ['photo2_1.tif', 'photo2_2.tif', 'photo2_3.tif', 'photo2_4.tif']

# 用于存储每张图像的CDF数据
cdfs = []

# 逐个处理图像
for i, image_path in enumerate(image_paths, start=1):
    image = load_image(image_path)  # 加载图像
    equalized_image, cdf = histogram_equalization(image)  # 进行直方图均衡化
    cdfs.append(cdf)  # 保存每张图像的CDF

    # 显示并保存图像和直方图
    plot_image_and_hist(image, equalized_image, cdf, i)
