#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_project, interface_zy
from methods.DBManager import DBManager


# 提交作业
def Transactions_Code_1015(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    pid = int(json_data["pid"])
    CLASSID = json_data["classid"]
    CourseID = json_data["courseid"]

    DB = DBManager()
    arr = interface_zy.TaskSend(DB, self_uid, uid, CLASSID, pid, CourseID)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


# 作业打分
def Transactions_Code_1016(self_uid, self_username, json_data):
    # 回调json
    json_back = {
            "code": 0,
            "msg": "",
            "pam": ""
    }

    # json_data 结构
    uid = int(json_data["uid"])
    TID = json_data["tid"]
    CLASSID = json_data["classid"]
    SCORE = int(json_data["score"])

    DB = DBManager()
    json_back["code"] = interface_zy.TaskMark(DB, self_uid, uid, CLASSID, TID, SCORE)
    DB.destroy()
    return json_back


# 班级分享
def Transactions_Code_1017(self_uid, self_username, json_data):
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
    FromPam = json_data["frompam"]

    DB = DBManager()
    json_back["code"] = interface_project.SetFrom(DB, uid, pid, From, FromPam)
    DB.destroy()
    return json_back
