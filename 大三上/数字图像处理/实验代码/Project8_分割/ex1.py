import numpy as np
import cv2
import matplotlib.pyplot as plt

# 读取图像并转换为灰度图
image_path = "photo1.tif"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用Canny边缘检测
edges = cv2.Canny(gray, 50, 150)

# 使用霍夫变换检测直线
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
lines_image = np.zeros_like(gray)

# 绘制检测到的满足角度范围的所有直线
all_lines = []
if lines is not None:
    for rho, theta in lines[:, 0]:
        if (np.abs(theta) < np.pi / 180):
            all_lines.append((rho, theta))
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

# 提取跑道的两条主要边线
filtered_lines = sorted(all_lines, key=lambda x: abs(x[0]))  # 按 rho 排序
if len(filtered_lines) > 2:
    filtered_lines = filtered_lines[2:8]

runway_image = image.copy()
for rho, theta in filtered_lines:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1250 * (-b))
    y1 = int(y0 + 1250 * (a))
    x2 = int(x0 - 1250 * (-b))
    y2 = int(y0 - 1250 * (a))
    cv2.line(runway_image, (x1, y1), (x2, y2), (0, 0, 255), 3)  # 在原图上绘制蓝色线条

fig, axes = plt.subplots(1, 3, figsize=(20, 5))

# 原始图像
axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axes[0].set_title("a) Original Image")
axes[0].axis("off")

# 边缘检测图像
axes[1].imshow(edges, cmap="gray")
axes[1].set_title("b) Canny Edge Detection")
axes[1].axis("off")


# 跑道的主要边线
axes[2].imshow(cv2.cvtColor(runway_image, cv2.COLOR_BGR2RGB))
axes[2].set_title("d) Runway Lines")
axes[2].axis("off")

plt.tight_layout()
plt.show()
