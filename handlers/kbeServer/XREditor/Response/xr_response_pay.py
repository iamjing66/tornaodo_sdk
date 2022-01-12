

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