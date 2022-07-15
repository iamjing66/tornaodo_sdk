from handlers.kbeServer.Editor.Interface import interface_gm
from methods.DBManager import DBManager


# 增加智慧豆
def Transactions_Code_1024(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]
    num = int(json_data["num"])

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.AddWit(DB, self_uid, username, num)
    DB.destroy()
    return json_back


# 账号信息查询
def Transactions_Code_1025(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = 1
    json_back["pam"] = interface_gm.GM_AccountData(DB, self_uid, username)
    # pam = "到期时间$账号信息"
    DB.destroy()
    return json_back


# GM修改账号信息
def Transactions_Code_1026(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]
    enddate = json_data["enddate"]  # 到期时间
    companyname = json_data["companyname"]  # 账号信息

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_Alter_AccountData(DB, self_uid, username, enddate, companyname)
    # pam = "到期时间$账号信息"
    DB.destroy()
    return json_back


# GM账号权限获取
def Transactions_Code_1027(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = 1
    json_back["pam"] = interface_gm.GetPowerAndBag(DB, self_uid, username)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# GM账号权限获取
def Transactions_Code_1028(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    username = json_data["username"]
    power = int(json_data["power"])
    bcbag = json_data["bcbag"]  # 这个是tb_cbag(课程包裹)中的cid

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.SetPowerAndBag(DB, self_uid, username, power, bcbag)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# 课程上架/下架
def Transactions_Code_1029(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = int(json_data["cid"])
    uid = int(json_data["uid"])
    lid = int(json_data["lid"])
    state = int(json_data["state"])

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_LessonUD(DB, self_uid, cid, uid, lid, state)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# 发送邮件
def Transactions_Code_1030(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    type = int(json_data["type"])
    pam = json_data["pam"]
    title = json_data["title"]
    tbody = json_data["tbody"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_SendMails(DB, self_uid, type, pam, title, tbody)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# 赠送存储包裹
def Transactions_Code_1035(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    num = int(json_data["num"])
    username = json_data["username"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_AddPBag(DB, self_uid, username, num)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# 到处工程
def Transactions_Code_1036(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    pname = json_data["pname"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_ExportProject(DB, self_uid, pid, uid, pname)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back


# 导入工程
def Transactions_Code_1037(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    tuid = int(json_data["tuid"])  # 需要导入到对方的UID
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    pname = json_data["pname"]

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_gm.GM_ImportProject(DB, self_uid, tuid, pid, uid, pname)
    # pam = "账号类型$补偿包裹"
    DB.destroy()
    return json_back
