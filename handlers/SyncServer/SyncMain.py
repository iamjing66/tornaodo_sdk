#!/usr/bin/env python
# coding=utf-8

import json
import time
from handlers.SyncServer.sockect import pro_status

class SyncMain:

    def __init__(self):
        pass

    def InsertSyncData(self,pam_apptype, code, pam, doserver, doclient, uid,_order,DB):
        pro_status.trigger(pam_apptype,uid,code,pam)
        _now = int(time.time())
        sql = "INSERT INTO TB_DATAQUEUE ( `APPTYPE`,`CODE`,BODY,DOSERVER,DOCLIENT,UID,CDATE,`order` ) VALUES ('" + str(pam_apptype) + "'," + str(code) + ",'" + pam + "'," + str(doserver) + "," + str(doclient) + "," + str(uid) + "," + str(_now) + ",'"+_order+"')"
        if DB.edit(sql,None):
            return True
        return False


SyncMainClass = SyncMain()
