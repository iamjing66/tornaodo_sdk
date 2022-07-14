#!/usr/bin/env python
# coding=utf-8

import Global
import logging
from handlers.kbeServer.Editor.Interface import interface_global


# ===================================================================================
# ================================下面是新接口=======================================
# ===================================================================================

# 获取作品列表数据
# call_type 0-INI结果 1-json结构
# cversions 版本号列表(用来比对是否需要同步)
# 回调 [服务器课程列表(用来比对需要删除得课程) ,课程数据]
def Data_Lessons_Base(sql, db, cid, uid, lversions, call_type, iupdate=0):
    _lid_strs = ""
    json_back = ""
    result = db.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchall_json(result, 1)
        else:
            if call_type == 0:
                json_back = ""
            elif call_type == 2:
                json_back = []
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                lid = int(minfo_list[1])
                obj_dic = {}
                if uid in lversions.keys():
                    if cid in lversions[uid].keys():
                        str_p = lversions[uid][cid]
                        l_pdata = str_p.split('!')
                        for str_p_i in l_pdata:
                            d_data = str_p_i.split('`')
                            obj_dic[int(d_data[0])] = int(d_data[1])

                version = int(minfo_list[17])
                # 63^6^9^1`7!2`7!3`7!4`7!5`7!6`7!7`7!8`7*
                if len(obj_dic) > 0 and lid in obj_dic and version <= obj_dic[lid]:
                    continue
                if call_type == 0:
                    if json_back == "":
                        json_back = Get_Data_Lesson_Base_Ini(minfo_list)
                    else:
                        json_back = json_back + "!" + Get_Data_Lesson_Base_Ini(minfo_list)
                elif call_type == 2:
                    json_back.append(Get_Data_Lesson_Base_List(minfo_list))
    # 需要删除的课程(通过对比发现这些工程在本地有，但是在服务器上面没有)

    return json_back


def UpdateVersion(db, cid, uid, lid, version):
    sql = "update " + Global.GetLessonTableName(uid, cid) + " set version = " + str(version) + " where lid = " + str(
        lid)
    db.edit(sql, None)


# 课时最小基础数据(唯一结构)
def Get_Data_Lesson_Base_Ini(minfo_list):
    return "`".join([str(i) for i in minfo_list[1:]])


# 课时最小基础数据(唯一结构)
def Get_Data_Lesson_Base_List(minfo_list):
    return list(map(str, minfo_list[1:]))


# 课时最小基础数据(唯一结构)
def Get_Data_Lesson_Base_ListToIni(minfo_list):
    return "`".join([str(i) for i in minfo_list])


# 课时最小基础数据(唯一结构)
def Get_Data_Lesson_Base_JsonToIni(minfo_list):
    return "`".join(str(i) for i in minfo_list.values())


# 获取课时基础数据
def Data_Lesson_Base(uid, cid, target, db, call_type, xyHide=0):
    if target == 1:
        table_name = Global.GetMLessonTableName(uid, cid)  # 不包含下架的
        if xyHide == 0:
            sql = "select * from " + table_name + " where LID not in (select mlessonId from sys_course_res where uid = " + str(
                uid) + " and cid = " + str(cid) + " and flag = 0);"
        else:
            sql = "select * from " + table_name + " where buy = 0 and LID not in (select mlessonId from sys_course_res where uid = " + str(
                uid) + " and cid = " + str(cid) + " and flag = 0);"
        # params = [str(uid),str(cid)]
    else:
        table_name = Global.GetLessonTableName(uid, cid)
        sql = "select * from " + table_name + ";"

    return Data_Lessons_Base(sql, db, cid, uid, {}, call_type)


def GetLessonSQLFromType(itype, uid, cid, p_uid, p_cid, teacher=0, power=None, organization=None):
    if itype == 0:
        sql = "select * from " + Global.GetLessonTableName(uid, cid)
    elif itype == 1:
        sql_yinliu = ""
        if power == 4:
            sql_yinliu = " and t2.courseType = 3"
        if teacher == 1 or power == 4:
            sql = f"""
            select t1.`ID`,t1.`Lid`, t1.`Name`,t1.`Platform`,t1.`Stars`,
            t1.`Pid`,t1.`pic`,t1.`aim`,t1.`desc`,t1.`UID`,t1.`CreateDate`,
            t1.`p1`,t1.`p2`,t1.`p3`,t1.`p4`,t1.`Price`,t1.`Vision`,t1.`Version`,
            t1.`PriceAll`,UNIX_TIMESTAMP(t2.enddate) as pdata,t1.`buy`,t1.Sort
            from {Global.GetMLessonTableName(p_uid, p_cid)} as t1
            inner join tb_course_pool as t2 on
            t1.UID = t2.uid and
            t1.Lid = t2.lid and
            t2.cid = {p_cid} and
            t2.organization = {organization}{sql_yinliu};
            """
        else:
            sql = "select t1.`ID`,t1.`Lid`,t2.`Name`,t2.`Platform`,t2.`Stars`,t2.`Pid`,t2.`pic`,t2.`aim`,t2.`desc`,t2.`UID`,t1.`CreateDate`,t1.`p1`,t1.`p2`,t1.`p3`,t1.`p4`,t2.`Price`,t1.`Vision`,t1.`Version`,t2.`PriceAll`,t1.`PDate`,t1.`buy`,t1.Sort from " + Global.GetLessonTableName(
                uid, cid) + " t1 inner join " + Global.GetMLessonTableName(p_uid, p_cid) + " t2 on t1.LID = t2.LID;"
    elif itype == 2:
        sql = "select * from " + Global.GetMLessonTableName(uid, cid)
    elif itype == 3:
        sql = "select * from " + Global.GetLessonTableName(uid, cid)

    return sql


# itype 0-本地制作 1-购买课程 2-课程市场 3-审核课程
def GetLessonSQLFromTypeNew(itype, uid, cid, p_uid, p_cid, teacher=0, power=None, organization=None):
    if itype == 0:
        sql = "select * from " + Global.GetLessonTableName(uid, cid)
    elif itype == 1:
        sql_yinliu = ""
        if power == 4:
            sql_yinliu = " and t2.courseType = 3"
        if teacher == 1 or power == 4:
            sql = f"""
            select t1.`ID`,t1.`Lid`, t1.`Name`,t1.`Platform`,t1.`Stars`,
            t1.`Pid`,t1.`pic`,t1.`aim`,t1.`desc`,t1.`UID`,t1.`CreateDate`,
            t1.`p1`,t1.`p2`,t1.`p3`,t1.`p4`,t1.`Price`,t1.`Vision`,t1.`Version`,
            t1.`PriceAll`,UNIX_TIMESTAMP(t2.enddate) as pdata,t1.`buy`,t1.Sort
            from {Global.GetMLessonTableName(p_uid, p_cid)} as t1
            inner join tb_course_pool as t2 on
            t1.UID = t2.uid and
            t1.Lid = t2.lid and
            t2.cid = {p_cid} and
            t2.organization = {organization}{sql_yinliu};
            """
        else:
            sql = "select t1.`ID`,t1.`Lid`,t2.`Name`,t2.`Platform`,t2.`Stars`,t2.`Pid`,t2.`pic`,t2.`aim`,t2.`desc`,t2.`UID`,t1.`CreateDate`,t1.`p1`,t1.`p2`,t1.`p3`,t1.`p4`,t2.`Price`,t1.`Vision`,t1.`Version`,t2.`PriceAll`,t1.`PDate`,t2.`buy`,t2.Sort from " + Global.GetLessonTableName(
                uid, cid) + " t1 inner join " + Global.GetMLessonTableName(p_uid,
                                                                           p_cid) + " t2 on t1.LID = t2.LID order by t2.sort;"
    elif itype == 2:
        sql = "select * from " + Global.GetMLessonTableName(uid, cid)
    elif itype == 3:
        sql = "select * from " + Global.GetLessonTableName(uid, cid)

    return sql


def UpdateToDB(db, c_pdata, _del_data, cid, uid, target):
    arr_pids = []

    if target == 0:
        table_name = Global.GetLessonTableName(uid, cid)
    else:
        table_name = Global.GetMLessonTableName(uid, cid)
    if not interface_global.Global_TableExist(table_name, db):
        sql = "CREATE TABLE " + table_name + " like tb_lesson_bag;"
        db.edit(sql, None)

    if _del_data != "":
        sql = "DELETE FROM " + table_name + " WHERE LID in (" + str(_del_data) + ")"
        db.edit(sql, None)

        # DEBUG_MSG("l_pdata", c_pdata)
    l_pdata = c_pdata.split('!')
    for info in l_pdata:
        if info == "" or len(info) == 0:
            continue
        list_lesson_base = info.split('`')
        sql = "select Lid,PID from " + table_name + " where UID = " + str(uid) + " and LID = " + str(
            list_lesson_base[0])
        arr_pids.append([uid, list_lesson_base[4]])
        result = db.fetchone(sql, None)
        if result:
            sql = "Update " + table_name + " set  `Name`='" + str(list_lesson_base[1]) + "', Platform=1, Stars=" + str(
                list_lesson_base[3]) + ", Pid=" + str(list_lesson_base[4]) + ", pic='" + str(
                list_lesson_base[5]) + "', `aim`='" + str(list_lesson_base[6]) + "', `desc`='" + str(
                list_lesson_base[7]) + "', CreateDate=" + str(list_lesson_base[9]) + ", p1=" + str(
                list_lesson_base[10]) + ", p2=" + str(list_lesson_base[11]) + ", p3=" + str(
                list_lesson_base[12]) + ", p4=" + str(list_lesson_base[13]) + ", `Price`=" + str(
                list_lesson_base[14]) + ", Vision=" + str(list_lesson_base[15]) + ",Version=" + str(
                list_lesson_base[16]) + ",PriceAll=" + str(list_lesson_base[17]) + ",PDate=" + str(
                list_lesson_base[18]) + ",buy=" + str(list_lesson_base[19]) + ",Sort=" + str(
                list_lesson_base[20]) + " WHERE LID = " + str(list_lesson_base[0]) + " and UID = " + str(uid)
        else:
            sql = "INSERT INTO " + table_name + " (`Lid`,`Name`,`Platform`,`Stars`,`Pid`,`pic`,`aim`,`desc`,`UID`,`CreateDate`,`p1`,`p2`,`p3`,`p4`,`Price`,`Vision`,`Version`,PriceAll,PDate,buy,Sort) VALUES (" + str(
                list_lesson_base[0]) + ",'" + str(list_lesson_base[1]) + "',1," + str(list_lesson_base[3]) + "," + str(
                list_lesson_base[4]) + ",'" + str(list_lesson_base[5]) + "','" + str(list_lesson_base[6]) + "','" + str(
                list_lesson_base[7]) + "'," + str(uid) + "," + str(list_lesson_base[9]) + "," + str(
                list_lesson_base[10]) + "," + str(list_lesson_base[11]) + "," + str(list_lesson_base[12]) + "," + str(
                list_lesson_base[13]) + "," + str(list_lesson_base[14]) + "," + str(list_lesson_base[15]) + "," + str(
                list_lesson_base[16]) + "," + str(list_lesson_base[17]) + "," + str(list_lesson_base[18]) + "," + str(
                list_lesson_base[19]) + "," + str(list_lesson_base[20]) + ")"
        db.edit(sql, None)
    return arr_pids


def CopyToDB_New(db, cid, uid, target, pcid, puid, ptarget):
    arr_pids = []

    if target == 0:
        table_name = Global.GetLessonTableName(uid, cid)
    else:
        table_name = Global.GetMLessonTableName(uid, cid)

    if ptarget == 0:
        ptable_name = Global.GetLessonTableName(puid, pcid)
    else:
        ptable_name = Global.GetMLessonTableName(puid, pcid)

    if interface_global.Global_TableExist(table_name, db):
        sql = "delete from " + table_name + ";"
        db.edit(sql, None)
    else:
        sql = "CREATE TABLE " + table_name + " like tb_lesson_bag;"
        db.edit(sql, None)

    # 复制课时表
    sql = "insert into " + table_name + " select * from " + ptable_name + ";"
    db.edit(sql, None)

    sql = "select uid,pid from " + table_name + " where buy = 0;"
    data = db.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            arr_pids.append([minfo_list[0], minfo_list[1]])

    return arr_pids


def GetVersion(cid, uid, target, db):
    _back = ""
    if target == 0:
        table_name = Global.GetLessonTableName(uid, cid)
    else:
        table_name = Global.GetMLessonTableName(uid, cid)

    sql = "select Lid,Version from " + table_name
    data = db.fetchall(sql, None)
    l1 = []
    if data:
        for minfo in data:
            s1 = "`".join(minfo)
            l1.append(s1)
        _back = "!".join(l1)
    return _back
