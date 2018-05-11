#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/5 18:51
# @Author  : Wilson
# @Version : 0.8

#导入库文件
import requests
from bs4 import BeautifulSoup
import time
import re


#网络请求的请求头
# headers = {
#         'User-Agent': '',
#         'cookie': ''
#         }


#构造爬取函数
def get_page(url,data=None):

    #获取URL的requests
    wb_data = requests.get(url)
    wb_data.encoding = ('utf-8')
    soup = BeautifulSoup(wb_data.text,'lxml')
    urls = []
    titles = soup.find_all("a", "news-item__main__title")
    for title in titles:
        title_text = title.text
        title_text = title_text.replace("\n","")
        title_text = title_text.replace(" ","")
        # print(title_text)
        url = title.get('href')
        if url.find('premium') == -1:
            url = "https://wallstreetcn.com"+url
            urls.append([title_text,url])
        print(urls)


#迭代页数
def get_more_page(start,end):
    for one in range(start,end,10):
        get_page(url)
        time.sleep(2)

#定义保存文件函数
def saveFile(data):
    path = "./News.txt"
    file = open(path,'a',encoding='utf-8')
    file.write(str(data))
    file.write('\n')
    file.close()

#主体
#定义爬取关键词、页数
# keyword = input('请输入关键词\n')
pages = 1

#定义将要爬取的URL
# url = 'https://zhidao.baidu.com/search?word=' + keyword + '&ie=gbk&site=-1&sites=0&date=0&pn='
url = "https://wallstreetcn.com/news/global?from=home"
#开始爬取
get_more_page(0,int(pages)*10)