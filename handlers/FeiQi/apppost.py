#!/usr/bin/env python
# coding=utf-8

import logging
import copy
import Global
import json
from methods.db_mysql import DbHander


class apppost:

    #工程列表
    def App_EnterProject(self,request_data):

        JDATA = json.loads(request_data)
        uid = int(JDATA["uid"])
        pid = int(JDATA["pid"])
        ismarket = int(JDATA["ismarket"])

        p_string = self.ReadPData(pid, uid, ismarket)
        obj_string = self.ReadObjData(pid, uid, ismarket)
        p_back = str(ismarket) + "!" + p_string + "!" + obj_string

        return p_back


    def ReadPData(self,pid,uid,ismarket):
        _back = ""
        if ismarket == 0:
            table_name = "tb_project"
        else:
            table_name = "tb_mproject"

        sql = "select PID,UID,PNAME,C_POSX,C_POSY,C_POSZ,C_RotX,C_RotY,C_RotZ,LightIntensity,LightColor,LightAngle,SID from " + table_name + " where UID = " + str(uid) + " and PID = " + str(pid) + ";"
        #DEBUG_MSG("sql : " , sql)
        db = DbHander.DBREAD()
        Cur = db.cursor()
        Cur.execute(sql)
        db.commit()
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _back = str(data[0]) + "`" + str(data[1])+ "`" + data[2]+ "`" + str(data[3])+ "`" + str(data[4])+ "`" + str(data[5])+ "`" + str(data[6])+ "`" + str(data[7])+ "`" + str(data[8])+ "`" + str(data[9])+ "`" + data[10]+ "`" + data[11]+ "`" + str(data[12])
        db.close()
        return _back

    def ReadObjData(self,pid,uid,ismarket):
        _cback = ""
        if ismarket == 0:
            table_name = "tb_obj_"+str(uid)+"_"+str(pid)
        else:
            table_name = "tb_mobj_"+str(uid)+"_"+str(pid)
        sql = "select * from " + table_name + " where bdelete = 0;"
        db = DbHander.DBREAD()
        Cur = db.cursor()
        Cur.execute(sql)
        db.commit()
        data = Cur.fetchall()
        if data != None and len(data) > 0:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)
                if minfo_list[15] == None:
                    minfo_list[15] = b""
                if _cback == "":
                    _cback = str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + minfo_list[14] + "`" + minfo_list[15].decode() + "`" + minfo_list[16] + "`" + minfo_list[17] + "`" + str(minfo_list[18]) + "`" + str(minfo_list[19]) + "`" + str(minfo_list[20]) + "`" + minfo_list[21] + "`" + minfo_list[22] + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + minfo_list[25] + "`" + str(minfo_list[26])
                else:
                    _cback =_cback + "^" + str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + minfo_list[14] + "`" + minfo_list[15].decode() + "`" + minfo_list[16] + "`" + minfo_list[17] + "`" + str(minfo_list[18]) + "`" + str(minfo_list[19]) + "`" + str(minfo_list[20]) + "`" + minfo_list[21] + "`" + minfo_list[22] + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + minfo_list[25] + "`" + str(minfo_list[26])
        db.close()
        return _cback


AppInst = apppost()