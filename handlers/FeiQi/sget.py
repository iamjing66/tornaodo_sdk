#!/usr/bin/env python
# coding=utf-8

import logging
import copy
import Global
import json
from handlers.base import BaseHandler
from methods.db_mysql import DbHander



class s_clistHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #课程列表
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #获取课程列表
            sql_str = "select 0,t1.`NAME`,t1.UID,t1.CID,t1.PIC,t1.CT,t1.ZK1,t1.ZK2,t1.Platform,t2.UserName from tb_course_market as t1 inner join tb_userdata as t2 on t1.UID = t2.uid;"

            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            if lines and len(lines) > 0:
                for arr_info in lines:
                    _pos+=1
                    json_info = {
                        "CID":int(arr_info[0]),
                        "CNAME": arr_info[1],
                        "PUID": int(arr_info[2]),
                        "PCID": int(arr_info[3]),
                        "PIC": arr_info[4],
                        "CT": int(arr_info[5]),
                        "ZK1": float(arr_info[6]),
                        "ZK2":float(arr_info[7]),
                        "PLATFORM": int(arr_info[8]),
                        "PUSERNAME": arr_info[9],
                    }
                    JSON_Data[_pos] = json_info
                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data

            # BODY=====================================
            db.close()

            self.write(JSON_Bck)


class s_wlistHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #共享作品列表
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()

            #获取作品列表
            sql_str = "select T3.*,T4.UserName from (select PID  ,`Name`,uid ,`desc`,ct,SID,Wid,price2,Platform,CreateDate,stime,etime from tb_workmarket) t3 inner join tb_userdata as t4 on t3.uid = t4.UID;"
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            if lines and len(lines) > 0:
                for arr_info in lines:
                    _pos += 1
                    json_info = {
                        "PID":int(arr_info[0]),
                        "WNAME": arr_info[1],
                        "UID": int(arr_info[2]),
                        "DESC": arr_info[3],
                        "CT": int(arr_info[4]),
                        "SID": int(arr_info[5]),
                        "WID": int(arr_info[6]),
                        "PRICE2":int(arr_info[7]),
                        "PLATFORM": int(arr_info[8]),
                        "CDATE": int(arr_info[9]),
                        "STIME": str(arr_info[10]),
                        "ETIME": str(arr_info[11]),
                        "PUSERNAME": arr_info[12],
                    }
                    JSON_Data[_pos] = json_info
                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data

            # BODY=====================================
            db.close()


            self.write(JSON_Bck)


class s_pcheckHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据版本号获取
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            JDATA = json.loads(self.JData)
            gpid = int(JDATA["gpid"])
            guid = int(JDATA["guid"])
            gtype = int(JDATA["gtype"])

            table_project = ""
            table_obj = ""
            if gtype == 0:
                table_project = "tb_project"
                table_obj = "tb_obj_"+str(guid)+"_"+str(gpid)
            else:
                table_project = "tb_mproject"
                table_obj = "tb_mobj_" + str(guid) + "_" + str(gpid)
            #获取工程数据版本号
            sql_str = "select sum(v) from(select version as v from "+table_project+" where UID = "+str(guid)+" AND PID = "+str(gpid)+" union all SELECT sum(version) as v from "+table_obj+" where bdelete = 0) t;"
            Cur.execute(sql_str)
            db.commit()
            data = Cur.fetchone()
            if data != None and len(data) > 0:
                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = str(data[0])
            else:
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "工程不存在"
                JSON_Bck["Data"] = ""
            # BODY=====================================
            db.close()
            #print("s_pcheckHandler - JSON_Data : ", JSON_Bck)
            self.write(JSON_Bck)



class s_pdataHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据获取
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {
                "project":{},
                "obj":{},
                "version":0
            }

            # BODY=====================================

            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            #工程数据
            JDATA = json.loads(self.JData)
            gpid = int(JDATA["gpid"])
            guid = int(JDATA["guid"])
            gtype = int(JDATA["gtype"])

            table_project = ""
            table_obj = ""
            if gtype == 0:
                table_project = "tb_project"
                table_obj = "tb_obj_" + str(guid) + "_" + str(gpid)
            else:
                table_project = "tb_mproject"
                table_obj = "tb_mobj_" + str(guid) + "_" + str(gpid)
            # 获取工程数据版本号
            sql_str = "select PID,UID,PNAME,C_POSX,C_POSY,C_POSZ,C_RotX,C_RotY,C_RotZ,LightIntensity,LightColor,LightAngle,SID from " + table_project + " where UID = " + str(guid) + " and PID = " + str(gpid) + ";"
            Cur.execute(sql_str)
            db.commit()
            data = Cur.fetchone()
            if data != None and len(data) > 0:
                JSON_Data["project"]["PID"] = data[0]
                JSON_Data["project"]["UID"] = data[1]
                JSON_Data["project"]["PNAME"] = data[2]
                JSON_Data["project"]["C_POSX"] = data[3]
                JSON_Data["project"]["C_POSY"] = data[4]
                JSON_Data["project"]["C_POSZ"] = data[5]
                JSON_Data["project"]["C_RotX"] = data[6]
                JSON_Data["project"]["C_RotY"] = data[7]
                JSON_Data["project"]["C_RotZ"] = data[8]
                JSON_Data["project"]["LightIntensity"] = data[9]
                JSON_Data["project"]["LightColor"] = data[10]
                JSON_Data["project"]["LightAngle"] = data[11]
                JSON_Data["project"]["SID"] = data[12]
            else:
                db.close()
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "工程不存在"
                JSON_Bck["Data"] = ""
                self.write(JSON_Bck)
                return

            #获取资源数据
            sql_str = "select * from " + table_obj + " where bdelete = 0;"
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            if lines and len(lines) > 0:
                for arr_info in lines:
                    _pos += 1
                    json_info = {
                        "OBJID":int(arr_info[1]),
                        "OBJNAME": arr_info[2],
                        "CREATEDATE": int(arr_info[3]),
                        "POSX": float(arr_info[4]),
                        "POSY": float(arr_info[5]),
                        "POSZ": float(arr_info[6]),
                        "ROTEX": float(arr_info[7]),
                        "ROTEY": float(arr_info[8]),
                        "ROTEZ": float(arr_info[9]),
                        "SCALEX": float(arr_info[10]),
                        "SCALEY": float(arr_info[11]),
                        "SCALEZ": float(arr_info[12]),
                        "COMMENTS": arr_info[15].decode(),
                        "PARENTID":int(arr_info[18]),
                        "RESTYPE": int(arr_info[19]),
                        "COMID": int(arr_info[20]),
                        "FULLPATH": str(arr_info[21]),
                        "SIZEX": int(arr_info[23]),
                        "SIZEY": int(arr_info[24]),
                        "COLLIDER": int(arr_info[26]),
                        "ACTIVE": int(arr_info[13]),
                        "CONTENT": arr_info[25],
                    }
                    JSON_Data["obj"][_pos] = json_info

                sql_str = "select sum(v) from(select version as v from " + table_project + " where UID = " + str(guid) + " AND PID = " + str(gpid) + " union all SELECT sum(version) as v from " + table_obj + " where bdelete = 0) t;"
                Cur.execute(sql_str)
                db.commit()
                data = Cur.fetchone()
                if data != None and len(data) > 0:
                    JSON_Data["version"] = int(data[0])

                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data
            else:
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "资源不存在"
                JSON_Bck["Data"] = ""

            # BODY=====================================
            db.close()

            #print("JSON_Data : " , JSON_Data)
            self.write(JSON_Bck)


class s_lcheckHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #课时数据获取
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            JDATA = json.loads(self.JData)
            gcid = int(JDATA["gcid"])
            guid = int(JDATA["guid"])
            gtype = int(JDATA["gtype"])

            table_lesson = ""
            if gtype == 0:
                table_lesson = "tb_lesson_"+str(guid)+"_"+str(gcid)
            else:
                table_lesson = "tb_mlesson_" + str(guid) + "_" + str(gcid)

            #获取工程数据版本号
            sql_str = "select sum(version) from "+table_lesson+";"

            Cur.execute(sql_str)
            db.commit()
            data = Cur.fetchone()
            if data != None and len(data) > 0:
                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = str(data[0])
            else:
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "课程不存在"
                JSON_Bck["Data"] = ""
            # BODY=====================================

            db.close()
            #print(sql_str)
            self.write(JSON_Bck)



class s_ldataHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据获取
    def post(self):
        UID = self.POSTNOACCOUNT_VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {
                "ldata":{},
                "version":0
            }

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            #课时数据
            JDATA = json.loads(self.JData)
            gcid = int(JDATA["gcid"])
            guid = int(JDATA["guid"])
            gtype = int(JDATA["gtype"])

            table_lesson = ""
            if gtype == 0:
                table_lesson = "tb_lesson_" + str(guid) + "_" + str(gcid)
            else:
                table_lesson = "tb_mlesson_" + str(guid) + "_" + str(gcid)

            # 获取工程数据版本号
            sql_str = "select LID,UID,PID,PIC,`NAME`,P1,P2,P3,P4,CreateDate,`DESC`,PDATE,BUY from "+table_lesson+";"
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            if lines and len(lines) > 0:
                for arr_info in lines:
                    _pos += 1
                    json_info = {
                        "LID":int(arr_info[0]),
                        "UID": int(arr_info[1]),
                        "PID": int(arr_info[2]),
                        "PIC": arr_info[3],
                        "NAME": arr_info[4],
                        "P1": int(arr_info[5]),
                        "P2": int(arr_info[6]),
                        "P3": int(arr_info[7]),
                        "P4": int(arr_info[8]),
                        "CDATE": int(arr_info[9]),
                        "DESC": arr_info[10],
                        "PDATE": int(arr_info[11]),
                        "BUY": int(arr_info[12]),
                    }
                    JSON_Data["ldata"][_pos] = json_info

                sql_str = "select sum(version) from " + table_lesson + ";"
                Cur.execute(sql_str)
                db.commit()
                data = Cur.fetchone()
                if data != None and len(data) > 0:
                    JSON_Data["version"] = int(data[0])

                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data
            else:
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "课时不存在"
                JSON_Bck["Data"] = ""

            # BODY=====================================
            db.close()


            self.write(JSON_Bck)

