#!/usr/bin/env python
# coding=utf-8

#作品买看数据
def Data_W_Base(DB, uid, w_uid, wid,call_type):
    _pdate = 0
    json_back = None
    sql = "select * from tb_work_look_B WHERE UID = " + str(uid) + " and W_UID = " + str(w_uid) + " and W_CID = " + str(wid)
    result = DB.fetchone(sql,None)
    if result:
        if call_type == 1:
            json_back = DB.fetchone_json(result)
        elif call_type == 0:
            json_back = Get_Data_W_Base_Ini(result)
        elif call_type == 2:
            json_back = Get_Data_W_Base_List(result)
    return json_back


def Get_Data_W_Base_Ini(minfo_list):
    return str(minfo_list[1]) + "`" + str(minfo_list[2]) + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4])+ "`" + str(minfo_list[5])

def Get_Data_W_Base_List(minfo_list):
    return [ str(minfo_list[1]) , str(minfo_list[2]) , str(minfo_list[3]) , str(minfo_list[4]), str(minfo_list[5])]