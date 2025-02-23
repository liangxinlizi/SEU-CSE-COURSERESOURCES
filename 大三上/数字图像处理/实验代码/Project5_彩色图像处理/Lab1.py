import numpy as np
import matplotlib.pyplot as plt
from skimage import io

# 设置字体为黑体 (SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 读取图像
image = io.imread('image1.tiff', as_gray=True)

# 中值滤波器
def median_filter(image, kernel_size=3):
    pad_size = kernel_size // 2  # 填充边缘
    padded_image = np.pad(image, pad_size, mode='edge')  # 填充边缘
    filtered_image = np.zeros_like(image)  # 输出图像

    for i in range(image.shape[0]):  # 遍历图像
        for j in range(image.shape[1]):
            window = padded_image[i:i + kernel_size, j:j + kernel_size]
            filtered_image[i, j] = np.median(window) # 中值滤波

    return filtered_image # 返回滤波后的图像


# 自适应中值滤波器
def adaptive_median_filter(image, max_size=7):
    pad_size = max_size // 2  # 填充边缘
    padded_image = np.pad(image, pad_size, mode='edge')  # 填充边缘
    filtered_image = image.copy()  # 输出图像

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            local_area = []  # 局部区域
            for size in range(3, max_size + 1, 2):  # 从3到max_size，逐步增加窗口大小
                win_size = size // 2  # 窗口大小
                window = padded_image[i:i + win_size, j:j + win_size].flatten()  # 局部窗口
                median = np.median(window)  # 中值滤波
                min_val = np.min(window)
                max_val = np.max(window)

                center_pixel = padded_image[i + pad_size, j + pad_size]  # 中心像素

                if min_val < median < max_val:  # 窗口内噪声影响较小，可用中值替代中心像素。
                    if min_val < center_pixel < max_val:  # 局部窗口内有中心像素
                        filtered_image[i, j] = center_pixel  # 局部窗口内有中心像素，直接赋值
                    else:
                        filtered_image[i, j] = median  # 局部窗口内无中心像素，使用中值滤波
                    break
                else:
                    filtered_image[i, j] = median  # 限制最大窗口大小

    return filtered_image


# 应用滤波器
median_filtered = median_filter(image, kernel_size=3)
adaptive_median_filtered = adaptive_median_filter(image, max_size=7)

# 显示图像
plt.figure(figsize=(24, 12))
plt.subplot(1, 3, 1), plt.imshow(image, cmap='gray'), plt.title('原始图像')
plt.subplot(1, 3, 2), plt.imshow(median_filtered, cmap='gray'), plt.title('中值滤波')
plt.subplot(1, 3, 3), plt.imshow(adaptive_median_filtered, cmap='gray'), plt.title('自适应中值滤波')
output_path='Lab1.png'
plt.savefig(output_path,dpi=300,bbox_inches='tight')

