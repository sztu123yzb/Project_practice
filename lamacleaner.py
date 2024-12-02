import os
from lama_cleaner.model_manager import ModelManager
from lama_cleaner.schema import Config
from PIL import Image
import numpy as np
import torch

def remove_watermark_batch(input_dir, output_dir):
    # 如果输出目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的图片
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # 处理图片文件
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, filename)

            try:
                # 读取图像并转换为 RGB 格式
                image = Image.open(input_image_path).convert("RGB")
                image_np = np.array(image).astype(np.uint8)

                # 获取图像尺寸并定义水印区域
                height, width, _ = image_np.shape
                watermark_width = int(width * 0.45)
                watermark_height = int(height * 0.06)

                # 计算水印区域的坐标
                x = (width - watermark_width) // 2
                y = height - watermark_height - 10

                # 创建遮罩
                mask = np.zeros((height, width), dtype=np.uint8)
                mask[y:y + watermark_height, x:x + watermark_width] = 255

                # LaMa Cleaner 配置
                config = Config(
                    ldm_steps=20,
                    sd_mask_blur=5,  # 遮罩模糊程度
                    sd_strength=0.75,  # 修复强度
                    hd_strategy='resize',  # 高分辨率图像策略
                    hd_strategy_crop_margin=32,  # 裁剪边距
                    hd_strategy_resize_limit=1024,  # 高分辨率最大尺寸
                    hd_strategy_crop_trigger_size=1024,
                    controlnet_method="./control_v11p_sd15_canny.pth"
                )

                # 使用 LaMa Cleaner 进行水印去除处理
                result_image = model(image_np, mask, config)

                # 保存处理后的图片
                result_pil = Image.fromarray(result_image)
                result_pil.save(output_image_path, format="PNG")
                print(f"处理完成：{filename} -> {output_image_path}")

            except Exception as e:
                print(f"处理 {filename} 时发生错误: {e}")

    # 清理 GPU 内存
    if device == 'cuda':
        torch.cuda.empty_cache()

if __name__ == '__main__' :
    # 初始化 LaMa Cleaner 模型
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = ModelManager(name='lama', device=device)
    input_dir = "E:/pythonProject/imagedy"  # 替换为包含待处理图像的文件夹路径
    output_dir = "E:/pythonProject/image"  # 替换为保存结果的文件夹路径
    remove_watermark_batch(input_dir, output_dir)
