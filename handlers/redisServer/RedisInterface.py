#!/usr/bin/env python
# coding=utf-8

import redis
import logging

import time

import Global

class RedisBase(object):
    """缓存类父类"""
    _host = Global.RedisCreatex_options["host"]
    _port = Global.RedisCreatex_options["port"]
    _database = Global.RedisCreatex_options["database"]
    _password = Global.RedisCreatex_options["password"]

    @property
    def redis_ctl(self):
        """redis控制句柄,就是连接对象"""
        redis_ctl = redis.Redis(host=self._host, port=self._port, db=self._database, password=self._password)
        return redis_ctl



#检测写入公共配置
class RedisWorker(RedisBase):

    def GetWorkMainState(self):

        return self.redis_ctl.get("mainserver")



    def SetWorkMain(self):
        self.redis_ctl.set("mainserver",str(int(time.time())))


    #ServerRt - 0-本地测试 1-外网正式 2-外网测试
    #def WriteConfig(self):

        #配置
        #name = cxconfig

        #写入 负载地址
        #name = balancing
        #self.redis_ctl.decr("balancing")
        #self.redis_ctl.set("balancing",Global.GetConfig(ServerRt,0))
        #self.redis_ctl.hdel("cxconfig","balancing")
        #print(Global.GetConfig(0))
        self.redis_ctl.hset("cxconfig","balancing",Global.get_config.redis_config)
        #l = self.redis_ctl.hget("cxconfig","balancing")
        #print("list = " , list(l))



class ServerAddressCache(RedisBase):


    def SetUser(self,username,cmode,Adresse):
        self.redis_ctl.hset(username,cmode,Adresse)

    def GetAddress(self,username,cmode):
        return self.redis_ctl.hget(username,cmode)

C_ServerAddressCache = ServerAddressCache()

class TokenCache(RedisBase):
    """微信token缓存"""
    _expire_access_token = 7200  # 微信access_token过期时间, 2小时
    _expire_js_token = 7200  # 微信jsapi_ticket, 过期时间, 7200秒

    def set_access_cache(self, key, value):
        """添加微信access_token验证相关redis"""
        self.redis_ctl.set(key, value)
        # 设置过期时间
        self.redis_ctl.expire(key, self._expire_access_token)
        logging.info('更新了 access_token')

    def set_js_cache(self, key, value):
        """添加网页授权相关redis"""
        self.redis_ctl.set(key, value)
        # 设置过期时间
        self.redis_ctl.expire(key, self._expire_js_token)
        logging.info('更新了 js_token')

    def get_cache(self, key):
        """获取redis"""
        try:
            v = (self.redis_ctl.get(key)).decode('utf-8')
            return v
        except Exception as e:
            logging.error('wxcache' + str(e))
            return None


class RedisData():
    def __init__(self, database) -> None:
        self.database = database
        self.redis_config = Global.get_config.redis_options(self.database)

    def redis_pool(self):
        print(self.redis_config)
        rdp = redis.ConnectionPool(self.redis_config)
        #rdc = redis.Redis(self.redis_config)
        #print(rdc)
        rdc = redis.StrictRedis(connection_pool=rdp, encoding='utf8', decode_responses=True)
        return rdc
