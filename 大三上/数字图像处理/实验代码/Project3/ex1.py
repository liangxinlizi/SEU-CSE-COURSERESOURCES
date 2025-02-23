import numpy as np
import cv2
import matplotlib.pyplot as plt


# 定义高斯核函数
def gaussian_kernel(size, sigma):
    # 输入滤波核的大小和高斯分布标准差
    k = size // 2 # 计算滤波核的半径
    x, y = np.mgrid[-k:k + 1, -k:k + 1] # 创建坐标矩阵
    g = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2)) # 用高斯公式计算每个点的权重值
    return g / g.sum() # 把权重归一化，使总和为1，确保图像亮度保持一致


# 自定义卷积操作
def apply_filter(image, kernel):
    # 输入图像和滤波核，输出滤波后的图像
    img_height, img_width = image.shape # 获取图像的大小
    kernel_size = kernel.shape[0] # 获取卷积核的大小
    pad_size = kernel_size // 2 # 获取填充像素的数量
    padded_image = np.pad(image, pad_size, mode='constant') # 0填充图像

    result = np.zeros_like(image) # 创建滤波卷积结果图像
    for i in range(img_height):
        for j in range(img_width):
            window = padded_image[i:i + kernel_size, j:j + kernel_size] # 获取与卷积核大小相同的滤波窗口
            result[i, j] = np.sum(window * kernel) # 对窗口里的像素和卷积核进行卷积

    return result


# 自定义中值滤波
def median_filter(image, kernel_size):
    # 输入图像和滤波核大小，输出滤波后的图像
    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='constant')
    result = np.zeros_like(image)

    img_height, img_width = image.shape
    for i in range(img_height):
        for j in range(img_width):
            window = padded_image[i:i + kernel_size, j:j + kernel_size] # 获取与滤波核大小相同的滤波窗口
            result[i, j] = np.median(window) # 对窗口里的像素求中值

    return result


# 读取图像
image_noisy1_1 = cv2.imread('1_1_1.tif', cv2.IMREAD_GRAYSCALE)
image_noisy1_2 = cv2.imread('1_1_2.tif', cv2.IMREAD_GRAYSCALE)
image_clean1 = cv2.imread('1_1_3.tif', cv2.IMREAD_GRAYSCALE)

image_noisy2_1 = cv2.imread('1_2_1.jpg', cv2.IMREAD_GRAYSCALE)
image_noisy2_2 = cv2.imread('1_2_2.jpg', cv2.IMREAD_GRAYSCALE)
image_clean2 = cv2.imread('1_2_3.jpg', cv2.IMREAD_GRAYSCALE)

# 定义高斯滤波器参数
kernel_size = 5
sigma = 1.5
gaussian_k = gaussian_kernel(kernel_size, sigma)

# 对图像进行高斯滤波
image_gaussian1_1 = apply_filter(image_noisy1_1, gaussian_k)
image_gaussian1_2 = apply_filter(image_noisy1_2, gaussian_k)

image_gaussian2_1 = apply_filter(image_noisy2_1, gaussian_k)
image_gaussian2_2 = apply_filter(image_noisy2_2, gaussian_k)

# 对图像进行自定义中值滤波
image_median1_1 = median_filter(image_noisy1_1, kernel_size)
image_median1_2 = median_filter(image_noisy1_2, kernel_size)

image_median2_1 = median_filter(image_noisy2_1, kernel_size)
image_median2_2 = median_filter(image_noisy2_2, kernel_size)

# 显示处理后的结果
plt.figure(figsize=(12, 10))

# 第一组
plt.subplot(4, 4, 1), plt.imshow(image_noisy1_1, cmap='gray')
plt.title('Noisy Image 1_1'), plt.axis('off')

plt.subplot(4, 4, 2), plt.imshow(image_gaussian1_1, cmap='gray')
plt.title('Gaussian Filtered 1_1'), plt.axis('off')

plt.subplot(4, 4, 3), plt.imshow(image_median1_1, cmap='gray')
plt.title('Median Filtered 1_1'), plt.axis('off')

plt.subplot(4, 4, 4), plt.imshow(image_clean1, cmap='gray')
plt.title('Clean Image 1_3'), plt.axis('off')

plt.subplot(4, 4, 5), plt.imshow(image_noisy1_2, cmap='gray')
plt.title('Noisy Image 1_2'), plt.axis('off')

plt.subplot(4, 4, 6), plt.imshow(image_gaussian1_2, cmap='gray')
plt.title('Gaussian Filtered 1_2'), plt.axis('off')

plt.subplot(4, 4, 7), plt.imshow(image_median1_2, cmap='gray')
plt.title('Median Filtered 1_2'), plt.axis('off')

plt.subplot(4, 4, 8), plt.imshow(image_clean1, cmap='gray')
plt.title('Clean Image 1_3'), plt.axis('off')

# 第二组
plt.subplot(4, 4, 9), plt.imshow(image_noisy2_1, cmap='gray')
plt.title('Noisy Image 2_1'), plt.axis('off')

plt.subplot(4, 4, 10), plt.imshow(image_gaussian2_1, cmap='gray')
plt.title('Gaussian Filtered 2_1'), plt.axis('off')

plt.subplot(4, 4, 11), plt.imshow(image_median2_1, cmap='gray')
plt.title('Median Filtered 2_1'), plt.axis('off')

plt.subplot(4, 4, 12), plt.imshow(image_clean2, cmap='gray')
plt.title('Clean Image 2_3'), plt.axis('off')

plt.subplot(4, 4, 13), plt.imshow(image_noisy2_2, cmap='gray')
plt.title('Noisy Image 2_2'), plt.axis('off')

plt.subplot(4, 4, 14), plt.imshow(image_gaussian2_2, cmap='gray')
plt.title('Gaussian Filtered 2_2'), plt.axis('off')

plt.subplot(4, 4, 15), plt.imshow(image_median2_2, cmap='gray')
plt.title('Median Filtered 2_2'), plt.axis('off')

plt.subplot(4, 4, 16), plt.imshow(image_clean2, cmap='gray')
plt.title('Clean Image 2_3'), plt.axis('off')

plt.tight_layout()
plt.show()
