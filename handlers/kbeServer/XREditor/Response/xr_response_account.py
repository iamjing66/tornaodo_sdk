import logging

import Global
from methods.DBManager import DBManager
from handlers.kbeServer.XREditor.Interface import interface_account
from handlers.kbeServer.Editor.Interface import interface_res,interface_update

#验证码获取
def Transactions_Code_1001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    phone = json_data["phone"]       #手机号
    if len(phone) != 11:
        json_back["code"] = -4  #手机号错误
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_1_4",languageStr)
    else:
        code = int(json_data["code"])    #401-账号注册，402-微信登录绑定手机
        # 获取下db的句柄，如果需要操作数据库的话
        DB = DBManager()
        json_back = interface_account.account_phonecode(DB,self_uid,self_username,languageStr, phone, code)
        DB.destroy()

    return json_back



#注册账号
def Transactions_Code_1002(self_uid,self_username,languageStr,json_data):

    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    #回调json
    #json_data 结构
    phone = json_data["phone"]       #手机号
    code = json_data["code"]            # 验证码
    password = json_data["password"]  # 密码
    if len(phone) != 11:
        json_back["code"] = -1  #手机号错误
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_1_4",languageStr)

    else:
        if len(code) != 6:
            json_back["code"] = -2  # 验证码异常
            json_back["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_6",languageStr)

        else:

            if len(password) < 6 or len(password) > 50:
                json_back["code"] = -3  # 密码长度不符
                json_back["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_7",languageStr)
            else:
                # 获取下db的句柄，如果需要操作数据库的话
                DB = DBManager()
                json_back = interface_account.Register(DB,languageStr,phone,password,code)
                DB.destroy()
    return json_back

#获取微信登录状态
def Transactions_Code_1003(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    state = json_data["state"]
    # password = json_data["password"] #
    # passwordnew = json_data["passwordnew"] #
    # logging.info("alter user：[%s] - [%s] " % (username,password))

    # 获取下db的句柄，如果需要操作数据库的话
    #DB = DBManager()
    json_back = interface_account.WechatLogin(state,languageStr)
    #DB.destroy()
    return json_back



#微信登录绑定手机
def Transactions_Code_1004(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    unionid = json_data["unionid"]
    phone = json_data["phone"]
    phonecode = json_data["phonecode"]       #
    password = json_data["password"]  #
    #type = int(json_data["type"])  #
    if len(unionid) < 1 or len(phonecode) < 1 or len(phone) < 1 or len(password) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.LoginAutoRegester(DB,phone,phonecode,unionid , languageStr,402,password)
    DB.destroy()
    return json_back


#手机验证码登录
def Transactions_Code_1005(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    phone = json_data["phone"]
    phonecode = json_data["phonecode"]       #
    #type = int(json_data["type"])  #
    if len(phonecode) < 1 or len(phone) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.LoginAutoRegester(DB,phone,phonecode,"" , languageStr,403)
    DB.destroy()
    return json_back

#微信登录
def Transactions_Code_1006(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    unionid = json_data["unionid"]
    username = ""
    #type = int(json_data["type"])  #
    if len(unionid) < 1 :
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    sql = "select username from tb_userdata where unionid = '"+unionid+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        username = data[0]
        json_back = interface_account.Login(DB,username,"", languageStr)
    else:
        json_back["code"] = -1  # 参数异常
        json_back["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)
    DB.destroy()
    return json_back


#账号密码登录
def Transactions_Code_1007(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    username = json_data["username"]
    password = json_data["password"]
    #type = int(json_data["type"])  #
    if len(username) < 1 or len(password) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.Login(DB,username,password, languageStr)
    DB.destroy()
    return json_back


#忘记密码
def Transactions_Code_1008(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    phone = json_data["phone"]
    phonecode = json_data["phonecode"]
    password = json_data["password"]
    #type = int(json_data["type"])  #
    if len(phone) < 1 or len(phonecode) < 1 or len(password) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.FindPassword(DB,phone,phonecode,password, languageStr)
    DB.destroy()
    return json_back


#登录获取用户数据
def Transactions_Code_1009(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.Logined(DB, self_uid, self_username,languageStr)
    DB.destroy()

    return json_back


#配置资源版本获取
def Transactions_Code_2001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_res.new_get_update_version(DB, json_data)
    DB.destroy()
    return json_back


#配置资源版本获取
def Transactions_Code_2002(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_res.new_anlyze_code(DB, json_data)
    DB.destroy()
    return json_back

#配置资源版本获取
def Transactions_Code_3001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_update.GetUpdateCxVersionNew(DB,json_data)
    DB.destroy()
    return json_back
