#!/usr/bin/env python
# coding=utf-8

import Global
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface.interface_config import IC
from handlers.kbeServer.Editor.Interface import interface_sms
#判断表在库中是否存在
def Global_TableExist(tablename,DB):

    sql = "select COUNT(1) as count from INFORMATION_SCHEMA.TABLES where TABLE_NAME='" + tablename + "' and TABLE_SCHEMA = '" + Global.get_config.mysql_options()["database"] + "'"
    #params = [str(uid), str(cid)]
    result = DB.fetchone(sql, None)
    if result and result[0] > 0:
        #print("tableExist [%s] " % tablename)
        return True
    #print("table Not Exist [%s] " % tablename)
    return False

#是否是GN权限
def Global_IsGM(uid,DB):

    sql = "select GMSTATE from tb_userdata where UID = "+str(uid)+";"
    result = DB.fetchone(sql,None)
    if result and result[0] == 5:
        return True
    return False


#设置
def Global_SetGM(username,DB):

    sql = "update tb_userdata set GMSTATE = 5 where UserName = '"+username+"';"
    result = DB.edit(sql,None)
    if result:
        return 1
    return 0



#设置账号永久权限
def AccountPowerSet(username,DB):

    sql = "update tb_userdata set AccountPower = 1, EndDate = 1 where username = '" + username + "';"
    DB.edit(sql,None)



# ===========================================
# 制作者增加经验
# ===========================================
def AddFabricator(username,value,DB):

    if value <= 0:
        return 0

    sql = "update tb_userdata set fabricator = fabricator + " + str(value) + " where username = '"+username+"';"
    DB.edit(sql,None)
    #print(username+"-增加创作经验-"+str(value))


def NewPID(DB,UID):

    NID = 0
    sql = "select PID FROM tb_userdata WHERE uid = " + str(UID)
    result = DB.fetchone(sql,None)
    if result:
        NID = 10001 + int(result[0])
        #NID = NID + 1
        sql = "update tb_userdata set PID = PID + 1 WHERE uid = " + str(UID)
        DB.edit(sql,None)

    return NID


def NewCID(DB,UID):

    NID = 0
    sql = "select CID FROM tb_userdata WHERE uid = " + str(UID)
    result = DB.fetchone(sql,None)
    if result:
        NID = 10001 + int(result[0])
        #NID = NID + 1
        sql = "Update tb_userdata set CID = CID + 1 WHERE uid = " + str(UID)
        DB.edit(sql,None)

    return NID

def NewPIDFromUserName(DB,username):

    NID = 0
    UID = 0
    sql = "select PID,UID FROM tb_userdata WHERE UserName = '"+str(username)+"'"
    result = DB.fetchone(sql,None)
    if result:
        NID = 10001 + int(result[0])
        #NID = NID + 1
        UID = int(result[1])
        sql = "Update tb_userdata set PID = PID + 1 WHERE UserName = '"+str(username)+"'"
        DB.edit(sql,None)

    return [NID,UID]


def NewCIDFromUserName(DB,username):
    NID = 0
    UID = 0
    sql = "select CID,UID FROM tb_userdata WHERE UserName = '" + str(username) + "'"
    result = DB.fetchone(sql, None)
    if result:
        NID = 10001 + int(result[0])
        #NID = NID + 1
        UID = int(result[1])
        sql = "Update tb_userdata set CID = CID + 1 WHERE UserName = '" + str(username) + "'"
        DB.edit(sql, None)

    return [NID, UID]


def GetUserMaxID(DB, UserName):
    json_data = {
        "code": 0,
        "msg": ""
    }
    _PID = 0
    _CID = 0
    sql = "select PID,CID FROM tb_userdata WHERE UserName = '" + str(UserName)+"'"

    data = DB.fetchone(sql,None)

    if data:
        _PID = 10001 + int(data[0])
        _CID= 10001 + int(data[1])
        json_data["code"] = "1"
        json_data["msg"] = str(_PID)+"|"+str(_CID)
    else:
        json_data["code"] = "0"
        json_data["msg"] = "0"
    # BODY=====================================
    return json_data


def GetCreateMaxID(DB,subcode,UserName):
    json_data = {
        "code": 0,
        "msg": ""
    }

    _ID = []
    if subcode == 30:  # PID
        _ID = NewPIDFromUserName(DB,UserName)
    else:
        _ID = NewCIDFromUserName(DB, UserName)

    json_data["msg"] = _ID[0]+1
    json_data["code"] = "1"
    return json_data


#频道畅想
def MonthedChannel(DB,self_uid,channelID,monthID,AppType):

    if channelID not in IC.ChannelConfig:
        return 0      #频道不存在

    if monthID not in IC.ChannelZKConfig:
        return -1     #包月期限不存在

    if AppType != 0 and AppType != 1:
        return -2      #支付类型有误

    sql = "select phone from tb_userdata where uid = " + str(self_uid)
    sData = DB.fetchone(sql,None)
    if sData:
        pay_url = str(channelID) + "@" + str(monthID)  # + "$" + str(AppType) + "$" + str(self.Editor_UID)
        smsResponse = interface_sms.SendSms(3,self_uid,sData[0], pay_url)
        #print("smsResponse", smsResponse)
        return 99
    else:
        return -3      #请绑定手机号


def Test():
    DB = DBManager()
    sql = "select * from tb_userdata where uid1 = 1399"
    DB.fetchone(sql,None)

    DB.destroy()