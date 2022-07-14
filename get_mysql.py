# 连接mysql数据库
import pymysql
import redis
# connect redis
rdp = redis.ConnectionPool(host='127.0.0.1', port=6379, db=4)
rdc = redis.StrictRedis(connection_pool=rdp, encoding='utf8', decode_responses=True)

# connect mysql database
conn = pymysql.connect(host='192.168.0.9',
                       user='root',
                       password='root',
                       db='createx_kbe',
                       port=3306,
                       charset='utf8')
cursor = conn.cursor()
sql = "select * from tb_userdata limit 100;"
cursor.execute(sql)
data = cursor.fetchall()
conn.close()
d1 = {}
l1 = []

for x in cursor.description:
    l1.append(x[0])
for i in data:
    d1[i[15]] = {}
    for j, z in enumerate(i):
        d1[i[15]][l1[j]] = str(z) if str(z) != 'None' else ''
    rdc.hmset(i[15], d1[i[15]])
    rdc.expire(i[15], 60)
    print(i[15])

z = rdc.hmget('wk2', ['organization','distributor', 'editor_ip', 'app_ip', 'platform', 'UID', 'Power', 'UserName', 'AccountPower'])
data_list = [str(x, encoding='utf-8') if x is not None else '' for x in z]
