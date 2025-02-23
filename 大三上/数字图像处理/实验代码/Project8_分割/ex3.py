import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread


# Otsu 方法
def otsu_threshold(image):
    # 计算灰度直方图
    hist, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    total_pixels = image.size

    # 归一化直方图 (每个灰度级的概率)
    pixel_probs = hist / total_pixels

    # 初始化变量
    max_variance = 0
    optimal_threshold = 0
    sum_total = np.sum(np.arange(256) * pixel_probs)  # 整体灰度值的加权平均
    sum_foreground = 0
    weight_foreground = 0

    # 遍历每个可能的阈值0-255
    for threshold in range(256):
        # 前景权重 (C1)
        weight_foreground += pixel_probs[threshold]
        if weight_foreground == 0:
            continue

        # 背景权重 (C2)
        weight_background = 1 - weight_foreground
        if weight_background == 0:
            break

        # 前景平均灰度
        sum_foreground += threshold * pixel_probs[threshold]
        mean_foreground = sum_foreground / weight_foreground

        # 背景平均灰度
        mean_background = (sum_total - sum_foreground) / weight_background

        # 类间方差
        variance_between = weight_foreground * weight_background * (mean_foreground - mean_background) ** 2

        # 找到最大类间方差对应的阈值
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_threshold = threshold

    return optimal_threshold


# 应用 Otsu 方法并阈值化图像
def apply_threshold(image, threshold):
    binary_image = (image > threshold).astype(np.uint8) * 255
    return binary_image


# 加载图像 (以灰度模式读取)
image_path = "photo3.tif"  # 替换为你的图像路径
image = imread(image_path, as_gray=True)
image = (image * 255).astype(np.uint8)  # 将像素值归一化到 [0, 255]

# 计算 Otsu 阈值
otsu_thresh = otsu_threshold(image)
print(f"Otsu 方法计算的最佳阈值: {otsu_thresh}")

# 使用阈值进行分割
binary_image = apply_threshold(image, otsu_thresh)

# 显示原图和二值化图像
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title(f"Thresholded Image (T={otsu_thresh})")
plt.imshow(binary_image, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()
