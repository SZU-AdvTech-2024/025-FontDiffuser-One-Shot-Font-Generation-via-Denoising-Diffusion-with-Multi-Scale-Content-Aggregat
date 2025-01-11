import json
import random
import os
from get_stroke import get_stroke 

def load_word_data(json_path):
    """
    加载 word.json 文件并返回汉字列表。
    
    :param json_path: word.json 文件的路径
    :return: 包含所有汉字信息的列表
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"未找到文件：{json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            print(f"成功加载 {len(data)} 个汉字记录。")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"解析 JSON 文件时出错：{e}")

def filter_chars_by_strokes(word_data, maxn, min_strokes=1, max_strokes=2):
    """
    筛选出笔画数在 min_strokes 到 max_strokes 之间的汉字。
    
    :param word_data: 包含所有汉字信息的列表
    :param min_strokes: 最小笔画数
    :param max_strokes: 最大笔画数
    :return: 符合条件的汉字列表
    """
    filtered = []
    n = 0
    for entry in word_data:
        if n > maxn:
            break
        try:
            strokes = int(entry.get('strokes', 0))
            if min_strokes <= strokes <= max_strokes:
                strokes = int(get_stroke(entry['word']))
                if min_strokes <= strokes <= max_strokes:
                    filtered.append({'word': entry['word'], 'strokes': strokes})
                    entry['strokes'] = strokes
                    print(f"{entry['word']}\t {strokes}")
                    n = n + 1
        except ValueError:
            # 如果 'strokes' 不是有效的整数，则跳过该条目
            continue
    # print(f"筛选后共有 {len(filtered)} 个汉字符合笔画数 {min_strokes}-{max_strokes} 的要求。")
    print(f"成功选择了 {len(filtered)} 个汉字符合笔画数 {min_strokes}-{max_strokes} 的要求。")
    return filtered

def select_random_chars(filtered_chars, count=100):
    """
    从符合条件的汉字中随机选择指定数量的汉字。
    
    :param filtered_chars: 符合条件的汉字列表
    :param count: 需要选择的汉字数量
    :return: 随机选择的汉字列表
    """
    if len(filtered_chars) < count:
        raise ValueError(f"符合条件的汉字数量不足 {count} 个。当前可用数量：{len(filtered_chars)}")
    
    selected = random.sample(filtered_chars, count)
    print(f"成功随机选择了 {len(selected)} 个汉字。")
    return selected

def save_to_txt_file(selected_chars, output_path='generated_characters_with_strokes.txt'):
    """
    将选中的汉字及其笔画数保存到文本文件中，每行一个汉字及其笔画数，用制表符分隔。
    
    :param selected_chars: 选中的汉字列表
    :param output_path: 输出文件的路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in selected_chars:
            f.write(f"{entry['word']}\n")
    print(f"生成的汉字及笔画数已保存到 {output_path}")

def main():
    # 定义 word.json 文件的路径
    # 假设脚本与 chinese-xinhua 目录在同一层级
    json_path = os.path.join('/mnt/zjm/chinese-xinhua', 'data', 'word.json')
    
    try:
        # 加载 word.json 数据
        word_data = load_word_data(json_path)
        
        # 筛选符合笔画数要求的汉字
        filtered_chars = filter_chars_by_strokes(word_data, 100, min_strokes=6, max_strokes=10)
        
        # 随机选择 100 个汉字
        # selected_chars = select_random_chars(filtered_chars, count=100)
        
        # 保存结果到本地文件
        save_to_txt_file(filtered_chars, output_path='generated_characters_easy.txt')
    
    except Exception as e:
        print(f"程序出错：{e}")

if __name__ == "__main__":
    main()
