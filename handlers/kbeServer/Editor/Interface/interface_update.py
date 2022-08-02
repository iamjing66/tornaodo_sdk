#!/usr/bin/env python
# coding=utf-8

import logging


def GetUpdateCxVersion(DB):
    json_data = {
            "code": 0,
            "msg": ""
    }

    strSql = "select LowestVersion,NewestVersion,text,title from tb_apkversion where ID = 4"

    _cback = ""
    try:

        data = DB.fetchone(strSql, None)
        if data:
            _cback = data[0] + "|" + data[1] + "|" + data[2] + "|" + data[3]
            json_data["code"] = "1"
            json_data["msg"] = _cback
        else:
            json_data["code"] = "0"
            json_data["msg"] = _cback
    except:
        json_data["code"] = "0"
        json_data["msg"] = _cback
    return json_data


def GetUpdateCxVersionNew(DB, params):
    json_data = {
            "code": 0,
            "msg": ""
    }
    Pam = params["Pam"]
    ID, LocalVersion, code = Pam.split(',')
    logging.info("GetUpdateCxVersionNew: ID:%s, LocalVersion:%s, code:%s" % (ID, LocalVersion, code))
    strSql = ''
    if code == '999':
        strSql = "select LowestVersion,NewestVersion,text,title,LowFullVersion,UILowVersion from tb_apkversion_test where AID = %s;"
    else:
        strSql = "select LowestVersion,NewestVersion,text,title,LowFullVersion,UILowVersion from tb_apkversion where AID = %s;"

    _cback = ""
    BForcedUpdate = "0"

    data = DB.fetchone(strSql, ID)
    if data:

        # print("data", data[1], type(data[1]), len(data[1]), float("6.3"), type(LocalVersion), LocalVersion)
        if len(LocalVersion) == 0:
            LocalVersion = "0.0"
        if float(LocalVersion) >= float(data[1]):
            json_data["code"] = "0"
            _cback = str(data[0]) + "|" + str(data[1]) + "|||" + str(data[4]) + "|" + str(data[5]) + "|" + BForcedUpdate
        else:
            if float(LocalVersion) < float(data[0]):
                BForcedUpdate = "1"
            if float(LocalVersion) < float(data[4]):
                json_data["code"] = "1"
            else:
                if float(LocalVersion) >= float(data[5]):
                    json_data["code"] = "2"
                else:
                    json_data["code"] = "3"
            _cback = str(data[0]) + "|" + str(data[1]) + "|" + str(data[2]) + "|" + str(data[3]) + "|" + str(data[4]) + "|" + str(data[5]) + "|" + BForcedUpdate
    else:
        json_data["code"] = "-1"
    json_data["msg"] = _cback
    logging.info("GetUpdateCxVersionNew: json_data:%s" % json_data)
    # print("GetUpdateCxVersionNew:",json_data)
    return json_data
