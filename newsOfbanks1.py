# coding=utf-8  
""" 
Created on 2015-09-04 @author: Eastmount  
"""  
  
import time          
import re          
import os  
import sys
import codecs
from selenium import webdriver      
from selenium.webdriver.common.keys import Keys      
import selenium.webdriver.support.ui as ui      
from selenium.webdriver.common.action_chains import ActionChains  
from selenium.common.exceptions import NoSuchElementException
import MySQLdb
import urllib.parse
# from neo4j.v1 import GraphDatabase

# neo_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
  
#Open PhantomJS  
driver = webdriver.PhantomJS(executable_path=r"F:\phantomjs-2.1.1-windows\bin\phantomjs.exe")  
#driver = webdriver.Firefox()  
wait = ui.WebDriverWait(driver,10)
global info #全局变量
basePathDirectory = "news_of_Bank" 
baiduFile = os.path.join(basePathDirectory,"NewsofBank.txt")  
if not os.path.exists(baiduFile):  
    info = codecs.open(baiduFile,'w','utf-8')  
else:  
    info = codecs.open(baiduFile,'a','utf-8')  

conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='qa_base',charset='utf8')
cur=conn.cursor()

#Get the infobox of 5A tourist spots  
def getInfobox(name,num=0):  
    try:  
        #create paths and txt files
        global info
        basePathDirectory = "news_of_Bank"  
        if not os.path.exists(basePathDirectory):  
            os.makedirs(basePathDirectory)  
        baiduFile = os.path.join(basePathDirectory,"NewsofBank.txt")  
        if not os.path.exists(baiduFile):  
            info = codecs.open(baiduFile,'w','utf-8')  
        else:  
            info = codecs.open(baiduFile,'a','utf-8')  
      
        #locate input  notice: 1.visit url by unicode 2.write files  
        # print (name.rstrip('\n')) #delete char '\n'  
        # driver.get("https://zhidao.baidu.com/")  
        driver.get("http://search.cs.com.cn/search?page="+num+"&channelid=215308&searchword=%E9%93%B6%E8%A1%8C&keyword=%E9%93%B6%E8%A1%8C&was_custom_expr=DOCTITLE%3D%28%E9%93%B6%E8%A1%8C%29&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=DOCTITLE&timescope=&timescopecolumn=&orderby=")
        # elem_inp = driver.find_element_by_xpath("//form[@id='search-form-new']/input")  
        # elem_inp.send_keys(name)  
        # elem_inp.send_keys(Keys.RETURN)  
        # info.write(name.rstrip('\n')+'\r\n')  #codecs不支持'\n'换行
        # time.sleep(2)
        print (driver.current_url)
        print (driver.title)
        for i in range(30):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.2)

        #数据组装
        urls = []
        #load infobox basic-info cmn-clearfix
        tags = driver.find_elements_by_xpath("//div[@class='ant-timeline-item-content']/a")  
        for tag in tags:
            tag_txt = tag.get_attribute("href")
            # print(tag_txt)
            if tag_txt.find('mp.sohu') == -1:
                urls.append(tag_txt)
        # exit()
        image_news = driver.find_elements_by_xpath("//div[@class='ImageNewsCardContent']/a")
        for image_new in image_news:
            image_new_txt = image_new.get_attribute("href")
            # print(image_new_txt)
            if image_new_txt.find('mp.sohu') == -1:
                urls.append(image_new_txt)

        text_news = driver.find_elements_by_xpath("//div[@class='TextNewsCardContent']/a")
        for text_new in text_news:
            text_new_txt = text_new.get_attribute("href")
            # print(text_new_txt)
            if text_new_txt.find('mp.sohu') == -1:
                urls.append(text_new_txt)
        # print(urls)
        # exit()

        #抽取详细数据
        for url in urls:
            # print("\n")
            # print(url)
            driver.get(url)
            # print(driver.title)
            try:
                title = driver.find_element_by_class_name("text-title")
                keywords = driver.find_element_by_class_name("tag")
                article = driver.find_element_by_class_name("article")
            except NoSuchElementException as msg:
                # print(msg)
                continue
            else:
                title_ = title.text
                title_ = title_.split("\n")
                title_ = title_[0]
                print(title_)
                # print(keywords.text)
                # print(article.text)
                # exit()
                info.writelines(title_+'\r\n')  
                info.writelines(article.text+'\r\n')  
                # content = driver.find_element_by_class_name("best-text")
                # sql = 'select id from baidu_qa where question="'+ title.text +'"'
                # cur.execute(sql)
                # if cur.rowcount > 0:
                    # continue
                # cur.execute("insert into baidu_qa(question,answer,agrees,words) values('%s','%s','%d','%s')" %(str(title.text),str(content.text),int(agree),str(name)))
                # conn.commit()

        time.sleep(5)  
          
    except Exception as e: #'utf8' codec can't decode byte  
        print ("Error: ",e)  
    finally:  
        print ('\n')  
        # info.write('\r\n')  
  
#Main function  
def main():
    # global info
    #By function get information   
    # session = neo_driver.session()
    getInfobox('name')  
    exit()
    source = [u'借记卡转账',u'银行卡手机绑定',u'余额变动通知'] 
    for name in source:  
        name = name.replace("\n", "")
        # session.write_transaction(add_bank_dots,name)
        # name = bytes(name,"utf-8")  
        # if bytes('故宫',"utf-8") in name: #else add a '?'  
            # name = u'北京故宫' 
        # for i in range(100): 
            # getInfobox(name,10*i)  
        # exit()
    print ('End Read Files!')  
    source.close()  
    # info.close()  
    driver.close()  
    cur.close()
    conn.close()
# #添加节点
# def add_bank_dots(tx,name):
#     tx.run("MERGE (bank:Bank {name: $name})",name=name)

# def add_bank_field(tx,key,field):
#     tx.run("MERGE (field:Field {field: $key, value: $value})",key=key,value=field)
# #建立联系
# def add_dots_link(tx,bank,field,key):
#     tx.run("MATCH(bank:Bank {name: $name}),(field:Field {value:$value}) "
#     "CREATE (bank)-[LINKED_TO:LINKED_TO {attr:$key}]->(field)",name=bank,value=field,key=key)
  
if __name__ == "__main__":
    main()  
