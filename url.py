#!/usr/bin/env python
# coding=utf-8
"""
the url structure of website
"""
from handlers.WechatKFZ.kfz_view import WechatLoginRequest, WechatLoginCallBackRequest
from handlers.index import IndexHandler, XfHandler  # 假设已经有了

from handlers.LogServer.cxlog import writeLogHandler,WriteUserHanhler
from handlers.MainDataInterface import post_plistINIHandler
from handlers.CommonDataInterface import PostInterfaceRequest, GetNowTimeHandler
from handlers.TestServer.GetResUrlData import PostResUrlRequest


from handlers.FeiQi.iot import IotHelloHandler
from handlers.FeiQi.iot import IotDeviceListHandler
from handlers.kbeServer.Editor.Interface.interface_agara import AgaraTorkenHandler
from handlers.kbeServer.Editor.Interface.interface_agara import AgaraAppIPHandler
from handlers.solrServer.solrmain import SolrRequest
from handlers.payServer.paymain import PayOrder
from handlers.payServer.paymain import AliPayCallBack
from handlers.payServer.paymain import WechatPayCallBack
from handlers.smsServer.SmsInterface import SmsRequest
from handlers.smsServer.SmsInterface import SmsPayRequest,SendSmsRequest
from handlers.kbeServer.Editor.response.response_sis import TSisRequest,AccountApkHandler, ApkInfoHandler
from handlers.kbeServer.Editor.Evaluate.evaluate_course import EvaluateHandler
from handlers.huaweiServer.ISV.isvrequest import ISVHandler
from tornado.web import StaticFileHandler
from handlers.SyncServer.sockect import EchoWebSocket
import Global
from handlers.wechatGZH.wxhandler import getSignHandler,pageHandler,wechatShareHandler

#统一用户体系
#http://192.168.0.9:9001/pget/pdata?appid=fd17cb08-1824-11eb-a7df-408d5cf8276a&username=lyy&gpid=5&guid=24&gtype=0

#无用户体系
#http://192.168.0.9:9001/sget/pdata?appid=fd17cb08-1824-11eb-a7df-408d5cf8276a&gpid=5&guid=24&gtype=0

Urls = [
    ('/', IndexHandler),

    # 给前端返回当前时间戳
    ('/getnowtime', GetNowTimeHandler),

    #物联网
    ('/iot',IotHelloHandler),
    ('/v1/instruction/devices',IotDeviceListHandler),
    #声网
    ('/agaratorken',AgaraTorkenHandler),
    ('/agaraapp',AgaraAppIPHandler),

    #solr索引库
    ('/solr',SolrRequest),

    #支付接口
    ('/payorder',PayOrder),
    ('/alipaycallback',AliPayCallBack),
    ('/wechatpaycallback',WechatPayCallBack),
    ('/smspay',SmsPayRequest),#SmsPayRequest),
    #SIS接口
    ('/sisyz',TSisRequest),

    #短信业务
    ('/sms',SmsRequest),
    ('/smsrequest', SendSmsRequest),
    #('/alipay',Ali_PayHandler),
    #('/alipaybck',Ali_PayBckHandler),
    #('/wechatpaybck',Wechat_PayBckHandler),

    #

    #('/monthpay',AppPay_Monthly),
    #('/monthpaybck',Ali_MonthPayBckHandler),
    #('/wxmonthpaybck',Wechat_MonthPayBckHandler),

    #('/smpay',CxNative_Pay),
    #('/smwechatpaybck',CxNative_WechatPayBck),
    #('/smalipaybck',CxNative_AliPayBck),



    #('/test',TEstRequest),

    #====以下url-需要用户接入是 跟 编程有统一账号体系，并且 账号是作为参数传入
    # ('/pget/plist', plistHandler),          #自由工程列表获取                       pam: appid(SDK的appid) username(获取数据的用户名)
    # ('/pget/plist/ini', plistINIHandler),          #自由工程列表获取                       pam: appid(SDK的appid) username(获取数据的用户名)
    # ('/pget/clist', clistHandler),          #标准课程列表获取                       pam: appid(SDK的appid) username(获取数据的用户名)
    # ('/pget/wlist', wlistHandler),          #共享作品列表获取                       pam: appid(SDK的appid) username(获取数据的用户名)
    # #('/pget/pcheck', pcheckHandler),        #获取工程版本号(用来给客户端一个标记)   pam: appid(SDK的appid) username(获取数据的用户名)  gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/sget/lcheck', pcheckHandler),        #获取工程版本号(用来给客户端一个标记)   pam: appid(SDK的appid) username(获取数据的用户名)  gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/pget/pdata', pdataHandler),          #获取工程数据(json)                     pam: appid(SDK的appid) username(获取数据的用户名)  gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # #('/pget/pdata/ini', pdataIniHandler),   #获取工程数据(ini)                      pam: appid(SDK的appid) username(获取数据的用户名)  gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/sget/pdata/ini', pdataIniHandler),          #获取工程数据(json)                     pam: appid(SDK的appid) username(获取数据的用户名)  gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/pget/lcheck', lcheckHandler),        #获取课时版本号(用来给客户端一个标记)   pam: appid(SDK的appid) username(获取数据的用户名)  gcid(课程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/pget/ldata', ldataHandler),          #获课时数据                             pam: appid(SDK的appid) username(获取数据的用户名)  gcid(课程ID) guid(工程作者UID) gtype(0-本地 1-市场)


    #***===未来教室读取编程===***(未来教室-专用) *-无需编程账号读取
    # ('/sdk/noc/clist', s_clistHandler),         #课程市场获取                           pam: appid(SDK的appid)
    # ('/sdk/noc/wlist', s_wlistHandler),         #课程市场获取                           pam: appid(SDK的appid)
    # ('/sdk/noc/pcheck',s_pcheckHandler),        #获取工程版本号(用来给客户端一个标记)   pam: appid(SDK的appid) gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/sdk/noc/pdata', s_pdataHandler),         #获取工程数据                           pam: appid(SDK的appid) gpid(工程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/sdk/noc/lcheck', s_lcheckHandler),       #获取课时版本号(用来给客户端一个标记)   pam: appid(SDK的appid) gcid(课程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ('/sdk/noc/ldata', s_ldataHandler),         #获课时数据                             pam: appid(SDK的appid) gcid(课程ID) guid(工程作者UID) gtype(0-本地 1-市场)
    # ***===未来教室读取编程===***(未来教室-专用) *-无需编程账号读取


    #***===SIS读取编程===***(SIS教学管理系统-专用) *-通过编程账号读取
    #('/sdk/hasc/plist', GetPDataHasCHandler),  #获工程数据
    #('/sdk/hasc/clist', clistHandler),         #获课程数据
    #***===SIS读取编程===***(SIS教学管理系统-专用) *-通过编程账号读取


    #***===编程数据读写===***(XRCREATEX编程/XR云课堂)
    ('/xrcreatex/post', post_plistINIHandler),          #PC端     课程、工程相关数据获取
    ('/xrcode/post',    post_plistINIHandler),          #VR/APP端 课程、工程相关数据获取
    ('/cxlog/com', writeLogHandler),                    #编程写入日志
    ('/postinterface',PostInterfaceRequest),            #编程通用接口 POST
    ('/mail/read', post_plistINIHandler),               #邮件请求
    ('/xf', XfHandler),                                 #测试
    ('/resurl', PostResUrlRequest),                     #测试
    ('/xreditor/post', PostInterfaceRequest),           #内容制作时序版

    #***===编程数据读写===***(XRCREATEX编程/XR云课堂)

    # ***===get请求
    ('/getpackagename', AccountApkHandler),                     #软件包名请求
    # ***===get请求

    #微信登录
    ('/wechatkfz/login', WechatLoginRequest),                       #微信登录
    ('/wechatkfz/codeget', WechatLoginCallBackRequest),                     #软件回调


    # ========智能评价==========
    ('/getevalute', EvaluateHandler),                   # 获取课程智能评价


    # ======华为云市场=======
    ('/isv', ISVHandler),                   #
    # ('/isvxufei', XufeiHandler),                   #
    # ('/isvdongjie', DongjieHandler),                   #
    # ('/isvshifang', ShifangHandler)
    (r"/(auth_file\.txt)", StaticFileHandler, dict(path=Global.settings['static_path'])),   # 华为认证
    (r"/(MP_verify_q4URwV9WSW1LX34p\.txt)", StaticFileHandler, dict(path=Global.settings['static_path'])),   # 微信认证

    # websocket
    ('/socket', EchoWebSocket),


    #微信分享
    ('/wx/sign', getSignHandler),
    ('/wx/share', wechatShareHandler),
    ('/wx/page(.*)', pageHandler),

    # apk 相关
    ("/apkinfo", ApkInfoHandler),

]