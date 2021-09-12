'''
豆瓣电影爬虫
'''
import requests
import json
import time
import random
from tools.ua import get_header
from lxml import etree
from selenium import webdriver
import re
'''
访问解析主页--输出   剧情|喜剧|动作|爱情|科幻|动画|悬疑|惊悚|恐怖|
通过类型对应的数字选择返回电影的url
通过url 访问网络资源，获取电影信息
解析提取电影信息
打印输出
'''

class Douban_movie_spider:
    def __init__(self):
        self.url = 'https://movie.douban.com/chart'

    def get_html(self,url):

        headers ={
            'User-Agent':get_header()
        }
        html = requests.get(url=url,headers=headers).text

        return html

    def parse_html(self,html):
        # 解析主页
        eobj = etree.HTML(html)

        span_list = eobj.xpath('//div[@class="types"]/span')

        type_list = []
        num_list =[]
        for span in span_list:
            info = {}
            info['type'] =span.xpath('./a/text()')[0].strip()

            info['href'] =span.xpath('./a/@href')[0].strip()
            print(info['type'],end='|')

            regex ='/.*?&type=(.*?)&interval_id=100:90&action='
            num = re.findall(regex,info['href'],re.S)[0].strip()
            type_list.append(info['type'])
            num_list.append(num)
        print()
        self.choose_type_and_search(ul=num_list,ty=type_list)

    def choose_type_and_search(self,ul,ty):
        dict_of_choose = dict(zip(ty,ul))
        print(dict_of_choose)
        # 根据选择提取数据
        key = input('请输入需要查看的类型:')

        search_num = dict_of_choose[key]

        self.get_html_of_moving(search_num)

    def get_html_of_moving(self,sn):
        headers = {
            'User-Agent': get_header()
        }
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(sn)
        html =requests.get(url=url,headers=headers)
        html = html.json()
        print(html)
        total = html['total']
        op =input('请输入是否继续运行:y/n?')
        if op =='y':
            self.get_movie_list(total)
        else:
            pass

    def get_info(self,url):
        headers = {
            'User-Agent': get_header()
        }
        html = requests.get(url=url,headers=headers).json()
        # 访问得到的html是json格式的
        # 提取每个电影的信息，存入字典
        for html_of_1 in html:
            try:
                info ={}
                info['name'] = html_of_1['title']
                info['types'] = html_of_1['types']
                info['actors'] = html_of_1['actors']
                info['score'] = html_of_1['score']
                print(info)
            except:
                pass
        # 提取每个电影的信息，存入字典

    def get_movie_list(self,total):
        for i in range(0,total,20):
            page_url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'.format(i)
            self.get_info(page_url)
            time.sleep(random.uniform(0,1))

    def crawl(self):
        # 获取主页菜单栏
        html =self.get_html(self.url)
        self.parse_html(html)


if __name__ == '__main__':
    spider = Douban_movie_spider()
    spider.crawl()



