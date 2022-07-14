#!/usr/bin/env python
# coding=utf-8


import logging
from methods.DBManager import DBManager


# 获取课程市场基础数据(带制作者信息)

def Data_Project_Base(uid, pid, target, db, call_type):
    json_back = ""

    if target == 0:
        table_name = "tb_project"
    else:
        table_name = "tb_mproject"
    arrpam = [table_name, pid, uid]
    sql = GetProjectSQLFromType(2, uid, arrpam)
    # print("sql:",sql)
    result = db.fetchone(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchone_json(result)
        elif call_type == 0:
            json_back = Get_Data_Project_Base_Ini(result)
        elif call_type == 2:
            json_back = Get_Data_Project_Base_List(result)
    # print("Data_Project_Base:", json_back)
    return json_back


# 获取工程列表数据
# call_type 0-INI结果 1-json结构 2-列表
# cversions 版本号列表(用来比对是否需要同步)
# 回调 [服务器工程列表(用来比对需要删除得课程) ,课程数据]
def Data_Projects_Base(sql, db, p_server, call_type, self_uid):
    objlist = []
    _server_pid = {}
    json_back = ""

    result = db.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchall_json(result, 1)
        else:
            if call_type == 0:
                json_back = ""
            elif call_type == 2:
                json_back = []
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                pid = int(minfo_list[1])
                version = int(minfo_list[24])
                uid = int(minfo_list[25])
                if uid not in _server_pid.keys():
                    _server_pid[uid] = []
                _server_pid[uid].append(pid)
                # 判断版本号
                if uid not in p_server or pid not in p_server[uid] or version > p_server[uid][pid]:
                    # #记录下来服务器上得课程列表-用来判断客户端是否有删除得

                    objlist.append([pid, uid, int(minfo_list[13]), int(minfo_list[14])])
                    if call_type == 0:
                        if json_back == "":
                            json_back = Get_Data_Project_Base_Ini(minfo_list)
                        else:
                            json_back = json_back + "!" + Get_Data_Project_Base_Ini(minfo_list)
                    elif call_type == 2:
                        json_back.append(Get_Data_Project_Base_List(minfo_list))
            # json_back = json_back + "！"

    # 需要删除的工程(通过对比发现这些工程在本地有，但是在服务器上面没有)
    sdelete = ""
    s_list = []
    if _server_pid:
        for _c_uid in p_server.keys():
            values = p_server[_c_uid]
            for _c_pid in values.keys():
                if _c_uid not in _server_pid or _c_pid not in _server_pid[_c_uid]:
                    # if _c_uid != self_uid:
                    # 这里需要删除的工程
                    s_list.append("`".join([str(_c_uid), str(_c_pid)]))
        sdelete = "!".join(s_list)
    logging.info("需要删除工程：%s" % sdelete)

    # print("Data_Courses_Base:", json_back)
    # print("objlist:", objlist)
    return [objlist, json_back, sdelete]


# ini结构 - 工程数据交互的最基础结果，跟客户端是同步的
def Get_Data_Project_Base_Ini(minfo_list):
    return "`".join(str(i) for i in minfo_list[1:])


def Get_Data_Project_Base_List(minfo_list):
    return [str(i) for i in minfo_list[1:]]


def Get_Data_Project_Base_ListToIni(minfo_list):
    return "`".join(str(i) for i in minfo_list)


# itype 0-本地工程 1-市场工程 2-单个工程数据
def GetProjectSQLFromType(itype, self_uid, pam=None):
    if itype == 0:
        sql = "select AccountType from tb_userdata where uid = " + str(self_uid)
        db = DBManager()
        data = db.fetchone(sql, None)

        teacher = 0
        if data:
            teacher = int(data[0])
        if teacher == 0:
            sql = "select t1.*,t2.price1 from (select * from tb_project where uid = " + str(
                self_uid) + " AND `From` !=  201 union ALL SELECT * FROM tb_project where `From` = 201 and uid != " + str(
                self_uid) + " and FromPam IN (select CID FROM tb_class AS T5 WHERE FIND_IN_SET(T5.CID, (SELECT CLASSID FROM tb_userdata where uid = " + str(
                self_uid) + " )))) t1 left join tb_workmarket t2 on t1.P_UID = t2.uid AND t1.ParentPid = t2.pid"
        else:
            sql = "select t1.*,t2.price1 from (select * from tb_project where uid = " + str(
                self_uid) + " ) t1 left join tb_workmarket t2 on t1.P_UID = t2.uid AND t1.ParentPid = t2.pid"
        # print("teacher,",teacher,sql)

    elif itype == 1:
        sql = "select t1.*,t2.price1 from tb_mproject t1 left join tb_workmarket t2 on t1.P_UID = t2.uid AND t1.ParentPid = t2.pid;"
    elif itype == 2:
        table_name = pam[0]
        pid = pam[1]
        uid = pam[2]
        sql = "select *,0 from " + table_name + " where uid = " + str(uid) + " and pid = " + str(pid) + ";"
    else:
        sql = ""

    return sql


# 工程版本号
def GetPVersion(db, uid, pid, target):
    if target == 0:
        table_project = "tb_project"
    else:
        table_project = "tb_mproject"
    sql = "select version from " + table_project + " where uid = " + str(uid) + " AND pid = " + str(pid)
    result = db.fetchone(sql, None)
    if result:
        return result[0]
    return 0


# 获取工程加资源版本号
def GetVersion(pid, uid, db, target):
    table_name = "tb_project"
    if target == 1:
        table_name = "tb_mproject"
    sql = "select Version from " + table_name + " where uid = " + str(uid) + " and pid = " + str(pid)
    result = db.fetchone(sql, None)
    if result:
        return result[0]
    return 0


# 刪除工程
def Delete(db, uid, pid, ismarket):
    if ismarket == 0:
        table_name = "tb_project"
    else:
        table_name = "tb_mproject"
    sql = "delete from " + table_name + " where uid = " + str(uid) + " and pid = " + str(pid)
    result = db.edit(sql, None)
    if result:
        return True
    return False


def SetTemplate(db, uid, pid, template):
    sql = "update tb_project set template = " + str(template) + ",version = version + 1 where uid = " + str(
        uid) + " and pid = " + str(pid)
    result = db.edit(sql, None)
    if result:
        return True
    return False
