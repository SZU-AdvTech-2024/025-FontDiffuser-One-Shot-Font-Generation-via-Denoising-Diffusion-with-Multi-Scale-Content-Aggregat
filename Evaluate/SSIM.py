import cv2
from skimage import metrics
import numpy as np
from PIL import Image

def e_ssim(image1_path, image2_path):
    # Assume you have two image files: image1.jpg and image2.jpg

    # Load the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    ssim_score = metrics.structural_similarity(gray_image1, gray_image2)

    # print("SSIM score: ", ssim_score)
    return ssim_score

img1 = '/home/zjm/FontDiffuser/outputs/out_cs.png'
img2 = '/home/zjm/FontDiffuser/outputs/out_single.png'

if __name__ == "__main__":
    # 如果输入是多通道（彩色）图像，设置multichannel=True。
    e_ssim(img2, img1)