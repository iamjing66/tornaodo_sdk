#!/usr/bin/env python
# coding=utf-8


def InsertPayOrder(_order, _uid, _username, _from, _paytype, _price, _pam, _IP, _AppType, DB):
    sql = "INSERT INTO `tb_pay_order`(`order`,`UID`,`USERNAME`,`FROM`,`PAYTYPE`,`PRICE`,`PAM`,`IP`,APPTYPE)VALUES ( '" + _order + "','" + str(_uid) + "','" + _username + "','" + _from + "'," + str(
        _paytype) + "," + str(_price) + ",'" + _pam + "','" + _IP + "'," + str(_AppType) + " );"
    DB.edit(sql, None)


def UpdatePayOrder(_order, _flag, DB):
    sql = "Update tb_pay_order set Flag = " + str(_flag) + " where `order` = '" + _order + "';"
    DB.edit(sql, None)


def GetPayFlag(_order, DB):
    sql = "select Flag from tb_pay_order  where `order` = '" + _order + "';"
    data = DB.fetchone(sql, None)
    if data:
        return int(data[0])

    return -1
