#!/usr/bin/env python
# coding=utf-8

from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_account,interface_wit,interface_global,interface_user


#PC端登录数据
def Transactions_Code_1012(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])

    DB = DBManager()
    json_back["code"] = interface_account.PC_lOGON(DB,self_uid,uid)
    DB.destroy()
    return json_back


#验证身份信息
def Transactions_Code_1013(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    pam = json_data["pam"]
    username = json_data["username"]

    DB = DBManager()
    json_back["code"] = interface_account.VerifyIdentity(DB,self_uid,pam,username)
    DB.destroy()
    return json_back

#验证身份信息
def Transactions_Code_1014(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]

    DB = DBManager()
    json_back["code"] = 1
    json_back["pam"] = interface_account.FabricatorData(DB,self_uid,username)
    DB.destroy()
    return json_back

#PC端登录
def Transactions_Code_1019(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]
    password = json_data["password"]

    DB = DBManager()
    #验证下账号
    json_back["code"] = interface_account.BaseLogin(DB,username,password)
    if json_back["code"] == 1:
        json_back["pam"] = interface_account.PC_lOGON(DB,self_username,json_data)
    # TODO 用户登录后，更新用户的 redis
    # 顶号
    # interface_user.IUser_Diffusion(1, self_uid, username, {}, "editor")
    DB.destroy()
    return json_back


#智慧豆同步
def Transactions_Code_1031(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构

    DB = DBManager()
    json_back["code"] = 1
    json_back["pam"] = str(interface_wit.TB_Wit(DB,self_username))
    DB.destroy()
    return json_back


#购买资源
def Transactions_Code_1032(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    objid = int(json_data["objid"])
    type = int(json_data["type"])
    btype = int(json_data["btype"])
    # type 0-永久 1-一年
    # buytype 0-资源 1-场景

    DB = DBManager()
    arr = interface_account.N_ResNuy(DB,self_uid,objid,type,btype)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


#购买存储位
def Transactions_Code_1033(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    bid = int(json_data["bid"])
    num = int(json_data["num"])
    # type 0-永久 1-一年
    # buytype 0-资源 1-场景

    DB = DBManager()
    arr = interface_account.BuyPackage(DB,self_uid,0,bid,num)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


#存储位绑定工程
def Transactions_Code_1034(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    bid = int(json_data["bid"])
    pid = int(json_data["pid"])
    # type 0-永久 1-一年
    # buytype 0-资源 1-场景

    DB = DBManager()
    arr = interface_account.PackageBind(DB,self_uid,bid,pid)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


#APP_修改密码
def Transactions_Code_2005(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    oldpw = json_data["oldpw"]
    newpw = json_data["newpw"]

    DB = DBManager()
    json_back["code"] = interface_account.UpdatePassword_App(DB,self_username,oldpw,newpw)
    DB.destroy()
    return json_back


#APP_修改密码
def Transactions_Code_2006(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    atype = int(json_data["atype"])
    pam = json_data["pam"]
    DB = DBManager()
    json_back["code"] = interface_account.AlterAppPam(DB,self_uid,atype,pam)
    json_back["pam"] = str(atype)
    DB.destroy()
    return json_back


#注册相关
def Transactions_Register(DB,subCode,uid,username,data,phone_recode):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }
    if subCode == 3:    #APP端注册
        json_back = interface_account.Register(DB,uid, username, data, phone_recode)
    elif subCode == 4:  #VR端 忘记密码
        json_back = interface_account.UpdatePD(DB,uid, username, data, phone_recode)
    elif subCode == 5:  #PC修改密码
        json_back =  interface_account.FindPD(DB,uid, username, data)
    elif subCode == 33: #PC端绑定手机号
        return interface_account.BindPhone(DB,uid, username, data, phone_recode)
    return json_back


#身份信息修改
def Transactions_Code_1038( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    name = json_data["name"]
    iedent = json_data["iedent"]
    school = json_data["school"]
    _class = json_data["class"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_account.N_WriteRoleData(DB,self_uid,name,iedent,school,_class)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back

#设置GM
def Transactions_Code_1039( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    username = json_data["username"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_global.Global_SetGM(username,DB)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


def Transactions_Code_1040( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    #username = json_data["username"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_account.DoLogout(DB,self_username,json_data)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


def Transactions_Code_1041( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    tlong = int(json_data["tlong"])
    course_type = json_data["course_type"]
    video_type = json_data["video_type"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_account.DaochuVedio(DB,tlong,self_uid,course_type,video_type)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back

def Transactions_Code_1042():
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }
    DB = DBManager()
    json_back["code"],json_back["msg"] = interface_account.get_video_price(DB)
    DB.destroy()
    return json_back

def Transactions_Code_1043(self_uid):
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }
    DB = DBManager()
    json_back["code"], times = interface_account.get_account_outtimes(DB, self_uid)
    json_back["msg"] = "_".join(times)
    DB.destroy()
    return json_back


def Transactions_Code_1044( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    ismarket = int(json_data["market"])

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = 1
    json_back["msg"] = interface_account.projectConfig(DB,uid,pid,ismarket)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back

def Transactions_Code_1045( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    #name,iedent,school,_class
    audioid = json_data["audio"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = 1
    json_back["msg"] = interface_account.GetAudioPath(DB,audioid)
    #pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back