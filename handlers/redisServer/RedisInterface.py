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

    def DeleteKeys(self, key , name):
        return self.redis_ctl.hdel(key,name)





C_ServerEventCache = ServerEventCache()




