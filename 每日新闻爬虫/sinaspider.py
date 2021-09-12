import requests
import time
import random
from lxml import etree
from tools.ua import get_header
import datetime
import pymongo
# date =input('请输入今天日期：2021-8-3')
# 请求构造，
url_main  ='https://sports.sina.com.cn/'
headers = {
    'User-Agent':get_header()
}
# html = requests.get(url=url_main,headers=headers).content.decode('utf8','ignore')

# with open('sina-{}.html'.format(date),'w') as f:
#     f.write(html)

def get_data(div):
    info_list = []
    # 最热消息
    info_0 = {}
    info_0['title'] = div.xpath('.//h3[@class="ty-card-tt"]/a/text()')
    info_0['href'] = div.xpath('.//h3[@class="ty-card-tt"]/a[2]/@href')
    info_list.append(info_0)
    # 其他信息
    info_1 ={}
    li_list = div.xpath('.//ul/li')
    for li in li_list:
        info_1['title'] = li.xpath('./a/text()')
        info_1['href'] = li.xpath('./a/@href')
    info_list.append(info_1)
    return info_list

def get_text(li):
    info = ''
    for i in li:
        info += i
    return info
def save_into_text(main_data,main_href,dic_other,day):
    filename ='news_{}.text'.format(day)
    with open(filename, 'a+') as file:
        file.write('主要消息')
        file.write(main_data)
        file.write(main_href)
        file.write('\n')
        file.write('其他消息:')
        for i in dic_other:
            news = i
            href = dic_other[i]
            file.write(news)
            file.write(href)
        file.write('\n')



# 存入数据库预备
# day = input('请输入今天的日期（2021-8-2）：')
# conn = pymongo.MongoClient(host='localhost', port=27017)
# db = conn['newsdb']
# myset = db['sina_news_set']
# dic={'news': day, 'href': 'from sina'}
# myset.insert_one(dic)

# 存入数据库函数
# def save_into_mongo_news(main_data,main_href,dic_other,myset):
#     myset.insert_one({'主要消息': main_data, 'href': main_href})
#
#     for i in dic_other:
#         news = i
#         href = dic_other[i]
#         myset.insert_one({'其他消息':news,'href':href})

# 网页解析，
f = open('sina-2021-8-3.html','r')
html =f.read()

eobj = etree.HTML(html)
div_list = eobj.xpath('//div[@class="ty-top-ent"]/div')
for div in div_list:

    info_list =get_data(div)
    if info_list[0]['title']==[]:
        pass
    else:
        # 获取主要消息内容
        info_main_title = info_list[0]['title']
        info_main_text = get_text(info_main_title)
        # 获取主要消息链接
        info_main_href = info_list[0]['href']
        info_main_href_text = get_text(info_main_href)

        # 获取其他消息内容--不需要消息拼接
        info_other_title = info_list[1]['title']

        info_other_href = info_list[1]['href']
        info = dict(zip(info_other_title, info_other_href))
        data_list = [info_main_text,info_main_href_text,info]
        main_data = data_list[0]
        main_href = data_list[1]
        dic_other = data_list[2]
        day =datetime.datetime.now().date()
        # 存入text文件
        save_into_text(main_data=main_data,main_href=main_href,dic_other=dic_other,day=day)

        # 存入mongodb数据库
        # save_into_mongo_news(main_data=main_data, main_href=main_href, dic_other=dic_other, myset=myset)

