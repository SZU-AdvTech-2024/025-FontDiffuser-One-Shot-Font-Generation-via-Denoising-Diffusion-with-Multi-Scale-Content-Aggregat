# import os

# out = os.popen("CUDA_VISIBLE_DEVICES=1 python -m pytorch_fid /home/zjm/FontDiffuser/output_imgs/ /home/zjm/FontDiffuser/real_imgs/")
# print(out.readlines()[2].split(' ')[-1])

# CUDA_VISIBLE_DEVICES=1 python -m pytorch_fid ../output_imgs/ ../real_imgs/

from pytorch_fid import fid_score

real_images_path = '/home/zjm/FontDiffuser/real_imgs/'
generated_images_path = '/home/zjm/FontDiffuser/output_imgs/'

# 计算 FID 分数
fid_value = fid_score.calculate_fid_given_paths(
    [real_images_path, generated_images_path],
    batch_size=16,
    device='cuda',  # 使用 'cpu' 如果没有 GPU
    dims=2048
)

print(f'FID 分数: {fid_value}')
