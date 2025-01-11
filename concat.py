from PIL import Image
import os


def horizontal_concat_images(parent_folder):
    images = []
    sub_folders = [os.path.join(parent_folder, folder) for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))][:10]
    sub_folders = [os.path.join(parent_folder, str(i)) for i in [0,1,2,3,4]]

    for sub_folder in sub_folders:
        file_path = os.path.join(sub_folder, os.listdir(sub_folder)[0])
        print(file_path)
        img = Image.open(file_path)
        images.append(img)

    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    return new_image


if __name__ == "__main__":
    parent_folder = "./outputs"  # 替换为实际的主目录名称
    result_image = horizontal_concat_images(parent_folder)
    result_image.save("concat_result_ri.jpg")  # 保存拼接后的图片，可以根据需求修改保存的文件名和格式