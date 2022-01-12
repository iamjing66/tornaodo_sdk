#!/usr/bin/env python
# coding=utf-8

import redis
import logging

import time

import Global
import application


class RedisBase(object):
    """缓存类父类"""
    _host = Global.RedisCreatex_options["host"]
    _port = Global.RedisCreatex_options["port"]
    _database = Global.RedisCreatex_options["database"]
    _password = Global.RedisCreatex_options["password"]

    @property
    def redis_ctl(self):
        """redis控制句柄,就是连接对象"""
        redis_ctl = redis.Redis(host=self._host,
                                port=self._port,
                                db=self._database,
                                password=self._password)
        return redis_ctl


#检测写入公共配置
class RedisWorker(RedisBase):
    def GetWorkMainState(self):

        return self.redis_ctl.get("mainserver")

    def SetWorkMain(self):
        self.redis_ctl.set("mainserver", str(int(time.time())))

        # ServerRt - 0-本地测试 1-外网正式 2-外网测试
        # def WriteConfig(self):

        #     配置
        #     name = cxconfig

        #     写入 负载地址
        #     name = balancing
        #     self.redis_ctl.decr("balancing")
        #     self.redis_ctl.set("balancing",Global.GetConfig(ServerRt,0))
        #     self.redis_ctl.hdel("cxconfig","balancing")
        #     print(Global.GetConfig(0))
        self.redis_ctl.hset("cxconfig", "balancing",
                            Global.get_config.redis_config())

    #     l = self.redis_ctl.hget("cxconfig","balancing")
    #     print("list = " , list(l))

class RedisData():

    def __init__(self, database) -> None:
        self.database = database
        self.redis_config = Global.get_config.redis_options(self.database)

    def redis_pool(self):
        print(self.redis_config)
        return redis.Redis(host=self.redis_config["host"],
                    port=self.redis_config["port"],
                    db=self.redis_config["db"],
                    password=self.redis_config["password"])
        #rdp = redis.ConnectionPool(self.redis_config)
        #rdc = redis.StrictRedis(connection_pool=rdp,encoding='utf8',decode_responses=True)

        #return rdc


class ServerEventCache():

    def __init__(self):
        rds = RedisData(3)
        self.redis_ctl = rds.redis_pool()

    def SetEvent(self, key , name , value):
        self.redis_ctl.hset(key, name, value)

    def GetKeys(self, key):
        return self.redis_ctl.hkeys(key)


    def GetValue(self, key,name):
        return self.redis_ctl.hget(key,name)

    def DeleteKeys(self, key , name):
        return self.redis_ctl.hdel(key,name)

    def DeleteKey(self, key):
        return self.redis_ctl.key(key,self.GetKeys(key))



#验证码redis
class ServerSMSCache():

    def __init__(self):
        rds = RedisData(5)
        self.redis_ctl = rds.redis_pool()

    def SaveCode(self, phone ,sub  , code):
        key = phone + "$" + str(sub)
        self.redis_ctl.set( key , code)
        self.redis_ctl.expire(key,60)

    def GetCode(self,  phone ,sub):
        key = phone + "$" + str(sub)
        code = self.redis_ctl.get(key)
        #print("record phonecode = " , code)
        if not code:
            return "-99"

        return code.decode()

    def DetCode(self, phone ,sub):
        key = phone + "$" + str(sub)
        self.redis_ctl.delete(key)


class ServerWechatLoginCache():

    def __init__(self):
        rds = RedisData(5)
        self.redis_ctl = rds.redis_pool()

    def SaveCode(self, state , nickname  , headimg, sex , unionid):
        key = state
        self.redis_ctl.hset( key , "nickname" ,nickname )
        self.redis_ctl.hset(key, "headimg", headimg)
        self.redis_ctl.hset(key, "sex", sex)
        self.redis_ctl.hset(key, "unionid", unionid)

    def GetCode(self,  state , name):
        value = self.redis_ctl.hget(state,name)
        if value:
            return value.decode()
        return value


    def SavUserName(self,state,username):
        key = "un"+state
        self.redis_ctl.set(key,username)

    def GetUserName(self,state):
        key = "un"+state
        value = self.redis_ctl.get(key)
        if value:
            return value.decode()
        return value

    def DetCode(self, phone ,sub):
        key = phone + "$" + str(sub)
        self.redis_ctl.delete(key)


class ServerMailCache():

    def __init__(self):
        rds = RedisData(7)
        self.redis_ctl = rds.redis_pool()

    def SaveMailRead(self , uid,mid):

        key = "mailread"+str(uid)
        value = self.redis_ctl.get(key)
        msg = ""
        if value:
            msg = value.decode()
        if len(msg) > 0:
            msg = msg + ","+str(mid)
        else:
            msg = str(mid)
        self.redis_ctl.set(key,msg)

        return mid

    def SaveMailDelete(self, uid , mid):

        key = "maildet" + str(uid)
        value = self.redis_ctl.get(key)
        msg = ""
        if value:
            msg = value.decode()
        if len(msg) > 0:
            msg = msg + "," + str(mid)
        else:
            msg = str(mid)
        self.redis_ctl.set(key, msg)

        return mid


    def GetMailRead(self , uid):

        key = "mailread"+str(uid)
        value = self.redis_ctl.get(key)
        msg = ""
        if value:
            msg = value.decode()
        else:
            msg = "\'\'"
        return msg


    def GetMailDet(self , uid):

        key = "maildet"+str(uid)
        value = self.redis_ctl.get(key)
        msg = ""
        if value:
            msg = value.decode()
        else:
            msg = "\'\'"
        return msg


class ServerWechatLoginCache():

    def __init__(self):
        rds = RedisData(5)
        self.redis_ctl = rds.redis_pool()

    def SaveCode(self, state , nickname  , headimg, sex , unionid):
        key = state
        self.redis_ctl.hset( key , "nickname" ,nickname )
        self.redis_ctl.hset(key, "headimg", headimg)
        self.redis_ctl.hset(key, "sex", sex)
        self.redis_ctl.hset(key, "unionid", unionid)

    def GetCode(self,  state , name):
        value = self.redis_ctl.hget(state,name)
        if value:
            return value.decode()
        return value


    def SavUserName(self,state,username):
        key = "un"+state
        self.redis_ctl.set(key,username)

    def GetUserName(self,state):
        key = "un"+state
        value = self.redis_ctl.get(key)
        if value:
            return value.decode()
        return value

    def DetCode(self, phone ,sub):
        key = phone + "$" + str(sub)
        self.redis_ctl.delete(key)



class ServerWitCache():

    def __init__(self):
        rds = RedisData(8)
        self.redis_ctl = rds.redis_pool()

    def GetWit(self, uid , code):

        moneyg = 0
        moneyz = 0

        if code == 1 or code == 0:
            key = "witg"+str(uid)
            moneyg = self.redis_ctl.get( key)
            if not moneyg:
                moneyg = 0
            else:
                moneyg = int(moneyg.decode())
        if code == 2 or code == 0:
            key = "witz" + str(uid)
            moneyz = self.redis_ctl.get(key)
            #print("moneyz", moneyz)
            if not moneyz:
                moneyz = 0
            else:
                moneyz = int(moneyz.decode())


        return moneyz + moneyg

    def SaveWit(self,uid,iWit,iWit_RMB,code):
        if code == 1 or code == 0:
            key = "witg" + str(uid)
            self.redis_ctl.set(key,str(iWit))
        if code == 2 or code == 0:
            key = "witz" + str(uid)
            self.redis_ctl.set(key, str(iWit_RMB))

    def AddWit(self,uid,iWit,iWit_RMB,code):
        if code == 1 or code == 0:
            key = "witg" + str(uid)
            money = self.redis_ctl.get(key)
            if not money:
                money = 0
            else:
                money = int(money.decode())
            money += iWit
            self.redis_ctl.set(key,money)
        if code == 2 or code == 0:
            key = "witz" + str(uid)
            money = self.redis_ctl.get(key)
            if not money:
                money = 0
            else:
                money = int(money.decode())
            money += iWit_RMB
            self.redis_ctl.set(key, money)

    def Exist(self,uid):

        key = "witg" + str(uid)
        return self.redis_ctl.exists(key)



class ServerUserCache():

    def __init__(self):
        rds = RedisData(9)
        self.redis_ctl = rds.redis_pool()

    def SaveUser(self, username,arr):
        key = username
        self.redis_ctl.hset( key , "uid" ,str(arr[0]) )
        self.redis_ctl.hset(key, "cdate", str(arr[1]))

    def GetData(self,  state , name):
        value = self.redis_ctl.hget(state,name)
        if value:
            return value.decode()
        return None

    def Exist(self,username):

        return self.redis_ctl.hexists("uid",username)



C_ServerEventCache = ServerEventCache()




