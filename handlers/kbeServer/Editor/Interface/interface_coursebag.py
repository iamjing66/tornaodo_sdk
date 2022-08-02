#!/usr/bin/env python
# coding=utf-8

import logging
from handlers.kbeServer.Editor.Interface import interface_course


def GetCBagData(DB, CID):
    sql = "SELECT IDS FROM tb_cbag WHERE CID =  " + str(CID)
    result = DB.fetchone(sql, None)
    if result:
        return result[0]
    return ""


def ComputeBag(DB, uid):
    bcbag = ""
    sql = "select BCBag from tb_userdata where uid = " + str(uid)
    result = DB.fetchone(sql, None)
    if result:
        bcbag = result[0]
    logging.info('BaseServer->Avatar_Editor->CheckBag(bcbag)->(uid[%i],bcbag[%s])' % (uid, bcbag))
    Bag_Base = {}
    if len(bcbag) > 0:
        Bag_Base = ComputeBaseBag(DB, uid, bcbag)

    if len(Bag_Base) > 0:
        DoBaseBag(DB, uid, Bag_Base)

    return 1


# 登录赠送检测
def ComputeBaseBag(DB, uid, bcbag):
    # -- CID&UID`LID(课时ID)&LID(课时ID)`时间(0-一年 1-永久 其他按天计算 -1-一天),另一条
    # 137&63`0`1,3&24`0`1,318&63`0`1
    # CDBID`LID&LID 6&63`1&2`0
    # 补偿包 - 一次性的

    # DEBUG_MSG("bcbag:", bcbag)
    CBagIds = {}
    bcids = bcbag.split(',')
    for bcid in bcids:
        if bcid == None or bcid == '':
            continue
        id = int(bcid)
        tuple_ids = GetCBagData(DB, id)
        # DEBUG_MSG("tuple_ids:",tuple_ids)
        if tuple_ids != "" and len(tuple_ids) > 0:
            _temp = tuple_ids.split(',')
            for cids in _temp:
                if len(cids) < 1:
                    continue
                _ctemp = cids.split('`')
                if len(_ctemp) < 2:
                    continue
                    # DEBUG_MSG("_ctemp =",_ctemp)
                cdbid = _ctemp[0]
                lids = _ctemp[1]
                btype = int(_ctemp[2])

                if btype == 0:  # 一年
                    btype = 365 * 24 * 60 * 60
                elif btype == -1:  # 一天
                    btype = 24 * 60 * 60
                else:
                    btype = btype * 24 * 60 * 60

                if cdbid not in CBagIds.keys():
                    CBagIds[cdbid] = {"a": [], "b": {}}
                if btype not in CBagIds[cdbid]["b"]:
                    CBagIds[cdbid]["b"][btype] = []

                _ctemp_id = cdbid.split('&')
                _c_buy = [int(_ctemp_id[0]), int(_ctemp_id[1])]
                if len(_c_buy) > 0:
                    CBagIds[cdbid]["a"] = [_c_buy[0], _c_buy[1], 1]
                    _ltemp = lids.split('&')  # 1&2
                    for _lid in _ltemp:
                        lid = int(_lid)
                        CBagIds[cdbid]["b"][btype].append(lid)
                else:
                    del CBagIds[cdbid]
    return CBagIds


# 机构内老师课程检测
def ComputeJGCourse(DB, uid, distributor, JGTC_Date):
    sql = "select BID,WDATE,TLONG from tb_jgtc_fc where JGID = " + str(distributor) + " AND WDATE > '" + str(JGTC_Date) + "' ORDER BY WDATE"
    # print("sql",sql)
    BID = ""
    WDATE = ""
    TLONG = 0
    Bag_JG = []
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            BID = str(minfo_list[0])
            WDATE = str(minfo_list[1])
            EDATE = int(minfo_list[2])

            if EDATE > 0:
                ETIME = EDATE * 24 * 60 * 60  # + int(time.time())
                sql = "select contentbIds from sys_course_order where id = '" + BID + "'"
                data = DB.fetchone(sql, None)
                if data:
                    string_id = data[0]
                    arr_id = string_id.split('_')
                    Bag_JG.append([int(arr_id[0]), int(arr_id[1]), ETIME])
    # DEBUG_MSG("WDATE:%s" % WDATE)
    if WDATE != "":
        sql = "update tb_userdata set JGTC_DATE = '" + WDATE + "'"
        DB.edit(sql, None)

    return Bag_JG


def DoBaseBag(DB, self_uid, CBagIds):
    if len(CBagIds) > 0:
        # DEBUG_MSG("BcItem",self.CIndex)

        keys = list(CBagIds.keys())
        for _id in keys:
            data = CBagIds[_id]
            # --
            cid = data["a"][0]
            uid = data["a"][1]
            ctype = data["a"][2]
            for btype in data["b"].keys():
                for lid in data["b"][btype]:
                    interface_course.BuyNew(DB, self_uid, uid, cid, lid, btype)
        # lids_1 = data[1]
        # lids_2 = data[2]
        # for lid in lids_1:
        #     self.N_BuyCourse(cid,uid,lid,0,0)
        # for lid in lids_2:
        #     self.N_BuyCourse(cid,uid,lid,1,0)
        # del self.CBagIds[_id]

        sql = "update tb_userdata set BCBag = '' where uid = " + str(self_uid)
        DB.edit(sql, None)


def DoJGBag(DB, self_uid, TeacherCData):
    if len(TeacherCData) > 0:

        for data in TeacherCData:
            cid = data[0]
            uid = data[1]
            etime = data[2]
            # DEBUG_MSG("给老师赠送课程：",cid,uid,etime)
            interface_course.Buy(DB, self_uid, uid, cid, 0, etime, 0, 2)
            # self.N_BuyCourse_Do(cid, uid, 0, etime, 0, 2)
