#!/usr/bin/env python
# coding=utf-8


def PAYPAM_Changxiang(paydata ,DB):

    _id = 0
    _price2 = 0
    _name = ""
    json_data = paydata
    channel = json_data["changel"]
    w_type = json_data["WType"]
    month = int(json_data["month"])
    organization = json_data["organization"]
    distributor = json_data["distributor"]
    CIDS = ""

    json_pay = {
        "Code": 0,
        "Data": {},
    }
    sql_str = "select Price,`Desc`,WTYPE,CID from tb_channel where CID = %s;"

    data = DB.fetchall(sql_str, channel)
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
            if w_type == "0":
                w_type = str(minfo[2])

    if _price2 > 0:
        sql_str = "select Days,`Discount` from tb_discount where CID = " + str(month) + ";"

        data = DB.fetchone(sql_str, None)
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
                params = str(channel) + "@" + str(month) + "@" + str(days) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@" + json_data["ip"] + "@" + str(w_type)

                Data = {
                    "name": "频道畅享",
                    "price": _price,  # 分
                    "params": params,
                }
                json_pay["Code"] = 1
                json_pay["Data"] = Data

    return json_pay