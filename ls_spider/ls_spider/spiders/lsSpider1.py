# -*- coding: utf-8 -*-
import scrapy
from ls_spider.items import LishiBaiduItem
import os
import re
import time
import redis
import numpy as np
import ls_spider.settings as settings
class Lsspider1Spider(scrapy.Spider):
    name = 'lsSpider1'
    allowed_domains = None
    start_urls = ['http://www.baidu.com/s?wd=lishi']
    num_1=0 #一级个数
    num_2=0 #二级个数

    # 初始化redis
    pool = redis.ConnectionPool(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    custom_settings = {
                    'LOG_LEVEL': 'DEBUG',
                    'LOG_FILE': 'D:\\pyrun\\log\\level_1_log_%s.log' % time.strftime('%Y%m%d_%H%M%S',time.localtime()),
                    "DEFAULT_REQUEST_HEADERS": {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                    }
    }

    page=1

    def __init__(self, category="沉积学数据库", *args, **kwargs):
        super(Lsspider1Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.logger.info('初始化')
        if self.r.exists('urllist1'):
            self.r.delete('urllist1') #删除历史值
        if self.r.exists('urllist2'):
            self.r.delete('urllist2')  # 删除历史值
        if self.r.exists('urllist3'):
            self.r.delete('urllist3')  # 删除历史值
        #删除之前的结果
        list_keys = self.r.keys("result1:*")
        for key in list_keys:
            self.r.delete(key)

        list_keys = self.r.keys("result2:*")
        for key in list_keys:
            self.r.delete(key)

        list_keys = self.r.keys("result3:*")
        for key in list_keys:
            self.r.delete(key)
        self.logger.info('初始化结束，开始运行')
        # 初始化删除之前的创建的文件
        if os.path.exists("1.txt"):
            os.remove("1.txt")
        if os.path.exists("2.txt"):
            os.remove("2.txt")
        if os.path.exists("3.txt"):
            os.remove("3.txt")

        # 删除result目录下的所有文件
        #b = os.path.join(os.getcwd(),"result")
        b='D:\\pyrun\\result\\'
        f= os.listdir(b)
        for i in f:
            address1=os.path.join(b,i)
            if os.path.isdir(address1):
                ff=os.listdir(address1)
                for ii in ff:
                    os.remove(os.path.join(address1,ii))
            else:
                os.remove(os.path.join(b,i))

        # 从redis中读出百度搜索到的网页链接，然后进行内容的读取
        self.start_urls=list(self.r.smembers('urllist'))
        self.logger.info(self.start_urls)
        # self.r.delete('urllist')


        """
        根据cookies模拟登陆人人网，注意settings.py文件的cookies必须是开启的
        :return:
        """
        cookies="BD_UPN=12314753; sug=3; sugstore=1; ORIGIN=0; bdime=0; COOKIE_SESSION=5466_0_9_8_10_1_0_0_9_1_55_0_1302_0_0_0_1574432730_0_1574445720%7C9%23584926_3_1574387516%7C2; BD_HOME=1; BD_CK_SAM=1; H_PS_645EC=cfbcuVnl9k1g%2BWjgzzxE5hz9FZT837MxZQgTAgMJFHmA21xaVD2w9W8zNLRgQAK06AEr; BAIDUID=1276D794AFBAF28F503A0F7C62D53930:FG=1; BDUSS=EI5MW1MazNRMUFWQlBJd1N3MFUxczhHS25SWkFQbFFqTGJvbm0wVHhwcn5LZ0JlRVFBQUFBJCQAAAAAAAAAAAEAAACgHzslwO7V~jAzMDMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP-d2F3~ndhdT; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSVRTM=0"
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}


        i=0
        for url in self.start_urls:
            i=i+1
            # if i%16 == 0 :
            #     time.sleep(10)
            #     print("stopstopstop")
            yield scrapy.Request(
                url,
                callback=self.parse,
                cookies=cookies,
            )

    def parse(self, response):
        # item = response.meta["item"]
        # item["item2"] = []

        item = LishiBaiduItem()
        # 后面添加一个随机字符串，避免名字相同
        item['name'] = re.sub(r'[\s\:\/\\\*\<\>\|\"\?]',' ',str(response.css('title::text').get())) + randam_letter()#获取标题
        item['url'] = str(response.url)  # 提取链接
        item['cc'] = 0
        item['content'] = ''
        item['cj'] = 1
        item['searchTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.logger.info('处理链接：%s',str(response.url))
        content=''
        # 获取网页中所有文字,并赋给第一级网址
        textlist_no_scripts = response.selector.xpath('//*[not(self::script or self::style)]/text()[normalize-space(.)]').extract()
        for i in range(0, len(textlist_no_scripts)):
            content = re.sub(r'[\s:/\\]','',content + textlist_no_scripts[i].strip())  # 删除掉空白符换行符等
        # print(content)
        # self.logger.info(content)
        # print(content)
        # if str(content)=='':
        #     print(content)
        #     pass
        item['content']=str(content)
        self.r.sadd('urllist1',item['url'])

        for i, a in enumerate(response.xpath('//a')):
            url = a.xpath('@href').get()
            if url != None and url != '':
                if url.find("javascript:") < 0 and url.find("baidu") < 0 and url.find("zhihu")<0 and url.find('360doc')<0:
                    if url.find('http')>-1 or url.find('https')>-1:
                        url=str(url).strip()
                    else:
                        url=response.urljoin(str(url).strip())
                    self.r.sadd('urllist2',url)
        self.r.set('num_2',self.r.scard('urllist2'))
        yield item
def randam_letter():
    a3 = np.random.randint(65, 91, 10)
    b3 = [chr(i) for i in a3]
    return ''.join(b3)