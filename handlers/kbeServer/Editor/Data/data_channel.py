#!/usr/bin/env python
# coding=utf-8


def PAYPAM_Changxiang(paydata, DB):
    _price2 = 0
    json_data = paydata
    channel = json_data["changel"]
    w_type = json_data["WType"]
    month = int(json_data["month"])
    organization = json_data["organization"]
    distributor = json_data["distributor"]
    json_pay = {
        "Code": 0,
        "Data": {},
    }
    sql_str = "select Price,`Desc`,WTYPE,CID from tb_channel where CID in (" + channel + ");"

    data = DB.fetchall(sql_str, None)
    _price_record = ""
    w_types = ""
    w_types_list = []
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _price_record == "":
                _price_record = str(minfo[0])
            else:
                _price_record = _price_record + "#" + str(minfo[0])
            _price2 += int(minfo[0])
            w_type = str(minfo[2])
            w_types_list.append(w_type)
        w_types = ",".join(w_types_list)

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
                params = str(channel) + "@" + str(month) + "@" + str(days) + "@" + str(organization) + "@" + str(distributor) + "@" + json_data["from"] + "@" + str(_power) + "@" + json_data["ip"] + "@" + str(w_types)

                Data = {
                    "name": "频道畅享",
                    "price": _price,  # 分
                    "params": params,
                }
                json_pay["Code"] = 1
                json_pay["Data"] = Data

    return json_pay
