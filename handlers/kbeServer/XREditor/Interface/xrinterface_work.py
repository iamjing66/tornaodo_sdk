import hashlib
import json
import time

from handlers.SyncServer.SyncMain import SyncMainClass
from handlers.SyncServer.sockect import pro_status
from handlers.kbeServer.Editor.Interface import interface_wit
import requests

import Global
from handlers.kbeServer.XREditor.data import xr_data_work
from handlers.kbeServer.XREditor.Interface import interface_account
import application
import logging



#新建作品(自由创作)
def NewWork(DB,uid,wname,sid,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    #这里要判断这个用户是否可以创建作品

    #新建工程
    code = xr_data_work.CreateWork(DB,uid,wname,sid,101,0,0,0)
    if code < 1:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_1",languageStr)
    else:
        json_data["code"] = 1
        data = xr_data_work.GetDatas(DB,5,0,0,uid,code)
        if not data:
            json_data["msg"] = ""
        else:
            json_data["msg"] = json.dumps(data)

    return json_data


#设为模板
def Template(DB,self_uid,pid,flag,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    #
    workData = xr_data_work.GetData(DB,0,0,self_uid,pid,0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    elif workData["from"] == 104:
        json_data["code"] = -4
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_23", languageStr)
    else:
        if flag == 1:
            if workData["template"] == 1:
                json_data["code"] = -2
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_3", languageStr)
            else:
                sql = "update tb_xr_worklocal set template = 1 where uid = "+str(self_uid) + " and pid = "+str(pid)
                data = DB.edit(sql,None)
                if not data:
                    json_data["code"] = -3
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)
                else:
                    json_data["code"] = 1
                    json_data["pam"] = str(flag)
                    json_data["msg"] = str(pid)
        else:
            if workData["template"] == 0:
                json_data["code"] = -2
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_4", languageStr)
            else:
                sql = "update tb_xr_worklocal set template = 1 where uid = "+str(self_uid) + " and pid = "+str(pid)
                data = DB.edit(sql,None)
                if not data:
                    json_data["code"] = -3
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)
                else:
                    json_data["code"] = 1
                    json_data["pam"] = str(flag)
                    json_data["msg"] = str(pid)


    return json_data


def TemplateNewWork(DB,self_uid,pid,wname,languageStr):

    #回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    #作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    elif workData["from"] == 104:
        json_data["code"] = -4
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_23", languageStr)
    else:
        if workData["template"] != 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_4", languageStr)
        else:
            code = xr_data_work.CreateWork(DB, self_uid, wname, 0, 102, self_uid , pid, 0)
            if code < 1:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_1", languageStr)
            else:
                json_data["code"] = 1
                data = xr_data_work.GetDatas(DB, 7, 0, 0, self_uid, code)
                if not data:
                    json_data["msg"] = ""
                else:
                    json_data["msg"] = json.dumps(data)


    return json_data

#转移作品
def transferWork(DB,self_uid,pid,wname,username,flag,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    elif workData["from"] == 104:
        json_data["code"] = -4
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_23", languageStr)
    else:
        uid = interface_account.JugeUserExist(DB,username)
        if  uid == 0:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_16", languageStr)
        else:

            code = xr_data_work.CreateWork(DB, uid, wname, 0, 103, self_uid, pid, flag)
            if code < 1:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_5", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = ""

                #异步通知转移成功
                pro_status.syncTrigger("xreditor", uid, 407, json.dump(xr_data_work.GetDatas(DB,6,0,0,uid,code)))


    return json_data


#发布
def Publish(DB,self_uid,pid,wname,classiy,platform,price,tab,desc,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["state"] == 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_8", languageStr)
        elif workData["from"] == 104:
            json_data["code"] = -4
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_23", languageStr)
        else:
            code = xr_data_work.Publish(DB,self_uid,pid,wname,classiy,platform,price,tab,desc)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_9", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = ""


    return json_data


#取消发布
def CancelPublish(DB,self_uid,pid,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        mworkdata = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 1)
        if mworkdata:
            if mworkdata["publish"] == 1:
                json_data["code"] = -4
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_32", languageStr)
                return json_data
        if workData["publish"] == 0:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_29", languageStr)
        else:
            code = xr_data_work.CancelPublish(DB,self_uid,pid)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_9", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = ""


    return json_data



#下架作品
def MarketOff(DB,self_uid,pid,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 1)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["publish"] == 0:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_30", languageStr)
        else:
            code = xr_data_work.MarketOff(DB,self_uid,pid)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_9", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = str(self_uid)+"_"+str(pid)


    return json_data


#上架作品
def MarketOn(DB,self_uid,pid,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 1)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["publish"] == 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_31", languageStr)
        else:
            code = xr_data_work.MarketOn(DB,self_uid,pid)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_9", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = json.dumps(xr_data_work.GetDatas(DB,9,0,0,self_uid,pid))


    return json_data



def AlterName(DB,self_uid,pid,wname,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["state"] == 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_8", languageStr)
        else:
            code = xr_data_work.AlterName(DB,self_uid,pid,wname)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_12", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_11", languageStr)


    return json_data



def DeleteWork(DB,self_uid,pid,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["state"] == 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_8", languageStr)
        else:
            code = xr_data_work.DeleteWork(DB, self_uid, pid,0)
            if code == 0:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_13", languageStr)
            else:
                json_data["code"] = 1
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_14", languageStr)

    return json_data


#审核列表
def SHList(DB,self_uid,page,num,languageStr):

    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    lineget = num
    maxpage = 0
    maxline = xr_data_work.MaxSHPage(DB)
    if maxline == 0:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_15", languageStr)
    else:
        if maxline%lineget == 0:
            maxpage = int(maxline/lineget)
        else:
            maxpage = int(maxline / lineget) + 1

        if page > maxpage:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_16", languageStr)

        data = xr_data_work.GetDatas(DB,0,page,lineget)
        if not data:
            json_data["code"] = -3
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_17", languageStr)
        else:
            json_data["code"] = 1
            json_data["msg"] = json.dumps(data)
            json_data["pam"] = maxpage

    return json_data


#审核作品
def SHWork(DB,uid,pid,state,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["state"] != 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_18", languageStr)
        else:
            code = xr_data_work.SHWork(DB, uid, pid, state)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_19", languageStr)
            else:

                #审核通过发布到市场
                if state == 1:
                    code = xr_data_work.PushInMarket(DB,uid,pid)
                    if not code:
                        json_data["code"] = -4
                        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_21", languageStr)
                    else:
                        json_data["code"] = 1
                        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_20", languageStr)
                else:
                    json_data["code"] = 1
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_22", languageStr)
    return json_data


def Market(DB,flag,languageStr):

    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }


    if flag == 0:
        type = 1
    else:
        type = 2

    data = xr_data_work.GetDatas(DB, type , 0, 0)
    if not data:
        json_data["code"] = 1
        json_data["msg"] = ""
    else:
        json_data["code"] = 1
        json_data["msg"] = json.dumps(data)

    return json_data

def MyWorks(DB,uid,languageStr):

    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }


    data = xr_data_work.GetDatas(DB, 3 , 0, 0,uid)
    if not data:
        json_data["code"] = 1
        json_data["msg"] = ""
    else:
        json_data["code"] = 1
        json_data["msg"] = json.dumps(data)

    return json_data

#购买作品-购买的作品只能看不能编辑
def Buy(DB,self_uid,ppid,puid,languageStr,rmb = 0):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, puid, ppid, 1)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        price =  workData["price"]
        if price < 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_26", languageStr)
        else:

            #扣钱
            code = 1
            if rmb == 0:
                code = interface_wit.ReduceWitScore(DB,self_uid,price)
            if not code:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_3", languageStr)
            else:
                workBuy = xr_data_work.GetData(DB,0,0,puid,ppid,0,1)
                now = int(time.time())
                timelong = Global.WORK_BUY_XR_TIMELONG
                bend = now
                pid = 0
                if workBuy:
                    bend = workBuy["end"]
                    if bend < now:
                        bend = now
                    pid = workBuy["pid"]
                bend += timelong
                code = xr_data_work.CreateWork(DB,self_uid,workData["wname"],workData["sid"],104,puid,ppid,0,pid,bend)
                if code < 1:
                    json_data["code"] = -4
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_27", languageStr)
                else:
                    data = xr_data_work.GetDatas(DB, 4, 0, 0 , self_uid,code)
                    if not data:
                        json_data["code"] = 1
                        json_data["msg"] = ""
                    else:
                        json_data["code"] = 1
                        json_data["msg"] = json.dumps(data)

    return json_data

#人名币购买作品回调
def RmbBuy(_order, CData, DB):
    _arr_pam = CData.split('@')
    self_uid = int(_arr_pam[6])
    puid = int(_arr_pam[14])
    ppid = int(_arr_pam[15])

    json_back = Buy(DB,self_uid,ppid,puid,"ch")

    if json_back["code"] == 1:
        SyncMainClass.InsertSyncData("xeeditor", 402, json_back["msg"], 1, 1, self_uid, _order, DB)



#复制作品
def CopyWork(DB,self_uid,pid,languageStr):
    # 回执数据
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 作品数据
    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    print("info - ", workData)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    elif workData["from"] == 104:
        json_data["code"] = -2
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_28", languageStr)
    else:
            copy = workData["copy"] + 1
            wname = workData["wname"] + "("+str(copy)+")"
            code = xr_data_work.CreateWork(DB, self_uid, wname, workData["sid"], 105, self_uid, pid, 0)
            if code < 1:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_5", languageStr)
            else:
                json_data["code"] = 1
                info = xr_data_work.GetDatas(DB,8,0,0,self_uid,code)

                if not info:
                    json_data["msg"] = ""
                else:
                    json_data["msg"] = json.dumps(info)
                sql = "update tb_xr_worklocal set p1 = '"+str(copy)+"' where uid = " + str(self_uid) + " and pid = " + str(pid)
                DB.edit(sql,None)

    return json_data