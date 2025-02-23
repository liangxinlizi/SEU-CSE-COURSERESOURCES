import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# 设置图像路径
original_image_path = 'image.png'  
transformed_images_folder = '1_2_results' 

# 指定需要配准的文件名列表
selected_filenames = ['Rotate_transformed.jpg', 'Scale_transformed.jpg', 'Translate_transformed.jpg', 'Shear_transformed.jpg']

# 图像配准
def register_images(ref_img, target_img):
    # 转化为灰度图像
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    # ORB 特征点监测
    orb = cv2.ORB_create(nfeatures=100)
    # 检测关键点和描述符
    keypoints_ref, descriptors_ref = orb.detectAndCompute(ref_gray, None)
    keypoints_target, descriptors_target = orb.detectAndCompute(target_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # 找到匹配
    matches = bf.match(descriptors_ref, descriptors_target)
    matches = sorted(matches, key=lambda x: x.distance)# 把配准结果按照距离排序 距离越小代表匹配越好
    # 筛选匹配点
    good_matches = matches[:int(len(matches) * 0.15)]
    # 提取匹配点坐标
    src_pts = np.float32([keypoints_ref[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_target[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    # 计算变换矩阵M 内点标识mask
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
    # 生成配准图像
    h, w = ref_img.shape[:2] # 获取参考图像的高度和宽度
   
    aligned_img = cv2.warpPerspective(target_img, M, (w, h))
    # 绘制结果
    matched_image = cv2.drawMatches(ref_img, keypoints_ref, target_img, keypoints_target, matches[:100], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return aligned_img, matched_image


# 加载指定图像
def load_selected_images(folder, selected_filenames):
    images = []
    for filename in selected_filenames:
        img_path = os.path.join(folder, filename)
        if os.path.exists(img_path):  # 检查文件是否存在
            images.append((filename, cv2.imread(img_path)))  # 加载图像并将其与文件名一起保存
    return images

if __name__ == '__main__':
    # 读取参考图像
    ref_img = cv2.imread(original_image_path)

    # 加载指定的变换图像
    transformed_images = load_selected_images(transformed_images_folder, selected_filenames)

    # 存储配准结果
    registered_images = []
    matched_images = []

    for filename, target_img in transformed_images:
        # 进行图像配准
        registered_image, matched_image = register_images(ref_img, target_img)
        registered_images.append((filename, registered_image))
        matched_images.append((filename, matched_image))

    # 显示配准结果
    plt.figure(figsize=(15, 10))

    # 显示配准后的图像
    for i, (filename, reg_image) in enumerate(registered_images):
        plt.subplot(len(registered_images), 2, i * 2 + 1)  # 创建子图，按照图像数量显示配准结果
        plt.imshow(cv2.cvtColor(reg_image, cv2.COLOR_BGR2RGB))  # 将 BGR 图像转换为 RGB 显示
        plt.title(f'Registration Result: {filename}')  # 设置子图标题
        plt.axis('off')

        plt.subplot(len(registered_images), 2, i * 2 + 2)  # 画出匹配的特征点
        plt.imshow(cv2.cvtColor(matched_images[i][1], cv2.COLOR_BGR2RGB))
        plt.title(f'Matching Points: {filename}')
        plt.axis('off')

    result_filename = "1_3_result.png"
    plt.tight_layout()
    plt.savefig(result_filename)
    plt.show()
