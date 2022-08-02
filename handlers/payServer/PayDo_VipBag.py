#!/usr/bin/env python
# coding=utf-8

import json
import time
from handlers.kbeServer.Editor.Data import data_ppackage, data_vip
from handlers.SyncServer.SyncMain import SyncMainClass


class paydo_vipbag:

    def __init__(self):
        pass

    def Do(self, _arr_pam, DB):

        uid = int(_arr_pam[6])
        price = int(_arr_pam[4])
        paytype = int(_arr_pam[0])
        _order = _arr_pam[3]
        UserName = _arr_pam[7]
        extra = _arr_pam[9]
        model = int(_arr_pam[8])
        _pdate = int(_arr_pam[10])
        _bagid = int(_arr_pam[11])

        organization = _arr_pam[12]
        distributor = _arr_pam[13]
        _from = _arr_pam[14]

        # 64*10*1*0*0$1*WechatC16062229482*0*0
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

        # proType = 0
        # proName = ""
        # supplement = ""
        # cName = ""
        # classification = 0
        _date = 0

        cdata = ""
        if model == 0:
            # proType = 6
            # proName = "VIP购买"
            # supplement = "VIP购买(一年)"
            # cName = "vip"
            if _pdate < int(time.time()):
                _pdate = int(time.time())
            _date = _pdate + b_date * 30 * 86400
            data_vip.UpdateToDB(DB, _date, uid)
            cdata = str(_date)
            # InsertSyncData("editor", 101, cdata, 0, 1, uid, Cur, Db)
            SyncMainClass.InsertSyncData("editor", 101, cdata, 0, 1, uid, _order, DB)

        else:
            # proType = 7
            # proName = "包裹位购买"
            # supplement = "包裹位购买(一年)"
            # cName = "包裹位"
            if _bagid == 0:
                _date = int(time.time()) + 31536000
                # sql = "select last_insert_id();"
                for i in range(b_num):
                    i_id = data_ppackage.InsertToDB(DB, uid, _date)

                    if cdata == "":
                        cdata = str(i_id) + "$" + str(_date)
                    else:
                        cdata = cdata + "@" + str(i_id) + "$" + str(_date)
                # InsertSyncData("editor", 102, cdata, 0, 1, uid, Cur, Db)
                SyncMainClass.InsertSyncData("editor", 102, cdata, 0, 1, uid, _order, DB)
            else:
                if _pdate < int(time.time()):
                    _pdate = int(time.time())
                _date = _pdate + 31536000
                data_ppackage.UpdateToDB(DB, _date, _bagid)
                cdata = str(_bagid) + "$" + str(_date)
                # InsertSyncData("editor", 102, cdata, 0, 1, uid, Cur, Db)
                SyncMainClass.InsertSyncData("editor", 102, cdata, 0, 1, uid, _order, DB)

        # 订单记录
        # sql = "Insert Into tb_saomazhifu (model,uid,paytype,price,`desc`,`Order`) values (" + str(model) + "," + str(uid) + "," + str(paytype) + "," + str(price) + ",'" + str(extra) + "','" + _order + "');"
        # Cur.execute(sql)
        # Db.commit()

        if model == 0:
            sql = "update tb_userdata set AccountPower = 1, EndDate = 1 where uid = " + str(uid) + ";"
            DB.edit(sql, None)

        # VIP包裹 - 索引库日志
        return _date

    def DoChongzhi(self, uid, score, Cur, Db):

        sql = "update tb_userdata set Wit_Rmb = Wit_Rmb + " + str(score) + " where uid = " + str(uid) + ";"
        Cur.execute(sql)
        Db.commit()


PayDoVipBagClass = paydo_vipbag()
