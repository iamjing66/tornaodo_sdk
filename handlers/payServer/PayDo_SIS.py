#!/usr/bin/env python
# coding=utf-8

import json
import time
import Global
from methods.SolrInterface import SolrInst
from methods.db_mysql import DbHander
from handlers.kbeServer.Editor.Interface import interface_sis


class paydo_sis:

    def __init__(self):
        pass

    def Get_EduProject(self, VID, UID, Cur, Db):

        _back = []

        sql = "select t3.coursePrice,t3.courseYearPrice,t3.courseExpireTime,t3.`name` from (select t1.coursePrice,t1.courseYearPrice,t2.courseExpireTime,t1.courseId,t2.userId,t1.`name` from new_coursedetails as t1 left join new_coursebuy as t2 on t1.courseId = t2.courseId and t2.userId = " + str(
            UID) + ") t3 where t3.courseId = '" + VID + "' order by t3.courseExpireTime desc  limit 0,1;"

        Cur.execute(sql)
        Db.commit()
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _back.append(data[0])
            _back.append(data[1])
            _back.append(data[2])
            _back.append(data[3])
        return _back

    def Do(self, _arr_pam, DB):

        _order = _arr_pam[3]
        pname = _arr_pam[5]
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        CourseID = _arr_pam[8]
        BType = int(_arr_pam[9])

        organization = _arr_pam[10]
        distributor = _arr_pam[11]
        _from = _arr_pam[12]
        _userType = int(_arr_pam[13])
        _ip = _arr_pam[15]

        dataarr = interface_sis.VR_MK_SIS(DB, UID, CourseID, 2, 20, UserName, phone=True)
        toclient = ""
        if dataarr[0] == 1:
            toclient = dataarr[1]

        return toclient

    def Get_SISNGEduProject(self, VID, UID, Cur, Db):

        _back = []

        sql = "select ID,courseExpireTime from user_coursebuy where ActivationCode = '" + UID + "' and courseID = '" + str(VID) + "';"

        Cur.execute(sql)
        Db.commit()
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _back.append(data[0])
            _back.append(data[1])
        return _back

    def DoSISNG(self, _arr_pam):

        _order = _arr_pam[3]
        # pname = _arr_pam[5]
        UID = _arr_pam[6]
        # UserName = _arr_pam[7]
        CourseID = _arr_pam[8]
        # BType = int(_arr_pam[9])

        # organization = _arr_pam[10]
        # distributor = _arr_pam[11]
        _from = _arr_pam[12]
        Db = DbHander.SISDBREAD()
        Cur = Db.cursor()
        toclient = ""
        _now = int(time.time())
        # print(UID,CourseID,_from,Cur,Db)
        w_data = self.Get_SISNGEduProject(CourseID, UID, Cur, Db)

        _insert = 0
        enddate = None

        if len(w_data) > 0:
            _insert = w_data[0]
            enddate = w_data[1]

        if enddate == None:
            _pdate = _now
        else:
            timeArray = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
            _pdate = int(time.mktime(timeArray))

        if _pdate < _now:
            _pdate = _now
        # 时间改成固定一个月
        _pdate = _pdate + Global.COURSE_BUY_SIS_TIMELONG

        timeArray = time.localtime(_now)
        _date1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        timeArray1 = time.localtime(_pdate)
        _date2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)

        # ActivationCode,courseID,orderid,courseExpireTime
        if _insert == 0:
            sql = "INSERT INTO `user_coursebuy`(`ActivationCode`,`courseID`,`courseExpireTime`)VALUES('" + str(UID) + "','" + CourseID + "','" + str(_date2) + "');"
        else:
            sql = "update `user_coursebuy` set courseExpireTime = '" + _date2 + "' WHERE ID = " + str(_insert)

        Cur.execute(sql)
        Db.commit()
        Db.close()

    def Get_SISDirectNum(self, ptype, uid, cid, lid, wid, sis_username, cx_username, Cur, Db):

        _back = 0

        # `techerAccount`,`cxAccount`,`pType`,`uid`,`pid`,`wid`,`cid`,`lid`,`buyCount`
        if ptype == "2":
            sql = "select ID from tclientbuycxproj where uid = '" + str(uid) + "' and wid = '" + str(wid) + "' and techerAccount = '" + sis_username + "' and cxAccount = '" + cx_username + "';"
        else:
            sql = "select ID from tclientbuycxproj where uid = '" + str(uid) + "' and cid = '" + str(cid) + "' and lid = '" + str(
                lid) + "' and techerAccount = '" + sis_username + "' and cxAccount = '" + cx_username + "';"

        Cur.execute(sql)
        Db.commit()
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _back = int(data[0])
        return _back

    def DoSISDirectNum(self, _arr_pam):

        # str(paydata["puid"]) + "@" + str(paydata["cid"]) + "@" + str(paydata["lid"]) + "@" + str(paydata["wid"]) + "@" + str(paydata["buyCount"])

        sis_username = _arr_pam[7]
        cx_username = _arr_pam[6]

        UID = _arr_pam[13]
        cid = _arr_pam[14]
        lid = _arr_pam[15]
        wid = _arr_pam[16]
        buycount = _arr_pam[17]
        ptype = _arr_pam[18]

        Db = DbHander.SISDBREAD()
        Cur = Db.cursor()
        _now = int(time.time())
        # print(_arr_pam)
        _insert = self.Get_SISDirectNum(ptype, UID, cid, lid, wid, sis_username, cx_username, Cur, Db)

        # ActivationCode,courseID,orderid,courseExpireTime,techerAccount, cxAccount
        if _insert == 0:
            sql = "INSERT INTO `tclientbuycxproj`(`techerAccount`,`cxAccount`,`pType`,`uid`,`cid`,`lid`,`wid`,`buyCount`)VALUES('" + sis_username + "','" + cx_username + "','" + ptype + "','" + UID + "','" + cid + "','" + lid + "','" + wid + "'," + buycount + ");"
        else:
            sql = "update `tclientbuycxproj` set buyCount = buyCount + " + buycount + " WHERE ID = " + str(_insert)
        # print("sql" , sql)
        Cur.execute(sql)
        Db.commit()
        Db.close()


PayDoSisClass = paydo_sis()
