#!/usr/bin/env python
# coding=utf-8

import json

from handlers.kbeServer.Editor.Data import data_project
from handlers.kbeServer.Editor.Interface import interface_project
from methods.DBManager import DBManager


# 获取是否需要更新
def GetPVersion(jddata):
    db = DBManager()
    JDATA = json.loads(jddata)
    gpid = JDATA["gpid"]
    guid = JDATA["guid"]
    taget = int(JDATA["target"])
    From = JDATA["From"]

    _back = "0"

    # 获取工程数据版本号
    pversion = interface_project.GetPVersion(db, guid, gpid, taget)
    # BODY=====================================

    _back = str(pversion) + "$" + str(gpid) + "$" + str(guid) + "$" + str(taget) + "$" + From
    db.destroy()
    return _back


def Transactions_Code_1006(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])

    db = DBManager()
    json_back["code"] = interface_project.RemoveP(db, self_uid, uid, pid)
    db.destroy()
    return json_back


# 删除工程
def Transactions_Code_1007(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])

    db = DBManager()
    json_back["code"] = interface_project.DeleteP(db, self_uid, uid, pid, 0)
    db.destroy()
    return json_back


# 发布到背包
# 作品 - 4
# 课程 - 3
def Transactions_Code_1009(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = json_data["uid"]
    pid = json_data["pid"]
    template = json_data["template"]

    db = DBManager()
    json_back["code"] = interface_project.FB(db, self_uid, uid, pid, template)
    db.destroy()
    return json_back


# 设置为模板
def Transactions_Code_1010(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = json_data["uid"]
    pid = json_data["pid"]
    publish = json_data["publish"]

    db = DBManager()
    json_back["code"] = interface_project.SetPublish(db, self_uid, uid, pid, publish)
    db.destroy()
    return json_back


# 转移/复制工程
def Transactions_Code_1011(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    pname = json_data["pname"]  # 工程名转移后的
    username = json_data["username"]  # 转移方USERNAME
    cmode = int(json_data["cmode"])  # 0-复制 1-转移

    db = DBManager()
    json_back["code"] = interface_project.CopyMyProjectToAccount(db, uid, pid, pname, username, cmode)
    db.destroy()
    return json_back


# 获取工程数据
def Transactions_Code_1021(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    From = int(json_data["from"])
    target = int(json_data["target"])  # 工程名转移后的
    force = int(json_data["force"])  # 转移方USERNAME

    db = DBManager()
    json_back["code"] = 1
    json_back["pam"] = str(uid) + "!" + str(pid) + "!" + str(target) + "!" + str(force) + "!" + str(
            From) + "!" + data_project.Data_Project_Base(uid, pid, target, db, 0) + "！"
    # 1370!10008!0!1!106!
    # 10008`tt`1621503370`1621503370`0`1002`0.0`0.0`0.0`0.0`0.0`0.0`0`0.0```58`0``0`0`0`0`1`1370`0`0`0`101``0！
    db.destroy()
    return json_back
