#!/usr/bin/env python
# coding=utf-8


def GetQjtTypeList(DB):
    json_data = {
            "code": 0,
            "msg": ""
    }

    strSql = "select * from qjt_type_table"

    _cback = ""
    try:

        data = DB.fetchall(strSql, None)
        if data:
            minfo = list(data)
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "|" + str(info[1]) + "|" + str(info[2]) + "|" + str(info[3])
                else:
                    _cback = _cback + "*" + str(info[0]) + "|" + str(info[1]) + "|" + str(info[2]) + "|" + str(info[3])
            json_data["code"] = "1"
            json_data["msg"] = _cback
        else:
            json_data["code"] = "0"
            json_data["msg"] = _cback
    except:
        json_data["code"] = "0"
        json_data["msg"] = _cback
    return json_data


def GetQjtDetailList(DB, pam):
    json_data = {
            "code": 0,
            "msg": ""
    }

    strSql = "select * from qjt_details_table where qjt_Type = " + str(pam) + ""

    _cback = ""
    try:
        data = DB.fetchall(strSql, None)
        if data:
            minfo = list(data)
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "|" + str(info[1]) + "|" + str(info[2]) + "|" + str(info[3]) + "|" + str(info[4]) + "|" + str(info[5]) + "|" + str(info[6]) + "|" + str(
                            info[7]) + "|" + str(info[8]) + "|" + str(info[9])
                else:
                    _cback = _cback + "*" + str(info[0]) + "|" + str(info[1]) + "|" + str(info[2]) + "|" + str(info[3]) + "|" + str(info[4]) + "|" + str(info[5]) + "|" + str(info[6]) + "|" + str(
                            info[7]) + "|" + str(info[8]) + "|" + str(info[9])
            json_data["code"] = "1"
            json_data["msg"] = _cback
        else:
            json_data["code"] = "0"
            json_data["msg"] = _cback
    except:
        json_data["code"] = "0"
        json_data["msg"] = _cback
    return json_data
