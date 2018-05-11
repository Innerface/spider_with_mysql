# coding=utf-8  
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
#Open PhantomJS  
driver = webdriver.PhantomJS(executable_path=r"F:\phantomjs-2.1.1-windows\bin\phantomjs.exe")  
#driver = webdriver.Firefox()  
wait = ui.WebDriverWait(driver,10)

conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='qa_base',charset='utf8')
cur=conn.cursor()

#Get the infobox of 5A tourist spots  
def getInfobox(name,num=0):  
    try:  
        driver.get("https://zhidao.baidu.com/search?pn="+str(num)+"&word="+urllib.parse.quote(name))
        elem_name = driver.find_elements_by_xpath("//div[@class='list']/dl/dt")  
        elem_value = driver.find_elements_by_xpath("//div[@class='list']/dl/dt/a")
        extra = driver.find_elements_by_xpath("//div[@class='list']/dl/dd[last()]")
        if len(elem_name) <1:
            return 
        #数据组装
        urls = []
        agrees = []
        for en,ev,ex in zip(elem_name,elem_value,extra):
            title = en.text
            url_ = ev.get_attribute("href")
            agrees_txt = ex.text
            agrees_txt = agrees_txt.split()
            agree_ = agrees_txt[-1]
            if agree_.isdigit() == False:
                continue
            # elif int(agrees) < 3:
                # continue
            # print(agree_)
            urls.append(url_)
            agrees.append(agree_)
        if len(urls) < 1:
            return

        #抽取详细数据
        for url,agree in zip(urls,agrees):
            # print("\n")
            # print(url)
            driver.get(url)
            # print(driver.title)
            try:
                title = driver.find_element_by_class_name("ask-title")
            except NoSuchElementException as msg:
                # print(msg)
                continue
            else:
                print(title.text)
                content = driver.find_element_by_class_name("best-text")
                print(content.text)
                title_str = title.text
                content_str = str(content.text)
                content_str = content_str.replace("\n","")
                content_str = content_str.replace("\t","")
                title_str = re.sub('【.*?】', '', title_str)
                sql = 'select id from baidu_qa_1 where question="'+ title_str +'"'
                cur.execute(sql)
                if cur.rowcount > 0:
                    continue
                cur.execute("insert into baidu_qa_1(question,answer,agrees,words) values('%s','%s','%d','%s')" %(title_str,content_str,int(agree),str(name)))
                conn.commit()
                # exit()

        time.sleep(15)  
          
    except Exception as e: #'utf8' codec can't decode byte  
        print ("Error: ",e)  
    finally:  
        print ('\n')  
        # info.write('\r\n')  
  
#Main function  
def main():
    source = [u'银行转账',u'网上支付',
    u'股票',u'期权',u'共同基金',u'定期存单',u'电子银行',u'人民币理财',u'外币理财',
    u'保证收益理财',u'非保证收益理财',u'债券型理财',u'信托型理财',u'挂钩型理财'] 
    for name in source:  
        name = name.replace("\n", "")
        # session.write_transaction(add_bank_dots,name)
        # name = bytes(name,"utf-8")  
        # if bytes('故宫',"utf-8") in name: #else add a '?'  
            # name = u'北京故宫' 
        for i in range(20): 
            getInfobox(name,10*i)  
        # exit()
    print ('End Read Files!')  
    source.close()  
    # info.close()  
    driver.close()  
    cur.close()
    conn.close()
  
if __name__ == "__main__":
    main()  
