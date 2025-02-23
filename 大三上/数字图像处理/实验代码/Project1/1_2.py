from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

# 设置字体为黑体 (SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 定义仿射变换函数
def apply_affine_transform(image, matrix, size=None, fillcolor=(255, 255, 255)):
    # 应用仿射变换带背景填充
    return image.transform(size if size else image.size, Image.AFFINE, matrix, fillcolor=fillcolor)

def main():
    input_image_path = 'image.png'
    image = Image.open(input_image_path)

    # 创建输出文件夹
    output_folder = '1_2_results'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 仿射变换矩阵
    transformations = {
        'Translate': [1, 0, 60, 0, 1, 60],  # 平移 (x方向60, y方向60)
        'Rotate': [0, -1, 0, 1, 0, 0],  # 旋转 90度
        'Scale': [1.5, 0, 0, 0, 1.5, 0],  # 放大1.5倍
        'Shear': [1, 0.5, -image.width * 0.2, 0, 1, 0]  # 剪切并调整偏移
    }
    # 创建一个 matplotlib 子图，图像行数为仿射变换数量，每行包含3列，分别显示：原始图像、仿射变换后的图像、逆变换后的图像
    fig, axs = plt.subplots(len(transformations), 3, figsize=(15, 5 * len(transformations)))

    for i, (transform_name, matrix) in enumerate(transformations.items()):
        # 原始图像
        axs[i, 0].imshow(image)
        axs[i, 0].set_title('Original Image\n(未变换的图像)')
        axs[i, 0].axis('on')

        # 处理旋转变换
        if transform_name == 'Rotate':
            angle = 90  # 旋转90度
            transformed_image = image.rotate(angle, expand=True)

        # 处理剪切变换
        elif transform_name == 'Shear':
            new_width = int(image.width + abs(image.height * 0.5))
            transformed_image = apply_affine_transform(image, matrix, size=(new_width, image.height), fillcolor=(255, 255, 255))

        elif transform_name == 'Translate':
            # 创建一个比原图大100像素的空白画布，将原图贴到画布中心，应用平移矩阵，并在超出部分填充白色
            new_size = (image.width + 100, image.height + 100)
            canvas = Image.new('RGB', new_size, (255, 255, 255))
            canvas.paste(image, (50, 50))
            transformed_image = canvas.transform(new_size, Image.AFFINE, matrix, fillcolor=(255, 255, 255))

            # 设置坐标轴范围
            axs[i, 1].set_xlim(0, new_size[0])
            axs[i, 1].set_ylim(new_size[1], 0)  # y轴反转，使坐标与图像位置匹配


        else:
            transformed_image = apply_affine_transform(image, matrix, fillcolor=(255, 255, 255))

        # 保存变换后的图像
        transformed_image_path = os.path.join(output_folder, f'{transform_name}_transformed.jpg')
        transformed_image.save(transformed_image_path)

        # 显示仿射变换后的图像
        axs[i, 1].imshow(transformed_image)
        axs[i, 1].set_title(f'{transform_name}\n(经过{transform_name}变换的图像)')
        axs[i, 1].axis('on')

        # 刷新坐标轴
        axs[i, 1].set_xticks(np.arange(0, new_size[0], step=20))
        axs[i, 1].set_yticks(np.arange(0, new_size[1], step=20))
        axs[i, 1].grid(which='both', color='gray', linestyle='--', linewidth=0.5)

        # 在平移变换中添加坐标标签
        if transform_name == 'Translate':
            for x in range(0, new_size[0], 20):
                axs[i, 1].text(x, new_size[1] - 10, f'({x - 50}, 50)', color='red', fontsize=8)  # 平移后坐标
            for y in range(0, new_size[1], 20):
                axs[i, 1].text(10, new_size[1] - y, f'(50, {y - 50})', color='red', fontsize=8)

        # 应用逆变换
        if transform_name == 'Translate':
            inverse_matrix = [1, 0, -60, 0, 1, -60]  # 反向平移
        elif transform_name == 'Rotate':
            inverse_matrix = [0, 1, 0, -1, 0, 0]  # 反向旋转
        elif transform_name == 'Scale':
            inverse_matrix = [1 / 1.5, 0, 0, 0, 1 / 1.5, 0]  # 反向缩放
        elif transform_name == 'Shear':
            inverse_matrix = [1, -0.5, image.width * 0.2, 0, 1, 0]  # 反向剪切并调整偏移

        if transform_name == 'Rotate':
            inverse_transformed_image = transformed_image.rotate(-angle, expand=True)
        elif transform_name == 'Translate':
            inverse_transformed_image = apply_affine_transform(transformed_image, inverse_matrix, size=new_size, fillcolor=(255, 255, 255)).crop((50, 50, 50 + image.width, 50 + image.height))
        else:
            inverse_transformed_image = apply_affine_transform(transformed_image, inverse_matrix, size=image.size, fillcolor=(255, 255, 255))

        # 保存逆变换后的图像
        inverse_transformed_image_path = os.path.join(output_folder, f'{transform_name}_inverse_transformed.jpg')
        inverse_transformed_image.save(inverse_transformed_image_path)

        # 显示逆变换后的图像
        axs[i, 2].imshow(inverse_transformed_image)
        axs[i, 2].set_title(f'{transform_name} + Inverse\n(经过{transform_name}逆变换的图像)')
        axs[i, 2].axis('on')

        # 刷新坐标轴
        axs[i, 2].set_xlim(0, new_size[0])
        axs[i, 2].set_ylim(new_size[1], 0)  # y轴反转
        axs[i, 2].set_xticks(np.arange(0, new_size[0], step=20))
        axs[i, 2].set_yticks(np.arange(0, new_size[1], step=20))
        axs[i, 2].grid(which='both', color='gray', linestyle='--', linewidth=0.5)

        # 添加逆变换的坐标标签
        if transform_name == 'Translate':
            for x in range(0, new_size[0], 20):
                axs[i, 2].text(x, new_size[1] - 10, f'({x + 60}, 60)', color='blue', fontsize=8)  # 逆变换后的坐标
            for y in range(0, new_size[1], 20):
                axs[i, 2].text(10, new_size[1] - y, f'(60, {y + 60})', color='blue', fontsize=8)

    result_filename = "1_2_result.png"
    plt.tight_layout()
    plt.savefig(result_filename)
    plt.show()

if __name__ == "__main__":
    main()


