import os
import numpy as np
import cv2

# 创建输出文件夹
output_folder = "outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取图像
def read_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Image at path '{path}' could not be read.")
    return img

# 生成频率坐标网格和距离矩阵
def frequency_grid(rows, cols):
    u = np.arange(-cols / 2, cols / 2)
    v = np.arange(-rows / 2, rows / 2)
    u, v = np.meshgrid(u, v)
    D = np.sqrt(u ** 2 + v ** 2)
    return u, v, D

# 大气湍流模型
def atmospheric_turbulence(img, k=0.001):
    rows, cols = img.shape
    fft_img = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft_img)

    _, _, D = frequency_grid(rows, cols)
    H = np.exp(-k * (D ** (5 / 3)))

    fft_blurred = fft_shift * H
    img_blurred = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_blurred)))
    return np.clip(img_blurred, 0, 255).astype(np.uint8)

# 运动模糊模型
def motion_blur(img, a=0.1, b=0.1, T=1):
    rows, cols = img.shape
    u, v, _ = frequency_grid(rows, cols)

    denominator = (u * a + v * b)
    H = (T / (np.pi * denominator)) * np.sin(np.pi * denominator)
    H[np.isnan(H)] = 0

    fft_img = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft_img) * H
    img_blurred = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_shift)))
    return np.clip(img_blurred, 0, 255).astype(np.uint8)

# 加性高斯噪声
def add_gaussian_noise(img, mean=0, std=10):
    noise = np.random.normal(mean, std, img.shape)
    noisy_img = img + noise
    return np.clip(noisy_img, 0, 255).astype(np.uint8)

# 逆滤波
def inverse_filtering(img, H, HB, threshold=1e-6):
    H_inverse = np.where(np.abs(H) > threshold, 1 / H, 0)
    fft_img = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft_img)

    dft_filtered = fft_shift * H_inverse * HB
    img_restored = np.abs(np.fft.ifft2(np.fft.ifftshift(dft_filtered)))
    return np.clip(img_restored, 0, 255).astype(np.uint8)

# 维纳滤波
def wiener_filtering(img, H, K=0.01):
    fft_img = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft_img)

    HW = np.conj(H) / (np.abs(H) ** 2 + K)
    dft_filtered = fft_shift * HW
    img_restored = np.abs(np.fft.ifft2(np.fft.ifftshift(dft_filtered)))
    return np.clip(img_restored, 0, 255).astype(np.uint8)

# 运行退化处理并保存结果
def process_images(photo1_path, photo2_path):
    photo1 = read_image(photo1_path)
    photo2 = read_image(photo2_path)

    photo1_turbulence = atmospheric_turbulence(photo1)
    photo1_turbulence_noisy = add_gaussian_noise(photo1_turbulence)

    photo2_motion_blur = motion_blur(photo2)
    photo2_motion_blur_noisy = add_gaussian_noise(photo2_motion_blur)

    # 生成退化函数
    rows1, cols1 = photo1.shape
    _, _, D1 = frequency_grid(rows1, cols1)
    H_turbulence = np.exp(-0.002 * (D1 ** (5 / 3)))
    HB_turbulence = 1 / (1 + (D1 / 60) ** 20)

    rows2, cols2 = photo2.shape
    u2, v2, D2 = frequency_grid(rows2, cols2)
    H_motion_blur = (1 / (np.pi * (u2 * 0.1 + v2 * 0.1))) * np.sin(np.pi * (u2 * 0.1 + v2 * 0.1))
    H_motion_blur[np.isnan(H_motion_blur)] = 0
    HB_motion_blur = 1 / (1 + (D2 / 60) ** 10)

    # 逆滤波恢复
    photo1_restored_inverse = inverse_filtering(photo1_turbulence_noisy, H_turbulence, HB_turbulence)
    photo2_restored_inverse = inverse_filtering(photo2_motion_blur_noisy, H_motion_blur, HB_motion_blur)

    # 维纳滤波恢复
    photo1_restored_wiener = wiener_filtering(photo1_turbulence_noisy, H_turbulence)
    photo2_restored_wiener = wiener_filtering(photo2_motion_blur_noisy, H_motion_blur)

    # 保存结果
    cv2.imwrite(os.path.join(output_folder, "photo1_original.png"), photo1)
    cv2.imwrite(os.path.join(output_folder, "photo1_turbulence.png"), photo1_turbulence)
    cv2.imwrite(os.path.join(output_folder, "photo1_turbulence_noisy.png"), photo1_turbulence_noisy)
    cv2.imwrite(os.path.join(output_folder, "photo1_restored_inverse.png"), photo1_restored_inverse)
    cv2.imwrite(os.path.join(output_folder, "photo1_restored_wiener.png"), photo1_restored_wiener)

    cv2.imwrite(os.path.join(output_folder, "photo2_original.png"), photo2)
    cv2.imwrite(os.path.join(output_folder, "photo2_motion_blur.png"), photo2_motion_blur)
    cv2.imwrite(os.path.join(output_folder, "photo2_motion_blur_noisy.png"), photo2_motion_blur_noisy)
    cv2.imwrite(os.path.join(output_folder, "photo2_restored_inverse.png"), photo2_restored_inverse)
    cv2.imwrite(os.path.join(output_folder, "photo2_restored_wiener.png"), photo2_restored_wiener)

# 测试代码
process_images("photo1.png", "photo2.jpg")
