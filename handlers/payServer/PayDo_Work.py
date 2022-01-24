#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_work

class paydo_work:

    def __init__(self):
        pass

    def WorkLoogPDate(self, uid, w_uid, wid , Cur , Db):

        _pdate = 0

        sql = "select P_DATE from tb_work_look_B WHERE UID = " + str(uid) + " and W_UID = " + str(w_uid) + " and W_CID = " + str(wid)
        Cur.execute(sql)
        Db.commit()
        data = Cur.fetchone()
        if data != None and len(data) > 0:
            _pdate = int(data[0])
        else:
            _pdate = 0
        return _pdate



    def Do(self,_arr_pam,DB):

        toclient = ""
        _order = _arr_pam[3]
        price = int(_arr_pam[4])
        pname = _arr_pam[5]
        UID = int(_arr_pam[6])
        UserName = _arr_pam[7]
        wid = int(_arr_pam[8])
        p_uid = int(_arr_pam[9])

        organization = _arr_pam[10]
        distributor = _arr_pam[11]
        _from = _arr_pam[12]
        _userType = int(_arr_pam[13])
        _ip = _arr_pam[15]

        data_arr = interface_work.VR_BuyWork(DB, UID, wid, p_uid, 2,20,UserName,phone=True)
        code = data_arr[0]
        if code == 1:
            toclient = data_arr[1]

        return toclient



PayDoWorkClass = paydo_work()

