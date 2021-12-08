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


# print(rdc.hvals('wk2'))
z = rdc.hmget('wk2', ['organization','distributor', 'editor_ip', 'app_ip', 'platform', 'UID', 'Power', 'UserName', 'AccountPower'])
data_list = [str(x, encoding='utf-8') if x is not None else '' for x in z]
print(data_list)
# print([str(i, encoding='utf8') for i in rdc.hvals('wk2')])


# res = {
#     'wk2': {
#         'ID': '105',
#         'UID': '12',
#         'Phone': '',
#         'Power': '0',
#         'UPower': '0',
#         'MainAccount': '0',
#         'TheName': '2',
#         'TheSchool': '2222222222222',
#         'TheClass': '222222222222',
#         'identity': '222222222222222222',
#         'COMID': '0',
#         'EndDate': '1',
#         'AccountDesc': '飞蝶研发',
#         'BCBag': '',
#         'Wit_Score': '0',
#         'UserName': 'wk2',
#         'organization': '0',
#         'distributor': '0',
#         'AccountType': '0',
#         'isDel': 'None',
#         'uversion': '0',
#         'makec': '0',
#         'AccountSource': '0',
#         'AccountOther': '0',
#         'CLASSID': '',
#         'NickUrl': '',
#         'NickName': '',
#         'fabricator': '0',
#         'savepnum': '3',
#         'adminType': '0',
#         'state': '0',
#         'appstate': '0',
#         'c_viplv': '0',
#         'JGTC_DATE': '2021-01-06 09:55:22',
#         'tryoutCourse': 'None',
#         'useType': 'None',
#         'AccountPower': '0',
#         'VipPower': '0',
#         'VipDate': '0',
#         'Wit_Rmb': '0',
#         'DeleteMail': 'None',
#         'ReadMail': 'None',
#         'PID': '31',
#         'CID': '28',
#         'editor_ip': '',
#         'app_ip': '',
#         'app_device': '',
#         'GMSTATE': '0',
#         'phonecode': '',
#         'phonecodedate': '0',
#         'RmbPayTotal': '0',
#         'WitPayTotal': '0',
#         'address': 'None',
#         'birthday': 'None',
#         'nation': 'None',
#         'parentName': 'None',
#         'TotalTimes': '0',
#         'UsedTimes': '0'
#     }
# }
