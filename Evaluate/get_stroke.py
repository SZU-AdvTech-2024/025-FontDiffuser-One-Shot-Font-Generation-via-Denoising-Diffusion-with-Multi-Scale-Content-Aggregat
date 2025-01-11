from urllib.parse import urlparse
import re
import requests

def get_stroke(zi):
# 定义基础 URL
    base_url = 'https://zidian.gushici.net/search/zi.php'

    # 定义参数，其中 'zi' 对应的值为汉字
    params = {
        'zi': f'{zi}'  # 将 '汉字' 替换为你需要查询的具体汉字
    }

    try:
        # 发送 GET 请求，requests 会自动处理 URL 编码

        requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        response = s.get(base_url, params=params) # 需要的网址
        print("请求的完整 URL:", response.url)

        # 检查响应状态码是否为 200（成功）
        if response.status_code == 200:
            return extract_stroke_count(response.url)
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # 捕获并打印请求过程中可能发生的异常
        print("请求过程中发生错误:", e)
    except requests.exceptions.ConnectionError:
      r.status_code = "Connection refused"

    return 0

def extract_stroke_count(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    parts = path.strip('/').split('/')
    if len(parts) >= 1 and parts[0].isdigit():
        return parts[0]

def main():
    stroke = get_stroke('隆')
    print(stroke)

if __name__ == "__main__":
    main()