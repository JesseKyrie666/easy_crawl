'''
https://search.jd.com/Search?keyword=ipad&page=1
https://search.jd.com/Search?keyword=ipad&page=3
'''
import requests
from lxml import etree
from tools.ua import get_header
import time
import random
import pymongo

class Paipaispider:
    def __init__(self):
        self.url = 'https://search.jd.com/Search?keyword={}&page={}'

    def get_html(self,url,headers):
        html = requests.get(url=url,headers = headers).text
        self.parse_html(html)

    def parse_html(self,html):
        eobj = etree.HTML(html)
        li_list = eobj.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            info = {}
            name = li.xpath('.//a/em/text()')[0].strip()
            if not name:
                pass
            else:
                info['name'] = name
                info['href'] = 'https:'+li.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0].strip()
                info['price'] = li.xpath('.//div[@class="p-price"]/strong/i/text()')[0].strip()
                print(info)
                self.save_data(info)

    def save_data(self,info):
        self.myset.insert_one(info)



    def crawl(self):
        self.keyword = input('请输入关键字:')
        # 链接数据库
        self.conn = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.conn['{}_db'.format(self.keyword)]
        self.myset = self.db['{}_set'.format(self.keyword)]

        # 拼接url
        for i in range(1,30,2):
            url = self.url.format(self.keyword,i)
            headers = {
                'User-Agent': get_header()
            }
            self.get_html(url,headers)
            time.sleep(random.uniform(0,1))




if __name__ == '__main__':
    spider = Paipaispider()
    spider.crawl()




