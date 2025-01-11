from PIL import Image
import numpy as np
def l1(image1_path, image2_path):
    # 打开井读取图片
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # 转换为灰度像,如果它们是彩色的
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')

    #将图像換为numpy数
    array1 = np.array(image1)
    array2 = np.array(image2)

    # 算像素点差値
    diff = array1 - array2

    # 对差値数取绝对値,因为負数的差可能会致和変小 
    abs_diff = np.abs(diff)

    # 求和得到所有像素点差値的和
    sum_diff = abs_diff.sum()/array1.size/255
    # print(f"L1 loss: {sum_diff}")
    return sum_diff


