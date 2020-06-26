from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# 等待元素渲染库
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
import redis
import time
import re
import  shutil
import io

#windows客户端打印因为系统自带的是gbk编码，如果我们用UTF8会导致一些字符不能识别而报错
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')



def run():

    #建立D:\\pyrun\\result文件夹
    p="D:\\pyrun\\"
    if os.path.exists(p):
        shutil.rmtree(p)
        
    os.mkdir(p);
    os.mkdir(os.path.join(p,'log'))
    os.mkdir(os.path.join(p,'result'))
    os.mkdir(os.path.join(p,'result','result1'))
    os.mkdir(os.path.join(p,'result','result2'))
    os.mkdir(os.path.join(p,'result','result3'))



    # selenium 配置
    #chromePath = r'./chromedriver.exe'  #配置到path路径中就不需要这个了
    url='https://www.google.com/search?q='

    #wd = webdriver.Chrome(executable_path=chromePath)#配置到path路径中就不需要这个了
    wd = webdriver.Chrome()
    wait = WebDriverWait(wd, 3)


    sys.stdout.flush()

    #redis配置及其初始化
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    pool = redis.ConnectionPool(host="127.0.0.1", port=6379,decode_responses=True)
    conn = redis.Redis(connection_pool=pool)

    conn.set('num_1',0)
    conn.set('num_2',0)
    conn.set('num_3',0)
    conn.set('parse_num_1',0)
    conn.set('parse_num_2',0)
    conn.set('parse_num_3',0)

    conn.delete('urllist')

    guanjianci=None

    while True:
        guanjianci=conn.get("guanjianci")
        print("等待分词结果，请启动C#程序分词")
        if guanjianci!=None:
            url=url+guanjianci
            print("google搜索url:%s"% url)

            break
        time.sleep(2);



    wd.get(url)
    title_list=wd.find_elements_by_css_selector('#rso>.g>.rc>.r>a>h3')
    url_set= wd.find_elements_by_css_selector('#rso>.g>.rc>.r>a:first-child')
    for title in title_list:
        title_text = re.sub(r'[\\/:*\"<>\!\? ]', '_', title.text)  # 不能使用replace方法， 因为replace方法一次只能替换一个值，但是这里一次可能多个值
        print(title_text)
        sys.stdout.flush()
    for u in url_set:
        print(u.get_attribute("href"))
        conn.sadd('urllist',u.get_attribute('href'))
        sys.stdout.flush()


    i=1
    while True:
        if len(wd.find_elements_by_id('pnnext'))==1:
            i=i+1
            print('解析第%s页'%i)
            if i>10:
                break
            wd.find_element_by_id('pnnext').click()
            title_list_p=wd.find_elements_by_css_selector('#rso>.g>.rc>.r>a>h3')
            url_set= wd.find_elements_by_css_selector('#rso>.g>.rc>.r>a:first-child')
            for title in title_list_p:
                title_text = re.sub(r'[\\/:*\"<>\!\? ]', '_', title.text)  # 不能使用replace方法， 因为replace方法一次只能替换一个值，但是这里一次可能多个值
                print(title_text)
                sys.stdout.flush()
            for u in url_set:
                print(u.get_attribute("href"))
                sys.stdout.flush()
                conn.sadd('urllist',u.get_attribute('href'))
        else:
            break

    num_1=conn.scard('urllist')
    conn.set('num_1',num_1)
    conn.close()
    print('搜索完成，请关闭窗口')
    exit(0)


if __name__=='__main__':
    run()
