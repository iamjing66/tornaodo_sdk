#!/usr/bin/env python
# coding=utf-8

import json
import logging,requests
from time import time
from handlers.base import BaseHandler
from handlers.kbeServer.Editor.response import response_account,response_mail,response_class,response_resversion,response_other,response_update,response_sis,response_fullview,response_collect,response_global
from handlers.kbeServer.Editor.Interface import interface_sms,interface_account,interface_work,interface_user
from handlers.redisServer.RedisInterface import C_ServerAddressCache
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Avatar_Editor import AvatarEditorInst
from handlers.kbeServer.App.Avatar_App import AvatarAppInst
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU

class PostInterfaceRequest(BaseHandler):

    def post(self):
        json_back = {}
        self.SOLR_VERIFY
        # AppCode = 2 & phone = 18740487328 & organization = 0 & distributor = 0 & UID = 9 & UserName = lyy &
        # from=VR & data = 1010004 % 249 % 241
        json_data = self.SolrData
        opencode = int(json_data["opencode"])
        subcode = int(json_data["subcode"])
        UID = int(json_data["UID"])
        username = json_data["username"]
        if isinstance(json_data["data"],dict):
            data = json_data["data"]
        elif isinstance(json_data["data"],str):
            data = json.loads(json_data["data"])
        else:
            data = json_data["data"]
        print("PostInterfaceRequest opencode[%i] subcode[%i] UID[%i] UserName[%s]" % (opencode,subcode,UID,username))
        logging.info("PostInterfaceRequest -> UID[%i],opencode[%i],subcode[%i],username[%s]" % (UID,opencode,subcode,username))
        DB = DBManager()
        if opencode == 0:
            json_back = interface_sms.interface_sendSMS(DB,subcode,UID,username,data)
            #print("json_back1 ",json_back)
            if json_back["code"] == 1:
                self.SetPhoneCode(DB,username,json_back["msg"])
                #del json_back["phone"]
        elif opencode == 1:
            phoneCode = ""
            if subcode == 3 or subcode == 4 or subcode == 33:
                phoneCode = self.GetPhoneCode(DB,username)
            json_back = response_account.Transactions_Register(DB,subcode,UID,username,data,phoneCode) #AccountInst.DoCodeVer(subcode,UID,username,data,phoneCode)
            # if json_back["code"] == 1 and (subcode == 3 or subcode == 4 or subcode == 33):
            #     self.SetPhoneCode(json_back["phone"], "")
            #     del json_back["phone"]
        elif opencode == 2:
             json_back = response_mail.mailresponse(DB,subcode, UID, data)
        elif opencode == 3:
             json_back = response_resversion.ResVersionResponse(DB,subcode, UID, data)
        elif opencode == 4:
             json_back = response_class.classWorkresponse(DB,subcode, UID, data)
        elif opencode == 5:
             json_back = response_resversion.ConfigGet_Server(DB,data)
        elif opencode == 6:

            #登录前获取服务器地址
            cmode = data["cmode"]
            url = globalRedisU.redis_getAdreese()
            logging.info("login - get serverAddresse = " + url)
            #顶号
            #interface_user.IUser_Diffusion(1,UID,username,{},cmode)
            #记录
            #C_ServerAddressCache.SetUser(username,cmode, url )
            json_back = {
                "code": "1",
                "msg": url #self.LOGINCGET
            }
            #登录排队
            #logging.info("getLoginConfig:[%s]" % json_back)
        elif opencode == 7:
            json_back = response_other.DataOperate(DB,subcode,data)
        elif opencode == 8:
            json_back = interface_account.LoginList(DB)
        elif opencode == 9:
            json_back = response_update.SoftVersionGet(DB,subcode,data)
        elif opencode == 10:
            json_back = interface_work.GetWorkFreetime(DB,data)
        elif opencode == 11:
            json_back = response_sis.GetSISCourse(DB,subcode,data)
        elif opencode == 12:
            json_back = response_fullview.FullViewResponse(DB,subcode,data)
        elif opencode == 13:
            json_back = response_collect.CollectResponse(DB,subcode,UID,data)
        elif opencode == 14:
            json_back = response_global.MaxIDResponse(DB,subcode,data)
        elif opencode == 100:
            json_back = AvatarEditorInst.Transactions_Code(subcode,UID,username,data)
        elif opencode == 200:
            json_back = AvatarAppInst.Transactions_Code(subcode,UID,username,data)
        elif opencode == 300:
            json_back = interface_user.IUser_DiffusionDo(subcode,UID,username,data)
        json_back["opencode"] = opencode
        json_back["subcode"] = subcode
        if "pam" not in json_back.keys():
            json_back["pam"] = ""
        self.write(json_back)

    def set_default_headers(self):
        self.allowMyOrigin()    


class GetNowTimeHandler(BaseHandler):
    def get(self):
        now_time = int(time())
        self.write({"time": now_time})
