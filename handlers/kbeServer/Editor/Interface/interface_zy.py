#!/usr/bin/env python
# coding=utf-8

import time

#CLASSID    班级ID
#PID        工程ID
#CourseID   课表对应课程ID
def TaskSend(DB,self_uid,UID,CLASSID,PID,CourseID):

    #获取下班级信息
    # _classids = self.ClassID.split(',')
    # #DEBUG_MSG("TaskSend",CLASSID,PID,CourseID,_classids)
    # if str(CLASSID) not in _classids:
    #     self.client.TaskToClient(0)     #班级不存在
    #     return
    _pid = 0
    sql = "select PID,`Power` from tb_project where UID = " + str(UID) + " and PID = " + str(PID)
    data = DB.fetchone(sql, None)
    if data != None and len(data) > 0:
        _pid = int(data[0])
        _Power = int(data[1])
    if _pid == 0:
        return [-1,""]
    if _Power != 0:
        return [-6,""] #作业已经提交

    _CourseID = 0
    _start = ""
    _end = ""
    sql = "select id,start,`end` from events where ID = '" + CourseID + "';"
    data = DB.fetchone(sql, None)
    if data != None and len(data) > 0:
        _CourseID = data[0]
        _start = data[1]
        _end = data[2]
    if _CourseID == 0:
        return [-2,""] #课表不存在
    _now = time.time()
    _data = _start.replace("T", " ").replace(".000Z", "")
    timeArray = time.strptime(_data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))

    if _now < timeStamp:
        return [-3,""]  # 未到提交时间

    _data = _end.replace("T", " ").replace(".000Z", "")
    timeArray = time.strptime(_data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    if _now > timeStamp:
        return [-4,""]  # 已超过了提交时间

    _tableName = "tb_tasbase_" + str(CLASSID)
    sql = "select ID from "+_tableName+" where UID = " + str(UID) + " and PID = " + str(PID)+ " and TID = '" + str(_CourseID) + "';"
    data = DB.fetchone(sql, None)
    _ID = 0
    if data:
        _ID = int(data[0])
    if _ID != 0:
        return [-5,""]  # 已经提交过

    sql = "INSERT INTO " + _tableName + " (PID,UID,TID) values(" + str(PID) + "," + str(UID) + " ,'" + str(_CourseID) + "');"
    DB.edit(sql, None)

    sql = "update tb_project set `From`=106,`FromPam` = "+str(CLASSID)+",Version = Version + 1 where UID = "+str(UID)+" and PID = "+str(PID)+";"
    DB.edit(sql, None)


    return [1,str(PID)+","+str(CLASSID)]




#作业打分
#UID 学生UID
#CLASSID 班级ID
#课表对应的课程ID (WID)
#SCORE 分数
def TaskMark(DB,self_uid,UID,CLASSID,TID,SCORE):

    if SCORE < 1 or SCORE > 100:
        return 0    #分数异常
    # _classids = self.ClassID.split(',')
    # if str(CLASSID) not in _classids:
    #     self.client.TaskMark_ToC(-1)  # 你没有这个班级
    #     return

    _tableName = "tb_tasbase_" + str(CLASSID)
    sql = "select Score,PID from "+_tableName + " where UID = "+str(UID) + " AND TID = '"+TID+"';"
    data = DB.fetchone(sql, None)
    _SCORE = 0
    _PID = 0
    if data != None and len(data) > 0:
        _SCORE = int(data[0])
        _PID = int(data[1])
    else:
        return -2
    if _PID == 0:
        return -3     #未提交作品
    if _SCORE != -1:
        return -4     #已经打过分了

    sql = "UPDATE " + _tableName + " SET SCORE = "+str(SCORE)+" where UID = " + str(UID) + " AND TID = '" + TID + "';"
    DB.edit(sql,None)
    return 1

