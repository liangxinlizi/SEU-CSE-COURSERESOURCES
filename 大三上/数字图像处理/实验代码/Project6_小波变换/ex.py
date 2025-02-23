import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pywt

def add_gaussian_noise(image, mean=0, std_dev=20):
    """添加高斯噪声到图像"""
    noise = np.random.normal(mean, std_dev, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 255)  # 确保像素值在 [0, 255]

def wavelet_denoise(image, wavelet='haar', level=3, threshold=30, mode='soft'):
    """使用小波去噪"""
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    denoised_coeffs = [coeffs[0]]  # 保留近似部分
    # 阈值化细节系数
    for detail in coeffs[1:]:
        h, v, d = detail
        h = pywt.threshold(h, threshold, mode)
        v = pywt.threshold(v, threshold, mode)
        d = pywt.threshold(d, threshold, mode)
        denoised_coeffs.append((h, v, d))
    # 小波重构
    return pywt.waverec2(denoised_coeffs, wavelet)

def wavelet_approximation_based_edge_detection(image, wavelet='haar', level=3):
    """消除最低尺度近似分量，再进行反变换"""
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    coeffs[0] = np.zeros_like(coeffs[0])  # 设置最低尺度的近似分量为零
    coeffs[0] = np.zeros_like(coeffs[0])  # 设置最低尺度的近似分量为零
    reconstructed_image = pywt.waverec2(coeffs, wavelet)
    if np.max(reconstructed_image) == 0:  # 检查是否为全零
        print(f"Warning: Edge detection for {wavelet} resulted in a blank image.")

    return pywt.waverec2(coeffs, wavelet)

if __name__ == "__main__":
    # 图像路径
    image_path = r'photo.tif'

    # 读取图像并转换为灰度图
    image = Image.open(image_path).convert('L')
    image_array = np.array(image, dtype=np.float32)

    # 参数配置
    wavelets = ['haar', 'coif1', 'db4', 'sym2']
    level = 2
    threshold = 30
    mode = 'soft'
    noise_std_dev = 20

    # 添加高斯噪声
    noisy_image = add_gaussian_noise(image_array, mean=0, std_dev=noise_std_dev)

    # 创建大图
    plt.figure(figsize=(20, 8))

    # 原始图像
    plt.subplot(2, 5, 1)
    plt.title("Original")
    plt.imshow(image_array, cmap='gray')
    plt.axis('off')

    # 含噪声图像
    plt.subplot(2, 5, 2)
    plt.title("Noisy")
    plt.imshow(noisy_image, cmap='gray')
    plt.axis('off')

    # 逐一处理每种小波
    for i, wavelet in enumerate(wavelets):
        # 去噪图像
        denoised_image = wavelet_denoise(noisy_image, wavelet=wavelet, level=level, threshold=threshold, mode=mode)
        # 边缘检测
        edge_image = wavelet_approximation_based_edge_detection(denoised_image, wavelet, level)

        # 去噪结果
        plt.subplot(2, 5, 3 + i)
        plt.title(f"Denoised ({wavelet})")
        plt.imshow(np.clip(denoised_image, 0, 255), cmap='gray')
        plt.axis('off')

        # 边缘检测结果
        plt.subplot(2, 5, 7 + i)
        plt.title(f"Edges ({wavelet})")
        plt.imshow(edge_image, cmap='gray')
        plt.axis('off')

    # 保存和展示结果
    plt.tight_layout()
    output_path = 'comparison_output.png'
    plt.savefig(output_path)
    plt.show()
