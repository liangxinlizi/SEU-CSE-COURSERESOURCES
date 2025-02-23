import cv2
import numpy as np
import matplotlib.pyplot as plt
# 设置字体为黑体 (SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
# 读取图像
image = cv2.imread('image2.jpeg')

# 将图像转换为 HSV 颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定义红色的 HSV 范围
lower_red1= np.array([0, 43, 46])  # 0度
upper_red1 = np.array([10, 255, 255])  # 10度
lower_red2 = np.array([156, 43, 46])  # 156度
upper_red2 = np.array([180, 255, 255])   # 180度

# 创建红色掩码
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)  # 0-10度
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)  # 156-180度
red_mask = mask1 + mask2  # 合并掩码

# 对原始图像应用掩码
result = cv2.bitwise_and(image, image, mask=red_mask)

# # 显示结果
# cv2.imshow('Original Image', image)
# cv2.imshow('Red Mask', red_mask)
# cv2.imshow('Segmented Red Strawberries', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 将图像从 BGR 转换为 RGB 格式
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
red_mask_rgb = cv2.cvtColor(red_mask, cv2.COLOR_GRAY2RGB)  # 掩膜是灰度图，转换为RGB
result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(24, 12))
plt.subplot(1, 3, 1), plt.imshow(image_rgb), plt.title('原始图像')
plt.subplot(1, 3, 2), plt.imshow(red_mask_rgb), plt.title('掩膜')
plt.subplot(1, 3, 3), plt.imshow(result_rgb), plt.title('结果')
output_path='Lab2.png'
plt.savefig(output_path,dpi=300,bbox_inches='tight')
