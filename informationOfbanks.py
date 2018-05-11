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
from neo4j.v1 import GraphDatabase

neo_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
  
#Open PhantomJS  
driver = webdriver.PhantomJS(executable_path=r"F:\phantomjs-2.1.1-windows\bin\phantomjs.exe")  
#driver = webdriver.Firefox()  
wait = ui.WebDriverWait(driver,10)
global info #全局变量
basePathDirectory = "Banks_of_China" 
baiduFile = os.path.join(basePathDirectory,"informationBanks.txt")  
if not os.path.exists(baiduFile):  
    info = codecs.open(baiduFile,'w','utf-8')  
else:  
    info = codecs.open(baiduFile,'a','utf-8')  

#Get the infobox of 5A tourist spots  
def getInfobox(name):  
    try:  
        #create paths and txt files
        global info
        basePathDirectory = "Banks_of_China"  
        if not os.path.exists(basePathDirectory):  
            os.makedirs(basePathDirectory)  
        baiduFile = os.path.join(basePathDirectory,"informationBanks.txt")  
        if not os.path.exists(baiduFile):  
            info = codecs.open(baiduFile,'w','utf-8')  
        else:  
            info = codecs.open(baiduFile,'a','utf-8')  
      
        #locate input  notice: 1.visit url by unicode 2.write files  
        print (name.rstrip('\n')) #delete char '\n'  
        driver.get("http://baike.baidu.com/")  
        elem_inp = driver.find_element_by_xpath("//form[@id='searchForm']/input")  
        elem_inp.send_keys(name)  
        elem_inp.send_keys(Keys.RETURN)  
        info.write(name.rstrip('\n')+'\r\n')  #codecs不支持'\n'换行
        time.sleep(2)
        print (driver.current_url)
        print (driver.title)
  
        #load infobox basic-info cmn-clearfix
        elem_name = driver.find_elements_by_xpath("//div[@class='basic-info cmn-clearfix']/dl/dt")  
        elem_value = driver.find_elements_by_xpath("//div[@class='basic-info cmn-clearfix']/dl/dd")
        # for e in elem_name:
        #     print (e.text)
        # for e in elem_value:
        #     print (e.text)

        session = neo_driver.session()
        #create dictionary key-value
        #字典是一种散列表结构,数据输入后按特征被散列,不记录原来的数据,顺序建议元组
        elem_dic = dict(zip(elem_name,elem_value)) 
        for key in elem_dic:  
            print (key.text,elem_dic[key].text)  
            #写属性节点
            session.write_transaction(add_bank_field,key.text,elem_dic[key].text)
            #建立属性和实体关系
            session.write_transaction(add_dots_link,name,elem_dic[key].text,key.text)
            info.writelines(key.text+" "+elem_dic[key].text+'\r\n')  
        time.sleep(5)  
          
    except Exception as e: #'utf8' codec can't decode byte  
        print ("Error: ",e)  
    finally:  
        print ('\n')  
        info.write('\r\n')  
  
#Main function  
def main():
    global info
    #By function get information   
    session = neo_driver.session()
    source = open("Banks_of_China_lists.txt",'r',encoding='utf-8')  
    for name in source:  
        name = name.replace("\n", "")
        session.write_transaction(add_bank_dots,name)
        # name = bytes(name,"utf-8")  
        # if bytes('故宫',"utf-8") in name: #else add a '?'  
            # name = u'北京故宫'  
        getInfobox(name)  
        # exit()
    print ('End Read Files!')  
    source.close()  
    info.close()  
    driver.close()  
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
