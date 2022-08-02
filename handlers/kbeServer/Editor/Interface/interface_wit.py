#!/usr/bin/env python
# coding=utf-8


import logging
import application
from handlers.SyncServer.sockect import pro_status


def ReduceWitScore(DB, uid, score_num):
    # iWit = 0
    # iWit_RMB = 0
    # #print("ReduceWitScore:", uid, score_num)
    # sql = "select Wit_Score,Wit_RMB from tb_userdata where uid = "+str(uid)
    # result = DB.fetchone(sql, None)
    # if result:
    #     iWit = int(result[0])
    #     iWit_RMB = int(result[1])
    #     #print("ZHD:",iWit,iWit_RMB)

    iWit = application.App.Redis_Wit.GetWit(uid, 1)
    iWit_RMB = application.App.Redis_Wit.GetWit(uid, 2)

    if iWit + iWit_RMB < score_num:
        return False
    # 先扣除赠送
    if iWit >= score_num:
        iWit = iWit - score_num
    else:
        ionly = iWit - score_num
        iWit = 0
        if ionly < 0:
            iWit_RMB = iWit_RMB + ionly

    application.App.Redis_Wit.SaveWit(uid, iWit, iWit_RMB, 0)

    pro_status.syncTrigger("xreditor", uid, 405, str((iWit + iWit_RMB)))

    return True
    # sql = "update tb_userdata set Wit_Score = "+str(iWit)+",Wit_RMB = "+str(iWit_RMB)+" where uid = "+str(uid)
    # result = DB.edit(sql, None)
    # if result:
    #     return True


# 增加智慧豆
def AddWitScoreWithType(DB, uid, score_num, type):
    ##print("AddWitScoreWithType",uid ,score_num ,type)

    if score_num <= 0:
        return False

    # if type == 0:
    #     sql = "update tb_userdata set Wit_Score = Wit_Score + " + str(score_num)+ " where uid = " + str(uid)
    # else:
    #     sql = "update tb_userdata set Wit_RMB = Wit_RMB + " + str(score_num) + " where uid = " + str(uid)
    # ##print("sql",sql)
    # result = DB.edit(sql, None)
    # if result:
    #     logging.info("智慧豆充值成功")
    #     return True
    # logging.info("智慧豆充值失败")
    # return False

    if type == 0:
        application.App.Redis_Wit.AddWit(uid, score_num, 0, 1)
    else:
        application.App.Redis_Wit.AddWit(uid, score_num, 0, 2)

    wit = application.App.Redis_Wit.GetWit(uid, 0)
    pro_status.syncTrigger("xreditor", uid, 405, str(wit))

    return True


# 增加智慧豆
def AddWitScoreWithUserName(DB, username, score_num, type):
    print("AddWitScoreWithUserName = ", username, score_num, type)

    if score_num <= 0:
        return False

    uid = application.App.Redis_User.GetData(username, "uid")
    print("AddWitScoreWithUserName1 = ", uid)
    if not uid:
        return False

    # if type == 0:
    #     sql = "update tb_userdata set Wit_Score = Wit_Score + " + str(score_num)+ " where UserName = '"+username+"'"
    # else:
    #     sql = "update tb_userdata set Wit_RMB = Wit_RMB + " + str(score_num) + " where UserName = '"+username+"'"
    #
    # result = DB.edit(sql, None)
    # if result:
    #     return True
    #
    # return False

    if type == 0:
        application.App.Redis_Wit.AddWit(uid, score_num, 0, 1)
    else:
        application.App.Redis_Wit.AddWit(uid, score_num, 0, 2)

    wit = application.App.Redis_Wit.GetWit(uid, 0)
    pro_status.syncTrigger("xreditor", uid, 405, str(wit))
    return True


def TB_Wit(DB, username):
    # sql = "select Wit_Score,Wit_RMB from tb_userdata where UserName = '"+str(username)+"'"
    # result = DB.fetchone(sql, None)
    # if result:
    #     return int(result[0]) + int(result[1])
    # return 0

    uid = application.App.Redis_User.GetData(username, "uid")
    if not uid:
        return 0

    return application.App.Redis_Wit.GetWit(uid, 0)


def PAYPAM_WitScore(UID, paydata, DB):
    json_pay = {
            "Code": 0,
            "Data": {},
    }

    organization = paydata["organization"]
    distributor = paydata["distributor"]

    rmb = int(paydata["rmb"])
    if rmb <= 0:
        json_pay["Code"] = 0  # 价格异常
    else:
        price = rmb * 100
        _power = 0
        if "power" in paydata.keys():
            _power = paydata["power"]
        params = str(price) + "@" + str(organization) + "@" + str(distributor) + "@" + paydata["from"] + "@" + str(_power) + "@" + paydata["ip"]
        Data = {
                "name": "充值中心",
                "price": price,  # 分
                "params": params,
        }
        json_pay["Code"] = 1
        json_pay["Data"] = Data

    return json_pay
