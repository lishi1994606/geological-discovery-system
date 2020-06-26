# -*- coding: utf-8 -*-
import scrapy
from ls_spider.items import LishiBaiduItem
import os
import time
import redis
import ls_spider.settings as settings
class Lsspider1Spider(scrapy.Spider):
    name = 'lsSpider1'
    allowed_domains = None
    start_urls = ['http://www.baidu.com/s?wd=lishi']
    num_1=0 #一级个数
    num_2=0 #二级个数
    num_3=0 #三级个数

    custom_settings = {
                          # 'LOG_LEVEL': 'ERROR',
                           'LOG_LEVEL': 'DEBUG',
                          'LOG_FILE': '5688_log_%s.txt' % time.time(),
                            "DEFAULT_REQUEST_HEADERS": {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                            }
    }

    page=1
    r=0

    def __init__(self, category="沉积学数据库", *args, **kwargs):
        super(Lsspider1Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.baidu.com/s?wd=%s' % category]


    def start_requests(self):

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
            os.remove(os.path.join(b,i))

        """
        根据cookies模拟,注意settings.py文件的cookies必须是开启的
        :return:
        """
        pool = redis.ConnectionPool(host=settings.REDIS_SERVER, port=settings.REDIS_PORT,decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

        cookies="BD_UPN=12314753; sug=3; sugstore=1; ORIGIN=0; bdime=0; COOKIE_SESSION=5466_0_9_8_10_1_0_0_9_1_55_0_1302_0_0_0_1574432730_0_1574445720%7C9%23584926_3_1574387516%7C2; BD_HOME=1; BD_CK_SAM=1; H_PS_645EC=cfbcuVnl9k1g%2BWjgzzxE5hz9FZT837MxZQgTAgMJFHmA21xaVD2w9W8zNLRgQAK06AEr; BAIDUID=1276D794AFBAF28F503A0F7C62D53930:FG=1; BDUSS=EI5MW1MazNRMUFWQlBJd1N3MFUxczhHS25SWkFQbFFqTGJvbm0wVHhwcn5LZ0JlRVFBQUFBJCQAAAAAAAAAAAEAAACgHzslwO7V~jAzMDMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP-d2F3~ndhdT; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSVRTM=0"
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies,
        )


    # 循环遍历百度搜索的前10页数据
    def parse(self, response):

        # 拿到当前页码
        current_page = int(response.xpath('//div[@id="page"]/strong/span[@class="pc"]/text()').extract_first())

        # 当前页面查找内容
        for i, a in enumerate(response.xpath('//div[@class="result c-container "]/h3/a')):
            # 拿到标题文本
            title = ''.join(a.xpath('./em/text() | ./text()').extract_first())
            if title.find("zhihu")>-1:
                return
            item = LishiBaiduItem()
            item['name'] = str(title)
            item['url'] = str(a.xpath('@href').extract_first()).strip()  # 提取链接
            item['cc'] = 0
            item['content'] = ''
            item['cj'] = 1
            item['searchTime'] = '##'
            self.num_1+=1
            self.r.set("num_1",self.num_1)
            yield scrapy.Request(item['url'],meta={'item':item}, callback=self.parse_2)

        # 依次访问百度下面的更多页面，再次分别查找
        for p in response.xpath('//div[@id="page"]/a'):
            if self.page<10:
                self.page += 1
                p_url = 'http://www.baidu.com' + str(p.xpath('./@href').extract_first())
                yield scrapy.Request(p_url, callback=self.parse)
            else:
                break
        # 使用next_page来获取下一页
        next_page= response.css('.n')

    def parse_2(self, response):
        item = response.meta["item"]
        item["item2"] = []
        content=''
        # 获取网页中所有文字,并赋给第一级网址
        textlist_no_scripts = response.selector.xpath('//*[not(self::script or self::style)]/text()[normalize-space(.)]').extract()
        for i in range(0, len(textlist_no_scripts)):
            content = content + textlist_no_scripts[i].strip()

        # if str(content)=='':
        #     print(content)
        #     pass
        item['content']=str(content)

        for i, a in enumerate(response.xpath('//a')):
            url = a.xpath('@href').extract_first()
            if url != None and url != '':
                if url.find("javascript:") < 0 and url.find("baidu") < 0 and url.find("http:") > -1 and url.find("zhihu")<0 and url.find('360doc')<0:
                    #获取这个连接的名字
                    title = a.xpath('text()').extract_first()
                    url=str(url).strip()
                    item2 = LishiBaiduItem()
                    item2['name'] = str(title)
                    item2['url'] = str(url)
                    item2['cc'] = 0
                    item2['content'] = ''
                    item2['cj'] = 2
                    item2['searchTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    item["item2"].append(item2)
                    weizhi=item["item2"].index(item2)
                    self.num_2+=1
                    self.r.set("num_2",self.num_2)
                    yield scrapy.Request(url, meta={'item_2': item,'weizhi':weizhi}, callback=self.parse_3)
        # yield item
    def parse_3(self, response):
        item = response.meta['item_2']
        weizhi=response.meta['weizhi']
        item['item3'] = []
        content=''
        # 获取网页中所有文字,并赋给第二级网址
        textlist_no_scripts = response.selector.xpath('//*[not(self::script or self::style)]/text()[normalize-space(.)]').extract()
        for i in range(0, len(textlist_no_scripts)):
            content = content + textlist_no_scripts[i].strip()

        # if str(content) == '':
        #     print(content)
        #     pass
        item["item2"][weizhi]["content"]=str(content)

        for i, a in enumerate(response.xpath('//a')):
            url = a.xpath('@href').extract_first()
            if url != None and url != '':
                if url.find("javascript:") < 0 and url.find("baidu") < 0 and url.find("http:") > -1 and url.find("zhihu") < 0:
                    title = a.xpath('text()').extract_first()
                    url = str(url).strip()
                    item3 = LishiBaiduItem()
                    item3['name'] = str(title)
                    item3['url'] = str(url)
                    item3['cc'] = 0
                    item3['content'] =''
                    item3['cj'] = 3
                    item3['searchTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    item["item3"].append(item3)
                    weizhi3 = item["item3"].index(item3)
                    # print("parse3  weizhi3 is："+str(weizhi))
                    self.num_3+=1
                    self.r.set("num_3",self.num_3)
                    yield scrapy.Request(url, meta={'item_3': item, 'weizhi3': weizhi3}, callback=self.parse_4)
        # yield item

    def parse_4(self, response):
        item = response.meta['item_3']
        weizhi = response.meta['weizhi3']
        content = ''
        # 获取网页中所有文字,并赋给第二级网址
        textlist_no_scripts = response.selector.xpath('//*[not(self::script or self::style)]/text()[normalize-space(.)]').extract()
        for i in range(0, len(textlist_no_scripts)):
            content = content + textlist_no_scripts[i].strip()
        # if str(content)=='':
        #     print(content)
        #     pass
        try:
            item["item3"][weizhi]["content"] = str(content)
        except:
            pass
        finally:
            # print(str(item)+'\n')
            # print("weizhi："+str(weizhi))
            pass
        yield item