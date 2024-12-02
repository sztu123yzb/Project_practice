import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import os

# 定义图像文件夹路径
folder_path = "E:\pythonProject\imagedy"
output_folder = "E:\pythonProject\image"

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取文件夹中所有 PNG 文件（可以根据需要修改文件格式）
image_files = glob.glob(os.path.join(folder_path, "*.jpg"))

# 批量处理图像
for image_path in image_files:
    # 加载图片
    image = cv2.imread(image_path)

    # 检查图像是否成功加载
    if image is None:
        print(f"图像加载失败：{image_path}")
        continue

    # # 定义水印位置的坐标 (根据红框的位置进行调整)
    # x, y, width, height = 267, 1692, 289, 40
    # mask = np.zeros(image.shape[:2], dtype=np.uint8)
    # mask[y:y+height, x:x+width] = 255

    #获取图片尺寸
    height,width = image.shape[:2]

    #水印大小在图片占比
    watermark_height = int(height*0.06)
    watermark_width = int(width*0.45)

    #计算水印区域坐标
    x=(width-watermark_width)//2
    y=height-watermark_height-10

    # 创建遮罩并去除水印
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y:y + watermark_height, x:x + watermark_width] = 255
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)


    # # 从周围区域创建一个填充图像（使用水印区域的上方内容）
    # # 使用上方区域的相同宽度和高度生成填充图像
    # fill_region = image[y - watermark_height:y, x:x + watermark_width]
    # mask = 255 * np.ones(fill_region.shape, fill_region.dtype)
    #
    # # 将填充图像合成到水印区域
    # center = (x + watermark_width // 2, y + watermark_height // 2)
    # result = cv2.seamlessClone(fill_region, image, mask, center, cv2.NORMAL_CLONE)


    # 保存处理后的图像到输出文件夹
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, result)
    print(f"处理完成并保存到：{output_path}")

print("所有图像处理完成。")
