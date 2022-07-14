#!/usr/bin/env python
# coding=utf-8
import Global
from handlers.kbeServer.Editor.Data import data_lesson
import logging


# ===================================================================================
# ================================下面是新接口=======================================
# ===================================================================================


# 获取课程列表数据
# call_type 0-INI结果 1-json结构
# cversions 版本号列表(用来比对是否需要同步)
# 回调 [服务器课程列表(用来比对需要删除得课程) ,课程数据]
def Data_Courses_Base(sql, db, cversions, call_type, iupdate=0):
    lesson_datas = []
    # scourseCLientNotHas = {}
    json_back = ""
    result = db.fetchall(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchall_json(result)
        elif call_type == 2:
            json_back = list(result)
        elif call_type == 0:
            json_back = ""
            for minfo in result:
                minfo_list = list(minfo)

                # 验证下版本号
                cid = int(minfo_list[1])
                version = int(minfo_list[12])
                uid = int(minfo_list[10])
                lesson_datas.append([cid, uid, int(minfo_list[13]), int(minfo_list[14])])
                if uid not in cversions or cid not in cversions[uid] or version > cversions[uid][cid]:
                    if json_back == "":
                        json_back = Get_Data_Course_Base_Ini(minfo_list)
                    else:
                        json_back = json_back + "!" + Get_Data_Course_Base_Ini(minfo_list)

                    # 更新下本地版本号
                    if iupdate == 1:
                        UpdateVersion(db, cid, uid, int(minfo_list[14]), int(minfo_list[13]), version, minfo_list[2])

    # 需要删除的课程(通过对比发现这些工程在本地有，但是在服务器上面没有)
    return [lesson_datas, json_back]


def UpdateVersion(db, cid, uid, pcid, puid, version, cname):
    sql = "update tb_course_bag set version = {0} where cid = {1} and uid = {2}".format(str(version), str(cid),
                                                                                        str(uid))
    state = db.edit(sql, None)
    if state:
        sql = "update " + Global.GetLessonTableName(uid, cid) + " t1," + Global.GetMLessonTableName(puid, pcid) + " t2 set t1.Version = t2.Version where t1.lid = t2.lid;"
        db.edit(sql, None)

    logging.info(
        "[%s]courseBuys[%s] Course Is Updated , pam = [uid = %i cid = %i puid = %i pcid = %i courseVersion = %d]" % (
        str(state), cname, uid, cid, puid, pcid, version))


# 获取课程市场基础数据(带制作者信息)

def Data_Course_Base(uid, cid, target, db, call_type):
    json_back = None

    if target == 0:
        table_name = "tb_course_bag"
    else:
        table_name = "tb_course_market"
    arrpam = [table_name, uid, cid]
    sql = GetCourseSQLFromTypeNew(4, db, uid, arrpam)
    result = db.fetchone(sql, None)
    if result:
        if call_type == 1:
            json_back = db.fetchone_json(result)
        elif call_type == 0:
            json_back = Get_Data_Course_Base_Ini(result)
        elif call_type == 2:
            json_back = Get_Data_Course_Base_List(result)
    # print("Data_Course_Base:", json_back)
    return json_back


# 课程最小基础数据(唯一结构)
def Get_Data_Course_Base_Ini(result):
    # result[1] = str(result[10]) + str(result[13]) + str(result[14])
    return "`".join([str(i) for i in result[1:]])


def Get_Data_Course_Base_Ini_New(result):
    return "`".join([str(i) for i in result[1:]])


# 课程最小基础数据(唯一结构)
def Get_Data_Course_Base_List(result):
    return list(map(str, result[1:]))


# 课程最小基础数据(唯一结构)-不带ID的转INI
def Get_Data_Course_Base_ListToIni(result):
    return "`".join([str(i) for i in result])


# 待审核的课程数量
def SHCourseAllCount(db):
    sql = "select count(ID) as c from tb_course_bag WHERE state = 1;"
    result = db.fetchone(sql, None)
    if result:
        return int(result[0])
    return 0


# 修改，状态
def UpdateCourseFlag(db, cid, uid, sign):
    sql = "update tb_course_bag set State = " + str(sign) + ",Version = Version + 1 where CID = " + str(
        cid) + " and UID = " + str(uid)
    db.edit(sql, None)


def UpdateToDB(db, json_ccourse_base, cid, uid, target):
    table_name = ""
    if target == 0:
        table_name = "tb_course_bag"
    else:
        table_name = "tb_course_market"
    sql = "select CID from " + table_name + " where UID = " + str(uid) + " and CID = " + str(cid)
    result = db.fetchone(sql, None)
    if result:
        if len(json_ccourse_base) == 19:
            sql = "Update " + table_name + " set  `Name`='" + str(json_ccourse_base[1]) + "', Platform=" + str(
                json_ccourse_base[2]) + ", Stars=" + str(json_ccourse_base[3]) + ", pic='" + str(
                json_ccourse_base[4]) + "', price=" + str(json_ccourse_base[5]) + ", `desc`='" + str(
                json_ccourse_base[6]) + "', State=" + str(json_ccourse_base[7]) + ", CreateDate=" + str(
                json_ccourse_base[8]) + ", Vision=" + str(json_ccourse_base[10]) + ", Version=" + str(
                json_ccourse_base[11]) + ", P_UID=" + str(json_ccourse_base[12]) + ", P_CID=" + str(
                json_ccourse_base[13]) + ", ResNum=" + str(json_ccourse_base[14]) + ", `ZK1`=" + str(
                json_ccourse_base[15]) + ", ZK2=" + str(json_ccourse_base[16]) + ",ct=" + str(
                json_ccourse_base[17]) + ",Sort=" + str(json_ccourse_base[18]) + ",Plat='1'" + " WHERE CID = " + str(
                cid) + " and UID = " + str(uid)
        else:
            sql = "Update " + table_name + " set  `Name`='" + str(json_ccourse_base[1]) + "', Platform=" + str(
                json_ccourse_base[2]) + ", Stars=" + str(json_ccourse_base[3]) + ", pic='" + str(
                json_ccourse_base[4]) + "', price=" + str(json_ccourse_base[5]) + ", `desc`='" + str(
                json_ccourse_base[6]) + "', State=" + str(json_ccourse_base[7]) + ", CreateDate=" + str(
                json_ccourse_base[8]) + ", Vision=" + str(json_ccourse_base[10]) + ", Version=" + str(
                json_ccourse_base[11]) + ", P_UID=" + str(json_ccourse_base[12]) + ", P_CID=" + str(
                json_ccourse_base[13]) + ", ResNum=" + str(json_ccourse_base[14]) + ", `ZK1`=" + str(
                json_ccourse_base[15]) + ", ZK2=" + str(json_ccourse_base[16]) + ",ct=" + str(
                json_ccourse_base[17]) + ",Sort=" + str(json_ccourse_base[18]) + ",Plat=" + str(
                json_ccourse_base[19]) + " WHERE CID = " + str(cid) + " and UID = " + str(uid)
    else:
        if len(json_ccourse_base) == 19:
            sql = "Insert INTO " + table_name + " (CID,`Name`,Platform,Stars,pic,price,`desc`,State,CreateDate,UID,Vision,Version,P_UID,P_CID,ResNum,ZK1,ZK2,ct,Sort,Plat) values (" + str(
                json_ccourse_base[0]) + ",'" + str(json_ccourse_base[1]) + "'," + str(json_ccourse_base[2]) + "," + str(
                json_ccourse_base[3]) + ",'" + str(json_ccourse_base[4]) + "'," + str(
                json_ccourse_base[5]) + ",'" + str(json_ccourse_base[6]) + "'," + str(json_ccourse_base[7]) + "," + str(
                json_ccourse_base[8]) + "," + str(uid) + "," + str(json_ccourse_base[10]) + "," + str(
                json_ccourse_base[11]) + "," + str(json_ccourse_base[12]) + "," + str(
                json_ccourse_base[13]) + "," + str(json_ccourse_base[14]) + "," + str(
                json_ccourse_base[15]) + "," + str(json_ccourse_base[16]) + "," + str(
                json_ccourse_base[17]) + "," + str(json_ccourse_base[18]) + ",'1'" + ")"
        else:
            sql = "Insert INTO " + table_name + " (CID,`Name`,Platform,Stars,pic,price,`desc`,State,CreateDate,UID,Vision,Version,P_UID,P_CID,ResNum,ZK1,ZK2,ct,Sort,Plat) values (" + str(
                json_ccourse_base[0]) + ",'" + str(json_ccourse_base[1]) + "'," + str(json_ccourse_base[2]) + "," + str(
                json_ccourse_base[3]) + ",'" + str(json_ccourse_base[4]) + "'," + str(
                json_ccourse_base[5]) + ",'" + str(json_ccourse_base[6]) + "'," + str(json_ccourse_base[7]) + "," + str(
                json_ccourse_base[8]) + "," + str(uid) + "," + str(json_ccourse_base[10]) + "," + str(
                json_ccourse_base[11]) + "," + str(json_ccourse_base[12]) + "," + str(
                json_ccourse_base[13]) + "," + str(json_ccourse_base[14]) + "," + str(
                json_ccourse_base[15]) + "," + str(json_ccourse_base[16]) + "," + str(
                json_ccourse_base[17]) + "," + str(json_ccourse_base[18]) + "," + str(json_ccourse_base[19]) + ")"
    db.edit(sql, None)


def UpdateToDBNew(db, json_ccourse_base, cid, uid, target):
    table_name = ""
    if target == 0:
        table_name = "tb_course_bag"
    else:
        table_name = "tb_course_market"
    sql = "select CID, version from " + table_name + " where UID = " + str(uid) + " and CID = " + str(cid)
    result = db.fetchone(sql, None)
    if result:
        data_version = int(json_ccourse_base[11]) if target and int(json_ccourse_base[11]) > result[1] else result[1]
        sql = "Update " + table_name + " set  `Name`='" + str(json_ccourse_base[1]) + "', Platform=" + str(
            json_ccourse_base[2]) + ", Stars=" + str(json_ccourse_base[3]) + ", pic='" + str(
            json_ccourse_base[4]) + "', price=" + str(json_ccourse_base[5]) + ", `desc`='" + str(
            json_ccourse_base[6]) + "', State=" + str(json_ccourse_base[7]) + ", CreateDate=" + str(
            json_ccourse_base[8]) + ", Vision=" + str(json_ccourse_base[10]) + ", Version=" + str(
            data_version) + ", P_UID=" + str(json_ccourse_base[12]) + ", P_CID=" + str(
            json_ccourse_base[13]) + ", ResNum=" + str(json_ccourse_base[14]) + ", `ZK1`=" + str(
            json_ccourse_base[15]) + ", ZK2=" + str(json_ccourse_base[16]) + ",ct=" + str(
            json_ccourse_base[17]) + ",Sort=" + str(json_ccourse_base[18]) + ",Plat='" + str(
            json_ccourse_base[20]) + "' WHERE CID = " + str(cid) + " and UID = " + str(uid)
    else:
        sql = "Insert INTO " + table_name + " (CID,`Name`,Platform,Stars,pic,price,`desc`,State,CreateDate,UID,Vision,Version,P_UID,P_CID,ResNum,ZK1,ZK2,ct,Sort,Plat) values (" + str(
            json_ccourse_base[0]) + ",'" + str(json_ccourse_base[1]) + "'," + str(json_ccourse_base[2]) + "," + str(
            json_ccourse_base[3]) + ",'" + str(json_ccourse_base[4]) + "'," + str(json_ccourse_base[5]) + ",'" + str(
            json_ccourse_base[6]) + "'," + str(json_ccourse_base[7]) + "," + str(json_ccourse_base[8]) + "," + str(
            uid) + "," + str(json_ccourse_base[10]) + "," + str(json_ccourse_base[11]) + "," + str(
            json_ccourse_base[12]) + "," + str(json_ccourse_base[13]) + "," + str(json_ccourse_base[14]) + "," + str(
            json_ccourse_base[15]) + "," + str(json_ccourse_base[16]) + "," + str(json_ccourse_base[17]) + "," + str(
            json_ccourse_base[18]) + ",'" + str(json_ccourse_base[20]) + "')"
    new_course = db.edit(sql, None)
    logging.info("审核 sql = %s" % sql)
    logging.info("新发布课程添加: %s" % new_course)
    return 1


def DoCourseConfig(db, uid, cid, Name):
    sql = "select ID from tb_course_sort where UID = {0} and CID = {1}".format(str(uid), str(cid))
    result = db.fetchone(sql, None)
    if result:
        pass
    else:
        sql = "Insert INTO tb_course_sort (`uid`,`cid`,`sort`,`course_desc`) values (" + str(uid) + ",'" + str(cid) + "', 9999, '" + Name + "',)"
    db.edit(sql, None)

    tablename = "tb_mlesson_" + str(uid) + "_" + str(cid)
    sql = "select lid from " + tablename
    result = db.fetchall(sql, None)
    if result:
        for info in result:
            lid = int(info[0])
            sql = "select ID from sys_course_res where cid = " + str(cid) + " and uid = " + str(
                uid) + " and mlessonID = " + str(lid) + " LIMIT 0,1";
            result = db.fetchone(sql, None)
            if result:
                pass
            else:
                sql = "Insert INTO sys_course_res (`uid`,`cid`,`mlessonID`) values (" + str(uid) + ",'" + str(
                    cid) + "','" + str(lid) + "')"
                db.edit(sql, None)


# itype 0-本地制作 1-购买课程 2-课程市场 3-审核课程 4-单个课程数据
def GetCourseSQLFromType(itype, db, self_uid, pam, account_type=None, power=None):
    if itype == 0:
        sql = "select t1.*,t2.UserName from tb_course_bag t1 inner join tb_userdata t2 on t1.UID = t2.UID AND t1.uid = " + str(
            self_uid) + " and t1.P_UID = 0 ; "
    elif itype == 1:
        if account_type == 1 or power == 4:
            sql_yinliu = ""
            if power == 4:
                # 账号类型C端引流账号
                sql_yinliu = " and l.courseType = 3"
            sql = f"""
            select
            m.`ID`, CONCAT(p.duid,p.luid,p.cid) as cpupc_id, m.`Name`,
            m.`Platform`, m.`Stars`, m.`pic`, m.`Price`,m.`desc`, m.`State`,
            m.`CreateDate`, p.duid, m.`Vision`, m.`Version`, p.luid,p.cid,
            m.`ResNum`, m.`ZK1`,m.`ZK2`, m.`ct`, m.`Sort`, p.UserName
            from tb_course_market m
            inner join (
                select l.`uid` as luid, l.cid, d.`UID` as duid, d.UserName
                from
                tb_course_pool as l
                left join
                tb_userdata as d
                on l.organization = d.distributor
                where d.UID = {self_uid}
                and l.enddate > curdate(){sql_yinliu}
                group by cid) p
            on m.UID = p.luid and m.CID = p.cid;
            """
        else:
            sql = "select t3.*,t4.UserName from (select t1.`ID`,t1.`CID`,t2.`Name`,t2.`Platform`,t2.`Stars`,t2.`pic`,t2.`Price`,t2.`desc`,t2.`State`,t1.`CreateDate`,t1.`UID`,t1.`Vision`,t1.`Version`,t1.`P_UID`,t1.`P_CID`,t2.`ResNum`,t2.`ZK1`,t2.`ZK2`,t2.`ct`,t2.`Sort` from tb_course_bag t1 inner join tb_course_market t2 on t1.P_UID = t2.UID AND t1.P_CID = t2.CID AND t1.uid = " + str(
                self_uid) + " and t1.P_UID != 0) t3 inner join tb_userdata t4 on t3.P_UID = t4.UID"

    elif itype == 2:
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2, t1.ct, t1.Sort,t2.UserName  from tb_course_market t1 inner join tb_userdata t2 on t1.UID = t2.UID;"
    elif itype == 3:
        now_page = pam[0]
        max_page = pam[1]
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2,t1.ct, t1.Sort, t2.UserName, t1.Plat from tb_course_bag as t1 INNER join tb_userdata as t2 on t1.UID = t2.UID and t1.State = 1 and t1.P_UID = 0 order by t1.CID limit " + str(
            (now_page - 1) * max_page) + "," + str(max_page) + ";"
    elif itype == 4:
        sql = "select t1.*,t2.UserName from " + pam[
            0] + " as t1 inner join tb_userdata as t2 on t1.UID = t2.UID and t1.UID = " + str(
            pam[1]) + " and t1.CID = " + str(pam[2]) + ";"
    return sql


def GetCourseSQLFromTypeNew(itype, db, self_uid, pam, account_type=None, power=None):
    if itype == 0:
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2,t1.ct, t1.Sort, t2.UserName, t1.Plat from tb_course_bag t1 inner join tb_userdata t2 on t1.UID = t2.UID AND t1.uid = " + str(
            self_uid) + " and t1.P_UID = 0 ; "
    elif itype == 1:
        if account_type == 1 or power == 4:
            sql_yinliu = ""
            if power == 4:
                # 账号类型C端引流账号
                sql_yinliu = " and l.courseType = 3"
            sql = f"""
            select
            m.`ID`, CONCAT(p.duid,p.luid,p.cid) as cpupc_id, m.`Name`,
            m.`Platform`, m.`Stars`, m.`pic`, m.`Price`,m.`desc`, m.`State`,
            m.`CreateDate`, p.duid, m.`Vision`, m.`Version`, p.luid,p.cid,
            m.`ResNum`, m.`ZK1`,m.`ZK2`, m.`ct`, m.`Sort`,p.UserName, m.`Plat`
            from tb_course_market m
            inner join (
                select l.`uid` as luid, l.cid, d.`UID` as duid, d.UserName
                from
                tb_course_pool as l
                left join
                tb_userdata as d
                on l.organization = d.distributor
                where d.UID = {self_uid}
                and l.enddate > curdate(){sql_yinliu}
                group by cid) p
            on m.UID = p.luid and m.CID = p.cid;
            """
        else:
            sql = "select t3.`ID`,t3.`CID`,t3.`Name`,t3.`Platform`,t3.`Stars`,t3.`pic`,t3.`Price`,t3.`desc`,t3.`State`,t3.`CreateDate`,t3.`UID`,t3.`Vision`,t3.`Version`,t3.`P_UID`,t3.`P_CID`,t3.`ResNum`,t3.`ZK1`,t3.`ZK2`,t3.`ct`,t3.`Sort`,t4.UserName, t3.`Plat` from (select t1.`ID`,t1.`CID`,t2.`Name`,t2.`Platform`,t2.`Stars`,t2.`pic`,t2.`Price`,t2.`desc`,t2.`State`,t1.`CreateDate`,t1.`UID`,t1.`Vision`,t2.`Version`,t1.`P_UID`,t1.`P_CID`,t2.`ResNum`,t2.`ZK1`,t2.`ZK2`,t2.`ct`,t2.`Sort`, t2.`Plat` from tb_course_bag t1 inner join tb_course_market t2 on t1.P_UID = t2.UID AND t1.P_CID = t2.CID AND t1.uid = " + str(
                self_uid) + " and t1.P_UID != 0) t3 inner join tb_userdata t4 on t3.P_UID = t4.UID"
    elif itype == 2:
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2,t1.ct, t1.Sort, t2.UserName, t1.Plat, t1.type, t1.secondType from tb_course_market t1 inner join tb_userdata t2 on t1.UID = t2.UID;"
    elif itype == 3:
        now_page = pam[0]
        max_page = pam[1]
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2,t1.ct, t1.Sort, t2.UserName, t1.Plat from tb_course_bag as t1 INNER join tb_userdata as t2 on t1.UID = t2.UID and t1.State = 1 and t1.P_UID = 0 order by t1.CID limit " + str(
            (now_page - 1) * max_page) + "," + str(max_page) + ";"
    elif itype == 4:
        sql = "select t1.ID, t1.CID, t1.Name, t1.Platform, t1.Stars, t1.pic, t1.Price, t1.`desc`, t1.State, t1.CreateDate, t1.UID, t1.Vision, t1.Version, t1.P_UID, t1.P_CID, t1.ResNum, t1.ZK1, t1.ZK2,t1.ct, t1.Sort, t2.UserName, t1.Plat from " + \
              pam[0] + " as t1 inner join tb_userdata as t2 on t1.UID = t2.UID and t1.UID = " + str(
            pam[1]) + " and t1.CID = " + str(pam[2]) + ";"
    return sql


# 课程购买状态
def CourseFlag_Buy(self_uid, uid, cid, db):
    _cid = 0
    sql = "select CID from tb_course_bag where P_UID = %s and P_CID = %s and UID = %s"
    params = [str(uid), str(cid), str(self_uid)]
    result = db.fetchone(sql, params)
    if result:
        _cid = int(result[0])
    return _cid


def GetVersion(cid, uid, target, db):
    table_name = "tb_course_bag"
    if target == 1:
        table_name = "tb_course_market"

    sql = "select Version from " + table_name + " where uid = " + str(uid) + " and CID = " + str(cid)
    result = db.fetchone(sql, None)
    if result:
        return result[0]
    return 0


# 工程是否存在课时中
def ProjectInCourses(db, uid, pid, dtype):
    if dtype == 1:
        sql = "select cid from tb_course_bag where UID = " + str(uid) + " and p_uid = 0"
    else:
        sql = "select cid from tb_course_bag where UID = " + str(uid) + " and state = 1 and p_uid = 0"
    result = db.fetchall(sql, None)
    if result:
        for info in result:
            cid = int(info[0])
            list_data = data_lesson.Data_Lesson_Base(uid, cid, 0, db, 2)

            for i in list_data:
                if int(i[19]) == 0 and int(i[4]) == pid:
                    return True

    return False
