from PIL import Image
import os
import numpy as np
# 最近邻插值法，传入图像，目标图像的宽度和高度
def nearest_neighbor(image, new_width, new_height):
    width, height = image.size
    # 创建一个空图像
    resized_image = Image.new("RGB", (new_width, new_height))

    for y in range(new_height):
        for x in range(new_width):
            src_x = int(x * width / new_width)
            src_y = int(y * height / new_height)
            resized_image.putpixel((x, y), image.getpixel((src_x, src_y)))

    return resized_image

# 双线性插值法，传入图像，目标图像的宽度和高度
def bilinear_interpolation(image, new_width, new_height):
    width, height = image.size
    resized_image = Image.new("RGB", (new_width, new_height))

    for y in range(new_height):
        for x in range(new_width):
            # 通过比例映射计算新图像中每个像素在原图中的位置
            src_x = x * (width - 1) / (new_width - 1)
            src_y = y * (height - 1) / (new_height - 1)
            # 获取周围四个最近像素的坐标，并确保边界合理
            x0 = int(src_x)
            x1 = min(x0 + 1, width - 1)
            y0 = int(src_y)
            y1 = min(y0 + 1, height - 1)
            # 提取周围四个像素的颜色值
            c00 = image.getpixel((x0, y0))
            c01 = image.getpixel((x0, y1))
            c10 = image.getpixel((x1, y0))
            c11 = image.getpixel((x1, y1))
            # 线性插值计算颜色值
            r = (c00[0] * (1 - (src_x - x0)) + c10[0] * (src_x - x0)) * (1 - (src_y - y0)) + (c01[0] * (1 - (src_x - x0)) + c11[0] * (src_x - x0)) * (src_y - y0)
            g = (c00[1] * (1 - (src_x - x0)) + c10[1] * (src_x - x0)) * (1 - (src_y - y0)) + (c01[1] * (1 - (src_x - x0)) + c11[1] * (src_x - x0)) * (src_y - y0)
            b = (c00[2] * (1 - (src_x - x0)) + c10[2] * (src_x - x0)) * (1 - (src_y - y0)) + (c01[2] * (1 - (src_x - x0)) + c11[2] * (src_x - x0)) * (src_y - y0)
            # 填充给新图像
            resized_image.putpixel((x, y), (int(r), int(g), int(b)))
    return resized_image

# 定义双三次插值的核函数，计算像素的权重
def cubic_kernel(x):
    abs_x = np.abs(x)
    abs_x2 = abs_x ** 2
    abs_x3 = abs_x ** 3
    # 根据x值的大小，返回不同的权重值
    if abs_x <= 1:
        return 1.5 * abs_x3 - 2.5 * abs_x2 + 1
    elif 1 < abs_x < 2:
        return -0.5 * abs_x3 + 2.5 * abs_x2 - 4 * abs_x + 2
    else:
        return 0

def bicubic_interpolation(image, new_width, new_height):
    # 将图像转换为NumPy数组并获取其宽高
    image_np = np.array(image)
    original_height, original_width = image_np.shape[:2]
    # 创建空白图像并计算缩放比例    
    new_image = np.zeros((new_height, new_width, 3), dtype=np.float32)
    scale_x = original_width / new_width
    scale_y = original_height / new_height
    # 遍历新图像的每个像素，计算其在原图中的位置，并记录其与周围像素的相对位置
    for i in range(new_height):
        for j in range(new_width):
            x = j * scale_x
            y = i * scale_y
            # 计算插值所需的四个最接近的像素点的坐标
            x_int = int(np.floor(x))
            y_int = int(np.floor(y))
            # 计算相对位置
            dx = x - x_int
            dy = y - y_int
            # 对每个颜色通道进行插值
            for c in range(3):
                pixel_value = 0.0
                for m in range(-1, 3):  # 水平方向插值
                    for n in range(-1, 3):  # 垂直方向插值
                        # 获取周围的16个像素点的坐标
                        xi = np.clip(x_int + m, 0, original_width - 1)
                        yi = np.clip(y_int + n, 0, original_height - 1)
                        # 使用核函数计算权重
                        weight = cubic_kernel(m - dx) * cubic_kernel(n - dy)
                        pixel_value += image_np[yi, xi, c] * weight
                new_image[i, j, c] = np.clip(pixel_value, 0, 255)
    # 将插值结果转换为整数类型
    new_image = np.clip(new_image, 0, 255).astype(np.uint8)
    # 将NumPy数组转换回PIL图像
    new_image_pil = Image.fromarray(new_image)
    return new_image_pil

# 定义resize_image函数，输入为输入图片路径，输出文件夹路径，输出图片大小，插值方法
def resize_image(input_path, output_path, size, interpolation_method):
    image = Image.open(input_path)
    if interpolation_method == 'nearest':
        resized_image = nearest_neighbor(image, size[0], size[1])
    elif interpolation_method == 'bilinear':
        resized_image = bilinear_interpolation(image, size[0], size[1])
    elif interpolation_method == 'bicubic':
        resized_image = bicubic_interpolation(image, size[0], size[1])


    resized_image.save(output_path)
    return os.path.getsize(output_path)


def main():
    input_image_path = 'image.png'
    output_folder = '1_1_results'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sizes = [(500,200), (300,400)]
    # 创建插值方法的字典，将插值方法与字符串对应
    resampling_methods = {
        'Nearest Neighbor': 'nearest',
        'Bilinear': 'bilinear',
        'Bicubic': 'bicubic'
    }

    results = []

    for size in sizes:
        for method_name, method in resampling_methods.items():
            output_image_path = os.path.join(output_folder, f'resized_{size[0]}x{size[1]}_{method_name}.jpg')
            file_size = resize_image(input_image_path, output_image_path, size, method)
            results.append((size, method_name, file_size))

    print("Image resizing results:")
    # 输出输入图片的文件大小
    input_file_size = os.path.getsize(input_image_path)
    print(f"Input File Size: {input_file_size} bytes")
    for size, method_name, file_size in results:
        print(f"Size: {size}, Method: {method_name}, File Size: {file_size} bytes")


if __name__ == "__main__":
    main()
