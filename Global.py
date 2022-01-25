#!/usr/bin/env python
# coding=utf-8
import os

from methods.languageinterface import InterfaceLanguage

TLMaxNum = 5        #时间收益体力最大数
TLTimeLong = 600    #体力倒计时
COOKIES_TLONG = 600  #cookie有效时间

WechatAppId = "wx249be41a361e73fe"
Wechatsecret = "1a2d557e5a6337f39d0496262f2ed123"
WechatLoginUrl = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code"
WechatDYUrl = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={0}"
WechatAccessToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
WechatKFMsgUrl = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}"
SendSizeOne = 1024

# SolrUrl = "192.168.0.9:8099"    #索引库日志
#PAY_URL = "192.168.0.9:8001"    #支付服务

#声网配置
Agara_appID = "e5c17c18d29a4e3b8874ee3437f7f7d0"
Agara_appCertificate = "d5c537ba7e6e4509b196a59586d72861"

#扫码支付(XR CREATEX产品)-支付宝
ALI_CX_APPID = "2021001135621953"
ALI_CX_APP_PRIVATEKET = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCrdstbRePVChsvCkmck4HTpyFDBj7Xz/ZEh3uZikgtAKY1NCJA17h9nJ8tQZ7yJ9xuNE/fYl1+ry7src1XHebJQIwmFmoZNx/8KVjNDCq9mESmGwnjUjIaHSgedoIw4ktnwvUEcUkeU9KBuTFCZ6llC9XvakfAm0NiA3+xG2BcJSAgyQxT8qt/AM0h+WXPbPefIa/f4RVSOW72lyXRjxSKoOoWoXgQmNOo2yFZVpGSiOmNgOdF6i+FWZ0ZVonBTII/fvd4wyAnwFjpts/HgB5liEmfQJT7LADbHOFeZVAYTUDk43GaLQwNHWO+kuiXfl+ZxGEJ5OY1qIzJ0aXhY2ERAgMBAAECggEACK+j7aPEvu4cIm3q/LucQBSfYr3WQSiP2Tjj0gtnTKBTyy4w7gf/mJ1ukuRYIPxT9mFACpj5E4ncXrEPTfJ91oQmlWddSJm6TRPrI7gSEji8gY2tGo73ass/VQu73K4aE8+Uif0TLy4f4+J11F9b/Xp0BATmTaOP7k8vENHKN+C0FCgrUJD/Bf/orx33zdFzIdgwvdHbiQpgyJy1LkuVNYHGziHCljZxGMFC/FsA6zhpqr4Xrv/Lj+k1q/jQ3a6uik+MMBUxVl77lykd5sWVvVzgKxZ27OUe+Nt5DJMtHpzD4l+ViExjjUUvrqJkhjx4Ho8QhTbm9HQ6Frtq1aRC4QKBgQD281u1S6I63l8UA8Y6tvKvkZabCp+5erRcxc51MiX5VvomVieCyjzIt7XERt/e88vT15AYadTPlNwtfM3DAPr53tFEiIbSqYrXQwmp1C38JrfgmD2C8Qru954jPQhlawRa1RkPIOpG7tZalP8nEl/Na5eMnZj280D3opxQcmTA/wKBgQCxv0wR4vhCcJkwP51aTW582XhgPooLbPZvG2MTtPEp7CxK2ldbrUwOtILWx1xh8oeoSCgjmEStEgy8UgKLB+j03qq6/HdpmBe+3TbvrLqnQu411IjGhc66cwlkEGG4kp03jfsf3G2nYXWJLR5Ou/Gqnx/yUdDbQsaxTQeQkjnN7wKBgFh7le59rSEesD6Bo7NB/e6+YZIn2lchCiL7lSAU2dpfOb4mvH12bRUWDgDHzEscW3oKEM1OjjvagJGj2C342fRRy/WcXYJ50Q+UK5A4QEnKrbPBmLikGWDKRFUn9ywvjh3loNb02jyUMyW9oTaktMLrvB9cEITbX/nav9trQYKNAoGBAIR7L6iZQi7LG/KRR6f51KMruAQMOPnhIiCYChWzJJj5ld3ItZn4JZtEQczx1NKQYTo1Ze153Z4duO5YNdsIb0KsABbUe/BxUymIWhzz4j8urLvkiHlnXDkt6s7xQtS+On4gzg7mTbiW9HLk9RT8Elj4t2f2QTRbphqabkv8ISdzAoGBALuoME5+24Dc4KnksJ5Sy1Uj7CODoJUmPTmPvUPOCMOuaOZ1evhPbLdXxtr9aLv0Lv+tW1C/P/j1xjG69XmLDnb/Md9Ffpv47NQsI49bus/MknvPC81Z5dxOqVmhI39xR2vqjHf/KU5zvQdD8sdnq+w6teX6StDK6dfPqAujGwNf"
ALI_CX_PUBLICKEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtKELXc/hi0KBpH1ZhkF+mMuuWSJ9mFeB4T7QV1vLFGXYHCEaIc2btEYC7PAFG4UHznpFAhMwt4FOZDTa7BvMUCCOJT9jtJcY/OCI+cE1ucVR/nFFBTkt5gRN9JnDPzs5W3gyJMPiLhJ5Ap8Bp6M08Uv740XYb9vDyltrouwlBOIklvPdEwK/h5TCzRC6izLdqXo3quiC82E7ojqxmjvK1EaVWvFHPL3PSkrddT8O+fdDKXvwP9MUvQ30yKVWeYPbRKlPbxVE/78AJ82R3IJKHon5OmCO65EMvhN2/3YPIJg1RzJZHORsXxEy35ni5GWBMnx3lLh3Oqlk9JSOedt6mwIDAQAB"

#支付回调
# SAOMA_PAYBACK = "http://29w1v17148.qicp.vip"


settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    xsrf_cookies = False,
    login_url = '/',
    log_file=os.path.dirname(__file__)+"/tornado.log",
    )

#短信业务
ACCESS_KEY_ID = "LTAIMHlVisHZlKlU"
ACCESS_KEY_SECRET = "SrOjABIzMpOadT64RPOoaPA13N30V4"
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

COURSE_BUY_SIS_TIMELONG = 2592000
COURSE_BUY_CX_TIMELONG = 2592000
WORK_BUY_XR_TIMELONG = 2592000

#华为ISV
Global_IsvKey = "827d93f9-2e75-4842-a142-8813f31aaef9"  #"butflyvr"


class get_config():
    def __init__(self, env) -> None:
        self.env = env

    # createx 数据库
    def mysql_options(self) -> dict:
        mysql_option = {
            "test": dict(
                host="192.168.0.9",
                database="createx_kbe",
                user="root",
                password="root"
            ),
            "dev": dict(
                host="124.70.99.244",
                database="createx_kbe_test",
                user="fdroot",
                password="3dbutfly@hwmysql1"
            ),
            "pro": dict(
                host="192.168.0.13",
                database="createx_kbe_1",
                user="fdroot",
                password="3dbutfly@hwmysql1"
            )
        }
        return mysql_option[self.env]

    # SIS 数据库
    def mysqlSIS_options(self) -> dict:
        mysqlSIS_option = {
            "test": dict(
                host="192.168.0.128",
                database="cyycore",
                user="root",
                password="root"
            ),
            "dev": dict(
                host="rm-2zetnymy903bydowxzo.mysql.rds.aliyuncs.com",
                database="elevacoree",
                user="fdroot",
                password="Qaz@butfly12mysql"
            ),
            "pro": dict(
                host="rm-2zetnymy903bydowxzo.mysql.rds.aliyuncs.com",
                database="elevacoree",
                user="fdroot",
                password="Qaz@butfly12mysql"
            ),
        }
        return mysqlSIS_option[self.env]

    # redis 配置
    def redis_config(self):
        redis_dict = {
            "test": ["192.168.0.22:9001"],
            "dev": ["192.168.0.9:9001"],
            "pro": ["120.46.140.42:9101", "120.46.140.42:9102", "114.116.232.87:9101", "114.116.232.87:9102"]
        }
        print(redis_dict[self.env])
        return redis_dict[self.env]

    # redis 数据库
    def redis_options(self, database):
        redis_option = {
            "test": dict(
                host="192.168.0.9",
                port="6379",
                db=database,
                password="123123"
            ),
            "dev": dict(
                host="123.57.163.216",
                port="6379",
                db=database,
                password="123123"
            ),
            "pro": dict(
                host="120.46.155.36",
                port="8080",
                db=database,
                password="3dbutfly@hwredis1"
            )
        }
        return redis_option[self.env]

    # 索引库配置
    def solr_config(self):
        solr_url = {
            "test": "192.168.0.9:8099",
            "dev": "39.106.172.139:8099",
            "pro": "124.70.72.60:8099"
        }
        return solr_url[self.env]

    # 支付回调地址
    def pay_config(self):
        pay = {
            "test": "http://29w1v17148.qicp.vip",
            "dev": "http://www.mrbutfly.com:9001",
            "pro": "http://120.46.140.42:9002"
        }
        return pay[self.env]

ENV = "test"
get_config = get_config(ENV)

# 数据库配置参数
# mysql_options = dict(
#     host="192.168.0.9",
#     database="createx_kbe",
#     user="root",
#     password="root"
# )

# mysql_options = dict(
#     host="124.70.99.244",
#     database="createx_kbe_test",
#     user="fdroot",
#     password="3dbutfly@hwmysql1"
# )


# SIS数据库
# mysqlSIS_options = dict(
#     host="192.168.0.128",
#     database="cyycore",
#     user="root",
#     password="root"
# )



JSON_Bck = {
            "Code":0,
            "Msg":"",
            "Data":""
        }

Verify_Msg = {
    "-11":"APPID 参数异常",
    "-12":"APPID 未申请",
    "-13":"APPID 已到期",
    "-14":"流量已用完",
    "-21":"账号不存在",
    "-22":"账号到期",
    "-23":"账号异常，怀疑不是自己操作",
    "-24":"参数异常"
}

def GetObjTableName(uid,pid):
    return "tb_obj_"+str(uid)+"_"+str(pid)

def GetMObjTableName(uid,pid):
    return "tb_mobj_"+str(uid)+"_"+str(pid)

def GetExtraTableName(uid,pid):
    return "tb_extra_"+str(uid)+"_"+str(pid)

def GetMExtraTableName(uid,pid):
    return "tb_mextra_"+str(uid)+"_"+str(pid)

def GetLessonTableName(uid,pid):
    return "tb_lesson_"+str(uid)+"_"+str(pid)

def GetMLessonTableName(uid,pid):
    return "tb_mlesson_"+str(uid)+"_"+str(pid)

def GetWorkLogTableName(uid,pid):
    return "tb_work_log_"+str(uid)+"_"+str(pid)

def GetCourseLogTableName(uid,pid,lid):
    return "tb_course_log_"+str(uid)+"_"+str(pid)+"_"+str(lid)

def GetSisLogTableName(cid):
    return "tb_sis_log_"+cid

def GetWorkZanTableName(uid,pid):
    return "tb_work_zan_"+str(uid)+"_"+str(pid)

def GetCourseZanTableName(uid,pid,lid):
    return "tb_course_zan_"+str(uid)+"_"+str(pid)+"_"+str(lid)

def GetSisZanTableName(cid):
    return "tb_sis_zan_"+cid


def GetXRObjTableName(uid,pid):
    return "tb_xr_obj_"+str(uid)+"_"+str(pid)

def GetMXRObjTableName(uid,pid):
    return "tb_xr_mobj_"+str(uid)+"_"+str(pid)

#redis参数 -2021-11-19
RedisCreatex_options = dict(
    host="192.168.0.9",
    port="6379",
    database=1,
    password="123123"
)

#用来表示 服务类型 0-本地测试 1-外网正式 2-外网测试
Global_ServerRT = 0


LanguageInst = InterfaceLanguage()