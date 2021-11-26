#!/usr/bin/env python
# coding=utf-8
from handlers.kbeServer.Editor.Interface.interface_config import IC
from url import Urls
import Global
import logging
import hashlib
import methods.SolrInterface as sinter
import tornado.web
import threading
from methods.db_mysql import DbHander
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

        #app支付 - 阿里云支付
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = "https://openapi.alipay.com/gateway.do"
        alipay_client_config.app_id = "2021001160668207"
        alipay_client_config.app_private_key = "MIIEpQIBAAKCAQEAuIdOisWAzBnuE4V93jxgaQgyBrkuMnToGCQGx9Dj2yo/2n8ET3yVWd0As/2phI6aXtYAUHXiS7JkSd2naXVSlgjgtgZ28LSplJdvI4YQfYTfwYg1J9LXRI4zu9h7khk0JGrrVrOW1C7xvmywOyHlJ+V8Wf44MUbjvmojU0OTOEZNV3O9rVx4vxaPCF9RGQtAIKnLQGFwDu+B7Fu37HuxL6gvkd1XQPI8cs8FZDcLMHrYLyr79+MjLZx6phPPL4ZsptOCAPS9ty/6EGSACf4ad27byWHL8iu9LpkWbalAnBSisZJPDcN82Q4AHewJ8k02fkS1B4MGybotpXsga3a+jQIDAQABAoIBAGpVJhBXcTmrs4IySW63sgK0Q0eWjCVtMpU+pV2dZL/VX8hDqzM2okWPUalmgbmuBwyhGrtCwu1F1f6uqJrfjYCBiyO5I+7e3F2Qye1ZgsUhvWKjX6YcHAoYO32CaOqudVqK9iQXBtIsXweRUBgzFv7fgcHF+ZGDvRbryIFhjkM9XIBtGmBT1gnLigVoUWQvuD7rXA6P/Jys29b3EK8UDTe1o0sJUreTNNAlGOLa2AefNvLDYt5fqmYjJ3U9sWJvB+UfHGO+I3EhMxvHWTgXptaZ2jH/0SDRnVKAtQwyTMG9w77NKs5jDaYKCFtsnSTR5zrI0h+mMGEeG0QK1W3Nom0CgYEA6kEWKWhpFXeroavqk1k06Obp0/UYUkHLbw5jmtz70TRUda6WSzv0sFEwqwn++52+eyMbeXRut0SgdgfDiZPLjtnLTmlNBI1WjDKglMVnfASFkEHyURpYT9YMHWmu6RYTzDcwUfyscmdTfFQ3fOWm2NpEZd89aexNSB8JPvXmzDsCgYEAyaiEs2T+FQw6d5EjZby9Fj8urUp1U4n0Ed1w65TVMnzZkOYZn8biR9N8tbCWy3ozqLf2ArcQjTH1+xyl+nVFbctbjngw/DeZXkS7S+OxjudI0ON/be6XOVajjI5Ugaxr+Q19Qx1fw1yMDqeRT6T5osJPCBekOUhnjyD6ycbVG9cCgYEArf173XOcoYJKK4HKcHkQsHBaesEPuID//dO9LZg3PXLVzLbJEMZOfus+77sz9WV7xnAUBwjw9xR07lXj6Xqp9cdUlz/lIZ1tDCLKXNWmgFnHbpdcyNp9f4bnZq1Jafyo5cSUEkFPQIX4X18Z+52DaIvtw5ClR9hoqknLD0WLkGMCgYEAmvVbw15/wDy9UNO+l5cI1eeHPrJQpfkEDBZVhzG/AiTeKnImjpiNmRPyaMthlMo6mBOEf2Gc3mLd2jCRenxS9aOmnzvMqIMw3zeBlTdKYb1oPtwSN693lR/2XTOhzGNqNN8gukoAJGchWMF67/Cdw2v8vwMrtrjkmx+Elziq2dECgYEA4ao+0YAriMbbYCRGvsf8fGIQbe0n0NC4sh4JiFmrsF9BjAWxdu/dYkp5OKFnoYhxyxFEisIQETXa/mD06M68htnQqSWgAlI3z7zUR3nFe6lhUbgwQj0aoUTrYEqr3i1MDvsGv+OdQWzERK/igyiP3p8sW/rPZpU8ztdtnKej3Ig="
        alipay_client_config.alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAg5StQ8OYhj2+Brg3y3KxiTVLXSLeN9rfliGoFleLALKfBuZ7cYcPozJP7ZT0HDJRBHt9I22Fw2ZzG5u1nRcm+mV/XnbtnEeFDmkpjSLtesfuR/Dm2za4D88v5PbbkvFfpKWXFKbI6ZstQybiDv990ssy36lKSoxbzfrgTeAc0PUscgAGKUijADsTq/2VUYgvuf6CF7B8E0fbhprRtGqETetmlb4F4XgwACM/DjchyoxTu3kRptSm2DIZTWS3klcc39LYw+c86OlQEZQiMOjb77XZNTbxtkmfALm2Q0+wYpSS8QKfMP16ux8bvZbVbjQQckxOEZKNvjV6dxSvxSa72wIDAQAB"
        alipay_client_config.sign_type = "RSA2"
        self.Connect = 0
        self.aliclient = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        self.alimodel = AlipayTradeAppPayModel()
        # self.ALi_SM_Orders = {}

        # self.PayCodeWithLen = {}
        # self.PayOrders = []

        self.Ali_Order = 1
        self.SolrInst = sinter.SolrInterface()

        #缓存长连接池 - 模式 - 用来处理，
        #*固定维护几个长连接，来处理一些非常频繁的业务
        # self.db_list = [DbHander.DBREAD(),DbHander.DBREAD(),DbHander.DBREAD(),DbHander.DBREAD(),DbHander.DBREAD()]
        # self.db_pair = 0
        # self.db = None
        # self.Cur = None
        # logging.info("Application Inited")
        #self.post_upload_data = {}
        #self.post_data_temp_post = {}
        # self.PhoneCodes = {}
        #self.LoginData = {"l":[],"f":0,"t":0,"f1":0,"t1":0}


        # self.Ali_Order = 1
        # self.SolrInst = sinter.SolrInterface()
        IC.ReadConfig()
        # self.AppData = {}
        self.acs_client = AcsClient(Global.ACCESS_KEY_ID, Global.ACCESS_KEY_SECRET, Global.REGION)
        region_provider.add_endpoint(Global.PRODUCT_NAME, Global.REGION, Global.DOMAIN)

        t = threading.Timer(1, self.CkDb)
        t.start()


    # def DBPing(self):
    #
    #     self.db = self.db_list[self.db_pair]
    #     self.db.ping(reconnect=True)
    #     self.Cur = self.db.cursor()
    #     self.db_pair += 1
    #     if self.db_pair > 4:
    #         self.db_pair = 0


    # def GetLoginData(self):
    #
    #     ck_sql = "select LOGIN_IP FROM tb_config_login;"
    #     #logging.info("loginConfig:[%s]" % ck_sql)
    #     self.DBPing()
    #     self.Cur.execute(ck_sql)
    #     self.db.commit()
    #     lines = self.Cur.fetchall()
    #     if lines and len(lines) > 0:
    #         for arr_info in lines:
    #             self.LoginData["l"].append(arr_info[0])
    #     logging.info("loginConfig:[%s]" % self.LoginData)
    #     #print("loginConfig:[%s]" % self.LoginData)


    # def ComputeLoginConfig(self):
    #     _logindata = self.LoginData
    #     l = _logindata["l"]
    #     if len(l) < 1:
    #         return ""
    #     f = _logindata["f"]
    #     _t1 = _logindata["t1"]
    #     _ip = l[f]
    #     f += 1
    #     if f >= len(l):
    #         f = 0
    #     _t = _logindata["t"]
    #     _n = time.time()
    #     f1 = _t1 - (_n-_t)
    #     _xs = 0.5       #登录排队时间
    #     if f1 < -_xs:
    #         f1 =  -_xs
    #
    #     _to = _xs + f1
    #
    #     _logindata["f"] = f
    #     _logindata["t1"] = _to
    #     _logindata["t"] = _n
    #     self.LoginData = _logindata
    #
    #    # logging.info("_logindata :" % _logindata)
    #
    #     # ck_sql = "update tb_config_login set LVS = LVS + 1 WHERE LOGIN_IP = '"+_ip+"';"
    #     # #self.DBPing()
    #     # self.Cur.execute(ck_sql)
    #     # self.db.commit()
    #
    #     return str(_ip) + "-" + str(_to)


    def CkDb(self):
        # Do something

        # ck_sql = "select ID,APPID,FLOW,PASSDATE,FLOW_USE,appCertificate from tb_cxsdk_users;"
        # self.DBPing()
        # self.Cur.execute(ck_sql)
        # self.db.commit()
        # lines = self.Cur.fetchall()
        # if lines and len(lines) > 0:
        #     for arr_info in lines:
        #
        #         APPID = arr_info[1]
        #         appandcertificate = hashlib.md5((APPID+arr_info[5]).encode()).hexdigest()
        #         #print(appandcertificate)
        #         if appandcertificate not in self.AppData:
        #             self.AppData[appandcertificate] = {
        #                 "ID":int(arr_info[0]),
        #                 "APPID": arr_info[1],
        #                 "FLOW":int(arr_info[2]),
        #                 "PASSDATE": arr_info[3],
        #                 "FLOW_USE": int(arr_info[4]),
        #                 "appCertificate":arr_info[5]
        #             }
        #         else:
        #             self.AppData[appandcertificate]["FLOW"] = int(arr_info[2])
        #             self.AppData[appandcertificate]["PASSDATE"] = arr_info[3]
        #             self.AppData[appandcertificate]["FLOW_USE"] = int(arr_info[4])
        #             self.AppData[appandcertificate]["appCertificate"] = arr_info[5]
        #
        # #print(self.AppData)
        # logging.info("AppData - Geted:[%s]" % self.LoginData)
        # if self.LoginData != None and self.LoginData != "" and len(self.LoginData["l"]) == 0:
        #     self.GetLoginData()
        self.DoEvent()
        t = threading.Timer(60,self.CkDb)
        t.start()


    def DoEvent(self):
        pass




App = Application(
    handlers = Urls,
    **Global.settings
    )