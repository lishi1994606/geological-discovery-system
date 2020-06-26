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
    name = 'lsSpider3'
    allowed_domains = None
    start_urls = ['http://www.baidu.com/s?wd=lishi']
    num_3=0

    # 初始化redis
    pool = redis.ConnectionPool(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    custom_settings = {
                    'LOG_LEVEL': 'INFO',
                    'LOG_FILE': 'D:\\pyrun\\log\\level_3_log_%s.log' % time.strftime('%Y%m%d_%H%M%S',time.localtime()),
                    "DEFAULT_REQUEST_HEADERS": {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                    }
    }


    def __init__(self, category="沉积学数据库", *args, **kwargs):
        super(Lsspider1Spider, self).__init__(*args, **kwargs)


    def start_requests(self):
        # 删除result3目录下的所有文件  #spider0已经删去
        # b = os.path.join(os.getcwd(),"result3")
        # f= os.listdir(b)
        # for i in f:
        #     os.remove(os.path.join(b,i))

        # 从redis中读出百度搜索到的网页链接，然后进行内容的读取
        self.start_urls=list(self.r.smembers('urllist3'))
        self.logger.info(self.start_urls)

        i=0
        for url in self.start_urls:
            i=i+1
            # if i%16 == 0 :
            #     time.sleep(10)
            #     print("stopstopstop")
            yield scrapy.Request(
                url,
                callback=self.parse
            )

    def parse(self, response):
        item = LishiBaiduItem()
        # 后面添加一个随机字符串，避免名字相同
        item['name'] = re.sub(r'[\s\:\/\\\*\<\>\|\"\?]',' ',str(response.css('title::text').get())) + randam_letter()#获取标题
        item['url'] = str(response.url)  # 提取链接
        item['cc'] = 0
        item['content'] = ''
        item['cj'] = 3
        item['searchTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.logger.info('处理链接：%s',str(response.url))
        content=''
        # 获取网页中所有文字,并赋给第一级网址
        textlist_no_scripts = response.selector.xpath('//*[not(self::script or self::style)]/text()[normalize-space(.)]').extract()
        for i in range(0, len(textlist_no_scripts)):
            content = re.sub(r'\s','',content + textlist_no_scripts[i].strip())  # 删除掉空白符换行符等
        item['content']=str(content)
        yield item

def randam_letter():
    a3 = np.random.randint(65, 91, 10)
    b3 = [chr(i) for i in a3]
    return ''.join(b3)