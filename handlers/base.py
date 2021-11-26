#! /usr/bin/env python
# coding=utf-8

import tornado.web
import json
import time
import logging
import Global
import copy
import base64,hashlib,hmac
from methods.db_mysql import DbHander
import random,string

class BaseHandler(tornado.web.RequestHandler):

    #  允许跨域访问的地址
    def allowMyOrigin(self):
        allow_list = [
            #'http://127.0.0.1:7100',
            'http://localhost',
        ]

        print("self.request.headers = " , self.request.headers)

        if 'Origin' in self.request.headers:
            Origin = self.request.headers['Origin']
            print("Origin = ", Origin)
            # 域名
            #if Origin in allow_list:
             #   print("Origin1 = ", Origin)
            # self.set_header("Access-Control-Allow-Origin", Origin)  # 这个地方可以写域名也可以是*
            # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


            # 新header
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.set_header("Access-Control-Allow-Headers", "Accept, X-Access-Token, X-Application-Name, X-Request-Sent-Time, Content-Type")
            self.set_header("Access-Control-Expose-Headers", "Content-Type")
            self.set_header("Access-Control-Allow-Origin", "*")


            # re_ret = re.match(r".{1,}\.(xixi.com|haha.com)", Origin)
            # # 内网和本地
            # re_ret2 = re.match(r"^(192.168.1.*|127.0.0.1.*|192.168.0.*)", Origin)
            # if re_ret or re_ret2 or Origin in allow_list:
            #     self.set_header("Access-Control-Allow-Origin", Origin)  # 这个地方可以写域名也可以是*
            #     self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            #     self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def __init__(self, application, request, **kwargs):

        tornado.web.RequestHandler.__init__(self,application, request, **kwargs)
        self.AppID = ""
        self.UserName = ""
        self.SoftType = ""
        self.JData = None
        self.SolrData = None
        #self.post_data_temp = []
        self.OnePageNum = 2
        self.return_data = {
            "code": 200,
            "msg": "",
            "data": ""
        }

    def get_current_user(self):
        return self.get_secure_cookie("user")

    #自定义日志格式
    # def _request_summary(self):
    #     if self.request.method == 'post':
    #         return "%s %s (%s@%s)" % (self.request.method, self.request.uri,
    #                                   self._operator_name, self.request.remote_ip)
    #
    #     return "%s %s %s(%s@%s)" % (self.request.method, self.request.uri, self.request.body.decode(),
    #                                 self._operator_name, self.request.remote_ip)
    # def post_data_temp_init(self,uid):
    #     if uid in self.application.post_data_temp_post:
    #         del self.application.post_data_temp_post[uid]
    #
    # def post_data_temp_get(self,uid):
    #     if uid in self.application.post_data_temp_post:
    #         #logging.info("uid:" + str(self.application.post_data_temp_post[uid]))
    #         return self.application.post_data_temp_post[uid]
    #     return []
    #
    # def post_data_temp_set(self,uid,data):
    #
    #      _arr = []
    #      if len(data) < 1:
    #          self.application.post_data_temp_post[uid] = [""]
    #      else:
    #          _cdata = data
    #          #logging.info("uid:"+ str(uid))
    #          #logging.info("_cdata1:" + str(len(_cdata)))
    #          while len(_cdata) > Global.SendSizeOne:
    #              _rdata = _cdata[0:Global.SendSizeOne]
    #              #print("_rdata:", _rdata,_cdata)
    #              _arr.append(_rdata)
    #              _cdata = _cdata[Global.SendSizeOne:len(_cdata)]
    #              #logging.info("_cdata2:"+ str(len(_rdata)))
    #          if len(_cdata) > 0:
    #              _arr.append(_cdata)
    #          #logging.info("_arr:"+str(len(_arr)))
    #          self.application.post_data_temp_post[uid] = _arr

    def SetPhoneCode(self, DB, phone, code):
        sql = "select phonecode, phonecodedate from tb_register_user where username = %s"
        data = DB.fetchone(sql, phone)
        if data:
            sql_1 = "update tb_register_user set phonecode = %s, phonecodedate = %s where username = %s"
        else:
            sql_1 = "insert into tb_register_user (phonecode, phonecodedate, username) values (%s, %s, %s)"
        DB.edit(sql_1, (code, str(int(time.time())), phone))
        logging.info("username: %s, code: %s" % (str(phone), str(code)))

    def GetPhoneCode(self, DB, username):
        logging.info("GetPhoneCode: %s" % str(username))
        sql = "select phonecode,phonecodedate from tb_register_user where username = %s"
        data = DB.fetchone(sql, username)
        if data:
            Code = data[0]
            date = int(data[1])
            if int(time.time()) - date > 60:
                return "-99"
            return Code
        return ""


    # def post_upload_temp_init(self,uid):
    #     self.application.post_upload_data[uid] = ""
    #
    #
    # def post_upload_temp_get(self,uid):
    #     if uid in self.application.post_upload_data:
    #         return self.application.post_upload_data[uid]
    #     return ""
    #
    # def post_upload_temp_set(self,uid,data):
    #
    #     # _arr = []
    #     # if uid in self.application.post_data_temp_post:
    #     #     _arr = self.application.post_data_temp_post[uid]
    #     # _arr.append(data)
    #     self.application.post_upload_data[uid] += data

    # @property
    # def LOGINCGET(self):
    #
    #     return self.application.ComputeLoginConfig()

    @property
    def SOLR_VERIFY(self):
        logging.info("SOLR_VERIFY -> PayData[%s]" % self.request.body)
        # print("self.request.body,",self.request.body)
        self.SolrData = json.loads(self.request.body.decode('utf-8'))

    # def SetPayOrders(self,order ):
    #
    #     dcl = self.application.PayOrders
    #     dcl.append(order)

    # def GetPayOrders(self,order):
    #
    #     if order not in self.application.PayOrders:
    #         return 0
    #     return 1

    # def SetPCodeLen(self,Code , len):
    #
    #     dcl = self.application.PayCodeWithLen
    #     dcl[Code] = len

    # def GetPCodeLen(self,Code):
    #
    #     if Code not in self.application.PayCodeWithLen.keys():
    #         return 0
    #     return self.application.PayCodeWithLen[Code]

    @property
    def Ali_Order(self):
        return self.application.Ali_Order

    @property
    def SolrInst(self):
        return self.application.SolrInst

    @property
    def IsConnect(self):
        return self.application.Connect

    # def RecodeOrder_ALI(self, DD, ORDER):
    #
    #     # if DD not in self.application.ALi_SM_Orders.keys():
    #     #     self.application.ALi_SM_Orders[]
    #     # else:
    #     #     self.application.ALi_SM_Orders[DD] = ORDER
    #     self.application.ALi_SM_Orders[DD] = ORDER

    def GetOrder_ALI(self, DD):

        pass
        # if DD not in self.application.ALi_SM_Orders.keys():
        #     return ""
        # else:
        #     _order = self.application.ALi_SM_Orders[DD]
        #     del self.application.ALi_SM_Orders[DD]
        #     return _order

    # def SetPhoneCode(self, phone, code):
    #
    #     self.application.PhoneCodes[phone] = [code, int(time.time())]
    #
    # def GetPhoneCode(self, phone):
    #
    #     if phone not in self.application.PhoneCodes.keys():
    #         return ""
    #     arr = self.application.PhoneCodes[phone]
    #     Code = arr[0]
    #     date = arr[1]
    #     if int(time.time()) - date > 60:
    #         return "-99"
    #     return Code

    @property
    def ali_model(self):
        return self.application.alimodel

    @property
    def wechat_client(self):
        return self.application.wechatclient

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def ali_client(self):
        return self.application.aliclient


    @property
    def ali_client(self):
        return self.application.aliclient

    @property
    def ali_model(self):
        return self.application.alimodel

    @property
    def wechat_client(self):
        return self.application.wechatclient

    @property
    def db_ping(self):
        """作为RequestHandler对象的db属性"""
        self.application.DBPing()

    @property
    def Cur(self):
        return self.application.Cur


    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db


    @property
    def Ali_Order(self):
        return self.application.Ali_Order

    @property
    def SolrInst(self):
        return self.application.SolrInst

    @property
    def App_ID(self):
        return self.get_argument("appid")

    @property
    def USERNAME(self):
        return self.get_argument("username")

    @property
    def VERIFY_SMAIN(self):

        _appid = self.App_ID
        cxsdk_appid = self.get_cookie("cxsdk_appid")
        cxsdk_pdate = self.get_cookie("cxsdk_pdate")
        if cxsdk_pdate != None:
            cxsdk_pdate = int(cxsdk_pdate)
        if cxsdk_appid != None and cxsdk_pdate != None:
            #logging.info("Get cxsdk_appid:%s cxsdk_pdate:%i " % (cxsdk_appid, cxsdk_pdate))
            if cxsdk_appid == _appid:
                if int(time.time()) - cxsdk_pdate < Global.COOKIES_TLONG:
                    #logging.info("Cookieing Bcked")
                    return 1

        _UID = self.VERIFY(0)
        #logging.info("Cookieed Computeing")
        if _UID <= 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = _UID
            JSON_Bck["Msg"] = Global.Verify_Msg[str(_UID)]
            self.write(JSON_Bck)
        else:
            #logging.info("Set - cxsdk_appid:%s cxsdk_pdate:%i " % (_appid, int(time.time())))
            self.set_cookie("cxsdk_appid", _appid)
            self.set_cookie("cxsdk_pdate", str(int(time.time())))
        return _UID

    @property
    def VERIFY_MAIN(self):

        _username = self.USERNAME

        cxsdk_username = self.get_cookie("cxsdk_username")
        cxsdk_pdate = self.get_cookie("cxsdk_pdate")
        cxsdk_uid = self.get_cookie("cxsdk_uid")
        if cxsdk_pdate != None:
            cxsdk_pdate = int(cxsdk_pdate)
        if cxsdk_uid != None:
            cxsdk_uid = int(cxsdk_uid)
        if cxsdk_username != None and cxsdk_pdate != None and cxsdk_uid != None and cxsdk_uid != 0:
            #logging.info("Get cxsdk_username:%s cxsdk_pdate:%i cxsdk_uid:%i" % (cxsdk_username, cxsdk_pdate, cxsdk_uid))
            if cxsdk_username == _username:
                if int(time.time()) - cxsdk_pdate  < Global.COOKIES_TLONG:
                    #logging.info( "Cookieing Bcked")
                    return cxsdk_uid

        _UID = self.VERIFY(1)
        #logging.info("Cookieed Computeing")
        if _UID <= 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = _UID
            JSON_Bck["Msg"] = Global.Verify_Msg[str(_UID)]
            self.write(JSON_Bck)
        else:
            #logging.info("Set - cxsdk_username:%s cxsdk_pdate:%i cxsdk_uid:%i" % (_username, int(time.time()), _UID))
            self.set_cookie("cxsdk_username",_username)
            self.set_cookie("cxsdk_pdate", str(int(time.time())))
            self.set_cookie("cxsdk_uid", str(_UID))
        return _UID

    def VERIFY(self,type):

        if type == 2:
            APPID = self.AppID
        elif type == 3:
            APPID = self.AppID
        else:
            APPID = self.App_ID
        print("APPID:",APPID)
        if APPID == "" or len(APPID) < 1:
            return -11 #APPID 参数异常
        # appdata = self.application.AppData
        # if APPID not in appdata:
        #     return -12  # APPID 未申请，请联系管理员
        # data = appdata[APPID]
        # #验证下APPIP是否到期了
        # timeStamp = int(data["PASSDATE"].timestamp())
        # print(timeStamp)
        # if timeStamp < time.time():
        #     return -13  # APPID 已到期 请联系管理
        # if data["FLOW_USE"] >= data["FLOW"] and data["FLOW"] != -1:
        #     return -14  # 流量已用完

        if type == 0 or type == 3:
            return 1
        else:
            return self.VerifyIdentity(type)


    def VerifyIdentity(self,type):

        if type == 2:
            username = self.UserName
        else:
            username = self.USERNAME
        sql_str = "select T1.UID,T1.ENDDATE from tb_userdata AS T1 INNER JOIN kbe_accountinfos as T2 ON T1.USERNAME = T2.AccountName AND T1.UserName = '"+username+"';"

        #print("sql_str",sql_str)
        #self.db_ping
        db = DbHander.DBREAD()
        Cur = db.cursor()
        Cur.execute(sql_str)
        db.commit()
        _uid = 0
        _enddate = 0
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _uid = int(data[0])
            _enddate = int(data[1])
        db.close()
        if _uid == 0:
            return -21 #账号不存在
        if _enddate != 1 and _enddate < time.time():
            return -22  #账号到期
        # if password != _password:
        #     return -23  #账号异常，怀疑不是自己操作
        #logging.info("UID : %i" % _uid)
        return _uid  #成功

    @property
    def POST_VERIFY_MAIN(self):

        #print("asdasdasd")
        print("POST_VERIFY_MAIN -> self.request.body[%s]" % self.request.body)
        pdata = self.request.body.decode('utf-8')

        logging.info("POST_VERIFY_MAIN -> pdata[%s],Type[%s]" % (pdata,type(pdata)))
        #print("pdata",pdata,type(pdata))
        #logging.info("pdata:"+ pdata)
        if isinstance(pdata,str):
            # if "\x00" in pdata:
            #     pdata = pdata.replace("\x00", "")
            #     string_pdata = "\"pdata\":"
            #     pdata = pdata + "\"}"
            # logging.info("POST_VERIFY_MAIN1 -> pdata[%s]" % pdata)
            post_data = json.loads(pdata,strict=False)
        elif isinstance(pdata,dict):
            post_data = pdata
        else:
            post_data = pdata

        print("post_data", post_data, post_data["appid"], post_data["username"])
        if post_data == None or 'appid' not in post_data.keys():
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = -24
            JSON_Bck["Msg"] = Global.Verify_Msg[str(-24)]
            self.write(JSON_Bck)
            return 0
        self.UserName = post_data["username"]
        self.AppID = post_data["appid"]
        self.JData = post_data["pdata"]
        self.SoftType = post_data["softfrom"]

        cxsdk_username = self.get_cookie("cxsdk_username")
        cxsdk_pdate = self.get_cookie("cxsdk_pdate")
        cxsdk_uid = self.get_cookie("cxsdk_uid")
        if cxsdk_pdate != None:
            cxsdk_pdate = int(cxsdk_pdate)
        if cxsdk_uid != None:
            cxsdk_uid = int(cxsdk_uid)
        if cxsdk_username != None and cxsdk_pdate != None and cxsdk_uid != None and cxsdk_uid != 0:
            #logging.info("Get cxsdk_username:%s cxsdk_pdate:%i cxsdk_uid:%i" % (cxsdk_username, cxsdk_pdate, cxsdk_uid))
            if cxsdk_username == self.UserName:
                if int(time.time()) - cxsdk_pdate < Global.COOKIES_TLONG:
                    #logging.info("Cookieing Bcked")
                    return cxsdk_uid

        #无账号接口过来不验证账号
        if post_data["softfrom"] == "WLJS":
            return 1

        _UID = self.VERIFY(2)
        #logging.info("Cookieed Computeing")
        if _UID <= 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = _UID
            JSON_Bck["Msg"] = Global.Verify_Msg[str(_UID)]
            self.write(JSON_Bck)
        else:
            #logging.info("Set - cxsdk_username:%s cxsdk_pdate:%i cxsdk_uid:%i" % (self.UserName, int(time.time()), _UID))
            self.set_cookie("cxsdk_username", self.UserName)
            self.set_cookie("cxsdk_pdate", str(int(time.time())))
            self.set_cookie("cxsdk_uid", str(_UID))
        return _UID

    @property
    def POSTNOACCOUNT_VERIFY_MAIN(self):

        post_data = json.loads(self.request.body.decode('utf-8'))
        print("post_data", post_data, post_data["appid"])
        if post_data == None or 'appid' not in post_data.keys():
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = -24
            JSON_Bck["Msg"] = Global.Verify_Msg[str(-24)]
            self.write(JSON_Bck)
            return 0
        self.AppID = post_data["appid"]
        self.JData = post_data["pdata"]
        _appid = self.AppID
        cxsdk_appid = self.get_cookie("cxsdk_appid")
        cxsdk_pdate = self.get_cookie("cxsdk_pdate")
        if cxsdk_pdate != None:
            cxsdk_pdate = int(cxsdk_pdate)
        if cxsdk_appid != None and cxsdk_pdate != None:
            #logging.info("Get cxsdk_appid:%s cxsdk_pdate:%i " % (cxsdk_appid, cxsdk_pdate))
            if cxsdk_appid == _appid:
                if int(time.time()) - cxsdk_pdate < Global.COOKIES_TLONG:
                    #logging.info("Cookieing Bcked")
                    return 1
        _UID = self.VERIFY(3)
        #logging.info("Cookieed Computeing")
        if _UID <= 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Bck["Code"] = _UID
            JSON_Bck["Msg"] = Global.Verify_Msg[str(_UID)]
            self.write(JSON_Bck)
        else:
            #logging.info("Set - cxsdk_appid:%s cxsdk_pdate:%i " % (_appid, int(time.time())))
            self.set_cookie("cxsdk_appid", _appid)
            self.set_cookie("cxsdk_pdate", str(int(time.time())))
        return _UID

    @property
    def SOLR_VERIFY(self):

        # print("self.request.body,",self.request.body)
        logging.info("SOLR_VERIFY -> pdata[%s]" % self.request.body)
        self.SolrData = json.loads(self.request.body.decode('utf-8'))

    @property
    def ISV_TorkenCheck(self):

        json_pam = {}
        params = self.request.arguments
        timeStamp = self.get_argument("timeStamp", "")
        authToken = self.get_argument("authToken", "")
        #print("params = ", params)
        #print("timeStamp = ", timeStamp, " authToken = ", authToken)
        # 参数排序
        #urlencode = False
        buff = []
        slist = sorted(params)
        for k in slist:
            if k == "authToken":
                continue
            v = self.get_argument(k, "")  # quote(params[k]) if urlencode else params[k].decode("utf-8")
            # print("v = " , v)
            buff.append("{0}={1}".format(k, v))
            json_pam[k] = v
        reqParams = "&".join(buff)
        # activity=activity=[b'newInstance']&businessId=[b'c50dd5ef-7787-4dba-9aa3-8002ff9cd075']&customerId=[b'68cbc86abc2018ab880d92f36422fa0e']&customerName=[b'\xe9\xa3\x9e\xe8\x9d\xb6\xe6\xb5\x8b\xe8\xaf\x951']&email=[b'AB6156K8d19nB2s4iMWN7ddmMCoi8+IRO7F8StC7ekGbAlN2hgLEZ85dmFY=']&expireTime=[b'20210916133124']&mobilePhone=[b'38Io21U8q16fTTy9B6m29k/4Ibsia3zWfU7W8Q==']&orderAmount=[b'100']&orderId=[b'CS1906666666ABCDE']&periodNumber=[b'1']&periodType=[b'year']&productId=[b'00301-666666-0--0']&provisionType=[b'1']&testFlag=[b'1']&timeStamp=[b'20210916064657481']&userId=[b'fd1001']&userName=[b'fdtest']
        #print("reqParams = ", reqParams)

        key = Global.Global_IsvKey + timeStamp
        #print("key = ", key)

        ctorken = self.generateResponseBodySignature(key,reqParams)
        logging.info("ISV - reqParams = " + reqParams)
        return [ctorken == authToken,json_pam]

    @property
    def ISV_IVGet(self):
        return ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','0','1','2','3','4','5','6','7','8','9'], 16))#string.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',16)).replace(' ','')

    def generateResponseBodySignature(self,key,reqParams):

        sign = base64.b64encode(
            hmac.new(key.encode("utf-8"), reqParams.encode("utf-8"), digestmod=hashlib.sha256).digest())
        return sign.decode("utf-8")


    # def prepare(self):
    #     """预解析json数据"""
    #     if self.request.headers.get("Content-Type", "").startswith("application/json"):
    #         self.json_args = json.loads(self.request.body)
    #     else:
    #         self.json_args = {}
