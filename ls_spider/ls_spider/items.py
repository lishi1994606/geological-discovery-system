# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LishiBaiduItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url= scrapy.Field()
    cc= scrapy.Field() # 相关系数
    content=scrapy.Field() #内容
    cj= scrapy.Field() # 层级
    tt=scrapy.Field()  # 数据类型
    searchTime= scrapy.Field()
    item2= scrapy.Field() # 二级子节点
    item3=scrapy.Field() # 三级子节点


class LishiBaiduItem2(scrapy.Item):
    fitem=scrapy.Field()
    name = scrapy.Field()
    url= scrapy.Field()
    cc= scrapy.Field() # 相关系数
    content=scrapy.Field() #内容
    cj= scrapy.Field() # 层级
    tt=scrapy.Field()  # 数据类型
    searchTime= scrapy.Field()
    item3=scrapy.Field() # 三级子节点

class LishiBaiduItem3(scrapy.Item):
    fitem= scrapy.Field()
    name = scrapy.Field()
    url= scrapy.Field()
    cc= scrapy.Field() # 相关系数
    content=scrapy.Field() #内容
    cj= scrapy.Field() # 层级
    tt=scrapy.Field()  # 数据类型
    searchTime= scrapy.Field()