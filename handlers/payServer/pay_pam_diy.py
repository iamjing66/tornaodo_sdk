#!/usr/bin/env python
# coding=utf-8

import json


class pay_pam_diy:

    def __init__(self):
        # 支付参数获取
        pass

    def GetMaikanData(self, paydata, DB):

        _id = 0
        _price2 = 0
        _name = ""
        json_data = paydata
        wid = json_data["wid"]
        b_uid = json_data["b_uid"]
        organization = json_data["organization"]
        distributor = json_data["distributor"]

        json_pay = {
                "Code": 0,
                "Data": {},
        }

        sql_str = "select ID,price2,`Name` from tb_workmarket where WID = " + str(wid) + " AND UID = " + str(b_uid) + ";"
        data = DB.fetchone(sql_str, None)
        if data:
            _id = int(data[0])
            _price2 = int(data[1])
            _name = data[2]

        if _id == 0 or _price2 <= 0:
            json_pay["Code"] = 0  # 价格异常
        else:
            _power = 0
            if "power" in json_data.keys():
                _power = json_data["power"]
            params = str(wid) + "@" + str(b_uid) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@n@" + json_data["ip"]
            Data = {
                    "name": _name,
                    "price": _price2 * 10,  # 分
                    "params": params,
            }
            json_pay["Code"] = 1
            json_pay["Data"] = Data

        return json_pay

    def GetSISCourseData(self, paydata, DB):

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

        data = DB.fetchone(sql_str, None)
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
            params = str(CourseID) + "@" + str(BType) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@n@" + json_data["ip"]
            Data = {
                    "name": _name,
                    "price": _PRICE,  # 分
                    "params": params,
            }
            json_pay["Code"] = 1
            json_pay["Data"] = Data

        return json_pay

    def GetChangxiangData(self, paydata, DB):

        _id = 0
        _price2 = 0
        _name = ""
        json_data = paydata
        channel = json_data["changel"]
        month = int(json_data["month"])
        organization = json_data["organization"]
        distributor = json_data["distributor"]
        CIDS = ""

        json_pay = {
                "Code": 0,
                "Data": {},
        }

        sql_str = "select Price,`Desc`,WTYPE,CID from tb_channel where WID in (" + channel + ");"

        data = DB.fetchall(sql_str, None)
        _name = ""
        _wtype = ""
        _price_record = ""
        if data:
            list_data = list(data)
            for minfo in list_data:
                if _price_record == "":
                    _price_record = str(minfo[0])
                else:
                    _price_record = _price_record + "#" + str(minfo[0])
                _price2 += int(minfo[0])
                if _name == "":
                    _name = minfo[1]
                else:
                    _name = _name + "#" + minfo[1]
                if _wtype == "":
                    _wtype = str(minfo[2])
                else:
                    _wtype = _wtype + "#" + str(minfo[2])
                if CIDS == "":
                    CIDS = str(minfo[3])
                else:
                    CIDS = CIDS + "#" + str(minfo[3])

        if _price2 <= 0:
            json_pay["Code"] = 0  # 价格异常
        if _price2 > 0:
            sql_str = "select Days,`Discount` from tb_discount where CID = " + str(month) + ";"

            data = DB.fetchone()
            _price3 = 0
            days = 0
            if data:
                days = int(data[0])
                _price3 = float(data[1])
            if days == 0:
                json_pay["Code"] = -1  # 价格异常
            else:
                _price = int(int((days / 30)) * _price2 * _price3)
                if _price <= 0:
                    json_pay["Code"] = 0  # 价格异常
                else:
                    _power = 0
                    if "power" in json_data.keys():
                        _power = json_data["power"]
                    params = str(channel) + "@" + str(month) + "@" + str(days) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@" + json_data["ip"]

                    Data = {
                            "name": "频道畅享",
                            "price": _price,  # 分
                            "params": params,
                    }
                    json_pay["Code"] = 1
                    json_pay["Data"] = Data

        return json_pay

    def GetVipData(self, UID, paydata, DB):

        _id = 0
        _price2 = 0
        _name = ""
        json_data = paydata

        extra = json_data["extra"]
        model = int(json_data["model"])
        organization = json_data["organization"]
        distributor = json_data["distributor"]

        json_pay = {
                "Code": 0,
                "Data": {},
        }

        # vip
        b_date = 0
        # 存储位
        b_id = 0
        b_num = 0
        if model == 0:
            b_date = int(extra)
        elif model == 1:
            _arr = extra.split('$')
            b_id = int(_arr[0])
            b_num = int(_arr[1])

        bagID = 0
        pdate = 0
        # 验证下参数
        sql = ""
        if model == 0:
            sql = "select VIPDATE FROM Tb_Userdata where uid = " + str(UID)
        else:
            if b_id != 0:
                sql = "select ENDDATE,ID FROM TB_BAG where ID = " + str(b_id)
        _name = ""
        price = 0  # 分为单位
        if sql != "":

            data = DB.fetchone(sql, None)
            if data:
                _pam = int(data[0])
                if model == 0:
                    if _pam == 1:
                        json_pay["Code"] = -1
                        return json_pay
                    pdate = _pam
                else:
                    if extra != 0:
                        if _pam == 1:
                            json_pay["Code"] = -1
                            return json_pay
                        bagID = int(data[1])
                        pdate = _pam

        # 计算价格
        sql = "select VIPPrice,WorksAPrice,(select DiscountRate from tb_new_vipdiscount where ThePurchaseTime = " + str(b_date) + ") as rate from tb_new_config;"

        data = DB.fetchone(sql, None)
        _id = 0
        _price2 = 0

        if model == 0:
            _name = "VIP开通/续费"
        else:
            _name = "存储包裹"
        if data != None and len(data) > 0:
            # print("data", data)
            if model == 0:
                price = int(data[0] * data[2] * b_date)
            else:
                price = int(data[1]) * b_num

        if price <= 0:
            json_pay["Code"] = 0
        else:
            _power = 0
            if "power" in json_data.keys():
                _power = json_data["power"]
            params = str(model) + "@" + str(extra) + "@" + str(pdate) + "@" + str(bagID) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@" + \
                     json_data["ip"]

            Data = {
                    "name": _name,
                    "price": price,  # 分
                    "params": params,
            }
            json_pay["Code"] = 1
            json_pay["Data"] = Data

        return json_pay

    def GetWitScore(self, UID, paydata, DB):

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

    def GetProjectSisData(self, UID, paydata, DB):

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
                sql = "SELECT T1.price1,T1.`Name` FROM tb_workmarket AS T1 INNER JOIN tb_project AS T2 ON T1.UID = T2.P_UID AND T1.PID = T2.ParentPid AND T2.uid = " + str(
                    puid) + " and T2.PID = " + str(wid)
            else:  # 课程
                sql = "select Price,`Name` from tb_mlesson_" + str(puid) + "_" + str(cid) + " where lid = " + str(lid) + "; "

            if len(sql) > 0:
                price = 0
                _name = ""

                data = DB.fetchone(sql, None)
                if data:
                    price = int(data[0])
                    _name = data[1]
                if price <= 0:
                    json_pay["Code"] = 0  # 价格异常
                else:
                    params = str(price) + "@" + str(organization) + "@" + str(distributor) + "@" + paydata["from"] + "@" + str(UID) + "@" + str(paydata["puid"]) + "@" + str(
                            paydata["cid"]) + "@" + str(paydata["lid"]) + "@" + str(paydata["wid"]) + "@" + str(paydata["buyCount"]) + "@" + str(ptype) + "@" + paydata["ip"]
                    Data = {
                            "name": _name,
                            "price": price * buyCount * 10,  # 分
                            "params": params,
                    }
                    json_pay["Code"] = 1
                    json_pay["Data"] = Data

        return json_pay


PayPamDiyClass = pay_pam_diy()
