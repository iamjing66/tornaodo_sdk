#!/usr/bin/env python
# coding=utf-8

import logging
import time
from handlers.kbeServer.Editor.Data import data_sis
from handlers.kbeServer.Editor.Interface import interface_wit,interface_solr,interface_sms


#SIS买看
def VR_MK_SIS(DB, self_uid, vid, buy_type, plat, phone=None):

    UID = self_uid
    w_data = data_sis.Data_SIS_MK_Base(DB, UID, vid, 2)
    if not w_data:
        return [0, ""]
    if w_data[0] == "":
        price1 = 0
    else:
        price1 = int(w_data[0])
    #print("w_data",w_data)
    _insert = 0
    enddate = w_data[2]
    cname = w_data[3]
    if enddate == 'None':
        _insert = 1
        _pdate = time.time()
    else:
        timeArray = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
        _pdate = int(time.mktime(timeArray))
    _now = time.time()
    if _pdate > _now:
        return [-1, ""]  # 课程还在有效范围内，无需重复购买

    # 时间改成固定一个月
    price = price1
    _pdate = int(_now) + 2592000
    if buy_type == 0 or buy_type == 2:
        if buy_type == 0:
            # 扣钱
            if not interface_wit.ReduceWitScore(DB, UID, price):
                return [-2, ""]  #智慧豆不足
        timeArray = time.localtime(_now)
        _date1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        timeArray1 = time.localtime(_pdate)
        _date2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
        ##print(price,_date1,_date2,UID,vid)
        if _insert == 1:
            sql = "INSERT INTO `new_coursebuy`(`userId`,`courseId`,`buyPrice`,`courseBuyTime`,`courseExpireTime`)VALUES('" + str(UID) + "','" + str(vid) + "','" + str(price) + "',' " + str(_date1) + "','" + str(_date2) + "');"
        else:
            sql = "update `new_coursebuy` set buyPrice = '" + str(price) + "',courseBuyTime = '" + str(_date1) + "',courseExpireTime = '" + str(_date2) + "' WHERE userId = '" + str(UID) + "' AND courseId = '" + str(vid) + "'"

        DB.edit(sql, None)
        transaction_type = 0
        if plat == 20:
            _from = 3
        else:
            _from = 5
        if not phone:
            # interface_solr.Solr_Pay(DB,2, "", cname, plat, _from, 4, 0, price, 10, "", int(time.time()), _pdate,self_uid)
            interface_solr.Solr_PayLog(vid, cname, _from, 4, transaction_type, price, 11, "", int(time.time()), _pdate, self_uid, "vr", 2)
        # self.SolrInst.Log_Cost(10, "购买学习中心观看权", price, "购买["+cname+"]观看权(一个月)", _from, "", self.organization, self.distributor, self.UID)
        return [1, str(vid) + "$" + str(_date1) + "$" + str(_date2)]
    else:
        sql = "select Phone from tb_userdata where UID = " + str(UID) + ";"
        data = DB.fetchone(sql, None)
        _phone = ""
        if data:
            _phone = data[0]
        if _phone == "":
            return [-7, ""]  # 未绑定手机号
        # pay_url = "域名/vrpay/vrDWorkPay.do?w_uid=**&w_cid=**&uid=**"
        pay_url = str(vid)  # + "@" + "$" + str(etype) #+ str(UID)
        interface_sms.SendSms(2, UID, _phone, pay_url)
        return [99, ""]


def GetCourseTypeList(DB):
    json_data = {
        "code": 0,
        "msg": ""
    }
    str_sql = "select t1.* from new_coursetype as t1 inner join new_coursedetails t2 on t1.courseTypeId = t2.courseTypeId and t2.flag = 1 group by t2.courseTypeId, t1.sort order by t1.sort;"
    _cback = ""
    data = DB.fetchall(str_sql, None)
    if data:
        back_list = []
        for info in data:
            back_list.append(",".join(list(map(str, info[:6]))))
        _cback = "*".join(back_list)
        # minfo = list(data)
        # for info in minfo:
        #     if _cback == "":
        #         _cback = str(info[0]) + "," + str(info[1]) + "," + str(info[2]) + "," + str(info[3]) + "," + str(info[4]) + "," +  str(info[5])
        #     else:
        #         _cback = _cback + "*" + str(info[0]) + "," + str(info[1]) + "," + str(info[2]) + "," + str(info[3]) + "," +  str(info[4]) + "," + str(info[5])
        json_data["code"] = "1"
        json_data["msg"] = _cback

    return json_data


def GetCourseDetailList(DB, pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if pam == "":
        return json_data
    courseTypeId = pam["courseTypeId"]
    userId = pam["userId"]
    resType = pam["resType"]
    _isPhoneUI = pam["_isPhoneUI"]
    #strSql = "select * from new_coursedetails where courseTypeId = "+str(courseTypeId)+""
    strSql = "select * from (select T1.*,t2.courseExpireTime from new_coursedetails T1 LEFT JOIN (select courseId,courseExpireTime from new_coursebuy where userId = "+str(userId)+" group by courseId) T2 ON T1.courseId = t2.courseId)t3 where t3.courseTypeId = "+str(courseTypeId)+" and t3.flag = 1 order by t3.sort;"
    IsLock = "0"
    ##print("strSql,",strSql)
    _cback = ""
    try:
        data = DB.fetchall(strSql, None)
        if data:
            minfo = list(data)
            for info in minfo:
                if str(info[9]) == "0":
                    IsLock = "0"
                else:
                    if info[1] != "":
                        IsLock = "1"
                        cbuy = info[21]
                        if cbuy:
                            logging.info("已购买")
                            t = time.strptime(cbuy, "%Y-%m-%d %H:%M:%S")
                            # 将时间元组转换为时间戳
                            t = time.mktime(t)
                            if t > time.time():
                                IsLock = "0"
                                logging.info("课程未过期, 课程id: %s, 锁状态: %s" % (str(info[1]), IsLock))

                        #IsLock =  Msql_SearchCourseIsBuy(DB,info[1],userId)
                        ##print("--", IsLock)
                restype = str(info[15])
                if restype.find(resType) >= 0:
                    if _cback != "":
                        _cback = _cback + "*" + str(info[1]) + "&" + str(info[2]) + "&" + str(info[3]) + "&" + str(info[4]) + "&" + str(info[5]) + "&" + str(info[6]) + "&" + str(info[7]) + "&" + str(info[8]) + "&" + str(info[9]) + "&" + str(IsLock) + "&" + str(info[11]) + "&" + str(info[12]) + "&" + str(info[13]) + "&" + str(info[14]) + "&" + str(info[16]) + "&" + str(info[17])
                    else:
                        _cback =  str(info[1]) + "&" + str(info[2]) + "&" + str(info[3]) + "&" + str(info[4]) + "&" + str(info[5]) + "&" + str(info[6]) + "&" + str(info[7]) + "&" + str(info[8]) + "&" + str(info[9]) + "&" + str(IsLock) + "&" + str(info[11]) + "&" + str(info[12]) + "&" + str(info[13]) + "&" + str(info[14]) + "&" + str(info[16]) + "&" + str(info[17])
            json_data["code"] = "1"
    except:
        json_data["code"] = "0"
    _cback = courseTypeId + "`" + _isPhoneUI + "`" + _cback
    json_data["msg"] = _cback
    return json_data


def Msql_SearchCourseIsBuy(DB, buyCourseId, myUserId):
    isHave = "1"
    strSql = "select * from new_coursebuy where userId = "+str(myUserId)+" and courseId = " + str(buyCourseId) + ""
    try:
        data = DB.fetchone(strSql, None)
        if data:
            stime = data[6]
            Nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if stime > Nowtime:
                isHave = "0"
    except:
        isHave = "1"
    return isHave
