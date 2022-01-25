import logging

import Global
from methods.DBManager import DBManager
from handlers.kbeServer.XREditor.Interface import xrinterface_work,xr_interface_obj

#新建作品
def Transactions_Code_4001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    sid = int(json_data["sid"])         #场景ID
    wname = json_data["wname"]          #作品名称



    if sid < 1 or len(wname) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.NewWork(DB,self_uid,wname,sid,languageStr)
        DB.destroy()

    return json_back


#设为模板/取消模板
def Transactions_Code_4002(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID
    flag = int(json_data["flag"])       # 0-取消 1-设置
    if pid < 1 or flag < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.Template(DB,self_uid,pid,flag,languageStr)
        DB.destroy()

    return json_back


#模板新建
def Transactions_Code_4003(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID
    wname = json_data["wname"]     # 作品名称
    if pid < 1 or len(wname) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.TemplateNewWork(DB,self_uid,pid,wname,languageStr)
        DB.destroy()

    return json_back



#作品转移
def Transactions_Code_4004(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID
    username = json_data["username"]     #要转移的用户
    wname = json_data["wname"]          #转移后的作品名称
    flag = int(json_data["flag"])        #状态 0-复制 1-转移

    if pid < 1 or len(wname) < 1 or flag < 0 or len(username) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.transferWork(DB,self_uid,pid,wname,username,flag,languageStr)
        DB.destroy()

    return json_back


#获取资源服务器版本号
def Transactions_Code_4005(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID

    if pid < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xr_interface_obj.XrObjVersion(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back


#上传作品
def Transactions_Code_4006(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID
    obj = json_data["obj"]              # 资源数据

    if pid < 1 or len(obj) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xr_interface_obj.Upload(DB,self_uid,pid,obj,languageStr)
        DB.destroy()

    return json_back


#发布作品
def Transactions_Code_4007(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID
    wname = json_data["wname"]                  #作品名称
    classiy = int(json_data["classiy"])         #作品分类
    platform = json_data["platform"]            #发布平台
    price = int(json_data["price"])             #价格
    tab = json_data["tab"]                      # 标签
    desc = json_data["desc"]                    #介绍

    if price < 0 or len(wname) < 1  or len(tab) < 1  or len(desc) < 1  or len(platform) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.Publish(DB,self_uid,pid,wname,classiy,platform,price,tab,desc,languageStr)
        DB.destroy()

    return json_back

#作品改名
def Transactions_Code_4008(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID
    wname = json_data["wname"]                  #作品名称

    if pid < 0 or len(wname) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.AlterName(DB,self_uid,pid,wname,languageStr)
        DB.destroy()

    return json_back


#作品删除
def Transactions_Code_4009(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID

    if pid < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.DeleteWork(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back


#作品审核列表
def Transactions_Code_4010(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    page = int(json_data["page"])                      # 页数，从1开始
    num = int(json_data["num"])                       # 一页几条

    if page < 1 or  page < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.SHList(DB,self_uid,page,num,languageStr)
        DB.destroy()

    return json_back



#作品审核
def Transactions_Code_4011(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    uid = int(json_data["uid"])                      #用户id
    pid = int(json_data["pid"])                      #作品id
    state = int(json_data["state"])                  # 1-审核通过 0-审核未通过

    if uid < 1 or  pid < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.SHWork(DB,uid,pid,state,languageStr)
        DB.destroy()

    return json_back


#作品市场-普通作品
def Transactions_Code_5001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    flag = int(json_data["flag"])                    #0-普通市场 1-精品市场

    if flag< 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.Market(DB,flag,languageStr)
        DB.destroy()

    return json_back


#作品市场-个人作品集
def Transactions_Code_5002(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    #flag = int(json_data["flag"])                    #0-普通市场 1-精品市场

    DB = DBManager()
    json_back = xrinterface_work.MyWorks(DB, self_uid, languageStr)
    DB.destroy()

    return json_back


#购买作品
def Transactions_Code_4012(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID
    uid = int(json_data["uid"])         #用户id
    if pid < 1 or uid < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.Buy(DB,self_uid,pid,uid,languageStr)
        DB.destroy()

    return json_back

#作品复制
def Transactions_Code_4013(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])         #作品ID

    if pid < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.CopyWork(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back


#取消发布
def Transactions_Code_4014(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID

    if pid < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.CancelPublish(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back


#下架作品
def Transactions_Code_4015(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID

    if pid < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.MarketOff(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back

#上架作品
def Transactions_Code_4015(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    pid = int(json_data["pid"])                      # 作品ID

    if pid < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:

        DB = DBManager()
        json_back = xrinterface_work.MarketOn(DB,self_uid,pid,languageStr)
        DB.destroy()

    return json_back


