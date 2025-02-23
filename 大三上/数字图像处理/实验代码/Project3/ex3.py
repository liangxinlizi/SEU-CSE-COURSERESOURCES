import cv2
import numpy as np
import matplotlib.pyplot as plt

# 加载图像
image = cv2.imread('3_1.jpg', cv2.IMREAD_GRAYSCALE)

# 转换为频域
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT) # 转换为复数形式, 并进行傅里叶变换
dft_shift = np.fft.fftshift(dft) # 频谱平移，使得低频在频谱中心，高频移动到边缘

# 创建掩膜
rows, cols = image.shape # 获取图像的行列数
crow, ccol = rows // 2, cols // 2 # 获取图像的中心点坐标
mask = np.ones((rows, cols, 2), np.float32)  # 创建一个掩膜矩阵

# 定义要去除的干扰频率的位置
frequencies_to_remove = [(ccol, crow + 35), (ccol, crow - 35)]

# 遍历要处理的位置，将掩膜中对应的区域设置为0
for freq in frequencies_to_remove:
    x, y = freq # 获取频率坐标
    mask[y-5:y+5, x-5:x+5] = 0  # 设置掩膜区域为0

# 应用滤波器
filtered_dft_shift = dft_shift * mask  # 应用陷波滤波器，去除特定的干扰频率

# 转换回空间域
dft_ishift = np.fft.ifftshift(filtered_dft_shift) # 频谱平移，恢复到原来的位置
image_filtered = cv2.idft(dft_ishift) # 进行逆傅里叶变换
image_filtered = cv2.magnitude(image_filtered[:,:,0], image_filtered[:,:,1])

# 提取干扰信号的空间模式
# 创建一个与原图相同大小的掩膜，将未去除的频率部分设置为0
interference_mask = np.ones((rows, cols, 2), np.float32)
for freq in frequencies_to_remove:
    x, y = freq
    interference_mask[y-5:y+5, x-5:x+5] = 0  # 将干扰频率区域设置为0

# 应用掩膜到原始频域信号，以提取干扰信号
interference_dft = dft_shift * (1 - interference_mask)

# 转换干扰信号回空间域
dft_interference_ishift = np.fft.ifftshift(interference_dft)
interference_signal = cv2.idft(dft_interference_ishift)
interference_signal = cv2.magnitude(interference_signal[:,:,0], interference_signal[:,:,1])

# 显示结果
plt.figure(figsize=(12, 8))

plt.subplot(1, 3, 1)
plt.title('original')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('filtered')
plt.imshow(image_filtered, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('interference')
plt.imshow(np.log1p(interference_signal), cmap='gray')
plt.axis('off')

plt.show()
