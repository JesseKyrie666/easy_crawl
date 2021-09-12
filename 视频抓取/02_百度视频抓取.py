import requests
import time
from lxml import etree
import random
from tools.ua import get_header

# 获取10个视频链接
url_1 = 'http://v.baidu.com/movie'

headers = {
    'User-agent': get_header()
}
html_1 = requests.get(url=url_1, headers=headers).text

def get_vedio(href):
    headers = {
        'User-agent': get_header()
    }
    html_2 = requests.get(url=href,headers=headers).text
    print(html_2)

eobj = etree.HTML(html_1)

li_list = eobj.xpath('//*[@id="movie_show_hot"]/div[2]/div/ul/li')
for li in li_list:
    href = li.xpath('.//a[@class="title"]/@href')
    href_1 = href[0].strip()
    get_vedio(href_1)
    time.sleep(random.uniform(0,1))



