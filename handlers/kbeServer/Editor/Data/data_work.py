#!/usr/bin/env python
# coding=utf-8

# 待审核的课程数量
import logging


def SHWorkAllCount(DB):

    sql = "select count(ID) as c from tb_workbag WHERE state = 1;"
    result = DB.fetchone(sql, None)
    if result:
        return int(result[0])
    return 0


#itype 0-本地作品 1-市场作品
def GetWorkSQLFromType(itype,self_uid,pam, **kwargs):

    if itype == 0:
        sql = "select *,'',0 from tb_workbag where UID = " + str(self_uid)
    elif itype == 1:  # 作品市场
        # course_level: 1-精品课程  2-普通课程(不包含精品课)
        sql = "select T1.*,T2.username,0 from tb_workmarket t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.flag = 1 order by t1.sort;"
    elif itype == 2:
        mpage = pam[0]
        now_page = pam[1]
        max_page = pam[2]
        sql = "select T1.*,T2.username," + str(mpage) + " from tb_workbag t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.State = 1  order by t1.CreateDate desc limit " + str((now_page - 1) * max_page) + "," + str(max_page) + ";"
    elif itype == 3:
        if not kwargs["d_class"]:
            sql = "select T1.*,T2.username,0 from "+pam[0]+" t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.UID = "+str(pam[1])+" and t1.WID = "+str(pam[2])+";"
        else:
            sql = "select w.id, w.WID, w.Name, w.Platform, w.Stars, w.Pid, w.price, w.`desc`, w.State, w.NewPid, w.CreateDate, w.UID,w.Vision, w.Sid, w.Version, w.Game, w.GameStage, w.SNUM, w.identity, w.SNAME, w.ct, e.price1, e.price2, e.FREE, e.stime, e.etime, w.freestatus, w.boutique, e.sort, e.flag, w.Plat, t.UserName, 0 from tb_workmarket as w inner join tb_eservices_workmarket as e inner join tb_userdata as t on w.wid = e.wid and w.uid = e.uid and t.UID = %s and w.uid = %s and e.wid = %s and e.organization_id = t.distributor;" % (self_uid, pam[1], pam[2])
    return sql


def GetWorkSQLFromTypeNew(itype,self_uid,pam, **kwargs):

    if itype == 0:
        sql = "select *,'',0 from tb_workbag where UID = " + str(self_uid)
    elif itype == 1:  # 作品市场
        # kwargs  {course_level: 1-精品课程  2-普通课程(不包含精品课)}
        if not kwargs["d_class"]:
            sql = "select T1.*,T2.username,0 from tb_workmarket t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.boutique = %s;" % kwargs["course_level"]
        else:
            sql = "select w.id, w.WID, w.Name, w.Platform, w.Stars, w.Pid, w.price, w.`desc`, w.State, w.NewPid, w.CreateDate, w.UID,w.Vision, w.Sid, w.Version, w.Game, w.GameStage, w.SNUM, w.identity, w.SNAME, w.ct, e.price1, e.price2, e.FREE, e.stime, e.etime, w.freestatus, w.boutique, e.sort, e.flag, w.Plat, t.UserName, 0 from tb_workmarket as w inner join tb_eservices_workmarket as e inner join tb_userdata as t on w.wid = e.wid and w.uid = e.uid and t.UID = %s and e.organization_id = t.distributor and w.boutique = %s;" % (self_uid, kwargs["course_level"])
    elif itype == 2:
        mpage = pam[0]
        now_page = pam[1]
        max_page = pam[2]
        sql = "select T1.*,T2.username," + str(mpage) + " from tb_workbag t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.State = 1  order by t1.CreateDate desc limit " + str((now_page - 1) * max_page) + "," + str(max_page) + ";"
    elif itype == 3:
        sql = "select T1.*,T2.username,0 from "+pam[0]+" t1 inner join tb_userdata t2 on t1.UID = t2.UID and t1.UID = "+str(pam[1])+" and t1.WID = "+str(pam[2])+";"
    return sql


# 获取作品列表数据
# call_type 0-INI结果 1-json结构 2-列表
#cversions 版本号列表(用来比对是否需要同步)
#回调 [服务器工程列表(用来比对需要删除得课程) ,课程数据]
def Data_Works_Base(sql, DB, p_server, call_type):

    objlist = []
    _server_pid = {}
    json_back = ""

    result = DB.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = DB.fetchall_json(result)
        else:
            if call_type == 0:
                json_back = ""
            elif call_type == 2:
                json_back = []
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                uid = int(minfo_list[11])
                wid = int(minfo_list[1])
                version = int(minfo_list[14])

                # if type != 2:
                #     if uid not in _server_pid.keys():
                #         _server_pid[uid] = []
                #     _server_pid[uid].append(pid)

                if uid not in p_server or wid not in p_server[uid] or version > p_server[uid][wid]:
                # #记录下来服务器上得课程列表-用来判断客户端是否有删除得
                    objlist.append([wid, uid])
                    if call_type == 0:
                        if json_back == "":
                            json_back = Get_Data_Work_Base_Ini(minfo_list)
                        else:
                            json_back = json_back + "!" + Get_Data_Work_Base_Ini(minfo_list)
                    elif call_type == 2:
                        json_back.append(Get_Data_Work_Base_List(minfo_list))


    #需要删除的工程(通过对比发现这些工程在本地有，但是在服务器上面没有)
    # sdelete = ""
    # if len:
    #     for _c_uid in p_server.keys():
    #         values = p_server[_c_uid]
    #         for _c_pid in values.keys():
    #             if _c_uid not in _server_pid or _c_pid not in _server_pid[_c_uid]:
    #                 if _c_uid == theuid:
    #                     continue
    #                 # 这里需要删除的工程
    #                 if sdelete == "":
    #                     sdelete = str(_c_uid) + "`" + str(_c_pid)
    #                 else:
    #                     sdelete = sdelete + "!" + str(_c_uid) + "`" + str(_c_pid)
            # DEBUG_MSG("需要删除工程：",sdelete)


    #print("Data_Courses_Base:", json_back)
    #print("objlist:", objlist)
    return [objlist,json_back]


def Data_Works_Base_New(sql, DB, p_server, call_type):
    objlist = []
    json_back = ""
    result = DB.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = DB.fetchall_json(result)
        else:
            if call_type == 0:
                json_back = ""
            elif call_type == 2:
                json_back = []
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                uid = int(minfo_list[11])
                wid = int(minfo_list[1])
                version = int(minfo_list[14])

                if uid not in p_server or wid not in p_server[uid] or version > p_server[uid][wid]:
                # 记录下来服务器上得课程列表-用来判断客户端是否有删除得
                    objlist.append([wid, uid])
                    if call_type == 0:
                        if json_back == "":
                            json_back = Get_Data_Work_Base_Ini(minfo_list) + "`" + str(minfo_list[28])
                        else:
                            json_back = json_back + "!" + Get_Data_Work_Base_Ini(minfo_list) + "`" + str(minfo_list[28])
                    elif call_type == 2:
                        json_back.append(Get_Data_Work_Base_List(minfo_list))
    return [objlist,json_back]


def Data_Work_Base(uid,wid,target,DB,call_type,sh=False,d_class=False):

    json_back = None

    if target == 0:
        table_name = "tb_workbag"
    else:
        table_name = "tb_workmarket"
    arrPam = [table_name,uid,wid]
    sql = GetWorkSQLFromType(3,uid,arrPam,d_class=d_class)
    result = DB.fetchone(sql, None)
    if result:
        # GM审核
        if sh:
            if call_type == 1:
                json_back = DB.fetchone_json(result)
            elif call_type == 0:
                json_back = get_data_work_base_init_plat(result)
            elif call_type == 2:
                json_back = get_data_work_base_list_plat(result)
        else:
            if call_type == 1:
                json_back = DB.fetchone_json(result)
            elif call_type == 0:
                json_back = Get_Data_Work_Base_Ini(result)
            elif call_type == 2:
                json_back = Get_Data_Work_Base_List(result)
    ##print("Data_Work_Base:", json_back)
    return json_back


def Get_Data_Work_Base_Ini(minfo_list):
    return str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + minfo_list[7] + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + str(minfo_list[14]) + "`" + str(minfo_list[15]) + "`" + str(minfo_list[16]) + "`" + minfo_list[17] + "`" + minfo_list[18] + "`" + minfo_list[19] + "`" + str(minfo_list[20]) + "`" + str(minfo_list[21]) + "`" + str(minfo_list[22]) + "`" + str(minfo_list[23]) + "`" + str(minfo_list[24]) + "`" + str(minfo_list[25]) + "`" + str(minfo_list[31]) + "`" + str(minfo_list[32]) + "`" + str(minfo_list[30])


def Get_Data_Work_Base_List(minfo_list):
    return [str(minfo_list[1]), minfo_list[2], str(minfo_list[3]), str(minfo_list[4]), str(minfo_list[5]), str(minfo_list[6]), minfo_list[7], str(minfo_list[8]), str(minfo_list[9]), str(minfo_list[10]), str(minfo_list[11]), str(minfo_list[12]), str(minfo_list[13]), str(minfo_list[14]), str(minfo_list[15]), str(minfo_list[16]), minfo_list[17], minfo_list[18], minfo_list[19], str(minfo_list[20]), str(minfo_list[21]), str(minfo_list[22]), str(minfo_list[23]), str(minfo_list[24]), str(minfo_list[25]), str(minfo_list[31]), str(minfo_list[32]), str(minfo_list[30])]


def get_data_work_base_init_plat(minfo_list):
    return str(minfo_list[1]) + "`" + minfo_list[2] + "`" + str(minfo_list[3]) + "`" + str(minfo_list[4]) + "`" + str(minfo_list[5]) + "`" + str(minfo_list[6]) + "`" + minfo_list[7] + "`" + str(minfo_list[8]) + "`" + str(minfo_list[9]) + "`" + str(minfo_list[10]) + "`" + str(minfo_list[11]) + "`" + str(minfo_list[12]) + "`" + str(minfo_list[13]) + "`" + str(minfo_list[14]) + "`" + str(minfo_list[15]) + "`" + str(minfo_list[16]) + "`" + minfo_list[17] + "`" + minfo_list[18] + "`" + minfo_list[19] + "`" + str(minfo_list[20]) + "`" + str(minfo_list[21]) + "`" + str(minfo_list[22]) + "`" + str(minfo_list[23]) + "`'" + str(minfo_list[30]) + "'`" + str(minfo_list[31])


def get_data_work_base_list_plat(minfo_list):
    return [str(minfo_list[1]), minfo_list[2], str(minfo_list[3]), str(minfo_list[4]), str(minfo_list[5]), str(minfo_list[6]), minfo_list[7], str(minfo_list[8]), str(minfo_list[9]), str(minfo_list[10]), str(minfo_list[11]), str(minfo_list[12]), str(minfo_list[13]), str(minfo_list[14]), str(minfo_list[15]), str(minfo_list[16]), minfo_list[17], minfo_list[18], minfo_list[19], str(minfo_list[20]), str(minfo_list[21]), str(minfo_list[22]), str(minfo_list[23]), "'"+ str(minfo_list[30])+"'", str(minfo_list[31])]


#修改，状态
def UpdateWorkFlag(DB,wid,uid,flag):

    sign = 2
    if flag == 1:
        sign = 3
    sql = "update tb_workbag set State = "+str(sign) + ",Version = Version + 1 where WID = "+str(wid) + " and UID = "+str(uid)
    #print("UpdateWorkFlag : " , sql)
    DB.edit(sql,None)


#写入作品数据
def UpdateToDB(data,uid ,wID,DB,target):

    table_name = "tb_workbag"
    if target == 1:
        table_name = "tb_workmarket"
    sql = "select id,boutique, version from "+table_name+" where UID = " + str(uid) + " and WID = " + str(wID)
    result = DB.fetchone(sql, None)
    if result:
        sql_else = "'"
        data_version = int(data[13]) if target == 1 and int(data[13]) > result[2] else result[2]
        if result[1] != 1:
            sql_else = "',ct="+str(data[19])
        if len(data) == 23:
            sql = "Update "+table_name+" set WID = " + str(data[0]) + ", Name='" + str(data[1]) + "', Platform=" + str(data[2]) + ", Stars=" + str(data[3]) + ", Pid=" + str(data[4]) + ", price=" + str(data[5]) + ", `desc`='" + str(data[6]) + "', State=" + str(data[7]) + ", NewPid=" + str(data[8]) + ", CreateDate=" + str(data[9]) + ", Vision=" + str(data[11]) + ", Sid=" + str(data[12]) + ", Version=" + str(data_version) + ", Game=" + str(data[14]) + ", GameStage=" + str(data[15]) + ", SNUM='" + str(data[16]) + "', `identity`='" + str(data[17]) + "', SNAME='" + str(data[18]) + sql_else + ",price1=" + str(data[20]) + ",price2=" + str(data[21]) + ",Free = " + str(data[22]) + ",Plat='1'"+" where UID = " + str(uid) + " and WID =" + str(wID)
        else:
            sql = "Update "+table_name+" set WID = " + str(data[0]) + ", Name='" + str(data[1]) + "', Platform=" + str(data[2]) + ", Stars=" + str(data[3]) + ", Pid=" + str(data[4]) + ", price=" + str(data[5]) + ", `desc`='" + str(data[6]) + "', State=" + str(data[7]) + ", NewPid=" + str(data[8]) + ", CreateDate=" + str(data[9]) + ", Vision=" + str(data[11]) + ", Sid=" + str(data[12]) + ", Version=" + str(data_version) + ", Game=" + str(data[14]) + ", GameStage=" + str(data[15]) + ", SNUM='" + str(data[16]) + "', `identity`='" + str(data[17]) + "', SNAME='" + str(data[18]) + sql_else + ",price1=" + str(data[20]) + ",price2=" + str(data[21]) + ",Free = " + str(data[22]) + ",Plat=" + str(data[23]) + " where UID = " + str(uid) + " and WID =" + str(wID)
    else:
        if len(data) == 23:
            sql = "Insert INTO "+table_name+" (WID,`Name`,Platform,Stars,Pid,price,`desc`,State,NewPid,CreateDate,UID,Vision,Sid,Version,Game,GameStage,SNUM,`identity`,SNAME,ct,price1,price2,Free,Plat) values (" + str(wID) + ",'" + str(data[1]) + "'," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + ",'" + str(data[6]) + "'," + str(data[7]) + "," + str(data[8]) + "," + str(data[9]) + "," + str(uid) + "," + str(data[11]) + "," + str(data[12]) + "," + str(data[13]) + "," + str(data[14]) + "," + str(data[15]) + ",'" + str(data[16]) + "','"+str(data[17]) + "','" + str(data[18]) + "'," + str(data[19]) + "," + str(data[20]) + "," + str(data[21]) + "," + str(data[22]) + ",'1'" + ")"
        else:
            sql = "Insert INTO "+table_name+" (WID,`Name`,Platform,Stars,Pid,price,`desc`,State,NewPid,CreateDate,UID,Vision,Sid,Version,Game,GameStage,SNUM,`identity`,SNAME,ct,price1,price2,Free,Plat) values (" + str(wID) + ",'" + str(data[1]) + "'," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + ",'" + str(data[6]) + "'," + str(data[7]) + "," + str(data[8]) + "," + str(data[9]) + "," + str(uid) + "," + str(data[11]) + "," + str(data[12]) + "," + str(data[13]) + "," + str(data[14]) + "," + str(data[15]) + ",'" + str(data[16]) + "','"+str(data[17]) + "','" + str(data[18]) + "'," + str(data[19]) + "," + str(data[20]) + "," + str(data[21]) + "," + str(data[22]) + "," + str(data[23]) + ")"
    DB.edit(sql,None)


def GetVersion( WID,uid,DB,target):

    table_name = "tb_workbag"
    if target == 1:
        table_name = "tb_workmarket"
    sql = "select Version from "+table_name+" where UID = " + str(uid) + " and WID = " + str(WID)
    result = DB.fetchone(sql,None)
    if result:
        return result[0]

    return 0

def BuyFlag(DB,self_uid,uid,pid):
    _pdate = 0
    _version = 0
    _pid = 0
    sql = "select PDate,version,pid from tb_project where P_uid = " + str(uid) + " and ParentPid = " + str(pid) + " and UID = " + str(self_uid) + " limit 0,1"
    result = DB.fetchone(sql,None)
    if result and len(result) > 0:
        _pdate = int(result[0])
        _version = int(result[1])
        _pid = int(result[2])
    return [_pdate, _version, _pid]


def Delete(DB,uid,wid,target):

    if target == 0:
        table_name = "tb_workbag"
    else:
        table_name = "tb_workmarket"

    sql = "delete from " + table_name + " where UID = " + str(uid) + " and WID = " + str(wid)
    DB.edit(sql,None)


def PAYPAM_WorkMK(paydata,DB):

    _id = 0
    _price2 = 0
    _name = ""
    json_data = paydata
    wid = json_data["wid"]
    b_uid = json_data["b_uid"]
    organization = json_data["organization"]
    distributor = json_data["distributor"]

    json_pay = {
        "Code":0,
        "Data":{},
    }

    sql_str = "select ID,price2,`Name` from tb_workmarket where WID = " + str(wid) + " AND UID = " + str(b_uid) + ";"
    data = DB.fetchone(sql_str,None)
    if data:
        _id = int(data[0])
        _price2 = int(data[1])
        _name = data[2]

    #print("_price2",_price2)
    if _id == 0 or _price2 <= 0:
        #print("价格异常，为0")
        json_pay["Code"] = 0    #价格异常
    else:
        _power = 0
        if "power" in json_data.keys():
            _power = json_data["power"]
        params = str(wid) + "@" + str(b_uid)+ "@" + str(organization)+ "@" + str(distributor)+ "@" + json_data["from"]+ "@" + str(_power)+ "@n@" + json_data["ip"]
        Data = {
            "name": _name,
            "price": _price2 * 10,  # 分
            "params": params,
        }
        json_pay["Code"] = 1
        json_pay["Data"] = Data

    return json_pay


def get_utype_uid(DB, uid):
    sql = "select ID from tb_userdata where uid = %s and power = 5"
    data = DB.fetchone(sql, uid)
    if data:
        return True
    return False


def new_work_sort(DB, wid, uid, ct):
    sql_select = "select id from tb_work_sort where wid = %s and uid = %s"
    data = DB.fetchone(sql_select, (wid, uid))
    if data:
        sql = "update tb_work_sort set sort = 0, flag = 1, ct = %s where wid = %s and uid = %s"
    else:
        sql = "insert into tb_work_sort (ct, wid, uid) values (%s, %s, %s)"
    DB.edit(sql, (ct, wid, uid))
