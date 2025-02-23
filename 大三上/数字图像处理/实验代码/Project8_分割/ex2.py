import numpy as np
import matplotlib.pyplot as plt

def my_threshold(src, initial_threshold=150, epsilon=20):
    # 初始化变量
    T1 = initial_threshold
    T = 0
    rows, cols = src.shape
    dst = np.zeros_like(src, dtype=np.uint8)

    # 循环计算阈值直到收敛
    while abs(T1 - T) > epsilon:
        T = T1
        n1, n2 = 0, 0  # 类别 C1 和 C2 的像素数
        sum1, sum2 = 0, 0  # 类别 C1 和 C2 的灰度和

        for i in range(rows):
            for j in range(cols):
                if src[i, j] >= T:
                    n1 += 1
                    sum1 += src[i, j]
                else:
                    n2 += 1
                    sum2 += src[i, j]

        # 计算新阈值
        m1 = sum1 / n1 if n1 > 0 else 0
        m2 = sum2 / n2 if n2 > 0 else 0
        T1 = (m1 + m2) / 2

    # 根据最终阈值生成二值图像
    for i in range(rows):
        for j in range(cols):
            if src[i, j] >= T1:
                dst[i, j] = 255
            else:
                dst[i, j] = 0

    return dst

# 加载灰度图像
def read_image(filepath):
    from skimage.io import imread
    image = imread(filepath, as_gray=True)
    return (image * 255).astype(np.uint8)

# 主函数
if __name__ == "__main__":
    image_path = "photo2.tif"
    src = read_image(image_path)

    # 应用自定义阈值函数
    dst = my_threshold(src)

    # 显示原图和处理后的图像
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(src, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Thresholded Image")
    plt.imshow(dst, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
