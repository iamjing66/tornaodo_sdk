#!/usr/bin/env python
# coding=utf-8

def Data_Obj_Base(db, uid):
    data = {}

    sql = "select Version from respackage where uid = %s"
    result = db.fetchall(sql, str(uid))
    if result:
        for minfo in result:
            minfo_list = list(minfo)
            data[int(minfo_list[0])] = int(minfo_list[1])

    return data


def Data_Scene_Base(db, uid):
    data = {}

    sql = "select Version from scenepackage where uid = %s"
    result = db.fetchall(sql, str(uid))
    if result:
        for minfo in result:
            minfo_list = list(minfo)
            data[int(minfo_list[0])] = int(minfo_list[1])

    return data


def UpdateToDB(db, uid, RESID, RTYPE, DATE, INSERT):
    if not INSERT:
        if RTYPE == 0:
            sql = "update respackage set DATE = " + str(DATE) + " where uid = " + str(uid) + " and RESID = " + str(
                RESID)
        else:
            sql = "update scenepackage set DATE = " + str(DATE) + " where uid = " + str(uid) + " and RESID = " + str(
                RESID)
    else:
        if RTYPE == 0:
            sql = "insert into respackage (uid,RESID,DATE) value(" + str(uid) + "," + str(RESID) + "," + str(DATE) + ")"
        else:
            sql = "insert into scenepackage (uid,RESID,DATE) value(" + str(uid) + "," + str(RESID) + "," + str(
                DATE) + ")"
    result = db.edit(sql, None)
    if result:
        return True
    return False
