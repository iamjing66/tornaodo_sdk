#!/usr/bin/env python
# coding=utf-8

import json
import time
import Global
from handlers.kbeServer.Editor.Interface.interface_solr import Solr_PayLog

class paydo_changxiang:

    def __init__(self):
        pass


    def GetMonthBuy(self,cid , uid,DB):

        sql = "SELECT `DATE` FROM tb_channel_buy where UID = "+str(uid)+" and CID = "+str(cid)+";"

        data = DB.fetchone(sql,None)
        if data:
            return int(data[0])
        return 0



    def Do(self, CData,DB):

        _arr_pam = CData.split('@')

        price = int(_arr_pam[4])
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        CID = _arr_pam[8]
        mounth = int(_arr_pam[9])
        days = int(_arr_pam[10])

        organization = _arr_pam[11]
        distributor = _arr_pam[12]
        _from = _arr_pam[13]
        _userType = int(_arr_pam[14])
        _ip = _arr_pam[15]
        _wid = _arr_pam[16]

        toclient = ""
        _now = int(time.time())
        cids = CID.split(',')
        #print("cids", cids)
        for _cid in cids:
            #print("_cid", _cid)
            _pdate = self.GetMonthBuy(_cid , UID, DB)
            #print("_pdate", _pdate)
            _INSERT = 0
            if _pdate == 0:
                _INSERT = 1
                _pdate = _now
            if _pdate < _now:
                _pdate = _now
            # _ptruedate = _cpdate + 31536000
            _pdate = _pdate + days*86400
            if _INSERT == 1:
                sql = "insert INTO `tb_channel_buy` (UID,CID,`DATE`) values (" + str(UID) + ",'" + _cid + "'," + str(_pdate) + ");"
            else:
                sql = "update `tb_channel_buy` set `DATE` = " + str(_pdate) + " WHERE UID = " + str(UID) + " AND CID = '" + _cid + "';"
            DB.edit(sql,None)

            if toclient == "":
                toclient = str(_cid)+"$"+str(_pdate)
            else:
                toclient = toclient + "@" + str(_cid)+"$"+str(_pdate)


            # 日志索引库
            # 支付记录
            proId = str(_cid)
            name = "频道包月"
            #type = 1
            #saleModules = 7

            #SolrInst.Solr_Pay(2, proId, name, _from, saleModules,6, 1, price, "", type, int(time.time()), _pdate,organization, distributor, UserName, UID, _userType,_ip)
            Solr_PayLog(proId, name, 12, 6, 1, price, 1, "", int(time.time()), _pdate, UID, "vr", int(_wid))

        return toclient



PayDoChangxiangClass = paydo_changxiang()