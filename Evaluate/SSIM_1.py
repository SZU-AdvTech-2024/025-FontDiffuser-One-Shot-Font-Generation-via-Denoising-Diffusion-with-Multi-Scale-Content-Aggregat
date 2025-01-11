from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np

def calculate_ssim(image1_path, image2_path, win_size=None, data_range=1.0):
    """
    计算两张图像之间的 SSIM 值。

    参数：
        image1_path (str): 第一张图像的路径。
        image2_path (str): 第二张图像的路径。
        win_size (int, optional): 用于 SSIM 计算的窗口大小。默认为 None，使用默认值。
        data_range (float, optional): 图像数据的动态范围。默认为 1.0（适用于 [0, 1] 范围的浮点图像）。

    返回:
        float: 两张图像之间的 SSIM 值。
    """
    # 加载图像并转换为浮点型
    image1 = Image.open(image1_path).convert('RGB')
    image2 = Image.open(image2_path).convert('RGB')

    # 将图像转换为 NumPy 数组并归一化到 [0, 1]
    image1 = img_as_float(np.array(image1))
    image2 = img_as_float(np.array(image2))

    # 检查图像尺寸
    if image1.shape != image2.shape:
        raise ValueError("两张图像的尺寸或通道数不一致！请确保它们具有相同的尺寸和通道数。")

    # 设置 channel_axis
    if image1.ndim == 3:
        # 彩色图像，通常 channel_axis 为 2
        channel_axis = 2
    else:
        # 灰度图像
        channel_axis = None

    # 如果指定了 win_size，确保它是一个奇数且不超过图像的最小边长
    if win_size is not None:
        if not isinstance(win_size, int) or win_size % 2 == 0:
            raise ValueError("win_size 必须是一个奇数整数。")
        min_side = min(image1.shape[:2])
        if win_size > min_side:
            raise ValueError(f"win_size ({win_size}) 超过了图像的最小边长 ({min_side})。")

    # 计算 SSIM
    ssim_value, ssim_map = ssim(
        image1,
        image2,
        win_size=win_size,
        full=True,
        channel_axis=channel_axis,
        data_range=data_range
    )
    return ssim_value

if __name__ == "__main__":
    # 定义图像路径
    img1_path = "/home/zjm/FontDiffuser/real_imgs/out_cs.png"
    img2_path = "/home/zjm/FontDiffuser/output_imgs/out_single.png"

    try:
        # 计算 SSIM 值，设置 win_size=3 以避免窗口大小问题，data_range=1.0 适用于 [0, 1] 范围的图像
        ssim_score = calculate_ssim(img1_path, img2_path, win_size=3, data_range=1.0)
        print(f'SSIM 值: {ssim_score}')
    except ValueError as ve:
        print(f'错误: {ve}')
    except Exception as e:
        print(f'发生错误: {e}')
