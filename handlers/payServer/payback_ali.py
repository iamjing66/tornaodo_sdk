#!/usr/bin/env python
# coding=utf-8

import time
from handlers.payServer.PayDo_Work import PayDoWorkClass
from handlers.SyncServer.SyncMain import SyncMainClass
from handlers.payServer.PayDo_SIS import PayDoSisClass
from handlers.payServer.PayDo_Changxiang import PayDoChangxiangClass
from handlers.payServer.PayDo_VipBag import PayDoVipBagClass
from handlers.kbeServer.Editor.Interface.interface_solr import Solr_PayLog
import logging
from handlers.kbeServer.Editor.Interface import interface_wit
from handlers.kbeServer.XREditor.Interface import xrinterface_work,xr_interface_vip
class payback_ali:


    def __init__(self):
        pass



    def Do(self,AppCode , CData,_order,DB):

        logging.info("PayBack - ToDO -> AppCode[%i],CData[%s],_order[%s]" % ( AppCode, CData, _order))
        if AppCode == 1:
            self.DoMaikan(_order,CData,DB)
        elif AppCode == 2:
            self.DoSisCourse(_order,CData,DB)
        elif AppCode == 3:
            self.DoChangxiang(_order,CData,DB)
        elif AppCode == 4:
            self.DoVipBag(_order,CData,DB)
        elif AppCode == 5:
            self.DoChongzhi(_order,CData,DB)
        elif AppCode == 6:
            self.DoSISCourseBuyNum(_order,CData)
        elif AppCode == 401:
            self.DoChongzhi(_order, CData, DB,"xreditor")
        elif AppCode == 402:
            xrinterface_work.RmbBuy(_order, CData, DB)
        elif AppCode == 403:
            xr_interface_vip.VipBuy(_order, CData, DB)
    #DIY买看
    def DoMaikan(self,_order,CData,DB):

        _arr_pam = CData.split('@')

        _order = _arr_pam[3]
        price = int(_arr_pam[4])
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        wid = int(_arr_pam[8])
        b_uid = int(_arr_pam[9])

        organization = _arr_pam[10]
        distributor = _arr_pam[11]
        _from = _arr_pam[12]
        _userType = int(_arr_pam[13])
        _name = _arr_pam[5]
        _ip = _arr_pam[15]

        #Do
        toclient = PayDoWorkClass.Do(_arr_pam,DB)
        #广播消息
        SyncMainClass.InsertSyncData("app", 103, toclient, 0, 1, UID,_order,DB)
        #支付记录
        proId = str(wid)
        type = 10
        saleModules = 0
        if _from == "Android":
            saleModules = 4
        else:
            saleModules = 6

        #买看VR
        #SolrInst.Solr_Pay(2, proId, _name, _from, saleModules, 5,1, price, "", type, int(time.time()), 0, organization,distributor, UserName, UID, _userType,_ip)
        # interface_solr.Solr_PayLog("", objName, 1, 9, 0, _price, 7, "", int(time.time()), 0, UID, "pc")
        Solr_PayLog(proId, _name, saleModules, 5, 1, price, 10, "", int(time.time()), 0, UID, "vr", 2, UserName)
    # SIS课程购买
    def DoSisCourse(self,_order, CData,DB):
        _arr_pam = CData.split('@')

        _order = _arr_pam[3]
        price = int(_arr_pam[4])
        UID = _arr_pam[6]
        UserName = _arr_pam[7]
        wid = _arr_pam[8]
        b_uid = int(_arr_pam[9])

        organization = _arr_pam[10]
        distributor = _arr_pam[11]
        _from = _arr_pam[12]
        _userType = int(_arr_pam[13])
        _name = _arr_pam[5]
        _ip = _arr_pam[15]

        if _from == "SISNG":

            PayDoSisClass.DoSISNG(_arr_pam)

            # url = Global.SISNG_PURL + UID+"_"+wid+"_"+str(b_uid)+"_"+_order
            # res = requests.get(url=url)
            # print(res.text)
        else:
            # Do
            toclient = PayDoSisClass.Do(_arr_pam,DB)

            # 广播消息
            #cpam = str(wid) + "$" + str(b_uid)
            SyncMainClass.InsertSyncData("app", 104, toclient, 0, 1, UID, _order, DB)
            # 支付记录
            # type = 11
            saleModules = 0
            now = int(time.time())
            _pdate = now + 2592000
            if _from == "Android":
                saleModules = 3
            else:
                saleModules = 4
            # SolrInst.Solr_Pay(2, proId, _name, _from, saleModules,4, 1, price, "", type, int(time.time()), 0, organization,distributor, UserName, UID, _userType,_ip)
            Solr_PayLog(str(wid), _name, saleModules, 4, 1, price, 11, "", now, _pdate, UID, "vr", 2, UserName)

    #sis项目购买终端数量
    def DoSISCourseBuyNum(self,_order, CData):
        _arr_pam = CData.split('@')
        PayDoSisClass.DoSISDirectNum(_arr_pam)

    #频道畅享
    def DoChangxiang(self,_order, CData,DB):
        _arr_pam = CData.split('@')
        _order = _arr_pam[3]
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        channel = _arr_pam[8]
        mounth = int(_arr_pam[9])
        days = int(_arr_pam[10])

        # Do
        toclient = PayDoChangxiangClass.Do(CData,DB)
        # 广播消息
        #cpam = str(channel) + "$" + str(mounth)
        SyncMainClass.InsertSyncData("app", 105, toclient , 0, 1, UID,_order,DB)



    # VIP/BAG
    def DoVipBag(self,_order, CData,DB):
        _arr_pam = CData.split('@')

        UID = int(_arr_pam[6])
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
        _userType = int(_arr_pam[15])
        _ip = _arr_pam[16]
        # print("DoVipBag - pam : " , _arr_pam)
        # Do
        #Do(self,uid,price,model,extra,_pdate,_bagid,paytype,_order,Cur,Db):
        _date = PayDoVipBagClass.Do(_arr_pam,DB)
        # 广播消息
        #cpam = str(channel) + "$" + str(mounth)
        #SyncMainClass.InsertSyncData("app", 1003, cpam, 0, 1, UID, Cur, Db)

        # 日志索引库
        #支付记录
        proId = ""
        name = ""
        type = 0
        saleModules = 0
        _bt = 0
        if model==0:
            proId = "0"
            name = "VIP"
            type = 0
            saleModules = 8
            _bt = 1
        else:
            proId = "0"
            name = "工程存储位"
            type = 9
            saleModules = 9
            _bt = 2

        #SolrInst.Solr_Pay(2,proId,name,_from,saleModules,_bt,1,price,"",type,int(time.time()),_date,organization,distributor,UserName,UID,_userType,_ip)
        Solr_PayLog(proId, name, saleModules, _bt, 1, price, type, "", int(time.time()), _date, UID, "pc", 1, UserName)

    def DoChongzhi(self,_order, CData,DB , cmodel="editor"):

        _arr_pam = CData.split('@')
        _order = _arr_pam[3]
        price = int(_arr_pam[4])
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        _score = int(int(_arr_pam[8]) / 10)
        organization = _arr_pam[9]
        distributor = _arr_pam[10]
        _from = _arr_pam[11]
        _userType = int(_arr_pam[12])
        _ip = _arr_pam[13]
        logging.info(_arr_pam)
        #print("_arr_pam",_arr_pam)
        #PayDoVipBagClass.DoChongzhi(UID,_score,Cur,Db)
        interface_wit.AddWitScoreWithType(DB,UID,_score,1)
        # 广播消息
        if cmodel == "editor":
            SyncMainClass.InsertSyncData(cmodel, 104, str(_score) , 1, 1, UID,_order,DB)
        else:
            SyncMainClass.InsertSyncData(cmodel, 401, str(_score), 1, 1, UID, _order, DB)

        # 支付记录
        proId = "0"
        name = "智慧豆"
        type = 2
        saleModules = 10

        #SolrInst.Solr_Pay(2, proId, name, _from, saleModules,0, 1, price, "", type, int(time.time()), 0,organization, distributor, UserName, UID, _userType,_ip)
        Solr_PayLog(proId, name, saleModules, 0, 1, price, type, "", int(time.time()), 0, UID, "pc", 1, UserName)

PayBackAliClass = payback_ali()

