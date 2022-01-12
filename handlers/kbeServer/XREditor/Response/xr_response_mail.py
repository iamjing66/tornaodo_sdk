import Global
from methods.DBManager import DBManager
from handlers.kbeServer.XREditor.Interface import xr_interface_mail
#获取邮件列表
def Transactions_Code_6001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    page = int(json_data["page"])       #页数
    hnum = int(json_data["hnum"])       #一页几行

    if page < 0 or hnum < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_1_4",languageStr)
    else:
        # 获取下db的句柄，如果需要操作数据库的话
        DB = DBManager()
        json_back = xr_interface_mail.GetMail(DB,self_uid,page,hnum,languageStr)
        DB.destroy()

    return json_back


#读邮件
def Transactions_Code_6002(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    ID = int(json_data["ID"])       #邮件ID

    if ID < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_1_4",languageStr)
    else:
        # 获取下db的句柄，如果需要操作数据库的话
        json_back = xr_interface_mail.ReadMail(self_uid,ID,languageStr)

    return json_back


#删除邮件
def Transactions_Code_6003(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    ID = int(json_data["ID"])       #邮件ID

    if ID < 0:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_1_4",languageStr)
    else:
        # 获取下db的句柄，如果需要操作数据库的话
        json_back = xr_interface_mail.DetMail(self_uid,ID,languageStr)

    return json_back


#全部已读
def Transactions_Code_6004(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    #ID = int(json_data["ID"])       #邮件ID

    DB = DBManager()
    json_back = xr_interface_mail.ReadAll(DB, self_uid, languageStr)
    DB.destroy()

    return json_back

#删除已读
def Transactions_Code_6005(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    #ID = int(json_data["ID"])       #邮件ID

    DB = DBManager()
    json_back = xr_interface_mail.DeleteReaded(self_uid, languageStr)
    DB.destroy()

    return json_back