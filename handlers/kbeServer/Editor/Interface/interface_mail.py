#!/usr/bin/env python
# coding=utf-8

import logging
import time

from handlers.SyncServer.SyncMain import SyncMainClass



def WriteMail(DB,uid, title, tbody):
    # DEBUG_MSG("WriteMail username : [%s] - title : [%s] - tbody : [%s]" % (username, title, tbody))
    sql = "insert into tb_message (msg_channel,msg_title,msg_body) value ("+str(uid)+",'"+title+"','"+tbody+"');"
    #print("WriteMail,",sql)
    result = DB.edit(sql, None)
    if result:
        #这里增加一个异步通知
        # 广播消息
        SyncMainClass.InsertSyncData("editor", 106, "", 0, 1, uid, "邮件通知", DB)

        return True


    return False



#获取邮件数据
def GetMail(DB, uid,data):
    json_data = {
        "code": 0,
        "msg": ""
    }

    page = ""
    userdate =  GetUsernameMailData(DB,uid)
    _cback = ""
    _Index =(int( data["page"])-1)*8
    ##print("userdate",userdate)
    sql = "select t2.ID,t2.msg_writedate,t2.msg_title,t2.msg_body,t3.RFLAG,t2.msg_talker,t2.msg_channel from (SELECT * FROM (select ID,msg_writedate,msg_title,msg_body,msg_readed,msg_talker,msg_channel from tb_message where msg_channel = 0 or msg_channel = "+str(uid)+" and msg_writedate > '"+str(userdate)+"' order by ID desc) T1 where ID NOT IN (select `MID` from tb_message_rd where uid = "+str(uid)+" and DFLAG = 1) ) t2 left join tb_message_rd t3 on t2.ID = t3.`MID` AND T3.UID = "+str(uid)+" order by t2.ID desc limit "+str(_Index)+",8"

    #sql_str =  "select ID,msg_writedate,msg_title,msg_body,msg_readed+find_in_set (ID,'"+MailDataDeletes+"') AS msg_readed,msg_talker,msg_channel from (select ID,msg_writedate,msg_title,msg_body,msg_readed,msg_talker,msg_channel from tb_message where msg_channel = 0 or msg_channel = "+str(uid)+" and msg_writedate > '"+userdate+"') t1 where not find_in_set (ID,'"+MailDataReads+"') order by msg_writedate desc limit "+str(_Index)+",8"
    ##print("sql",sql)
    readmailBool = ""
    data = DB.fetchall(sql,None)
    if data:
        for minfo_data in data:
            _flag = 0
            ##print("minfo_data[4]",minfo_data[4])
            if minfo_data[4]:
                _flag = 1
            if _cback == "":
                _cback = str(minfo_data[0]) + "`" + str(minfo_data[1]) + "`" + str(minfo_data[2]) + "`" + str(minfo_data[3]) + "`" + str(minfo_data[5])+ "`" + str(_flag)+ "`" +  str(minfo_data[6])
            else:
                _cback = _cback + "!" +  str(minfo_data[0]) + "`" +  str(minfo_data[1])+ "`" + str(minfo_data[2]) + "`" + str(minfo_data[3])  + "`" +  str(minfo_data[5]) + "`" +  str(_flag)+ "`" +  str(minfo_data[6])
        json_data["code"] = "1"
        json_data["msg"] = _cback
    else:
        json_data["code"] = "2"
        json_data["msg"] = _cback
    ##print("_cback",_cback)
    return json_data

#获取邮件已读和删除邮件ID
def GetUsernameMailData(DB,UID):
    sql_str = "select create_time from tb_userdata where uid = %s;"
    data = DB.fetchone(sql_str, UID)
    _cback = ""
    if data:
        return data[0]

    return _cback

def GetDeleteMailIDs(DB,uid):

    table_project = "tb_message"
    sql_str = "select ID from "+table_project+" where msg_channel = " + str(uid) +" and msg_readed = 1"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data != None and len(data) > 0:
        list_data = list(data)
        for minfo in list_data:
            if _cback!="":
                _cback=_cback+","+str(minfo[0])
            else:
                _cback = str(minfo[0])
    else:
        _cback = "-1"
    return _cback

def GetDeleteZeroMailIDs(DB):
    table_project = "tb_message"
    sql_str = "select ID from "+table_project+" where msg_channel = 0"

    data = DB.fetchall(sql_str,None)
    _cback = ""
    if data != None and len(data) > 0:
        list_data = list(data)
        for minfo in list_data:
            if _cback!="":
                _cback=_cback+","+str(minfo[0])
            else:
                _cback = str(minfo[0])
    else:
        _cback = "-1"
    return _cback

#更新或删除邮件数据
def UpdateMail(DB,pam, uid):
    json_data = {
        "code": 0,
        "msg": ""
    }
    #print("UpdateMail",pam,uid)
    operateType = ""
    SqlID = ""
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = "false"
        return json_data
    strlist = pam["Data"].split('*')  # 用逗号分割str字符串，并保存到列表
    operateType = strlist[0]
    SqlID = strlist[1]
    if operateType == "0":  #删除单挑
        sql = "update tb_message_rd set DFLAG = 1 WHERE UID = " + str(uid) + " and MID = " + SqlID
    elif operateType == "1":
        sql = "insert into tb_message_rd (UID,MID,RFLAG) values (" + str(uid) + "," + str(SqlID) + ",1)"
    elif operateType == "2":
        sql = "select ID FROM tb_message_rd WHERE DFLAG = 0 AND UID = " + str(uid)
        data = DB.fetchall(sql,None)
        if not data:
            json_data["code"] = "-1"
            json_data["msg"] = operateType + ","
            return json_data
        sql = "update tb_message_rd set DFLAG = 1 WHERE UID = " + str(uid)

    DB.edit(sql,None)

    json_data["code"] = "1"
    json_data["msg"] = operateType+","
    return json_data




#更新username中的删除邮件或者已读邮件
def UpdateUsernameMailData(DB,operateType, UID,ID):

    table_project = "tb_userdata"
    sql_str = ""
    MailDatas = GetUsernameMailData(DB,UID)
    strlist = MailDatas.split('*')  # 用逗号分割str字符串，并保存到列表
    if(strlist[0]!=""):
        strlist[0]=strlist[0]+","
    if (strlist[1] != ""):
        strlist[1] = strlist[1] + ","
    if operateType == "1":
        sql_str = "Update " + table_project + " set ReadMail = '"+str(strlist[0]+ID)+"' where UID = " + str(UID)
    else:
        sql_str = "Update " + table_project + " set DeleteMail = '"+str(strlist[1]+ID)+"' where UID = " + str(UID)
    try:
        DB.edit(sql_str,None)
        operateSucc = operateType+",1"
    except:
        operateSucc = operateType+",0"
    return operateSucc



#获取当前更新的邮件uid
def GetMailDataUID(DB,ID):
    table_project = "tb_message"
    sql_str = "select * from " + table_project + " where ID  = " + str(ID)

    _cback = ""
    data = DB.fetchone(sql_str,None)
    if data:
        _cback = str(data[1])
    return _cback

#公告插入邮件
def Sendnotice(DB, pam, uid):
    json_data = {
        "code": 0,
        "msg": ""
    }

    operateSucc = ""
    operateType = ""
    SqlID = ""
    if pam == "":
        json_data["code"] = "0"
        json_data["msg"] = ""
        return json_data
    table_project = "tb_message"
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql_str = "INSERT INTO " + table_project + " (msg_channel, msg_writedate, msg_title, msg_body, msg_readed, msg_talker) Values (0,'"+str(localtime)+"','系统公告','"+str(pam["pam"])+"',0,0)"
    try:
        DB.edit(sql_str,None)
    except:
        json_data["code"] = "0"
        json_data["msg"] = "false"
        return json_data

    json_data["code"] = "1"
    json_data["msg"] = "true"
    return json_data

#存储后台反馈邮件
def InsertEmilData(DB, jddata,uid):
    json_data = {
        "code": "0",
        "msg": ""
    }
    if jddata == "":
        json_data["code"] = "0"
        json_data["msg"] = "false"
        logging.info("无数据")
        return json_data

    msg_channel = str(uid)
    msg_writedate = jddata["date"]
    msg_title = jddata["title"]
    msg_body = jddata["body"]
    operateSucc = ""
    table_project = "tb_message"
    timeArray = time.localtime(msg_writedate)
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sql_str = "INSERT INTO " + table_project + " (msg_channel, msg_writedate, msg_title, msg_body, msg_readed, msg_talker) Values ('"+str(msg_channel)+"','"+str(localtime)+"','"+str(msg_title)+"','"+str(msg_body)+"',0,0)"
    DB.edit(sql_str,None)
    author_id = DB.cur.lastrowid
    logging.info("InsertEmilData author_id:" + str(author_id))
    operateSucc = InsertDataQueData(DB, author_id, msg_channel)
    if operateSucc:
        json_data["code"] = "1"
        json_data["msg"] = "true"
    else:
        json_data["msg"] = "false"
    return json_data

#插入实时通知客户端
def InsertDataQueData(DB, emilId,uid):
    APPTYPE = "editor"
    CODE = "106"
    BODY = str(emilId)
    DOSERVER = "0"
    DOCLIENT = "1"
    UID = str(uid)
    order = ""
    operateSucc = SyncMainClass.InsertSyncData(APPTYPE, CODE, BODY, DOSERVER, DOCLIENT, UID, order, DB)
    logging.info("InsertDataQueData operateSucc:" + str(operateSucc))
    return  operateSucc
