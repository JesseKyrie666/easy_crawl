"""
    向 电影天堂发送请求, 查看响应内容
        https://www.dytt8.net/index.htm
"""
import requests


from tools.ua import get_header

url = 'https://www.dytt8.net/index.htm'
headers = {
    'User-Agent': get_header()
}

# 修改前
# resp = requests.get(url=url, headers=headers)
# html = resp.text
# print(html)


# 修改后
# content.decode() 手动转码
# ignore参数: 忽略 转码过程中的异常
# html = requests.get(url=url, headers=headers).content.decode('gb2312', 'ignore')
# print(html)


# 测试get_headers函数--每次都不一样
# print(headers)
