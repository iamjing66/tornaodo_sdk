import Global
import application
from handlers.SyncServer.SyncMain import SyncMainClass
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_mail
import time,json

def writemail(DB,channel,title,body,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }
    now = int(time.time())
    sql = "insert into tb_xr_message (msg_channel,msg_title,msg_body,msg_writedate) value (" + str(channel) + ",'" + title + "','" + body + "',"+str(now)+");"
    # print("WriteMail,",sql)
    result = DB.edit(sql, None)
    if result:
        # 这里增加一个异步通知
        # 广播消息
        SyncMainClass.InsertSyncData("xreditor", 404, "", 0, 0, channel, "", DB)
        json_data["code"] = 1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_3_1", languageStr)
    else:

        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)

    return json_data


def GetNotReadMailState(DB,uid):

    userdate = interface_mail.GetUsernameMailData(DB, uid)
    # 已删
    mdeted = application.App.Redis_Mail.GetMailDet(uid)
    # 已读
    mReaded = application.App.Redis_Mail.GetMailRead(uid)
    mReadedArr = mReaded.split(',')
    #print("[mail] maxnum = ", mdeted)
    #mdeted = "2095,2094"
    sql = "select ID from (select ID,msg_writedate,msg_title,msg_body,msg_talker,msg_channel from tb_xr_message where (msg_channel = " + str(
        uid) + " or msg_channel = 0) and msg_writedate >= "+str(userdate)+" and id not in ("+mdeted+") order by id desc ) t1 ;"
    data = DB.fetchall(sql,None)
    if data:
        list_data = list(data)
        for minfo_data in list_data:
            if str(minfo_data[0]) not in mReadedArr:
                return 1
    return 0



def GetMaxMailNum(DB,uid):

    userdate = interface_mail.GetUsernameMailData(DB, uid)
    # 已删
    mdeted = application.App.Redis_Mail.GetMailDet(uid)
    print("[mail] maxnum = ", mdeted)
    #mdeted = "2095,2094"
    sql = "select count(id) from (select ID,msg_writedate,msg_title,msg_body,msg_talker,msg_channel from tb_xr_message where (msg_channel = " + str(
        uid) + " or msg_channel = 0) and msg_writedate >= "+str(userdate)+" and id not in ("+mdeted+") order by id desc ) t1 ;"
    data = DB.fetchone(sql,None)
    if data:
        return int(data[0])
    return 0

def GetMail(DB,uid,page,hnum,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    maxnum = GetMaxMailNum(DB,uid)
    print("[mail] maxnum = ",maxnum)
    if maxnum == 0:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_3_2", languageStr)
    else:
        #print("maxnum%hnum",maxnum%hnum,maxnum,hnum,maxnum/hnum,int(maxnum/hnum))
        if maxnum%hnum == 0:
            maxpage =  int(maxnum/hnum)
        else:
            maxpage = int(maxnum / hnum) + 1
        if page > maxpage:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_3_3", languageStr)
        else:

            linit = " limit "+str((page-1)*hnum)+","+str(hnum)

            userdate = interface_mail.GetUsernameMailData(DB, uid)
            #已读
            mreaded = application.App.Redis_Mail.GetMailRead(uid)
            #mreaded = "2095,2094"
            #已删
            mdeted = application.App.Redis_Mail.GetMailDet(uid)
            #mdeted = "2095,2094"
            ##print("userdate",userdate)
            print("[mail] mreaded = ", mreaded)
            print("[mail] mdeted = ", mdeted)
            json_mail = {

            }
            sql = "select t1.*,find_in_set(t1.ID,'"+mreaded+"') from (select ID,msg_writedate,msg_title,msg_body,msg_talker,msg_channel from tb_xr_message where (msg_channel = "+str(uid)+" or msg_channel = 0) and msg_writedate >= "+str(userdate)+" and id not in ("+mdeted+") order by id desc ) t1 "+linit+";"
            data = DB.fetchall(sql, None)
            if data:
                for minfo_data in data:
                    info = {
                        "ID":int(minfo_data[0]),
                        "date": int(minfo_data[1]),
                        "title": minfo_data[2],
                        "body": minfo_data[3],
                        "channel": int(minfo_data[5]),
                        "read": int(minfo_data[6]),
                    }
                    json_mail[minfo_data[0]] = info
                json_data["code"] = "1"
                json_data["msg"] = json.dumps(json_mail)
                json_data["pam"] = str(maxpage)
            else:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)

    return json_data


def ReadMail(uid,ID,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    mreaded = application.App.Redis_Mail.GetMailRead(uid)
    if len(mreaded) > 0:
        tarr = mreaded.split(',')
        if str(ID) in tarr:
            json_data["code"] = -1
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_3_4", languageStr)
        else:
            application.App.Redis_Mail.SaveMailRead(uid,ID)
            json_data["code"] = 1
            json_data["msg"] = str(ID)

    return json_data


def DetMail(uid,ID,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    mreaded = application.App.Redis_Mail.GetMailDet(uid)
    if len(mreaded) > 0:
        tarr = mreaded.split(',')
        if str(ID) in tarr:
            json_data["code"] = -1
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_3_5", languageStr)
        else:
            application.App.Redis_Mail.SaveMailDelete(uid,ID)
            json_data["code"] = 1
            json_data["msg"] = str(ID)

    return json_data


def ReadAll(DB,uid,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    mreaded = application.App.Redis_Mail.GetMailRead(uid)
    if len(mreaded) > 0:
        tarr = mreaded.split(',')
    else:
        tarr = []

    userdate = interface_mail.GetUsernameMailData(DB, uid)
    sql = "select ID from tb_xr_message where (msg_channel = "+str(uid)+" or msg_channel = 0) and msg_writedate >= "+str(userdate)+";"
    data = DB.fetchall(sql, None)
    if data:
        for minfo_data in data:
            id = str(minfo_data[0])
            if id not in tarr:
                tarr.append(id)
                application.App.Redis_Mail.SaveMailRead(uid,id)
        json_data["code"] = "1"
        json_data["msg"] = ""
    else:
        json_data["code"] = -3
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)

    return json_data


def DeleteReaded(uid,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    mreaded = application.App.Redis_Mail.GetMailRead(uid)
    if len(mreaded) > 0:
        tarr = mreaded.split(',')
    else:
        tarr = []

    mdeted = application.App.Redis_Mail.GetMailDet(uid)
    if len(mdeted) > 0:
        tarr1 = mdeted.split(',')
    else:
        tarr1 = []


    for id in tarr:
        if id not in tarr1:
            tarr1.append(id)
            application.App.Redis_Mail.SaveMailDelete(uid, id)

    json_data["code"] = 1

    return json_data