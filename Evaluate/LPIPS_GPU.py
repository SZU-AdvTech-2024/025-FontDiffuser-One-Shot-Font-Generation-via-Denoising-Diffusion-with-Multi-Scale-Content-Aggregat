import torch
import lpips
from PIL import Image
from torchvision import transforms

def load_image(image_path, transform=None):
    """
    加载并预处理图像。
    
    参数：
        image_path (str): 图像的文件路径。
        transform (torchvision.transforms.Compose, optional): 预处理变换。
    
    返回：
        torch.Tensor: 预处理后的图像张量。
    """
    image = Image.open(image_path).convert('RGB')
    if transform:
        image = transform(image)
    return image

def calculate_lpips(image1_path, image2_path, device='cuda'):
    """
    计算两张图像之间的 LPIPS 值。
    
    参数：
        image1_path (str): 第一张图像的路径。
        image2_path (str): 第二张图像的路径。
        device (str or torch.device, optional): 计算设备，默认为 'cuda'。
    
    返回：
        float: 两张图像之间的 LPIPS 值。
    """
    # 定义图像预处理
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # 调整图像大小
        transforms.ToTensor(),          # 转换为张量
        transforms.Normalize(mean=[0.5, 0.5, 0.5],  # 归一化到 [-1, 1]
                             std=[0.5, 0.5, 0.5])
    ])
    
    # 加载并预处理图像
    img1 = load_image(image1_path, transform).unsqueeze(0).to(device)
    img2 = load_image(image2_path, transform).unsqueeze(0).to(device)
    
    # 初始化 LPIPS 模型
    loss_fn = lpips.LPIPS(net='alex').to(device)  # 可选 'vgg', 'squeeze'
    
    # 计算 LPIPS 值
    with torch.no_grad():
        lpips_value = loss_fn(img1, img2)
    
    return lpips_value.item()

if __name__ == "__main__":
    # 定义图像路径
    img1_path = "/home/zjm/FontDiffuser/real_imgs/out_cs.png"
    img2_path = "/home/zjm/FontDiffuser/output_imgs/out_single.png"
    
    # 确定使用的设备
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # print(f'使用设备: {device}')
    
    # 计算 LPIPS 值
    lpips_score = calculate_lpips(image1_path, image2_path, device=device)
    print(f'LPIPS 值: {lpips_score}')
