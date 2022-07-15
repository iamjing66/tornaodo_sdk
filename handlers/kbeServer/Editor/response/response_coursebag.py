#!/usr/bin/env python
# coding=utf-8

from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_coursebag


# 登录赠送课程包
def Transactions_Code_1018(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构

    DB = DBManager()
    json_back["code"] = interface_coursebag.ComputeBag(DB, self_uid)
    DB.destroy()
    return json_back
