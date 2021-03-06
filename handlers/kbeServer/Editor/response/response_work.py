from handlers.kbeServer.Editor.Interface import interface_work
from methods.DBManager import DBManager


# 审核作品
def Transactions_Code_1005(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    wid = int(json_data["wid"])
    uid = int(json_data["uid"])
    shcode = int(json_data["shcode"])  # 0-拒绝 1-通过

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_work.SH(DB, self_uid, uid, wid, shcode)
    DB.destroy()
    return json_back


# 购买作品
def Transactions_Code_1008(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    wid = int(json_data["wid"])
    type = int(json_data["type"])
    ptype = int(json_data["ptype"])

    DB = DBManager()
    arr = interface_work.Buy(DB, self_uid, wid, uid, type, ptype, self_username)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


# 撤销作品
def Transactions_Code_1023(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    wid = int(json_data["wid"])
    target = int(json_data["target"])

    DB = DBManager()
    json_back["code"] = interface_work.CX(DB, uid, wid, target)
    DB.destroy()
    return json_back


def Transactions_Code_1056():
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    DB = DBManager()
    sql = "select UID, CID, ct from tb_course_sort order by sort, CID;"
    data = DB.fetchall(sql)
    data_list = []
    DB.destroy()
    if data:
        json_back["code"] = 1
        for i in data:
            data_list.append("`".join(str(j) for j in i))
    json_back["pam"] = "!".join(data_list)

    return json_back


def Transactions_Code_1057():
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    DB = DBManager()
    sql = "select UID, WID , CT, flag from tb_work_sort order by sort, WID;"
    data = DB.fetchall(sql)
    data_list = []
    DB.destroy()
    if data:
        json_back["code"] = 1
        for i in data:
            data_list.append("`".join(str(j) for j in i))
    json_back["pam"] = "!".join(data_list)

    return json_back


def Transactions_Code_1058():
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    DB = DBManager()
    sql = "select e.UID, e.WID, t.CT, e.flag, e.organization_id, e.free, e.price2, e.sort, e.stime, e.etime from tb_eservices_workmarket as e left join tb_work_sort as t on e.UID = t.UID and e.WID = t.WID order by e.sort, e.WID;"
    data = DB.fetchall(sql)
    data_list = []
    DB.destroy()
    if data:
        json_back["code"] = 1
        for i in data:
            data_list.append("`".join(str(j) for j in i))
    json_back["pam"] = "!".join(data_list)

    return json_back


# 获取用户当前最大PID
def Transactions_Code_1059(self_uid):
    json_back = {
            "code": 0,
            "msg": "",
            "pam": 0
    }

    DB = DBManager()
    sql = "select PID+10002 FROM tb_userdata WHERE uid = %s"
    data = DB.fetchone(sql, self_uid)
    DB.destroy()
    if data:
        json_back["code"] = 1
        json_back["pam"] = data[0]

    return json_back


def Transactions_Code_1060(self_uid):
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    DB = DBManager()
    sql = "Update tb_userdata set PID = PID + 1 WHERE uid = %s"
    data = DB.edit(sql, self_uid)
    DB.destroy()
    if data:
        json_back["code"] = 1
    return json_back
