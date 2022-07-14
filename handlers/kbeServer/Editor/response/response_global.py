#!/usr/bin/env python
# coding=utf-8

import logging
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_global


# 下架的课程
def GetCourseXJ():
    _back = ""
    DB = DBManager()
    sql = "select cid,mlessonId,uid,flag from sys_course_res where flag = 0"
    result = DB.fetchall(sql, None)
    if result:
        list_data = list(result)
        for minfo in list_data:
            minfo_list = list(minfo)
            if _back == "":
                _back = str(minfo_list[0]) + "`" + str(minfo_list[1]) + "`" + str(minfo_list[2]) + "`" + str(
                    minfo_list[3])
            else:
                _back = _back + "^" + str(minfo_list[0]) + "`" + str(minfo_list[1]) + "`" + str(
                    minfo_list[2]) + "`" + str(minfo_list[3])

    DB.destroy()
    return _back


# 买看数据
def SDK_MK(_uid):
    # 买看数据
    DB = DBManager()
    _worklook_string = ""
    sql = "select * from tb_work_look_b where UID = " + str(_uid) + ""
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            if _worklook_string == "":
                _worklook_string = str(minfo_list[3]) + "^" + str(minfo_list[2]) + "^" + str(minfo_list[4])
            else:
                _worklook_string = _worklook_string + "!" + str(minfo_list[3]) + "^" + str(minfo_list[2]) + "^" + str(
                    minfo_list[4])
    DB.destroy()
    return _worklook_string


# 频道包月
def SDK_CHANNEL(_uid):
    # 频道包月数据
    DB = DBManager()
    _channel_string = ""
    sql = "select * from tb_channel_buy where UID = " + str(_uid) + ""
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            if _channel_string == "":
                _channel_string = str(minfo_list[1]) + "^" + str(minfo_list[2])
            else:
                _channel_string = _channel_string + "!" + str(minfo_list[1]) + "^" + str(minfo_list[2])
    DB.destroy()
    logging.info("SDK_CHANNEL : %s, %s" % (_uid, _channel_string))
    return _channel_string


# IP存储
def SetLoginIP(_uid, ip, SoftType):
    #
    sql = ""
    DB = DBManager()
    if SoftType == "XRCREATEX":
        sql = "update tb_userdata set editor_ip = '" + ip + "' where uid = " + str(_uid)
    elif SoftType == "XRCLOUND":
        sql = "update tb_userdata set app_ip = '" + ip + "' where uid = " + str(_uid)
    if len(sql) > 0:
        DB.edit(sql, None)
    DB.destroy()
    return ""


# 工程，课程最大ID获取
def MaxIDResponse(DB, subcode, params):
    UserName = params["username"]
    if subcode == 32:
        return interface_global.GetUserMaxID(DB, UserName)
    else:
        return interface_global.GetCreateMaxID(DB, subcode, UserName)


# 畅想包月
def Transactions_Code_2007(self_uid, self_username, json_data):
    # 回调json
    json_back = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    # json_data 结构
    apptype = int(json_data["atype"])
    channel = int(json_data["channel"])
    monthid = int(json_data["monthid"])
    DB = DBManager()
    json_back["code"] = interface_global.MonthedChannel(DB, self_uid, channel, monthid, apptype)
    DB.destroy()
    return json_back
