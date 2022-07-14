#!/usr/bin/env python
# coding=utf-8

import json
import Global
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_global
from handlers.kbeServer.Editor.Data import data_obj


def CopyToDB(target, db, uid, pid, sourceTableName):
    if target == 0:
        table_name = Global.GetObjTableName(uid, pid)
    else:
        table_name = Global.GetMObjTableName(uid, pid)

    if not interface_global.Global_TableExist(table_name, db):  # 新增
        db.callprocAll('N_CopyObjectTable', (pid, uid, target))

        sql = "insert into " + table_name + " select * from " + sourceTableName + ";"
        db.edit(sql, None)

    return 1


def CopyToDBNew(target, db, uid, pid, sourceTableName):
    if target == 0:
        table_name = Global.GetObjTableName(uid, pid)
    else:
        table_name = Global.GetMObjTableName(uid, pid)

    if not interface_global.Global_TableExist(table_name, db):  # 新增
        db.callprocAll('N_CopyObjectTable', (pid, uid, target))
    else:
        sql = "delete from " + table_name + ";"
        db.edit(sql, None)

    sql = "insert into " + table_name + " select * from " + sourceTableName + ";"
    db.edit(sql, None)

    return 1


def UpdateToDB(target, db, uid, pid, OBJdata):
    if target == 0:
        table_name = Global.GetObjTableName(uid, pid)
    else:
        table_name = Global.GetMObjTableName(uid, pid)

    sql = ""
    if not interface_global.Global_TableExist(table_name, db):  # 新增
        db.callprocAll('N_CopyObjectTable', (pid, uid, target))
    if OBJdata is not None and len(OBJdata) > 0:
        # data
        # 20`场景编程区`1621395011`0.0`0.0`0.0`0.0`0.0`0.0`1.0`1.0`1.0`0``&0,0&```0`0`1```0.0`0.0``0`1`0!
        # 5`3D相机`1621395011`0.0`0.0`0.0`0.0`0.0`0.0`1.0`1.0`1.0`0``&0,0&```0`0`2```0.0`0.0``0`1`0
        l_pdata = OBJdata.split('!')
        for info in l_pdata:
            if info == "" or len(info) == 0:
                continue
            l_obj_data = info.split('`')
            sql = "select ComID from " + table_name + " where ComID = " + str(l_obj_data[19]) + " limit 0,1"
            result = db.fetchone(sql, None)
            if result:
                sql = "Update " + table_name + " set  `ObjID`=" + l_obj_data[0] + ", objName='" + l_obj_data[
                    1] + "', CreateDate=" + l_obj_data[2] + ", Obj_PosX=" + l_obj_data[3] + ", Obj_PosY=" + l_obj_data[
                          4] + ", `Obj_PosZ`=" + l_obj_data[5] + ", Obj_RoteX=" + l_obj_data[6] + ", Obj_RoteY=" + \
                      l_obj_data[7] + ", Obj_RoteZ=" + l_obj_data[8] + ", Obj_ScaleX=" + l_obj_data[
                          9] + ", Obj_ScaleY=" + l_obj_data[10] + ", Obj_ScaleZ=" + l_obj_data[11] + ", `Active`=" + \
                      l_obj_data[12] + ", ResPath_User='" + l_obj_data[13] + "',Commonts='" + l_obj_data[
                          14] + "',AdsortDetection='" + l_obj_data[15] + "',AdsortBeDetection='" + l_obj_data[
                          16] + "',ParentID=" + l_obj_data[17] + ",ResType=" + l_obj_data[18] + ",ComID=" + l_obj_data[
                          19] + ",View_FullPath='" + l_obj_data[20] + "',View_FullAbPath='" + l_obj_data[
                          21] + "',sizeDeltaX=" + l_obj_data[22] + ",sizeDeltaY=" + l_obj_data[23] + ",Content='" + \
                      l_obj_data[24] + "',Collider=" + l_obj_data[25] + ",Version=" + l_obj_data[26] + ",BDelete=" + \
                      l_obj_data[27] + " WHERE ComID = " + l_obj_data[19]
            else:
                sql = "Insert INTO " + table_name + " (`ObjID`,`objName`,`CreateDate`,`Obj_PosX`,`Obj_PosY`,`Obj_PosZ`,`Obj_RoteX`,`Obj_RoteY`,`Obj_RoteZ`,`Obj_ScaleX`,`Obj_ScaleY`,`Obj_ScaleZ`,`Active`,`ResPath_User`,`Commonts`,`AdsortDetection`,`AdsortBeDetection`,`ParentID`,`ResType`,`ComID`,`View_FullPath`,`View_FullAbPath`,`sizeDeltaX`,`sizeDeltaY`,`Content`,`Collider`,`Version`,`BDelete`) VALUES (" + \
                      l_obj_data[0] + ",'" + l_obj_data[1] + "'," + l_obj_data[2] + "," + l_obj_data[3] + "," + \
                      l_obj_data[4] + "," + l_obj_data[5] + "," + l_obj_data[6] + "," + l_obj_data[7] + "," + \
                      l_obj_data[8] + "," + l_obj_data[9] + "," + l_obj_data[10] + "," + l_obj_data[11] + "," + \
                      l_obj_data[12] + ",'" + l_obj_data[13] + "','" + l_obj_data[14] + "','" + l_obj_data[15] + "','" + \
                      l_obj_data[16] + "'," + l_obj_data[17] + "," + l_obj_data[18] + "," + l_obj_data[19] + ",'" + \
                      l_obj_data[20] + "','" + l_obj_data[21] + "'," + l_obj_data[22] + "," + l_obj_data[23] + ",'" + \
                      l_obj_data[24] + "'," + l_obj_data[25] + "," + l_obj_data[26] + "," + l_obj_data[27] + ")"
            # print("insert Into Obj : ", sql)
            db.edit(sql, None)

    return 1


def Get(JData):
    JDATA = json.loads(JData)
    gpid = JDATA["gpid"]
    guid = JDATA["guid"]
    target = int(JDATA["target"])
    data_from = JDATA["From"]
    pdata = JDATA["data"]
    _server_pid = []
    p_server = {}
    db = DBManager()
    # INI结构转字典
    if pdata is not None and len(pdata) > 0:
        l_pdata = pdata.split('!')
        for info in l_pdata:
            sdata = info.split('`')
            comid = int(sdata[0])
            version = int(sdata[1])
            p_server[comid] = version
            _server_pid.append(comid)

    # print("gpid[%s]-guid[%s]-taget[%s]-From[%s]-pdata[%s]-" % (gpid,guid,str(taget),From,pdata))
    json_data = "！".join([str(gpid), str(guid), str(target), data_from])
    result = data_obj.Data_Objs_Base(target, db, gpid, guid, p_server, 0)
    return json_data + result + "！"
