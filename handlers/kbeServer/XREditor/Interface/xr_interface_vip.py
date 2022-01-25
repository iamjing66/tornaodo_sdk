

#人名币购买作品回调
import json
import logging
import time

import Global
from handlers.SyncServer.SyncMain import SyncMainClass


def DeleteVIP(DB,username, languageStr):
    json_data = {
        "code": 0,
        "msg": "",
        "pam": ""
    }

    sql = "update tb_userdata set vippower = 0,vipdate = 0 where username = '"+username+"'"
    DB.edit(sql,None)

    json_data["code"] = 1
    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_4", languageStr)

    return json_data

def VipBuy(_order, CData, DB):
    _arr_pam = CData.split('@')
    self_uid = int(_arr_pam[6])
    sx = int(_arr_pam[14])
    if sx == 1:
        timelong = 60*60*30
    elif sx == 2:
        timelong = 60 * 60 * 30 * 3
    elif sx == 2:
        timelong = 60 * 60 * 30 * 6
    else:
        timelong = 60 * 60 * 30 * 12

    jsondata = {

    }
    sql = "select vipdate from tb_userdata where uid = " + str(self_uid) + " limit 0,1;"
    data = DB.fetchone(sql, None)
    if data:
        vipdate = int(data[0])
        if vipdate == 1:
            jsondata["Code"] = 0  #已经永久
        else:
            now = int(time.time())
            if vipdate < now:
                vipdate = now
            vipdate = vipdate + timelong

        sql = "update tb_userdate set vippower = 1,vipdate = " + str(vipdate) + " where uid = "+str(self_uid)
        data = DB.edit(sql,None)
        if data:
            SyncMainClass.InsertSyncData("xeeditor", 403,json.dump({"date":vipdate,"sx":sx}), 1, 1, self_uid, _order, DB)

    else:
        logging.info("uid[%s] buy vip Err" % str(self_uid))

