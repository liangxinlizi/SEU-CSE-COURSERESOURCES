import cv2
import numpy as np
import matplotlib.pyplot as plt

def adaptive_threshold(image, window_size, a, b):
    pad_size = window_size // 2
    padded_image = np.pad(image, pad_size, mode='edge')

    thresholded_image = np.zeros_like(image, dtype=np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            local_window = padded_image[i:i + window_size, j:j + window_size]
            m_xy = np.mean(local_window)
            sigma_xy = np.std(local_window)
            T_xy = a * sigma_xy + b * m_xy + 1
            thresholded_image[i, j] = 255 if image[i, j] > T_xy else 0

    return thresholded_image

# 读取灰度图像
image_path = r'photo4.tif'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 自适应阈值分割
window_size = 45
a = 0.06
b = 0.96
thresholded_image = adaptive_threshold(image, window_size, a, b)

# 显示结果
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(thresholded_image, cmap='gray')
plt.title('Adaptive Thresholded Image')
plt.axis('off')

plt.tight_layout()
plt.show()
