#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:12:28 2017

@author: azurewit
"""

#导入库文件
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def get_page(Q_No, url, data = None):

    #问题编号
    page_question_No = 1 + Q_No
    #获取URL的requests
    wb_data = requests.get(url)
    wb_data.encoding = ('gbk')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #定义爬取的数据
    webdata = soup.select('a.ti')
    agrees = soup.select('span.f-black')
    print(agrees)

    if data==None:
        for title,url in zip(webdata, webdata):
            data = [
                title.get('title'),
                url.get('href')
                ]
            print ('\n')
            print (page_question_No)
            
            page_question_No += 1
            
            print (title.get_text())
            print (url.get('href'))
                                   
            url_sub = url.get('href')
            wb_data_sub = requests.get(url_sub)
            wb_data_sub.encoding = ('gbk')      
            soup_sub = BeautifulSoup(wb_data_sub.text, 'lxml')
            best_answer = soup_sub.find('pre', class_ = "best-text mb-10")
                        
            if best_answer != None:
                best = best_answer.get_text(strip = True)
                
                print ("\n\nBest Answer Is: \n")
                print (best)
            else:
                print ("\nNo Best Answer")
                better_answer = soup_sub.find_all('div', class_ = "answer-text line")
                
                if better_answer != None:
                    for i_better, better_answer_sub in enumerate(better_answer):
                        better = better_answer_sub.get_text(strip = True)
                        
                        print ("\nNo.%d Answer" % (i_better + 1))
                        print (better)
                                   
                else:
                    print ("Unanswered")
                    
#迭代页数
def get_more_page(start, end):
    for one in range(start, end, 10):
        get_page(one,url+str(one))
        time.sleep(2)

#主体
#定义爬取关键词、页数
key_word = input('请输入关键词\n')
#key_word = '彼岸花'
pages = 1
#定义将要爬取的URL
url = "https://zhidao.baidu.com/search?word=" + urllib.parse.quote(key_word) + "&pn="

#开始爬取
get_more_page(0, int(pages)*10)

