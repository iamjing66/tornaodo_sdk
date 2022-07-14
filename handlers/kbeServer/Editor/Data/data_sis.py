#!/usr/bin/env python
# coding=utf-8


# 作品买看数据
def Data_SIS_MK_Base(db, uid, vid, call_type):
    _pdate = 0
    json_back = None
    sql = "select t3.coursePrice,t3.courseYearPrice,t3.courseExpireTime,t3.`name` from (select t1.coursePrice,t1.courseYearPrice,t2.courseExpireTime,t1.courseId,t2.userId,t1.`name` from new_coursedetails as t1 left join new_coursebuy as t2 on t1.courseId = t2.courseId and t2.userId = " + str(
        uid) + ") t3 where t3.courseId = " + str(vid) + " order by t3.courseExpireTime desc  limit 0,1;"
    ##print("sql" , sql)
    result = db.fetchone(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchone_json(result)
        elif call_type == 0:
            json_back = Get_Data_SIS_MK_Base_Ini(result)
        elif call_type == 2:
            json_back = Get_Data_SIS_MK_Base_List(result)
    return json_back


def Get_Data_SIS_MK_Base_Ini(minfo_list):
    return str(minfo_list[0]) + "`" + str(minfo_list[1]) + "`" + str(minfo_list[2]) + "`" + str(minfo_list[3])


def Get_Data_SIS_MK_Base_List(minfo_list):
    return [str(minfo_list[0]), str(minfo_list[1]), str(minfo_list[2]), str(minfo_list[3])]


def PAYPAM_SISCourse(paydata, db):
    _id = 0
    _price2 = 0
    _name = ""
    json_data = paydata
    CourseID = json_data["wid"]
    BType = int(json_data["b_uid"])
    organization = json_data["organization"]
    distributor = json_data["distributor"]
    _from = json_data["from"]
    json_pay = {
        "Code": 0,
        "Data": {},
    }

    table_name = "new_coursedetails"
    if _from == "SISNG":
        table_name = "new_sis3dcoursedeta"

    if BType == 0:
        sql_str = "select id,coursePrice,`name` from " + table_name + " where courseId = '" + CourseID + "';"
    else:
        sql_str = "select id,courseYearPrice,`name` from " + table_name + " where courseId = '" + CourseID + "';"

    data = db.fetchone(sql_str, None)
    _PRICE = 0
    if data:
        _id = int(data[0])
        _price2 = int(data[1])
        _name = data[2]
        if _from == "SISNG":
            _PRICE = _price2
        else:
            _PRICE = _price2 * 10

    if _id == 0 or _price2 < 0:
        json_pay["Code"] = 0  # 价格异常
    else:
        _power = 0
        if "power" in json_data.keys():
            _power = json_data["power"]
        params = str(CourseID) + "@" + str(BType) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data[
            "from"] + "@" + str(_power) + "@n@" + json_data["ip"]
        Data = {
            "name": _name,
            "price": _PRICE,  # 分
            "params": params,
        }
        json_pay["Code"] = 1
        json_pay["Data"] = Data

    return json_pay


def PAYPAM_ProjectSisData(uid, paydata, db):
    json_pay = {
        "Code": 0,
        "Data": {},
    }

    organization = paydata["organization"]
    distributor = paydata["distributor"]
    ptype = int(paydata["ptype"])
    cid = int(paydata["cid"])
    puid = int(paydata["puid"])
    lid = int(paydata["lid"])
    wid = int(paydata["wid"])
    buyCount = int(paydata["buyCount"])

    if buyCount <= 0:
        json_pay["Code"] = 0  # 价格异常
    else:
        sql = ""
        if ptype == 1:  # 工程
            json_pay["Code"] = -1  # 价格异常
        elif ptype == 2:  # 购买的作品
            sql = "SELECT T1.price1,T1.`Name` FROM tb_workmarket AS T1 INNER JOIN tb_project AS T2 ON T1.uid = T2.P_UID AND T1.PID = T2.ParentPid AND T2.uid = " + str(
                puid) + " and T2.PID = " + str(wid)
        else:  # 课程
            sql = "select Price,`Name` from tb_mlesson_" + str(puid) + "_" + str(cid) + " where lid = " + str(
                lid) + "; "

        if sql:
            price = 0
            _name = ""

            data = db.fetchone(sql, None)
            if data:
                price = int(data[0])
                _name = data[1]
            if price <= 0:
                json_pay["Code"] = 0  # 价格异常
            else:
                params = str(price) + "@" + str(organization) + "@" + str(distributor) + "@" + paydata[
                    "from"] + "@" + str(uid) + "@" + str(paydata["puid"]) + "@" + str(paydata["cid"]) + "@" + str(
                    paydata["lid"]) + "@" + str(paydata["wid"]) + "@" + str(paydata["buyCount"]) + "@" + str(
                    ptype) + "@" + paydata["ip"]
                d_data = {
                    "name": _name,
                    "price": price * buyCount * 10,  # 分
                    "params": params,
                }
                json_pay["Code"] = 1
                json_pay["Data"] = d_data

    return json_pay
