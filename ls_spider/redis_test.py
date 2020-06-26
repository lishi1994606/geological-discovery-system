import redis

conn = redis.Redis(host='127.0.0.1', port=6379,)  # 创建连接redis

conn.set('k1', 'v1')  # 往redis中插入一条数据
val = conn.get('k1')  # 查询插入的数据

conn.hset("item1","name","ahah")
# conn.hmset("item1",'name',"haha","url","www.baidu.com")
conn.hmset("list:item1",{"name":"haha","url":"www.baidu.com"})


list_keys = conn.keys("result:**")

list= conn.smembers('urllist')

print(list)

for key in list:
    print(key)

for key in list_keys:
    conn.delete(key)

print(val)  # 打印值