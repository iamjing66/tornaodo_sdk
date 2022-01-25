import time

from handlers.kbeServer.Editor.Interface.interface_config import IC
from handlers.kbeServer.XREditor.data import xr_data_work

def GetPay_401(UID, paydata, DB):

    #智慧豆充值
    json_pay = {
        "Code": 0,
        "Data": {},
    }

    organization = 0 #paydata["organization"]
    distributor = 0#paydata["distributor"]

    rmb = int(paydata["num"])
    if rmb <= 0:
        json_pay["Code"] = -1  # 价格异常
    else:

        price = rmb * 10
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


def GetPay_402(UID, paydata, DB):

    #购买作品
    json_pay = {
        "Code": 0,
        "Data": {},
    }

    organization = 0 #paydata["organization"]
    distributor = 0#paydata["distributor"]

    uid = int(paydata["uid"])
    pid = int(paydata["pid"])
    if uid <= 0 or pid <= 0:
        json_pay["Code"] = -1  # 参数异常
    else:
        data = xr_data_work.GetData(DB, 0, 0, uid,pid,1)
        if not data:
            json_pay["Code"] = -2  # 作品不存在
        else:
            price = data["price"]
            if price <= 0:
                json_pay["Code"] = -3  # 作品不需要购买
            else:

                price = price * 10
                _power = 0
                if "power" in paydata.keys():
                    _power = paydata["power"]
                params = str(price) + "@" + str(organization) + "@" + str(distributor) + "@" + paydata["from"] + "@" + str(_power) + "@" + paydata["ip"] + "@" + str(uid) + "@" + str(pid)
                Data = {
                    "name": "作品["+data["wname"]+"]",
                    "price": price,  # 分
                    "params": params,
                }
                json_pay["Code"] = 1
                json_pay["Data"] = Data

    return json_pay


#购买vip
def GetPay_403(UID, paydata, DB):

    #购买作品
    json_pay = {
        "Code": 0,
        "Data": {},
    }

    organization = 0 #paydata["organization"]
    distributor = 0#paydata["distributor"]
    sx = int(paydata["sx"])         #时限 1-一个月 2-3个月 3-6个月 4-12个月

    if sx < 1 or sx > 4:
        json_pay["Code"] = -1  # 参数异常
    else:
        sql = "select vipdate from tb_userdata where uid = "+str(UID)+" limit 0,1;"
        data = DB.fetchone(sql,None)
        if data:
            vipdate = int(data[0])
            if vipdate == 1:
                json_pay["Code"] = -2  #vip已经永久
            else:
                now = int(time.time())
                if vipdate < now:
                    vipdate = now

                price = IC.XrVipConfig[sx]["cost"]
                # if sx == 1:
                #     timelong = 60*60*30
                # elif sx == 2:
                #     timelong = 60 * 60 * 30 * 3
                # elif sx == 2:
                #     timelong = 60 * 60 * 30 * 6
                # else:
                #     timelong = 60 * 60 * 30 * 12

                _power = 0
                if "power" in paydata.keys():
                    _power = paydata["power"]
                params = str(price) + "@" + str(organization) + "@" + str(distributor) + "@" + paydata["from"] + "@" + str(_power) + "@" + paydata["ip"] + "@" + str(sx)
                Data = {
                    "name": "购买vip",
                    "price": price,  # 分
                    "params": params,
                }
                json_pay["Code"] = 1
                json_pay["Data"] = Data
    print("json_pay = " , json_pay)
    return json_pay
