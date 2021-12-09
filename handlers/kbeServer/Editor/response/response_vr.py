
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_work,interface_sis,interface_account, interface_user


#作品买看
def Transactions_Code_2001( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    wid = int(json_data["wid"])
    uid = int(json_data["uid"])
    btype = int(json_data["btype"])    #0-智慧豆 1-RMB
    plat = int(json_data["plat"])


    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    arr = interface_work.VR_BuyWork(DB,self_uid,wid,uid,btype,plat,phone=False)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


#SIS买看
def Transactions_Code_2002( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    vid = int(json_data["vid"])
    btype = int(json_data["btype"])    #0-智慧豆 1-RMB
    plat = int(json_data["plat"])


    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    arr = interface_sis.VR_MK_SIS(DB,self_uid,vid,btype,plat,phone=False)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


#分享
def Transactions_Code_2003( self_uid , self_username , json_data):

    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    pid = int(json_data["pid"])
    pam = json_data["pam"]


    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_work.VR_ShareWork(DB,self_uid,pid,pam)
    DB.destroy()
    return json_back


#VR端登录
def Transactions_Code_2004(self_uid, self_username, json_data):
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
    # 验证下账号
    json_back["code"] = interface_account.BaseLogin(DB, username, password)
    if json_back["code"] == 1:
        json_back["pam"] = interface_account.VR_LOGIN(DB,self_username,json_data)
    # TODO 登录成功后，更新该用户的 redis
    # interface_user.IUser_Diffusion(1, self_uid, username, {}, "editor")
    DB.destroy()
    return json_back


# 获取课程间距
def Transactions_Code_2013(json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    market = int(json_data["market"])


    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"], json_back["pam"] = interface_work.get_course_slide(DB, uid, pid, market)
    DB.destroy()
    return json_back
