#!/usr/bin/env python
# coding=utf-8

import json
import Global
from handlers.kbeServer.Editor.Interface import interface_global


# 获取资源列表数据
# call_type 0-INI结果 1-json结构 2-list
# cversions 版本号列表(用来比对是否需要同步)
# 回调 [服务器课程列表(用来比对需要删除得课程) ,课程数据]
def Data_Objs_Base(target, db, pid, uid, p_server, call_type):
    table_obj = ""
    json_back = ""

    if target == 0:
        table_obj = "tb_obj_" + str(uid) + "_" + str(pid)
    else:
        table_obj = "tb_mobj_" + str(uid) + "_" + str(pid)
    sql = "select * from " + table_obj  # + " where bdelete = 0;"  #被删除的资源不同步
    result = db.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchall_json(result)
        else:
            if call_type == 0:
                json_back = ""
            elif call_type == 2:
                json_back = []
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                comid = int(minfo_list[20])
                version = int(minfo_list[27])

                if comid not in p_server or version > p_server[comid]:
                    if call_type == 0:
                        if json_back == "":
                            json_back = Get_Data_Obj_Base_Ini(minfo_list)
                        else:
                            json_back = json_back + "!" + Get_Data_Obj_Base_Ini(minfo_list)
                    elif call_type == 2:
                        json_back.append(Get_Data_Obj_Base_List(minfo_list))

    # 需要删除的课程(通过对比发现这些工程在本地有，但是在服务器上面没有)

    # print("Data_Courses_Base:", json_back)
    return json_back


def GetData_Objs_Ini(minfo_list):
    _ini = ""
    for info in minfo_list:
        if _ini == "":
            _ini = Get_Data_Obj_Base_Ini(info)
        else:
            _ini = _ini + "!" + Get_Data_Obj_Base_Ini(info)
    return _ini


def Get_Data_Obj_Base_Ini(minfo_list):
    if minfo_list[15] == "":
        minfo_list[15] = b''
    if minfo_list[15] is None:
        minfo_list[15] = b''
    return str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(
        minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(
        minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(
        minfo_list[13]) + "`" + minfo_list[14] + "`" + minfo_list[15].decode() + "`" + minfo_list[16] + "`" + \
           minfo_list[17] + "`" + str(minfo_list[18]) + "`" + str(minfo_list[19]) + "`" + str(minfo_list[20]) + "`" + \
           minfo_list[21] + "`" + minfo_list[22] + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + \
           minfo_list[25] + "`" + str(minfo_list[26]) + "`" + str(minfo_list[27]) + "`" + str(minfo_list[28])


def Get_Data_Obj_Base_List(minfo_list):
    if minfo_list[15] == "":
        minfo_list[15] = b''
    if minfo_list[15] is None:
        minfo_list[15] = b''
    return [str(minfo_list[1]), minfo_list[2], str(minfo_list[3]), str(minfo_list[4]), str(minfo_list[5]),
            str(minfo_list[6]), str(minfo_list[7]), str(minfo_list[8]), str(minfo_list[9]), str(minfo_list[10]),
            str(minfo_list[11]), str(minfo_list[12]), str(minfo_list[13]), minfo_list[14], minfo_list[15].decode(),
            minfo_list[16], minfo_list[17], str(minfo_list[18]), str(minfo_list[19]), str(minfo_list[20]),
            minfo_list[21], minfo_list[22], str(minfo_list[23]), str(minfo_list[24]), minfo_list[25],
            str(minfo_list[26]), str(minfo_list[27]), str(minfo_list[28])]


def GetVersion(pid, uid, db, target):
    _back = ""
    if target == 0:
        table_name = Global.GetObjTableName(uid, pid)
    else:
        table_name = Global.GetMObjTableName(uid, pid)
    # print("table_name", table_name)
    if interface_global.Global_TableExist(table_name, db):
        sql = "select ComID,Version from " + table_name
        data = db.fetchall(sql, None)
        if data:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)
                # 这里才同步
                if _back == "":
                    _back = str(minfo_list[0]) + "`" + str(minfo_list[1])
                else:
                    _back = _back + "!" + str(minfo_list[0]) + "`" + str(minfo_list[1])
    return _back


# 删除本地的工程
def Delete(db, uid, pid, ismarket):
    if ismarket == 0:
        table_name = Global.GetObjTableName(uid, pid)
    else:
        table_name = Global.GetMObjTableName(uid, pid)

    if interface_global.Global_TableExist(table_name, db):
        sql = "drop table " + str(table_name)
        db.edit(sql, None)

    return True
