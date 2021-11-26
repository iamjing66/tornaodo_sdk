#!/usr/bin/env python
# coding=utf-8


def Data_Buy_Base(DB,UID):

    data = {}

    sql = "select ID,PID,ENDDATE FROM tb_bag WHERE UID = " + str(UID) + ";"
    result = DB.fetchall(sql, None)
    if result:
        for minfo in result:
            minfo_list = list(minfo)

            data[int(minfo_list[0])] = [int(minfo_list[1]),int(minfo_list[2])]


    return data


def InsertToDB(DB,uid,_date):

    sql = "INSERT INTO tb_bag (UID,ENDDATE) VALUES (" + str(uid) + "," + str(_date) + ");"
    DB.edit(sql, None)
    sql = "select ID FROM tb_bag WHERE UID = " + str(uid) + " order by ID DESC limit 1"
    data = DB.fetchone(sql, None)
    if data:
        return int(data[0])
    return 0

def InsertToDBOfUserName(DB,username,_date):

    sql = "INSERT INTO tb_bag (UID,ENDDATE) VALUES ((SELECT UID FROM tb_userdata where UserName = '"+username+"' limit 1)," + str(_date) + ");"
    #print("sql",sql)
    DB.edit(sql, None)


def UpdateToDB(DB,_date,bid):

    sql = "update tb_bag set ENDDATE = " + str(_date) + " where id = " + str(bid) + ";"
    DB.edit(sql, None)


def BindProject(DB,pid,bid):

    sql = "update tb_bag set PID = " + str(pid) + " where id = " + str(bid) + ";"
    DB.edit(sql, None)


def PAYPAM_VIPANDPPACKAGE(UID,paydata,DB):
    _name = ""
    json_data = paydata

    #{"PayType":"2","AppType":"2","AppCode":"4","UID":"376","UserName":"wz1","PayData":"{\\"model\\":\\"0\\",\\"extra\\":\\"12\\",\\"ip\\":\\"117.22.69.197\\",\\"from\\":\\"XRCREATEX\\",\\"organization\\":\\"4\\",\\"distributor\\":\\"5\\"}"}
    extra = json_data["extra"]          #12
    model = int(json_data["model"])     #0
    organization = json_data["organization"]
    distributor = json_data["distributor"]

    json_pay = {
        "Code":0,
        "Data":{},
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

        data = DB.fetchone(sql,None)
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

    data = DB.fetchone(sql,None)

    if model == 0:
        _name = "VIP开通/续费"
    else:
        _name = "存储包裹"
    if data != None and len(data) > 0:
        ##print("data", data)
        if model == 0:
            price = int(data[0] * data[2] * b_date)
        else:
            price = int(data[1]) * b_num

    if price > 0:
        _power = 0
        if "power" in json_data.keys():
            _power = json_data["power"]
        params = str(model) + "@" + str(extra) + "@" + str(pdate)+ "@" + str(bagID) + "@" + str(organization)+ "@" + str(distributor) + "@" + json_data["from"]+ "@" + str(_power)+ "@" + json_data["ip"]

        Data = {
            "name": _name,
            "price": price,  # 分
            "params": params,
        }
        json_pay["Code"] = 1
        json_pay["Data"] = Data

    return json_pay
