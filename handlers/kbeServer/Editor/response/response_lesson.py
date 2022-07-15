from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_lesson


# 删除课时(如果lid不等于0后台是隐藏) - 用pdate来存储
def Transactions_Code_1003(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = int(json_data["cid"])
    uid = int(json_data["uid"])
    lid = int(json_data["lid"])  # 0-删除所有 其他删除对应的

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    if interface_lesson.Delete(self_uid, DB, uid, cid, lid):
        json_back["code"] = 1
    DB.destroy()
    return json_back
