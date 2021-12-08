#!/usr/bin/env python
# coding=utf-8
import random

import Global
from methods.DBManager import DBManager
from handlers.redisServer.RedisInterface import RedisData

class redisu:


    def __init__(self):
        self.redisUData = {}
        self.redisUName = {}
        self.configures = []
        self.GlobalIPIndex = 0
        self.GlobalIPs = None

    # 缓存用户数据
    def redis_user_set(self,userName, data):

        if "platform" not in data.keys():
            return
        # 终端平台
        platform = int(data["platform"])
        # 10PC平台
        # 11官网
        # 12二级平台
        # 20智能手机平台APP
        # 30XR平台
        # 31PicoVR
        # 32创维VR
        # 33影创VR
        # 34影创MR
        # 35Focus
        # 36大鹏
        # 37睿悦
        # 38HTC
        # 39海信
        # 40华为云
        # 41天翼云
        # 50TV平台

        #用户登录的IP
        local_ip = data["IP"]

        DB = DBManager()
        sql = "select ID from tb_solr_redis where username = '" + userName + "'"
        data = DB.fetchone(sql, None)
        if not data:
            sql = "insert into tb_solr_redis(UID,Phone,organization,UserName,distributor,Power,AccountPower) select UID,Phone,organization,UserName,distributor,Power,AccountPower from tb_userdata where username = '"+userName+"';"
            DB.edit(sql,None)


        #缓存udata
        if platform != 10:  #VR平台
            sql = "update tb_solr_redis set platform = " + str(platform) + ",app_ip = '"+local_ip+"' where username = '"+userName+"'"
        else:
            sql = "update tb_solr_redis set editor_ip = '" + local_ip + "' where username = '" + userName + "'"
        DB.edit(sql, None)
        DB.destroy()
        return True


    #获取缓存数据[分销商，机构，editorip,appip,平台]
    def redis_user_get(self,userName):

        # if userName not in self.redisUData.keys():
        DB = DBManager()
        sql = "select organization,distributor,editor_ip,app_ip,platform,UID,Power,UserName,AccountPower from tb_solr_redis where username = '"+userName+"'"
        data = DB.fetchone(sql, None)
        DB.destroy()
        if data:
            self.redisUData[userName] = [int(data[0]),int(data[1]),data[2],data[3],int(data[4]),int(data[5]),int(data[6]),data[7],data[8]]
            self.redisUName[int(data[5])] = userName
        else:
            return None
        return self.redisUData[userName]

    # 获取缓存数据[分销商，机构，editorip,appip,平台]
    def redis_user_u_get(self, uid):
        if not(self.redisUName.get(uid, "")):
            DB = DBManager()
            sql = "select organization,distributor,editor_ip,app_ip,platform,UID,Power,UserName,AccountPower from tb_solr_redis where UID = %s"
            data = DB.fetchone(sql, uid)
            DB.destroy()
            if not data:
                return None
            else:
                self.redisUData[data[7]] = [int(data[0]), int(data[1]), data[2], data[3], int(data[4]), int(data[5]),int(data[6]), data[7], data[8]]
                self.redisUName[uid] = data[7]
        return self.redisUData[self.redisUName[uid]]


    def redis_configure_get(self):

        DB = DBManager()
        sql = "select NETFLAG,QIDONGFLAG,DATINGFLAG,KECHENGFLAG,RIZHIFLAG from log_configure limit 0,1"
        data = DB.fetchone(sql, None)
        DB.destroy()
        if not data:
            return None

        return [data[0], data[1], data[2], data[3], data[4]]


    def redis_serverip_get(self):

        if not self.GlobalIPs:
            DB = DBManager()
            sql = "select `Data` from log_user where id = 1 limit 0,1"
            data = DB.fetchone(sql, None)
            DB.destroy()
            if not data:
                return None
            else:
                self.GlobalIPs = data[0].split('$')

        _ip = self.GlobalIPs[self.GlobalIPIndex]
        if self.GlobalIPIndex >= len(self.GlobalIPs) - 1:
            self.GlobalIPIndex = 0
        else:
            self.GlobalIPIndex += 1
        print("_ip = " ,_ip)
        return _ip


    def redis_serverip_save(self,username,cmode,url):
        DB = DBManager()
        sql = "select `ID` from tb_redis_user where username = '"+username+"' and `mode` = '"+cmode+"' limit 0,1"
        data = DB.fetchone(sql, None)
        if data:
            sql = "update tb_redis_user set uniqueurl = '"+url+"' where ID = " + str(data[0])
        else:
            sql = "insert into tb_redis_user (username,`mode`,uniqueurl) value('"+username+"','"+cmode+"','" + url + "')"
        DB.edit(sql,None)
        DB.destroy()



    def redisurl_get(self, uid,cmode):

        DB = DBManager()
        sql = "select `uniqueurl` from tb_redis_user where `mode` = '"+cmode+"' and username = (select username from tb_userdata where uid = "+str(uid)+" limit 0,1)"
        data = DB.fetchone(sql, None)
        DB.close()
        if data:
            return data[0]

        return None


    def redis_getAdreese(self):

        aalist = Global.get_config.redis_config()

        return random.choice(aalist)



    def redisurl_delete(self,uid,cmode):

        DB = DBManager()
        sql = "delete from tb_redis_user where `mode` = '" + cmode + "' and username = (select username from tb_userdata where uid = " + str(uid) + " limit 0,1)"
        DB.edit(sql, None)
        DB.close()


globalRedisU = redisu()


# 暂不上传
redis_db = RedisData(4)
DB = DBManager()
class redis_data():
    # 可用于用户信息全量入 redis
    def redis_user_set_all(self, data):
        sql = "select * from tb_userdata"
        data_user = DB.fetchall(sql)
        d1 = {}
        l1 = []
        # 获取所有的字段名
        for x in DB.cur.description:
            l1.append(x[0])
        for i in data_user:
            d1[i[15]] = {}
            for j, z in enumerate(i):
                d1[i[15]][l1[j]] = str(z) if str(z) != 'None' else ''
            # 用户名为键，用户信息为值
            redis_db.redis_pool.hmset(i[15], d1[i[15]])
            # 设置过期时间
            redis_db.redis_pool.expire(i[15], 60 * 5)
        DB.destroy()


    def redis_user_set(self, username, data):
        if data["platform"] != 10:
            redis_db.redis_pool.hset(username, "app_ip", data["local_ip"])
        else:
            redis_db.redis_pool.hset(username, "editor_ip", data["local_ip"])
        redis_db.redis_pool.hset(username, "platfrom", data["platform"])


    def redis_user_get(self, username):
        data_list = redis_db.redis_pool.hmget(username, ['organization', 'distributor', 'editor_ip', 'app_ip', 'platform', 'UID', 'Power', 'UserName', 'AccountPower'])
        # [b'0', b'0', b'', b'', None, b'12', b'0', b'wk2', b'0']
        data_list = [str(x, encoding='utf-8') if x is not None else '' for x in data_list]
        return data_list
