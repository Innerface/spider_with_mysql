# -*- coding: utf-8 -*-
# Author: YuYuE (1019303381@qq.com) 2018.01.30
import time          
import re          
import os  
import sys
import codecs
from selenium import webdriver      
from selenium.webdriver.common.keys import Keys      
import selenium.webdriver.support.ui as ui      
from selenium.webdriver.common.action_chains import ActionChains 
import MySQLdb 
import traceback
# from neo4j.v1 import GraphDatabase

# neo_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='qa_base',charset='utf8')
cur=conn.cursor()
#Open PhantomJS  
driver = webdriver.PhantomJS(executable_path=r"F:/phantomjs-2.1.1-windows/bin/phantomjs.exe")  
# driver = webdriver.Firefox() 
wait = ui.WebDriverWait(driver,100)
def getInfobox(name,link=False):  
    try:  
        print (name.rstrip('\n'))  
        if link == False:
            driver.get("http://baike.baidu.com/")  
            elem_inp = driver.find_element_by_xpath("//form[@id='searchForm']/input")  
            elem_inp.send_keys(name)  
            elem_inp.send_keys(Keys.RETURN)  
            time.sleep(2)
        else:
            print(link)
            driver.get(link)
            time.sleep(20)
        main_url = driver.current_url
        main_title = driver.title
        print(main_url)
        print(driver)
        exit()
        # #将页面滚动条拖到底部
        # for i in range(100):
        #     js="var q=document.documentElement.scrollTop=10000"
        #     driver.execute_script(js)
        #     time.sleep(3)
        
        content = ''
        news_item = driver.find_elements_by_xpath("//div[@class='news-item__main']") 
        for news in news_item:
            news_text = str(news.text)
            print(news_text)
            content += p_text
        exit()
        #保存正文
        if summary == '':
            summary = content
        update_status_of_words(name,summary)
        update_status_of_links(name)
        save_detail_of_word_desc(name,content)
        a_set = driver.find_elements_by_xpath("//*[@href]")
        #词条根url
        temp = main_url.split('/')
        suffix = temp[-1]
        root_url = main_url.replace(suffix,'')
        for a in a_set:
            url = a.get_attribute("href")
            word = str(a.text)
            if word.find("\n") != -1:
                word = re.sub('\d+','',word)
                word = word.replace("\n","")
            if url.find("https://baike.baidu.com/item/") != -1 and url.find(root_url) == -1 and word.strip()!="" and word.find('义词') ==-1 and word.find('义项') ==-1:
                print(word)
                print(url)
                save_word_and_desc(word,'',name)
                save_title_and_link(word,url)
            else:
                continue 
        time.sleep(5)  
          
    except Exception as e: #'utf8' codec can't decode byte  
        if str(e).find("Unable to find element with class name 'lemma-summary'"):
            pass_status_of_links(name)
        print ("Error: ",e)  
    finally:  
        print ('\n')  

#将标题和链接写入数据库
def save_title_and_link(title,link):
    sql = 'select id from link_queue where word="'+ title +'"'
    print(sql)
    cur.execute(sql)
    if cur.rowcount < 1:
        print(cur.rowcount)
        cur.execute("insert into link_queue(word,link) values('%s','%s')" %(title,link))
        conn.commit()

#更新连接池状态
def update_status_of_links(title):
    sql = 'select id from link_queue where word="'+ title +'"'
    cur.execute(sql)
    if cur.rowcount > 0:
        cur.execute("update link_queue set status=1 where word='"+title+"'")
        conn.commit()

#更新连接池状态
def pass_status_of_links(title):
    sql = 'select id from link_queue where word="'+ title +'"'
    cur.execute(sql)
    if cur.rowcount > 0:
        cur.execute("update link_queue set status=3 where word='"+title+"'")
        conn.commit()

#取前n链接处理
def fetch_links_with_num(num=1,sort=0):
    sql = 'select word,link from link_queue where status=0 and id >'+str(sort)+' limit '+str(num)+';'
    cur.execute(sql)
    result = cur.fetchall()
    return result

#保存词条数据
def save_word_and_desc(word,desc,source):
    sql = 'select id from vocabulary where word="'+ word +'"'
    print(sql)
    cur.execute(sql)
    if cur.rowcount < 1:
        print(cur.rowcount)
        cur.execute("insert into vocabulary(word,concept,source)value('"+word+"','"+desc+"','"+source+"')" )
        conn.commit()

#更新词条数据
def update_status_of_words(word,desc):
    sql = 'select id from vocabulary where word="'+ word +'"'
    cur.execute(sql)
    if cur.rowcount > 0:
        desc = re.sub('\'','',desc)
        cur.execute("update vocabulary set concept='"+desc+"' where word='"+word+"'")
        conn.commit()

#保存词条详细文本数据
def save_detail_of_word_desc(word,content):
    path = "D:/NLP/fact_triple_extraction/originaltext/"
    file = open(path+word+'.txt','w',encoding='utf-8')
    file.write(content)
#修复优化表
def repair_table():
    cur.execute("REPAIR TABLE `link_queue`")
    conn.commit()
    cur.execute("OPTIMIZE TABLE `link_queue`")
    conn.commit()
    cur.execute("REPAIR TABLE `vocabulary`")
    conn.commit()
    cur.execute("OPTIMIZE TABLE `vocabulary`")
    conn.commit()

def main():
    try:
        link = "http://wallstreetcn.com/news/global?from=home"
        getInfobox('name',link)  
        print ('End')  
    except:
        traceback.print_exc()  
    else: 
        driver.close()  
        cur.close()
        conn.close()

#添加节点
def add_bank_dots(tx,name):
    tx.run("MERGE (bank:Bank {name: $name})",name=name)

def add_bank_field(tx,key,field):
    tx.run("MERGE (field:Field {field: $key, value: $value})",key=key,value=field)
#建立联系
def add_dots_link(tx,bank,field,key):
    tx.run("MATCH(bank:Bank {name: $name}),(field:Field {value:$value}) "
    "CREATE (bank)-[LINKED_TO:LINKED_TO {attr:$key}]->(field)",name=bank,value=field,key=key)
  
if __name__ == "__main__":
    main()  
