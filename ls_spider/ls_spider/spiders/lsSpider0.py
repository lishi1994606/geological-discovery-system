# -*- coding: utf-8 -*-

'''

**** 获取百度搜索的页面链接
'''
import scrapy
from ls_spider.items import LishiBaiduItem
import os
import time
import redis
import re
import logging
import ls_spider.settings as settings
class Lsspider0Spider(scrapy.Spider):
    name = 'lsSpider0'
    allowed_domains = None
    # start_urls = ['http://www.baidu.com/s?wd=lishi']
    start_urls = ['https://www.google.com/search?q=lishi']
    num_1=0 #一级个数

    # redis配置
    pool = redis.ConnectionPool(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    custom_settings = {
                        'LOG_LEVEL': 'INFO',
                        'LOG_FILE': 'level_0_log_%s.log' % time.strftime('%Y%m%d_%H%M%S',time.localtime()),
                        "DEFAULT_REQUEST_HEADERS": {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        }
    }

    page=1

    logger = logging.getLogger()

    def __init__(self, category="沉积学数据库", *args, **kwargs):
        super(Lsspider0Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.google.com/search?q=%s' % category]


    def start_requests(self):

        if self.r.exists('urllist'):
            self.r.delete('urllist')  # 删除这个值得历史记录

        """
        根据cookies模拟登陆人人网，注意settings.py文件的cookies必须是开启的
        :return:
        """
        cookies="CGIC=Inx0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; ANID=AHWqTUkCmqG4qeuCV11tJp6IRG1IKz_seTClGD6rCdQKHraWDcyyXKM7ckG0i28i; NID=199=xrFsKZSPec9g4sH_9QZ-Ik2QyjDdkq0KV3hZh7N9CvCHhDJsocU8_D9Rmwnda7GaaLZPsvEX9PGktE_629Sx4bkNsZ3YQTvI-gMI5VK_wUkyFXbcIE-_A35ygoV62ngSbzXS5QdUG17_foAuXi-nRqWcdi3-VRBr79GJWIRHmAc; OGPC=19016257-7:; DV=k2QgC_2zumIv0J-HU_sc0eeietdlCpf9oYQs_p7gJQIAAAA; OGP=-19016257:; 1P_JAR=2020-03-04-16"
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}

        #开始爬取
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies,
        )


    def parse(self, response):
        # 初始化删除之前的创建的文件
        if os.path.exists("1.txt"):
            os.remove("1.txt")
        if os.path.exists("2.txt"):
            os.remove("2.txt")
        if os.path.exists("3.txt"):
            os.remove("3.txt")
        # 删除result目录下的所有文件
        b = os.path.join(os.getcwd(),"result")
        f= os.listdir(b)
        for i in f:
            address1=os.path.join(b,i)
            if os.path.isdir(address1):
                ff=os.listdir(address1)
                for ii in ff:
                    os.remove(os.path.join(address1,ii))
            else:
                os.remove(os.path.join(b,i))

        # 拿到当前页码
        # #此程序中暂时无用
        current_page = int(response.xpath('//div[@id="page"]/strong/span[@class="pc"]/text()').extract_first())

        # 当前页面查找内容
        # for i, a in enumerate(response.xpath('//div[@class="result c-container "]/h3/a')):
        for i, a in enumerate(response.css('div.result.c-container h3.t a')):  # 加上div.result 去掉百度搜索出来的广告
            # 拿到标题文本
            title = ''.join(a.xpath('.//text()').getall())  # 此处用.//而不用./，这两者相差很大
            #将标题中的特殊字符去除掉，避免因为含有特殊字符导致不能在windows下命名文件
            title= re.sub(r'[\\/:*\"<>\!\? ]','_',title)  # 不能使用replace方法， 因为replace方法一次只能替换一个值，但是这里一次可能多个值

            if title.find("zhihu")>-1:
                return

            item = LishiBaiduItem()
            item['name'] = str(title)
            item['url'] = str(a.xpath('@href').extract_first()).strip()  # 提取链接
            item['cc'] = 0
            item['content'] = ''
            item['cj'] = 1
            item['searchTime'] = time.strftime('%Y%m%d%H%M%S',time.localtime())
            # 上面的item不返回给piplines,因为这一步仅仅是用作保存百度搜索的网页网址
            self.num_1+=1
            self.r.set("num_1",self.num_1)
            self.r.sadd("urllist", str(item["url"]))
            self.logger.info('标题：%s,url:%s',item['name'],item['url'])
            # this step is error,because this spider is only crawl biadu site,
            # if we use it ,it will send the cookie for baidu to other site , this is error.
            # yield scrapy.Request(item['url'],meta={'item':item}, callback=self.parse_2)
            yield None

        # 依次访问百度下面的更多页面，再次分别查找
        for p in response.xpath('//div[@id="page"]/a'):
            if self.page<10:
                self.page += 1
                p_url = 'http://www.baidu.com' + str(p.xpath('./@href').extract_first())
                yield scrapy.Request(p_url, callback=self.parse)
            else:
                break

        # 使用css选择器直接获取下一个页面
            ## 获取网页中的下一页链接，这个在百度中是不起作用，
            # 因为百度页面中的下一页的链接同普通页面的链接不同，
            # 会导致从下一页获取的页面中的“下一页”标签通过js计算生成
            # next_page=response.css('div#page a')[-1].attrib['href']
            # scrapy.Request(response.urljoin(next_page),callback=self.parse)
