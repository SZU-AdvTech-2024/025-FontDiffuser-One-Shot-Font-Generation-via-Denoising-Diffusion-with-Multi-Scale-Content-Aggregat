import os
import SSIM
import SSIM_1
import LPIPS
import LPIPS_GPU
import L1
import subprocess
from pytorch_fid import fid_score

#在FontDiffuser目录运行
def eva(word, index, image1, image2):
    # word = "隆"
    cmd = f"""python sample.py \
        --ckpt_dir="ckpt/" \
        --style_image_path="data_examples/sampling/example_content.jpg" \
        --save_image \
        --character_input \
        --content_character={word} \
        --save_image_dir="outputs/{index}/" \
        --device="cuda:1" \
        --algorithm_type="dpmsolver++" \
        --guidance_type="classifier-free" \
        --guidance_scale=7.5 \
        --num_inference_steps=20 \
        --method="multistep"
        """
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取标准输出和标准错误
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')
        print("Output:", output)
    except subprocess.CalledProcessError as e:
        print(f"Error output: {e.stderr.decode('utf-8')}")
        print(word)
        return 0,0,0,0

    l1_score = L1.l1(image1, image2)
    # lpips_score = LPIPS.e_lpips(image1, image2)
    lpips_score = LPIPS_GPU.calculate_lpips(image1, image2, device='cuda')
    # ssim_score = SSIM.e_ssim(image1, image2)
    ssim_score = SSIM_1.calculate_ssim(image1, image2, win_size=None, data_range=1.0)
    out = os.popen("CUDA_VISIBLE_DEVICES=1 python -m pytorch_fid /home/zjm/FontDiffuser/output_imgs/ /home/zjm/FontDiffuser/real_imgs/")
    fid_value = float(out.readlines()[2].split(' ')[-1])
    print(f'FID score: {fid_value}')
    print(f"L1 score: {l1_score}")
    print(f"LPIPS score: {lpips_score}")
    print(f"SSIM score: {ssim_score}")
    print(word)    
    return l1_score, lpips_score, ssim_score, fid_value

image1 = "/home/zjm/FontDiffuser/real_imgs/out_cs.png"
image2 = "/home/zjm/FontDiffuser/output_imgs/out_single.png"
avg_l1_score = 0
avg_lpips_score = 0
avg_ssim_score = 0
avg_fid_score = 0
wordn = 0

with open("./Evaluate/generated_characters_medium.txt", "r", encoding="utf - 8") as file:
    content = file.read()
    words = content.split('\n')
    for index, word in enumerate(words):
        l1_score, lpips_score, ssim_score, fid_score = eva(word[0], index, image1, image2)
        if (l1_score==0):
            continue
        wordn += 1
        avg_l1_score += l1_score
        avg_lpips_score += lpips_score
        avg_ssim_score += ssim_score
        avg_fid_score += fid_score
print(f"wordn: {wordn}")
print(f"average FID score: {avg_fid_score / wordn}")
print(f"average L1 score: {avg_l1_score / wordn}")
print(f"average LPIPS score: {avg_lpips_score / wordn}")
print(f"average SSIM score: {avg_ssim_score / wordn}")