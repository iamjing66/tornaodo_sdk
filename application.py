#!/usr/bin/env python
# coding=utf-8
from handlers.SyncServer.sockect import pro_status
from handlers.kbeServer.Editor.Interface.interface_config import IC
from url import Urls
import Global
import logging
import redis
from handlers.redisServer.RedisInterface import RedisData, C_ServerEventCache
import tornado.web
import threading
from handlers.redisServer.RedisInterface import RedisWorker
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
import time

#############
#本服务用来负责读操作
#############


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.SIp = ""
        self.SPort = 0
        self.SAddress = ""
        self.RedisServerAddress = ""
        self.MainServer = False
        self.SUID = ""


    def DoInit(self,_ip,_port):

        self.SIp = _ip
        self.SPort = _port
        self.SAddress = _ip+":"+str(_port)
        self.RedisServerAddress = _ip+"*"+str(_port)
        logging.info("[ServerSetup] addresse = " + self.SAddress)
        serverlist = Global.get_config.redis_config()
        logging.info("[ServerSetup] serverlist = " + str(serverlist))
        rd = RedisData(1)
        rds = rd.redis_pool()
        akpos = rds.get("ak")
        ak = 1
        if akpos:
            ak = int(akpos)
        rds.set("ak",str(ak+1))
        self.SUID = str(serverlist.index(self.SAddress)) + str(ak)
        logging.info("[ServerSetup] SUID = " + str(self.SUID))

        #处理所有初始化
        self.DoInit_All()

        # rs = RedisData(1).redis_pool()
        # rs.set(self.SAddress.replace(":","*"),str(int(time.time())))

        sip = serverlist[0]
        if self.SAddress == sip:
            self.MainServer = True
            self.DoInit_Main()
        else:
            self.MainServer = False
        logging.info("[ServerSetup] MainServer = " + str(self.MainServer))
        #工作事务
        self.worktimer = time.strftime("%Y-%m-%d", time.localtime())

        print("self.MainServer", self.MainServer)

        t = threading.Timer(5, self.Worker)
        t.start()


    def Worker(self):
        # Do something
        self.WorkZero()

        self.DoEvent_All()

        if self.MainServer:
            self.DoEvent_Main()
        t = threading.Timer(5,self.Worker)
        t.start()


    #启动事务 - 所有服务
    def DoInit_All(self):

        # 配置数据
        IC.ReadConfig()

        #加密配置
        self.acs_client = AcsClient(Global.ACCESS_KEY_ID, Global.ACCESS_KEY_SECRET, Global.REGION)
        region_provider.add_endpoint(Global.PRODUCT_NAME, Global.REGION, Global.DOMAIN)

        #订单号
        self.Ali_Order = 1


        #app支付初始化
        # app支付 - 阿里云支付
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = "https://openapi.alipay.com/gateway.do"
        alipay_client_config.app_id = "2021001160668207"
        alipay_client_config.app_private_key = "MIIEpQIBAAKCAQEAuIdOisWAzBnuE4V93jxgaQgyBrkuMnToGCQGx9Dj2yo/2n8ET3yVWd0As/2phI6aXtYAUHXiS7JkSd2naXVSlgjgtgZ28LSplJdvI4YQfYTfwYg1J9LXRI4zu9h7khk0JGrrVrOW1C7xvmywOyHlJ+V8Wf44MUbjvmojU0OTOEZNV3O9rVx4vxaPCF9RGQtAIKnLQGFwDu+B7Fu37HuxL6gvkd1XQPI8cs8FZDcLMHrYLyr79+MjLZx6phPPL4ZsptOCAPS9ty/6EGSACf4ad27byWHL8iu9LpkWbalAnBSisZJPDcN82Q4AHewJ8k02fkS1B4MGybotpXsga3a+jQIDAQABAoIBAGpVJhBXcTmrs4IySW63sgK0Q0eWjCVtMpU+pV2dZL/VX8hDqzM2okWPUalmgbmuBwyhGrtCwu1F1f6uqJrfjYCBiyO5I+7e3F2Qye1ZgsUhvWKjX6YcHAoYO32CaOqudVqK9iQXBtIsXweRUBgzFv7fgcHF+ZGDvRbryIFhjkM9XIBtGmBT1gnLigVoUWQvuD7rXA6P/Jys29b3EK8UDTe1o0sJUreTNNAlGOLa2AefNvLDYt5fqmYjJ3U9sWJvB+UfHGO+I3EhMxvHWTgXptaZ2jH/0SDRnVKAtQwyTMG9w77NKs5jDaYKCFtsnSTR5zrI0h+mMGEeG0QK1W3Nom0CgYEA6kEWKWhpFXeroavqk1k06Obp0/UYUkHLbw5jmtz70TRUda6WSzv0sFEwqwn++52+eyMbeXRut0SgdgfDiZPLjtnLTmlNBI1WjDKglMVnfASFkEHyURpYT9YMHWmu6RYTzDcwUfyscmdTfFQ3fOWm2NpEZd89aexNSB8JPvXmzDsCgYEAyaiEs2T+FQw6d5EjZby9Fj8urUp1U4n0Ed1w65TVMnzZkOYZn8biR9N8tbCWy3ozqLf2ArcQjTH1+xyl+nVFbctbjngw/DeZXkS7S+OxjudI0ON/be6XOVajjI5Ugaxr+Q19Qx1fw1yMDqeRT6T5osJPCBekOUhnjyD6ycbVG9cCgYEArf173XOcoYJKK4HKcHkQsHBaesEPuID//dO9LZg3PXLVzLbJEMZOfus+77sz9WV7xnAUBwjw9xR07lXj6Xqp9cdUlz/lIZ1tDCLKXNWmgFnHbpdcyNp9f4bnZq1Jafyo5cSUEkFPQIX4X18Z+52DaIvtw5ClR9hoqknLD0WLkGMCgYEAmvVbw15/wDy9UNO+l5cI1eeHPrJQpfkEDBZVhzG/AiTeKnImjpiNmRPyaMthlMo6mBOEf2Gc3mLd2jCRenxS9aOmnzvMqIMw3zeBlTdKYb1oPtwSN693lR/2XTOhzGNqNN8gukoAJGchWMF67/Cdw2v8vwMrtrjkmx+Elziq2dECgYEA4ao+0YAriMbbYCRGvsf8fGIQbe0n0NC4sh4JiFmrsF9BjAWxdu/dYkp5OKFnoYhxyxFEisIQETXa/mD06M68htnQqSWgAlI3z7zUR3nFe6lhUbgwQj0aoUTrYEqr3i1MDvsGv+OdQWzERK/igyiP3p8sW/rPZpU8ztdtnKej3Ig="
        alipay_client_config.alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAg5StQ8OYhj2+Brg3y3KxiTVLXSLeN9rfliGoFleLALKfBuZ7cYcPozJP7ZT0HDJRBHt9I22Fw2ZzG5u1nRcm+mV/XnbtnEeFDmkpjSLtesfuR/Dm2za4D88v5PbbkvFfpKWXFKbI6ZstQybiDv990ssy36lKSoxbzfrgTeAc0PUscgAGKUijADsTq/2VUYgvuf6CF7B8E0fbhprRtGqETetmlb4F4XgwACM/DjchyoxTu3kRptSm2DIZTWS3klcc39LYw+c86OlQEZQiMOjb77XZNTbxtkmfALm2Q0+wYpSS8QKfMP16ux8bvZbVbjQQckxOEZKNvjV6dxSvxSa72wIDAQAB"
        alipay_client_config.sign_type = "RSA2"
        self.Connect = 0
        self.aliclient = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        self.alimodel = AlipayTradeAppPayModel()


        #清理业务缓存
        #顶号业务
        key = self.RedisServerAddress + "$C1"
        data = C_ServerEventCache.GetKeys(key)
        if len(data) > 0:
            for uuid in data:
                C_ServerEventCache.DeleteKeys(key, uuid)


    # 启动事务 - 主服务
    def DoInit_Main(self):
        # 清理业务缓存
        # 顶号业务
        key = "websocket"
        rd = RedisData(2)
        rds = rd.redis_pool()
        data = rds.hkeys(key)
        if len(data) > 0:
            for uuid in data:
                rds.hdel(key, uuid)


    #事务处理 - 所有服务
    def DoEvent_All(self):

        #处理事务
        #logging.info("[Do Event All]" + self.SAddress)

        #处理顶号事务
        key = self.RedisServerAddress+"$C1"
        data = C_ServerEventCache.GetKeys(key)

        if len(data) > 0:
            logging.info("[DoEvent_All] data = %s - key = %s" % ( data, key))
            for uuid in data:
                C_ServerEventCache.DeleteKeys(key,uuid)
                self.DoEvent_Kick(uuid.decode())

    def DoEvent_Kick(self,uuid):

        print("DoEvent = " , uuid)
        pro_status.user_kick(uuid)

    #事务处理 - 主服务
    def DoEvent_Main(self):
        pass


    #0点事务
    def WorkZero(self):

        now = time.strftime("%Y-%m-%d", time.localtime())
        if now != self.worktimer:
            self.worktimer = now
            self.DoZero()
            if self.MainServer:
                self.DoZero_Main()


    # 0点事务 - 所有服务
    def DoZero_All(self):
        pass

    # 0点事务 - 主服务
    def DoZero_Main(self):
        pass


App = Application(
    handlers = Urls,
    **Global.settings
    )