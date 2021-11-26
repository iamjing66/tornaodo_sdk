#!/usr/bin/env python
# coding=utf-8

def Data_Obj_Base(DB,UID):

    data = {}

    sql = "select Version from respackage where uid = " + str(UID)
    result = DB.fetchall(sql, None)
    if result:
        for minfo in result:
            minfo_list = list(minfo)

            data[int(minfo_list[0])] = int(minfo_list[1])


    return data


def Data_Scene_Base(DB,UID):

    data = {}

    sql = "select Version from scenepackage where uid = " + str(UID)
    result = DB.fetchall(sql, None)
    if result:
        for minfo in result:
            minfo_list = list(minfo)

            data[int(minfo_list[0])] = int(minfo_list[1])


    return data


def UpdateToDB(DB,UID,RESID,RTYPE,DATE,INSERT):
    if not INSERT:
        if RTYPE == 0:
            sql = "update respackage set DATE = " + str(DATE) + " where UID = " + str(UID) + " and RESID = "+str(RESID)
        else:
            sql = "update scenepackage set DATE = " + str(DATE) + " where UID = " + str(UID)+ " and RESID = "+str(RESID)
    else:
        if RTYPE == 0:
            sql = "insert into respackage (UID,RESID,DATE) value("+str(UID)+","+str(RESID)+","+str(DATE)+")"
        else:
            sql = "insert into scenepackage (UID,RESID,DATE) value(" + str(UID) + "," + str(RESID) + "," + str(DATE) + ")"
    result = DB.edit(sql, None)
    if result:
        return True
    return False