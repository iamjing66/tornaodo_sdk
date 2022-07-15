import logging
import copy
import Global
import json
import time
import random
from handlers.base import BaseHandler
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_course
from handlers.kbeServer.Editor.Interface import interface_lesson
from handlers.kbeServer.Editor.Data.data_course import *
from handlers.kbeServer.Editor.Data.data_lesson import *


# 购买课程/赠送课程
# 可单个购买也可多个购买
# lid 0-全部 其他单节
# itype 购买时 0-一年 1-永久 | 赠送时 = 赠送时长
# btype 0-赠送 1-购买
# ctype 0-等级包/权限包(时间叠加) 1-补偿包(时间叠加) 2-机构老师包(时间叠加) 3-购买课程 4 - 客户端多个购买(lid 用#分割)
def Transactions_Code_1001(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = int(json_data["cid"])
    uid = int(json_data["uid"])
    lid = json_data["lid"]
    itype = int(json_data["itype"])
    btype = int(json_data["btype"])
    ctype = int(json_data["ctype"])
    logging.info("BuyCourse：[%i] - [%i] - [%s] - [%i] - [%i] - [%i]" % (cid, uid, lid, itype, btype, ctype))

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    arr = interface_course.Buy(DB, self_uid, uid, cid, lid, itype, btype, ctype, self_username)
    json_back["code"] = arr[0]
    json_back["pam"] = arr[1]
    DB.destroy()
    return json_back


# 删除课程
def Transactions_Code_1002(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = json_data["cid"]
    uid = json_data["uid"]
    lid = json_data["lid"]  # 0-删除所有 其他删除对应的
    # logging.info("BuyCourse：[%i] - [%i] - [%i]" % (cid, uid, lid))

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    if interface_course.Delete(self_uid, DB, uid, cid):
        if interface_lesson.Delete(self_uid, DB, uid, cid, lid):
            json_back["code"] = 1
    DB.destroy()
    return json_back


# 审核课程
def Transactions_Code_1004(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = int(json_data["cid"])
    uid = int(json_data["uid"])
    shcode = int(json_data["shcode"])  # 0-拒绝 1-通过

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_course.SH(DB, self_uid, uid, cid, shcode)
    DB.destroy()
    return json_back


# 撤销课程
def Transactions_Code_1022(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    cid = int(json_data["cid"])
    uid = int(json_data["uid"])

    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back["code"] = interface_course.CX(DB, cid, uid)
    DB.destroy()
    return json_back
