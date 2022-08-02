#!/usr/bin/env python
# coding=utf-8

import time
import json


class pay_order:

    def __init__(self):
        # 支付宝支付
        pass

    def InsertPayOrder(self, _order, _uid, _username, _from, _paytype, _price, _pam, _IP, _AppType, DB):
        sql = "INSERT INTO `tb_pay_order`(`order`,`UID`,`USERNAME`,`FROM`,`PAYTYPE`,`PRICE`,`PAM`,`IP`,APPTYPE)VALUES ( '" + _order + "','" + str(
            _uid) + "','" + _username + "','" + _from + "'," + str(_paytype) + "," + str(_price) + ",'" + _pam + "','" + _IP + "'," + str(_AppType) + " );"
        DB.edit(sql, None)

    def UpdatePayOrder(self, _order, _flag, DB):
        sql = "Update tb_pay_order set Flag = " + str(_flag) + " where `order` = '" + _order + "';"
        DB.edit(sql, None)


PayOrderClass = pay_order()
