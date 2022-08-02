#!/usr/bin/env python
# coding=utf-8
import hashlib
import json
import logging
import time
from datetime import datetime

from handlers.base import BaseHandler
from handlers.kbeServer.Editor.Interface import interface_sis
from methods.DBManager import DBManager


def GetSISCourse(DB, subcode, params):
    pam = params["resType"]
    if subcode == 24:
        return interface_sis.GetCourseTypeList(DB)
    elif subcode == 25:
        return interface_sis.GetCourseDetailList(DB, params)


class TSisRequest(BaseHandler):

    def get(self):

        account = self.get_argument("account")
        DB = DBManager()
        sql_str = "select createxID from tclientbindingcreatex where tclientID = '" + account + "' limit 1;"

        data = DB.fetchone(sql_str, None)
        _cxaccount = ""
        if data:
            _cxaccount = data[0]
        if _cxaccount == "":
            self.write("")
        else:
            _time = 0
            sql_str = "select ENDDATE from tclientpower where SACCOUNT = '" + account + "';"

            data = DB.fetchone(sql_str, None)
            if data:
                _time = int(data[0])
            if _time == 0 or int(time.time()) > _time:
                self.write("")
            else:
                m = hashlib.md5(_cxaccount.encode())
                result = m.hexdigest()  # 获取加密后的结果
                self.write(result)
        DB.destroy()


class AccountApkHandler(BaseHandler):  # 继承base.py中的类BaseHandler

    # 课程列表
    def get(self):

        id = self.get_argument("id")
        wt = int(self.get_argument("wt"))

        DB = DBManager()
        # 获取 工程列表
        if wt == 0:
            sql_str = "select ID from tb_account_apk where jgid = " + str(id)
        else:
            sql_str = "select ID from tb_account_apk where teacherid = '" + str(id) + "'"

        datas = DB.fetchone(sql_str, None)
        packnamne = ""
        if datas:
            if wt == 0:
                packnamne = "com.butterfly.sis"
            else:
                packnamne = "com.butfly.diy"
        DB.destroy()
        self.write(packnamne)


# apk 相关
class ApkInfoHandler(BaseHandler):
    def post(self):
        json_back = {
                "code": 0
        }
        data = self.request.body.decode('utf-8')
        now_time = (datetime.now()).strftime("%y-%m-%d")
        if isinstance(data, str):
            data = json.loads(data, strict=False)
        sql = "select t2.id from tb_empower_apk as t1 inner join tb_empower_course as t2 on t1.id = t2.apkID and t2.UID = %s and t2.PID = %s and t2.FromType = %s and t2.endtime > %s where t1.code = %s;"
        DB = DBManager()
        uid = data["uid"]
        pid = data["pid"]
        apkid = data["apkid"]
        from_type = data["fromtype"]
        m_data = DB.fetchall(sql, (uid, pid, from_type, now_time, apkid))
        if m_data:
            json_back["code"] = 1
            logging.info(f"获取到授权信息, 用户id: {data['apkid']}")
        DB.destroy()

        self.write(json_back)
