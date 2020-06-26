# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import os

class LsSpiderPipeline(object):
    keyword_list=['空间数据库', '海洋地质学', '数据检索', '沉积动力学', '事件沉积学', '大地构造', '比较沉积学', '地震沉积学',
                  '沉积相模式', '数据存贮', '全球沉积地质计划', '地质事件', '地质学', '宏观沉积学', '构造沉积学', '沉积岩',
                  '沉积学', '地震勘探', '沉积地球化学', '沉积物', '沉积岩石学', '沉积岩石学;沉积作用;化学-沉积地球化学',' 沉积作用', '数据库']
    keyword_list_value=[0.8,0.5,0.8,0.5,0.5,0.5,0.5,0.5,
                        0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.8,
                        1,0.5,0.5,0.5,0.5,0.8,0.5,1] #对应keyword的权重
    keyword_list_content_frequency=[0]*50  #对应keyword出现的次数
    keyword_list_title_frequency=[0]*50  # 对应keyword在title中出现的次数
    ratio=0.6

    key_type=['.xml', '.json', '.ISO', '.RAR', '.html', '.zip', '.exe', '.pdf', '.rm', '.avi', '.tmp', '.xls', '.mdf', '.MID',
     '.pptx', '.wl', '.wp', '.wt', '.mpj', '.cdr', '.doc', '.txt', '', '.hlp', '', '.wps', '', '.rtf', '.mp3', '',
     '.avi', '', '.mov', '', '.swf', '', '.mpg', '', '.ram', '', '.mmf', '', '.au', '', '.aif', '.adf', '.tiff', '.shp',
     '.shx', '.dbf', '.dat', '.jpg', '.kml', '.kmz', '.png', '.grd', '.bmp', '.dem', '.img', '.csv', '.lrp', '.xls',
     '.xlsx', '.bsq', '.pos', '.bip', '.jpeg', '.bil', '.osgb', '.sid', '.s3c', '.gft', '.dae', '.ecw', '.3mx', '.ers',
     '.hdr', '.mif', '.vec', '.3ds', '.obj.max', '.dae', '.stl', '.c4d', '.max', '.maya']

    def __init__(self, REDIS_SERVER, REDIS_PORT):
        self.REDIS_SERVER = REDIS_SERVER
        self.REDIS_PORT = REDIS_PORT

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            REDIS_SERVER=crawler.settings.get('REDIS_SERVER'),
            REDIS_PORT=crawler.settings.get('REDIS_PORT')
        )

    def open_spider(self, spider):
        pool = redis.ConnectionPool(host=self.REDIS_SERVER, port=self.REDIS_PORT,decode_responses=True)
        self.conn = redis.Redis(connection_pool=pool)

        # 读取keyword_list和keyword_list_value
        self.keyword_list=[]
        self.keyword_list_value=[]
        self.keyword_list=self.conn.lrange("keyword_list",0,-1)
        try:
            self.keyword_list_value=self.conn.lrange("keyword_list_value",0,-1)
        except:
            print(str(self.keyword_list_value))
        finally:
            self.keyword_list_value=list(map(self.stringconvertdouble,self.keyword_list_value))
            print(str(self.keyword_list_value))



    def stringconvertdouble(self,a):
        if len(a) > 3:
            a = a[0:3]
        return float(a)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if item==None:
            return None
        if item["cj"] == 1 and item["name"]!='':
            print(item['url'])
            #p=os.path.join(os.getcwd(),"result")
            p='D:\\pyrun\\result'
            #result path写入redis
            self.conn.set("result_path",str(p))
            f = open(os.path.join(p,'result1',item['name'])+".txt", 'w',encoding='utf-8')
            cc1=self.calculation(item['content'],item['name'])
            tt1=self.find_data_type(item['content'])
            item['cc']=cc1
            item['tt']=tt1
            f.write('[一级地址]'+'\t' + str(item["name"]) + '\t' + str(item["url"]) + '\t\t' + str(item["cc"]) + '\t' + str(item["cj"]) + '\t'+ str(item["tt"])+'\t'+str(item["searchTime"])+'\n')
            #写入redis
            # self.conn.sadd("urllist",str(item["url"]))
            self.conn.hmset("result1:"+item["url"],{"name":str(item["name"]),"url":str(item["url"]),"cc":str(item["cc"]),"cj":str(item["cj"]),"tt":str(item["tt"]),"searchTime":str(item["searchTime"])})
            self.conn.incr('parse_num_1')
            f.close()
        if item["cj"] == 2 and item["name"]!='':
            print(item['url'])
            #p=os.path.join(os.getcwd(),"result")
            p='D:\\pyrun\\result'
            #result path写入redis
            self.conn.set("result_path",str(p))
            f = open(os.path.join(p,'result2',item['name'])+".txt", 'w',encoding='utf-8')
            cc1=self.calculation(item['content'],item['name'])
            tt1=self.find_data_type(item['content'])
            item['cc']=cc1
            item['tt']=tt1
            f.write('[二级地址]'+'\t' + str(item["name"]) + '\t' + str(item["url"]) + '\t\t' + str(item["cc"]) + '\t' + str(item["cj"]) + '\t'+ str(item["tt"])+'\t'+str(item["searchTime"])+'\n')
            #写入redis
            # self.conn.sadd("urllist",str(item["url"]))
            self.conn.hmset("result2:"+item["url"],{"name":str(item["name"]),"url":str(item["url"]),"cc":str(item["cc"]),"cj":str(item["cj"]),"tt":str(item["tt"]),"searchTime":str(item["searchTime"])})
            self.conn.incr('parse_num_2')
            f.close()

        if item["cj"] == 3 and item["name"]!='':
            print(item['url'])
            #p=os.path.join(os.getcwd(),"result")
            p='D:\\pyrun\\result'
            #result path写入redis
            self.conn.set("result_path",str(p))
            f = open(os.path.join(p,'result3',item['name'])+".txt", 'w',encoding='utf-8')
            cc1=self.calculation(item['content'],item['name'])
            tt1=self.find_data_type(item['content'])
            item['cc']=cc1
            item['tt']=tt1
            f.write('[三级地址]'+'\t' + str(item["name"]) + '\t' + str(item["url"]) + '\t\t' + str(item["cc"]) + '\t' + str(item["cj"]) + '\t'+ str(item["tt"])+'\t'+str(item["searchTime"])+'\n')
            #写入redis
            self.conn.hmset("result3:"+item["url"],{"name":str(item["name"]),"url":str(item["url"]),"cc":str(item["cc"]),"cj":str(item["cj"]),"tt":str(item["tt"]),"searchTime":str(item["searchTime"])})
            self.conn.incr('parse_num_3')
            f.close()

        return item

    def calculation(self,content,title):
         # 根据叙词表中词的数量来建立这个数
        self.keyword_list_content_frequency=[0]*self.conn.llen("keyword_list") #对应keyword出现的次数
        self.keyword_list_title_frequency=[0]*self.conn.llen("keyword_list") # 对应keyword在title中出现的次数

        if(content!=''):
            print(str(title))
            pass
        # content='沉积学数据库沉积相模式沉积学比较沉积学沉积地球化学沉积动力地质学数据库空间数据库数据存贮数据检索'
        content=content.lower()
        title=title.lower()

        n=0
        for kl in self.keyword_list:
            kl = kl.strip() # 有些分词前后有空格
            kl = re.sub(r'[()-]','',kl) 
            kl = kl.lower()
            try:
                key_content_num=re.findall(kl,content)
                key_title_num=re.findall(kl,title)
            except Exception as e:
                print(str(e))
            try:
                self.keyword_list_content_frequency[n]=len(key_content_num)*self.ratio
                self.keyword_list_title_frequency[n]=len(key_title_num)
            except Exception as e:
                print(str(e))
            n=n+1
        v_keyword_frequency=list(map(lambda x:x[0]+x[1],zip(self.keyword_list_title_frequency,self.keyword_list_content_frequency)))
        v= list(map(lambda x:x[0]*x[1],zip(self.keyword_list_value,v_keyword_frequency)))
        return sum(v)

    def find_data_type(self,content):
        type_list=[]
        result=''
        for kl in self.key_type:
            key_type_num=re.findall(kl,content)
            if(len(key_type_num)>0):
                type_list.append(kl)
        if len(type_list)==0:
            result='没有相关数据类型'
        else:
            for t in type_list:
                if t!='':
                    result=result+str(t)+','
        return result
