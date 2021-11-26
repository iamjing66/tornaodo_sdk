#!/usr/bin/env python
# coding=utf-8

import logging
import copy
import Global
from handlers.base import BaseHandler
from methods.db_mysql import DbHander

class plistHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程列表
    def get(self):
        UID = self.VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            db = DbHander.DBREAD()
            Cur = db.cursor()
            #获取 工程列表
            sql_str = "select PID,UID,PNAME,SID,HTYPE,P_UID,ParentPid,template,CreateDate from tb_project where UID = "+str(UID)+" AND Template < 10000 and template in (0,3,4) union ALL SELECT T1.PID,T1.UID,T1.PNAME,T1.SID,T1.HTYPE,T1.P_UID,T1.ParentPid,T1.template,T1.CreateDate FROM tb_project AS T1 inner join (select TID,CID+10000 AS CID FROM tb_class  AS T5 WHERE FIND_IN_SET(T5.CID, (SELECT CLASSID FROM tb_userdata where UID = "+str(UID)+" )))  as T2 ON T1.UID = T2.TID AND T1.Template = T2.CID order by CreateDate desc;"
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            if lines and len(lines) > 0:
                for arr_info in lines:
                    _pos += 1
                    json_info = {
                        "PID":int(arr_info[0]),
                        "UID": int(arr_info[1]),
                        "PNAME": arr_info[2],
                        "SID": int(arr_info[3]),
                        "HTYPE": int(arr_info[4]),
                        "PUID": int(arr_info[5]),
                        "PPID": int(arr_info[6]),
                        "TEMPLATE":int(arr_info[7]),
                        "CDATE": int(arr_info[8])
                    }
                    JSON_Data[_pos] = json_info
                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data

            # BODY=====================================


            db.close()
            self.write(JSON_Bck)

class plistINIHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程列表
    def get(self):
        UID = self.VERIFY_MAIN

        p_back = ""
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #获取 工程列表
            pdata = self.get_argument("pdata")

            p_server = {}
            if pdata != None and len(pdata) > 0:
                l_pdata = pdata.split('*')
                for info in l_pdata:
                    sdata = info.split('^')
                    uid = int(sdata[0])
                    pid = int(sdata[1])
                    version = int(sdata[2])
                    if uid not in p_server.keys():
                        p_server[uid] = {}
                    p_server[uid][pid] = version
            print("p_server", p_server)
            p_back = self.GetPDataWVersion(p_server,UID, 0)

            JSON_Bck["Code"] = 1
            JSON_Bck["Msg"] = "OK"
            JSON_Bck["Data"] = p_back
            # BODY=====================================



            self.write(JSON_Bck)

    def GetPDataWVersion(self, p_server, theuid, type=0):

        # _lback = []
        # pids = []
        _server_pid = {}
        _back = ""

        #self.db_ping
        # DEBUG_MSG("1 - p_server : [%s]" % p_server)
        db = DbHander.DBREAD()
        Cur = db.cursor()
        table_name = ""
        if type == 0:
            table_name = "tb_project"
        else:
            table_name = "tb_mproject"
        if type == 0:
            sql = "select * from tb_project where UID = " + str(theuid) + " AND Template < 10000 union ALL SELECT T1.* FROM tb_project AS T1 inner join (select TID,CID+10000 AS CID FROM tb_class AS T5 WHERE FIND_IN_SET(T5.CID, (SELECT CLASSID FROM tb_userdata where UID = " + str(theuid) + " )))  as T2 ON T1.UID = T2.TID AND T1.Template = T2.CID;"
            # sql = "select * from "+table_name+" where uid = "+str(self.databaseID)  #自由工程数据
        elif type == 1:
            sql = "select * from " + table_name + " where P_TYPE = 1"  # 课程中的工程
        elif type == 2:
            sql = "select * from " + table_name + " where P_TYPE = 0"  # 作品中的工程数据
        Cur.execute(sql)
        db.commit()
        data = Cur.fetchall()
        if len(data) > 0:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)
                # print("minfo_list",minfo_list)
                pid = int(minfo_list[1])
                _pid = pid
                version = int(minfo_list[24])
                uid = int(minfo_list[25])
                template = int(minfo_list[13])
                if type == 0 and theuid != uid:
                    pid = 10000000 + uid * 100 + pid
                # if type==0:
                #     #if int(minfo_list[26]) == 0:   #去掉这个购买判断，购买的也是出现在自有工厂
                #      pids.append([_pid,uid])  #只有自由工程
                # else:
                #     pids.append([_pid, uid])  # 只有自由工程
                if uid not in _server_pid.keys():
                    _server_pid[uid] = []
                _server_pid[uid].append(pid)
                if uid not in p_server or pid not in p_server[uid] or version > p_server[uid][pid]:
                    # 这里才同步
                    if _back == "":
                        _back = str(pid) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + str(minfo_list[14]) + "`" + minfo_list[15] + "`" + minfo_list[16] + "`" + str(minfo_list[17]) + "`" + str(minfo_list[18]) + "`" + minfo_list[19] + "`" + str(minfo_list[20]) + "`" + str(minfo_list[21]) + "`" + str(minfo_list[22]) + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + str(minfo_list[25]) + "`" + str(minfo_list[26]) + "`" + str(minfo_list[27]) + "`" + str(minfo_list[28])
                    else:
                        _back = _back + "!" + str(pid) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + str(minfo_list[14]) + "`" + minfo_list[15] + "`" + minfo_list[16] + "`" + str(minfo_list[17]) + "`" + str(minfo_list[18]) + "`" + minfo_list[19] + "`" + str(minfo_list[20]) + "`" + str(minfo_list[21]) + "`" + str(minfo_list[22]) + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + str(minfo_list[25]) + "`" + str(minfo_list[26]) + "`" + str(minfo_list[27]) + "`" + str(minfo_list[28])

        sdelete = ""
        if type == 0:
            for _c_uid in p_server.keys():
                values = p_server[_c_uid]
                for _c_pid in values.keys():
                    if _c_uid not in _server_pid or _c_pid not in _server_pid[_c_uid]:
                        if _c_uid == theuid:
                            continue
                        # 这里需要删除的工程
                        if sdelete == "":
                            sdelete = str(_c_uid) + "`" + str(_c_pid)
                        else:
                            sdelete = sdelete + "!" + str(_c_uid) + "`" + str(_c_pid)
                # DEBUG_MSG("需要删除工程：",sdelete)
        _back = _back + "！" + sdelete
        # _lback.append(pids)
        db.close()
        return _back



class clistHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #课程列表
    def get(self):
        UID = self.VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            #获取课程列表
            sql_str = "select T3.*,T4.UserName from (select T2.CID AS a,T1.`Name` as b,T1.UID as d,T1.CID as e,T1.pic as f,t1.ct,t1.ZK1,t1.ZK2,t1.Platform from tb_course_market t1 inner join tb_course_bag t2 on t2.P_CID = T1.CID AND T2.P_UID = T1.UID and t2.UID = "+str(UID)+" ) t3 left join tb_userdata as t4 on t3.d = t4.UID;"
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


class wlistHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #共享作品列表
    def get(self):
        UID = self.VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
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


class pcheckHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据版本号获取
    def get(self):
        UID = self.VERIFY_MAIN

        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            db = DbHander.DBREAD()
            Cur = db.cursor()
            gpid = self.get_argument("gpid")
            guid = self.get_argument("guid")
            gtype = int(self.get_argument("gtype"))

            table_project = ""
            table_obj = ""
            if gtype == 0:
                table_project = "tb_project"
            else:
                table_project = "tb_mproject"
            #获取工程数据版本号
            sql_str = "select version from "+table_project+" where UID = "+str(guid)+" AND PID = "+str(gpid)
            print("sql_str : ", sql_str)
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


            #print(sql_str)
            db.close()
            self.write(JSON_Bck)


class pdataHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据获取
    def get(self):
        UID = self.VERIFY_MAIN
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
            gpid = self.get_argument("gpid")
            guid = self.get_argument("guid")
            gtype = int(self.get_argument("gtype"))

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
                JSON_Data["Code"] = 0
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
                        "COLLIDER": int(arr_info[26])
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
                JSON_Data["Code"] = 0
                JSON_Bck["Msg"] = "资源不存在"
                JSON_Bck["Data"] = ""

            # BODY=====================================

            db.close()

            self.write(JSON_Bck)


class pdataIniHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据获取
    def get(self):
        UID = self.VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = ""

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()
            #工程数据
            gpid = self.get_argument("gpid")
            guid = self.get_argument("guid")
            gtype = int(self.get_argument("gtype"))

            type1 = self.get_argument("type1")
            type2 = self.get_argument("type2")
            type3 = self.get_argument("type3")

            JSON_Data = str(gpid)+"！"+str(guid)+"！"+str(gtype)+"！"

            table_project = ""
            table_obj = ""
            data_project = ""
            data_obj = ""
            _version = 0
            if gtype == 0:
                table_project = "tb_project"
                table_obj = "tb_obj_" + str(guid) + "_" + str(gpid)
            else:
                table_project = "tb_mproject"
                table_obj = "tb_mobj_" + str(guid) + "_" + str(gpid)
            # 获取工程数据版本号
            sql_str = "select * from " + table_project + " where UID = " + str(guid) + " and PID = " + str(gpid) + ";"
            Cur.execute(sql_str)
            db.commit()
            minfo_list = Cur.fetchone()
            if minfo_list != None and len(minfo_list) > 0:
                _version = int(minfo_list[24])
                data_project = _back = str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + str(minfo_list[14]) + "`" + minfo_list[15] + "`" + minfo_list[16] + "`" + str(minfo_list[17]) + "`" + str(minfo_list[18]) + "`" + minfo_list[19] + "`" + str(minfo_list[20]) + "`" + str(minfo_list[21]) + "`" + str(minfo_list[22]) + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24])+ "`" + str(minfo_list[25])+ "`" + str(minfo_list[26])+ "`" + str(minfo_list[27])+ "`" + str(minfo_list[28])
            else:
                db.close()
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "工程不存在"
                JSON_Data = JSON_Data + + str(_version) + "！" + str(type1) + "！" + str(type2) + "！" + str(type3) + "！" + data_project + "！" + data_obj
                JSON_Bck["Data"] = JSON_Data
                self.write(JSON_Bck)
                return

            #获取资源数据
            sql_str = "select * from " + table_obj + " where bdelete = 0;"
            Cur.execute(sql_str)
            db.commit()
            lines = Cur.fetchall()
            _pos = 0
            _cback = ""
            if lines and len(lines) > 0:
                for minfo_list in lines:
                    if _cback == "":
                        _cback = str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + minfo_list[14] + "`" + minfo_list[15].decode() + "`" + minfo_list[16] + "`" + minfo_list[17] + "`" + str(minfo_list[18]) + "`" + str(minfo_list[19]) + "`" + str(minfo_list[20]) + "`" + minfo_list[21] + "`" + minfo_list[22] + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + minfo_list[25] + "`" + str(minfo_list[26]) + "`" + str(minfo_list[27]) + "`" + str(minfo_list[28])
                    else:
                        _cback = _cback + "!" + str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + str(minfo_list[7]) + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + minfo_list[14] + "`" + minfo_list[15].decode() + "`" + minfo_list[16] + "`" + minfo_list[17] + "`" + str(minfo_list[18]) + "`" + str(minfo_list[19]) + "`" + str(minfo_list[20]) + "`" + minfo_list[21] + "`" + minfo_list[22] + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + minfo_list[25] + "`" + str(minfo_list[26]) + "`" + str(minfo_list[27]) + "`" + str(minfo_list[28])
                if _cback != "":
                    data_obj = str(gpid) + "^" + str(guid) + "^" + _cback

                # sql_str = "select sum(v) from(select version as v from " + table_project + " where UID = " + str(guid) + " AND PID = " + str(gpid) + " union all SELECT sum(version) as v from " + table_obj + " where bdelete = 0) t;"
                # self.Cur.execute(sql_str)
                # self.db.commit()
                # data = self.Cur.fetchone()
                # if data != None and len(data) > 0:
                #     JSON_Data = JSON_Data +str(data[0])+"！"

                JSON_Data = JSON_Data + str(_version) + "！" + str(type1) + "！" + str(type2) + "！" + str(type3) + "！" + data_project + "！" + data_obj

                JSON_Bck["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = JSON_Data
            else:
                JSON_Bck["Code"] = 0
                JSON_Bck["Msg"] = "资源不存在"
                JSON_Data = JSON_Data + str(_version) + "！" + str(type1) + "！" + str(type2) + "！" + str(type3) + "！" + data_project + "！" + data_obj
                JSON_Bck["Data"] = JSON_Data

            # BODY=====================================
            db.close()


            self.write(JSON_Bck)




class lcheckHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #课时数据获取
    def get(self):
        UID = self.VERIFY_MAIN
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}

            # BODY=====================================
            #self.db_ping
            db = DbHander.DBREAD()
            Cur = db.cursor()

            gcid = self.get_argument("gcid")
            guid = self.get_argument("guid")
            gtype = int(self.get_argument("gtype"))

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
                JSON_Data["Code"] = 1
                JSON_Bck["Msg"] = "OK"
                JSON_Bck["Data"] = str(data[0])
            else:
                JSON_Data["Code"] = 0
                JSON_Bck["Msg"] = "课程不存在"
                JSON_Bck["Data"] = ""
            # BODY=====================================


            #print(sql_str)
            db.close()
            self.write(JSON_Bck)



class ldataHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程数据获取
    def get(self):
        UID = self.VERIFY_MAIN
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
            gcid = self.get_argument("gcid")
            guid = self.get_argument("guid")
            gtype = int(self.get_argument("gtype"))

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
                JSON_Data["Code"] = 0
                JSON_Bck["Msg"] = "课时不存在"
                JSON_Bck["Data"] = ""

            # BODY=====================================
            db.close()


            self.write(JSON_Bck)