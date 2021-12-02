#!/usr/bin/env python
# coding=utf-8


def ClassSchedule(DB, pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = "false"
        return json_data
    classid = pam["Pam"]
    # &Schedule.WID, &Schedule.Chapter, &Schedule.CourseName, &Schedule.WSDate, &Schedule.WEDate, &Schedule.CourseID, &Schedule.LessonID, &Schedule.UID, &Schedule.PID, &susername, &Schedule.ID, &Schedule.SSDate, &Schedule.SEDate
    sql_str = "select * from (SELECT T3.*,T4.ID as tid,T4.`start` as tstart,t4.`end` as tend from(select t1.*,t2.UserName from (select id,chapter,courses,`start`,`end`,courseId,MlessonID,UID,PID FROM `events` WHERE scheduleId = (select scheduleId from tb_class where CID = " + str(classid) + ") and istask = 0 and mlessonId != 0 ORDER BY `end`) as t1 LEFT join tb_userdata as t2 on t1.UID = T2.UID) as T3 inner join `events` AS T4 ON t3.CourseID = t4.CourseID and t3.MLessonID = t4.MLessonID and t3.UID = t4.UID AND T3.PID = t4.PID AND T4.istask = 1 and T4.mlessonId != 0 and T4.scheduleId = (select scheduleId from tb_class where CID = " + str(classid) + ")) t5 order by `end`"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _cback != "":
                _cback = _cback + "*" + str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3]) + "," + str(minfo[4]) + "," + str(minfo[5]) + "," + str(minfo[6]) + "," + str(minfo[7]) + "," + str(minfo[8]) + "," + str(minfo[9]) + "," + str(minfo[10]) + "," + str(minfo[11]) + "," + str(minfo[12])
            else:
                _cback = str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3]) + "," + str(minfo[4]) + "," + str(minfo[5]) + "," + str(minfo[6]) + "," + str(minfo[7]) + "," + str(minfo[8]) + "," + str(minfo[9]) + "," + str(minfo[10]) + "," + str(minfo[11]) + "," + str(minfo[12])
    _cback = GetClassTeacher(DB,str(classid)) + "`" + _cback + "`" + pam["type"] + "`" + pam["Pam"]
    json_data["code"] = "1"
    json_data["msg"] = _cback
    return json_data


def GetClassTeacher(DB, classid):

    sql_str = "select UID,UserName from tb_userdata where UID = (SELECT TID from tb_class where CID = " + str(classid) + ")"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data != None and len(data) > 0:
        _cback = str(data[0][0]) + "," + str(data[0][1])

    return _cback


def StudentWork(DB, uid, pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = ""
        return json_data


    classid = pam["Pam"]
    sql_str = "select TID,WDATE,PID,SCORE from tb_tasbase_" + str(classid) + " where uid = " + str(uid)
    # &Schedule.TID, &Schedule.WDATE, &Schedule.PID, &Schedule.SCORE

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _cback != "":
                _cback = _cback + "*" + str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3])
            else:
                _cback = str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3])
    _cback = GetClassTeacher(DB,str(classid)) + "`" + _cback + "`" + pam["type"]

    json_data["code"] = "1"
    json_data["msg"] = _cback
    return json_data


def ClassStudentData(DB, uid, pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = ""
        return json_data

    classid = pam["Pam"].split(',')[0]
    TID = pam["Pam"].split(',')[1]
    # &Schedule.UID, &Schedule.WDATE, &Schedule.PID, &Schedule.SCORE, &Schedule.UserName
    sql_str = "select t1.UID,t1.WDATE,t1.PID,t1.SCORE,t2.UserName from tb_tasbase_" + str(classid) + " as t1 inner join tb_userdata as t2 on t1.UID = t2.UID AND t1.TID = '" + str(TID) + "'"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _cback != "":
                _cback = _cback + "*" + str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3]) + "," + str(minfo[4])
            else:
                _cback = str(minfo[0]) + "," + str(minfo[1]) + "," + str(minfo[2]) + "," + str(minfo[3]) + "," + str(minfo[4])

    json_data["code"] = "1"
    json_data["msg"] = _cback
    return json_data


def ClassStudentList(DB, uid, pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = ""
        return json_data

    classid = pam["Pam"]
    # &Schedule.UID, &Schedule.UserName
    sql_str = "select UID,UserName from tb_userdata where find_in_set('" + str(classid) + "',CLASSID)"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _cback != "":
                _cback = _cback + "*" + str(minfo[0]) + "," + str(minfo[1])
            else:
                _cback = str(minfo[0]) + "," + str(minfo[1])

    json_data["code"] = "1"
    json_data["msg"] = _cback
    return json_data