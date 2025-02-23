import cv2
import numpy as np
import matplotlib.pyplot as plt


# 图像二值化函数
def binarize_image(gray_image, threshold=127):
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return binary_image


# 自定义图像骨架化函数
def skeletonize(binary_image):
     # 创建一个空白的输出图像
    skeleton = np.zeros_like(binary_image)
    # 结构元素
    kernel = np.ones((3, 3), np.uint8)  # 3x3的矩形结构元素

    # 迭代腐蚀和膨胀操作，提取骨架
    while True:
        # 腐蚀操作
        eroded = cv2.erode(binary_image, kernel)
        # 开操作
        opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
        # 骨架部分计算：腐蚀结果减去开操作结果
        temp = cv2.subtract(eroded, opened)
        # 将骨架部分加到输出图像
        skeleton = cv2.bitwise_or(skeleton, temp)
        # 更新二值图像，进行下一轮迭代
        binary_image = eroded.copy()

        # 如果已经没有更多的骨架，退出
        if cv2.countNonZero(binary_image) == 0:
            break
    return skeleton


# 使用 OpenCV 提供的骨架化函数
def skeletonize_opencv(binary_image):
    # 使用OpenCV的thinning函数进行骨架化
    skeleton = cv2.ximgproc.thinning(binary_image)
    return skeleton


# 读取原始图像
image = cv2.imread('photo.png')
# 转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 将图像二值化
binary_image = binarize_image(gray_image)
# 提取中心线（骨架）使用自定义函数
skeleton_custom = skeletonize(binary_image)
# 提取中心线（骨架）使用OpenCV的函数
skeleton_opencv = skeletonize_opencv(binary_image)
# 打印骨架中非零像素的数量，检查是否有效提取了骨架
print(f"Number of non-zero pixels in skeleton (custom): {cv2.countNonZero(skeleton_custom)}")
print(f"Number of non-zero pixels in skeleton (opencv): {cv2.countNonZero(skeleton_opencv)}")
# 将骨架从二值图像转换为红色线条（自定义方法）
skeleton_colored_custom = np.zeros_like(image)
skeleton_colored_custom[skeleton_custom == 255] = [0, 0, 255]  # 红色的中心线
# 将骨架从二值图像转换为红色线条（OpenCV方法）
skeleton_colored_opencv = np.zeros_like(image)
skeleton_colored_opencv[skeleton_opencv == 255] = [0, 0, 255]  # 红色的中心线
# 将中心线叠加到原图像上（自定义方法）
overlay_image_custom = cv2.addWeighted(image, 0.7, skeleton_colored_custom, 1, 0)
# 将中心线叠加到原图像上（OpenCV方法）
overlay_image_opencv = cv2.addWeighted(image, 0.7, skeleton_colored_opencv, 1, 0)
# 显示骨架提取后的红色线条（自定义方法）
cv2.imshow('Skeleton Colored Custom', skeleton_colored_custom)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 显示骨架提取后的红色线条（OpenCV方法）
cv2.imshow('Skeleton Colored OpenCV', skeleton_colored_opencv)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 显示原图像和叠加后的图像对比
plt.figure(figsize=(10, 10))

# 原图
plt.subplot(2, 2, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

# 使用自定义方法叠加的图像
plt.subplot(2, 2, 2)
plt.title("Image with Centerline Overlay (Custom)")
plt.imshow(cv2.cvtColor(overlay_image_custom, cv2.COLOR_BGR2RGB))
plt.axis('off')

# 使用OpenCV方法叠加的图像
plt.subplot(2, 2, 3)
plt.title("Image with Centerline Overlay (OpenCV)")
plt.imshow(cv2.cvtColor(overlay_image_opencv, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()
