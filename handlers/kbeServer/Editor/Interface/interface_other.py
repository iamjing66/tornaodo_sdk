#!/usr/bin/env python
# coding=utf-8


def DoOperate_GetClientName(DB, pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if pam == "":
        return json_data

    _arrPam = pam.split("-")
    clientName = ""
    sql = ""
    if _arrPam[1] == "1":
        clientName = "XRCreateX"
        sql = "Select clientName from eservices where id = %s"
    elif _arrPam[1] == "2":
        clientName = "XR云课堂"
        sql = "Select appName from eservices where id = %s"
    elif _arrPam[1] == "3":
        clientName = "XR云课堂"
        sql = "Select vrName from eservices where id = %s"

    if _arrPam[0] != "0":
        data = DB.fetchone(sql, _arrPam[0])
        if data:
            if data[0]:
                clientName = data[0]
    json_data["code"] = "1"
    json_data["msg"] = clientName
    return json_data


def DoOperate_GetClientName_new(DB, pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if pam == "":
        return json_data

    _arrPam = pam.split("-")
    clientName = ""
    logo_path = "|"
    sql = ""
    if _arrPam[1] == "1":
        clientName = "XRCreateX"
        sql = "Select clientName from eservices where id = %s"
    elif _arrPam[1] == "2":
        clientName = "飞蝶XR"
        sql = "Select appName, logoImg from eservices where id = %s"
    elif _arrPam[1] == "3":
        clientName = "飞蝶XR"
        sql = "Select vrName, logoImg from eservices where id = %s"

    if _arrPam[0] != "0":
        data = DB.fetchone(sql, _arrPam[0])
        if data:
            if data[0]:
                clientName = data[0]
            if _arrPam[1] == "2" or _arrPam[1] == "3":
                if data[1]:
                    logo_path += str(data[1])
                clientName += logo_path
    json_data["code"] = "1"
    json_data["msg"] = clientName
    return json_data


def DoSaveModeGroup(DB, pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if pam == "":
        return json_data

    _arrPam = pam.split("$")
    _arrPam1 = _arrPam[0].split("|")
    CID = _arrPam1[0]
    NAME = _arrPam1[1]
    UID = _arrPam1[2]

    sql_str = "insert into tb_collect (UID,Name,CID) value (%s, %s, %s)"

    insert = DB.edit(sql_str, (str(UID), str(NAME), str(CID)))
    if insert:
        _arrPam2 = _arrPam[1].split("#")
        if len(_arrPam2) > 0:
            for apam in _arrPam2:
                _arrPam3 = apam.split("|")
                sql = "insert into tb_collect_tree (`UID`,`CID`,`ObjID`,`PID`,`Pos_X`,`Pos_Y`,`Pos_Z`,`Rot_X`,`Rot_Y`,`Rot_Z`,`Scale_X`,`Scale_Y`,`Scale_Z`,`Color`,`ZID`,`Pam`,`Name`) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insert_1 = DB.edit(sql, ((str(UID),)+tuple(_arrPam3)))
                if insert_1:
                    json_data["code"] = "1"
                    json_data["msg"] = ""

    return json_data


def DbGetApkVersionFromDeveceName(DB, Pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    _cback = ""
    arr = Pam.split(',')
    if len(arr) == 1:
        sql = "select LowestVersion,NewestVersion,VersionExplain,PackageSize,text,title from tb_apkversion where DeveceName = %s"
        data = DB.fetchone(sql, str(Pam))
        if data:
            _cback = "|".join(data[:6])
            json_data["code"] = "1"
            json_data["msg"] = _cback
    else:
        DeveceName = Pam.split(',')[0]
        LocalVersion = Pam.split(',')[1]
        code = Pam.split(',')[2]
        strSql = ''
        if code == '999':
            strSql = "select LowestVersion,NewestVersion,VersionExplain,PackageSize,text,title,LowFullVersion,UILowVersion from tb_apkversion_test where DeveceName = %s"
        else:
            strSql = "select LowestVersion,NewestVersion,VersionExplain,PackageSize,text,title,LowFullVersion,UILowVersion from tb_apkversion where DeveceName = %s"

        BForcedUpdate = "0"

        data = DB.fetchone(strSql, str(DeveceName))
        if data:
            data = list(data)
            if float(LocalVersion) >= float(data[1]):
                json_data["code"] = "0"
                data.append(BForcedUpdate)
                _cback = "|".join([str(i) if data.index(i) not in [4, 5] else "" for i in data[:8]])
            else:
                if float(LocalVersion) < float(data[0]):
                    BForcedUpdate = "1"
                else:
                    BForcedUpdate = "0"
                data.append(BForcedUpdate)
                _cback = "|".join([str(i) for i in data])
                if float(LocalVersion) < float(data[6]):
                    json_data["code"] = "1"
                else:
                    if float(LocalVersion) >= float(data[7]):
                        json_data["code"] = "2"
                    else:
                        json_data["code"] = "3"
            json_data["msg"] = _cback
        else:
            json_data["code"] = "-1"
            json_data["msg"] = _cback
    return json_data


def ProblemFeedback(DB, pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if not pam:
        return json_data

    _arrPam = pam.split("$")
    sql_str = "INSERT into feedback (createTime,createUserId,describes,imgPaths,tell,types,username) value (%s, %s, %s, %s, %s, %s, %s)"
    insert = DB.edit(sql_str, tuple(_arrPam))
    if insert:
        json_data["code"] = "1"
        json_data["msg"] = ""
    return json_data


def GetActiveUserFeedback(DB, pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if pam == "":
        return json_data
    strSql = "select count(createUserId) from feedback where createUserId = %s"

    _cback = ""
    data = DB.fetchone(strSql, str(pam))
    if data:
        _cback = data[0]
        json_data["code"] = "1"
        json_data["msg"] = _cback
    else:
        json_data["code"] = "0"
        json_data["msg"] = "-1"

    return json_data


def GetLocalFullViewPath(DB, Pam):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if Pam == "":
        return json_data
    strSql = "select count(*) as num from " + str(Pam) + " where BDelete = 0 and  View_FullPath like '%:%'"
    _cback = ""
    data = DB.fetchone(strSql, None)
    if data:
        _cback = data[0]
        json_data["code"] = "1"
        json_data["msg"] = _cback
    else:
        json_data["code"] = "0"
        json_data["msg"] = "0"

    return json_data
