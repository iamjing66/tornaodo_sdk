#!/usr/bin/env python
# coding=utf-8

from handlers.base import BaseHandler
import redis


class IndexHandler(BaseHandler):  # 继承base.py中的类BaseHandler
    def get(self):
        # err_data = []
        #
        # sql = "select * from tb_res_error group by (ResType)  order by id desc limit 0,50;"
        # self.Cur.execute(sql)
        # self.db.commit()
        # data = self.Cur.fetchall()
        # if data != None and len(data) > 0:
        #     list_data = list(data)
        #     for minfo in list_data:
        #         minfo_list = list(minfo)
        #         _data = {
        #             "ID": str(minfo_list[0]),
        #             "ResID": str(minfo_list[1]),
        #             "Error_Log": str(minfo_list[2]),
        #             "ResType": str(minfo_list[3]),
        #             "Date": str(minfo_list[4])
        #         }
        #         err_data.append(_data)

        # url = "http://192.168.0.9:9001/postinterface"
        # json_Data = {
        #     "opencode": 5,
        #     "subcode": 0,
        #     "UID": 0,
        #     "username": "",
        #     "data": {
        #         "OpenCode": "207",
        #         "Pam": " limit 200,500"
        #     }
        # }
        # res = requests.post(url=url, json=json_Data)
        # print("res:",res.json())

        str_txt = ""
        # with open("test.txt", "r") as f:  # 打开文件
        #     str_txt = f.read()  # 读取文件
        #     print(str_txt)
        # str_txt = str_txt.replace("\x00","")
        # print(str_txt)
        # for c in  str_txt:
        #     print(c,"->",ord(c))

        # str_txt = str_txt.replace("username","")

        # redis 测试
        # r = redis.StrictRedis(host='localhost',port=6379,db=0)
        # runoob = r.get('runoob')
        # print("runoob : " , runoob)

        # Data_CourseInst.Data_Course_Base(63,318,1,DBManager())
        # Data_CourseInst.CourseFlag_Buy(63,24,3,  DBManager())
        # Data_LessonInst.Data_Lesson_Base(63,137,0,DBManager())
        # interface_global.Test()
        # DB = DBManager()
        # sql = "select username from tb_userdata where uid = 9;"
        # data = DB.fetchone(sql, None)
        # wstr = "none data"
        # if data:
        #     wstr = "username = " + data[0]
        # DB.destroy()
        # #self.render("login.html")
        # self.write(wstr)

        # 获取本机计算机名称
        # hostname = socket.gethostname()
        # 获取本机ip
        # ip = socket.gethostbyname(hostname)
        # self.write(ip)

        # scache = ServerAddressCache()
        # scache.SetAddress()

        # scache = RedisConfigWrite()
        # scache.WriteConfig()

        # C_ServerAddressCache.SetUser("lyy","app","192.168.0.22:9001")
        # # for i in range(0, 20):  # 循环随机数100位
        # #     num = random.randint(0, 4)
        # #     print("num = " + str(num))
        # url = globalRedisU.redis_getAdreese()
        # print("login - get serverAddresse = " + url)

        # rc = redis.StrictRedis(host='192.168.0.9', port='6379', db=1, password='123123')
        # rc.publish("runoobChat","hello")
        self.write("ok")

    def post(self):
        ID = self.request.body_arguments["ID"][0].decode()
        self.db_ping
        sql = "delete from tb_res_error where ResType = (select n.ResType from (select ResType from tb_res_error where ID = " + ID + ") as n );"
        self.Cur.execute(sql)
        self.db.commit()
        data = {"error": ""}
        self.write(data)


class XfHandler(BaseHandler):  # 继承base.py中的类BaseHandler
    def get(self):
        self.write("ok")


class ErrorHandler(BaseHandler):  # 增加了一个专门用来显示错误的页面
    def get(self):  # 但是后面不单独讲述，读者可以从源码中理解
        self.render("error.html")
