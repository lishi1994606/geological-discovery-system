from scrapy.cmdline import execute
import sys
import os
import redis
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# #decode_responses=True,有这个之后读出来的字符串就不会是二进制了
pool = redis.ConnectionPool(host="127.0.0.1", port=6379,decode_responses=True)
conn = redis.Redis(connection_pool=pool)

conn.set('num_1',0)
conn.set('num_2',0)
conn.set('num_3',0)
conn.set('parse_num_1',0)
conn.set('parse_num_2',0)
conn.set('parse_num_3',0)

guanjianci=None


# keyword_list_value=conn.lrange("keyword_list_value",0,-1)
try:
    conn.delete("guanjianci")
finally:

    pass

while True:
    guanjianci=conn.get("guanjianci")
    print("等待分词结果，请启动C#程序分词")
    if guanjianci!=None:
        print("关键词："+guanjianci)
        break
    time.sleep(3);

# test scope
# guanjianci='沉积学数据库'
execute(['scrapy', 'crawl','lsSpider0', '-a  category='+guanjianci])  # 你需要将此处的spider_name替换为你自己的爬虫名称