#!/usr/bin/env python
# coding=utf-8

# 获取收藏的对象
def GetCollectData(DB, UID, pam):
    json_data = {
            "code": 0,
            "msg": ""
    }
    IDs = pam.split("|")
    strSql = "select * from tb_collect where UID = " + str(UID) + ""
    _cback = ""
    try:
        data = DB.fetchall(strSql, None)
        if data:
            minfo = list(data)
            for info in minfo:
                if IDs != None:
                    if str(info[4]) in IDs:
                        continue
                if _cback == "":
                    _cback = str(info[2]) + "|" + str(info[3]) + "|" + str(info[4])
                else:
                    _cback = _cback + "*" + str(info[2]) + "|" + str(info[3]) + "|" + str(info[4])
            collectree = GetCollectTreeData(DB, UID, IDs)
            if collectree != "":
                _cback = _cback + "#" + collectree
                json_data["code"] = "1"
                json_data["msg"] = _cback
            else:
                json_data["code"] = "1"
                json_data["msg"] = _cback
        else:
            json_data["code"] = "1"
            json_data["msg"] = _cback
    except:
        json_data["code"] = "0"
        json_data["msg"] = "获取收藏数据失败"
    return json_data


# 获取收藏的详细信息
def GetCollectTreeData(DB, UID, IDs):
    strSql = "select * from tb_collect_tree where UID = " + str(UID) + ""
    _cback = ""
    try:
        data = DB.fetchall(strSql, None)
        if data:
            minfo = list(data)
            for info in minfo:
                if IDs != "":
                    if str(info[2]) in IDs:
                        continue
                if _cback == "":
                    _cback = str(info[2]) + "|" + str(info[3]) + "|" + str(info[4]) + "|" + str(info[5]) + "|" + str(info[6]) + "|" + str(info[7]) + "|" + str(info[8]) + "|" + str(
                            info[9]) + "|" + str(info[10]) + "|" + str(info[11]) + "|" + str(info[12]) + "|" + str(info[13]) + "|" + str(info[14]) + "|" + str(info[15]) + "|" + str(
                            info[16]) + "|" + str(info[17]) + "|" + str(info[18])
                else:
                    _cback = _cback + "*" + str(info[2]) + "|" + str(info[3]) + "|" + str(info[4]) + "|" + str(info[5]) + "|" + str(info[6]) + "|" + str(info[7]) + "|" + str(info[8]) + "|" + str(
                            info[9]) + "|" + str(info[10]) + "|" + str(info[11]) + "|" + str(info[12]) + "|" + str(info[13]) + "|" + str(info[14]) + "|" + str(info[15]) + "|" + str(
                            info[16]) + "|" + str(info[17]) + "|" + str(info[18])
        else:
            _cback = ""
    except:
        _cback = ""
    return _cback


# 删除记录的收藏的对象
def CollectDelete(DB, UID, CID):
    json_data = {
            "code": 0,
            "msg": ""
    }
    strSql = "delete from tb_collect where  UID = " + str(UID) + " and CID = " + str(CID)

    _cback = ""
    try:
        DB.edit(strSql, None)
        json_data["msg"] = "删除收藏数据成功"
        json_data["code"] = CollectTreeDelete(DB, UID, CID)
    except:
        json_data["code"] = "0"
        json_data["msg"] = "删除收藏数据失败"
    return json_data


# 删除收藏的详细信息
def CollectTreeDelete(DB, UID, CID):
    strSql = "delete from tb_collect_tree where  UID = " + str(UID) + " and CID = " + str(CID)

    _cback = ""
    try:
        DB.edit(strSql, None)
        _cback = "1"
    except:
        _cback = "0"
    return _cback
