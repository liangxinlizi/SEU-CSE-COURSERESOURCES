import cv2
import numpy as np
import matplotlib.pyplot as plt


# 读取图像
def read_image(file_path):
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return img


# 二阶导数（Laplacian）锐化函数
def laplacian_sharpen(image):
    # 定义Laplacian Kernel
    laplacian_kernel = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])

    # 计算二阶导数
    laplacian = cv2.filter2D(image, -1, laplacian_kernel)

    # 原图与Laplacian结果相减
    sharpened_image = cv2.subtract(image, laplacian)
    return sharpened_image


# 自定义高斯模糊函数
def gaussian_blur(image, kernel_size=(3, 3), sigma=1.0):
    # 使用高斯模糊平滑图像
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
    return blurred_image


# 高提升滤波（High-boost）锐化函数（使用高斯模糊进行平滑）
def highboost_sharpen(image, A=1.5, kernel_size=(3, 3), sigma=1.0):
    # 使用自定义的高斯模糊函数进行平滑
    smoothed_image = gaussian_blur(image, kernel_size, sigma)

    # 计算掩膜：原图 - 平滑图像
    mask = cv2.subtract(image, smoothed_image)

    # 将掩膜加入到原图：A * 原图 + mask
    sharpened_image = cv2.addWeighted(image, A, mask, 1, 0)

    return sharpened_image


# 展示图像
def display_images(original, sharpened, method):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original, cmap='gray')

    plt.subplot(1, 2, 2)
    plt.title(f"Sharpened Image ({method})")
    plt.imshow(sharpened, cmap='gray')

    plt.show()


# 执行二阶导数（Laplacian）锐化
image_2_1 = read_image("2_1.tif")
sharpened_2_1 = laplacian_sharpen(image_2_1)
display_images(image_2_1, sharpened_2_1, "Laplacian")

# 执行高提升滤波（High-boost）锐化（使用高斯模糊）
image_2_2 = read_image("2_2.png")
sharpened_2_2 = highboost_sharpen(image_2_2, A=1.5, kernel_size=(5, 5), sigma=1.0)
display_images(image_2_2, sharpened_2_2, "High-boost (Gaussian Blur)")
