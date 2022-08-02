#!/usr/bin/env python
# coding=utf-8

import logging
import time

import Global
from handlers.kbeServer.Editor.Data import data_course, data_project
from handlers.kbeServer.Editor.Data import data_lesson
from handlers.kbeServer.Editor.Interface import interface_mail, interface_project, interface_obj, interface_global, \
    interface_solr, interface_wit
from methods.DBManager import DBManager


# 客户端列表(带版本号)转json，用来比对
def clientVersionDataToJson(pdata):
    # "data":
    # "5^118^2^4`2*
    # 5^238^3^1`3*
    # 9^327^2^1`2*
    # 63^319^7^1`6*
    # 63^6^9^1`7!2`7!3`7!4`7!5`7!6`7!7`7!8`7*
    # 63^320^8^1`7!2`7!3`7!17`7!5`7!6`7!7`7!4`7*
    # 63^318^25^2`20!5`20!6`20!7`20!8`20!9`20!10`20!11`20!17`20!3`20!1`20*
    # 63^137^21^2`16!3`16!4`16!1`16!6`16!7`16*
    # 63^321^82^9`80!10`80!1`80!11`80!12`80!15`80!16`80!18`80!3`80!8`80!4`80!21`80!23`80!24`80!28`80!14`80!30`80!20`80!31`80!13`80!17`80!22`80!27`80!33`80!34`80!2`80!25`80!29`80!19`80!32`80*
    # 63^322^41^2`40!1`40!3`40!4`40!5`40!9`40!7`40!6`40!8`40!10`40*
    # 63^323^41^1`40!2`40!3`40!5`40!6`40!7`40!8`40!11`40!9`40!4`40!10`40!12`40!13`40!14`40*
    # 283^220^3^1`3*283^223^2^2`2*
    # 283^226^7^1`7!2`7!3`7!4`7!5`7*
    # 283^230^2^1`2*283^231^4^1`4!5`4!2`4!4`4*
    # 283^233^3^1`3*283^236^4^1`4!2`4*
    # 283^238^2^1`2*283^242^4^1`4*
    # 283^241^6^1`6!2`6!3`6*
    # 283^10031^2^1`2!2`2*3
    # 76^119^2^1`2*376^8^3^1`3!2`3*376^127^2^1`2*
    # 376^128^24^1`24!2`24!3`24!4`24!5`24!6`24!7`24*

    p_server = {}
    obj_server = {}
    if pdata is not None and len(pdata) > 0:
        l_pdata = pdata.split('*')
        for info in l_pdata:
            sdata = info.split('^')
            uid = int(sdata[0])
            pid = int(sdata[1])
            version = int(sdata[2])
            if uid not in p_server.keys():
                p_server[uid] = {}
                obj_server[uid] = {}
            p_server[uid][pid] = version
            if sdata[3] != "" and len(sdata[3]) > 0:
                obj_server[uid][pid] = sdata[3]

    return [p_server, obj_server]


# 同步数据
# itype 类型0-本地课程 1-购买课程 2-课程市场 3-审核课程
# objtype 0-本地数据 1-市场数据
def Get(pdata, self_uid, itype, isupdate=0):
    cversions = {}
    lversions = {}
    pam = []
    # {"rtype":"5","data":"5^118^2^4`2*5^238^3^1`3*9^327^2^1`2*63^319^7^1`6*63^6^9^1`7!2`7!3`7!4`7!5`7!6`7!7`7!8`7*63^320^8^1`7!2`7!3`7!17`7!5`7!6`7!7`7!4`7*63^318^25^2`20!5`20!6`20!7`20!8`20!9`20!10`20!11`20!17`20!3`20!1`20*63^137^21^2`16!3`16!4`16!1`16!6`16!7`16*63^321^82^9`80!10`80!1`80!11`80!12`80!15`80!16`80!18`80!3`80!8`80!4`80!21`80!23`80!24`80!28`80!14`80!30`80!20`80!31`80!13`80!17`80!22`80!27`80!33`80!34`80!2`80!25`80!29`80!19`80!32`80*63^322^41^2`40!1`40!3`40!4`40!5`40!9`40!7`40!6`40!8`40!10`40*63^323^41^1`40!2`40!3`40!5`40!6`40!7`40!8`40!11`40!9`40!4`40!10`40!12`40!13`40!14`40*283^220^3^1`3*283^223^2^2`2*283^226^7^1`7!2`7!3`7!4`7!5`7*283^230^2^1`2*283^231^4^1`4!5`4!2`4!4`4*283^233^3^1`3*283^236^4^1`4!2`4*283^238^2^1`2*283^242^4^1`4*283^241^6^1`6!2`6!3`6*283^10031^2^1`2!2`2*376^119^2^1`2*376^8^3^1`3!2`3*376^127^2^1`2*376^128^24^1`24!2`24!3`24!4`24!5`24!6`24!7`24*376^10002^2^1`2*812^8^2^1`2*812^10065^3^1`3*812^10073^2^1`2*812^10085^3^2`3*812^10084^3^1`3!2`3*812^10103^2^1`2*812^10104^2^1`2*812^10114^2^1`4!2`4*839^48^2^1`2*839^49^2^1`2*1000^4^12^1`12!2`12!3`12!4`12!5`12!6`12*1000^5^10^2`10!3`10!5`10!1`10!4`10*1000^6^10^1`10!2`10!3`10!6`10!7`10!8`10!4`10!5`10*1000^8^14^1`14!3`14!4`14!5`14!6`14!7`14!8`14!2`14*1000^9^11^1`11!2`11!3`11!4`11!6`11!7`11!8`11!5`11*1000^10^10^1`10!2`10!3`10!4`10!5`10!6`10!7`10!8`10*1000^11^10^1`10!2`10!3`10!4`10!5`10!6`10!7`10!8`10*1000^12^13^2`13!3`13!4`13!5`13!6`13!7`13!1`13!8`13*1000^13^9^1`9!2`9!3`9!4`9!5`9!6`9!7`9*1000^7^13^1`13!2`13!3`13!4`13!5`13!7`13!8`13!6`13*1248^5^2^1`2!2`2!3`2*1248^6^2^1`2*1251^11^2^1`2*1251^6^6^1`6!2`6!3`6!4`6*1251^15^13^1`13!2`13!3`13!4`13!5`13!7`13!10`13!13`13*1252^7^2^1`2!3`2!2`2*1255^7^5^1`5!2`5*1294^5^2^1`2!2`2*1349^10013^2^9`2*1349^10114^2^1`2","upload":"0"}'}
    # 参数解析
    if itype != 3:
        re_bck = clientVersionDataToJson(pdata)
        cversions = re_bck[0]
        lversions = re_bck[1]
    else:
        arr = pdata.split('$')
        now_page = int(arr[0])
        max_page = int(arr[1])
        pam = [now_page, max_page]
    # 业务执行
    db = DBManager()
    sql_account_type = "select AccountType, Power, distributor from tb_userdata where UID = %s;"
    data = db.fetchone(sql_account_type, self_uid)
    account_type = int(data[0])
    power = int(data[1])
    organization = int(data[2])
    mpage = 0
    if itype == 3:
        mpage = data_course.SHCourseAllCount(db)
    sql = data_course.GetCourseSQLFromTypeNew(itype, db, self_uid, pam, account_type=account_type, power=power)
    logging.info("=== ayylt =  " + sql)
    arr = data_course.Data_Courses_Base(sql, db, cversions, 0, isupdate)
    lesson_datas = arr[0]
    data_course_ini = arr[1]
    data_lesson_ini = ""

    for li in lesson_datas:
        cid = li[0]
        uid = li[1]
        p_uid = li[2]
        p_cid = li[3]
        sql = data_lesson.GetLessonSQLFromTypeNew(itype, uid, cid, p_uid, p_cid, teacher=account_type, power=power,
                                                  organization=organization)
        if data_lesson_ini == "":
            data_lesson_ini = str(cid) + "^" + str(uid) + "^" + data_lesson.Data_Lessons_Base(sql, db, cid, uid,
                                                                                              lversions, 0, isupdate)
        else:
            data_lesson_ini = data_lesson_ini + "*" + str(cid) + "^" + str(uid) + "^" + data_lesson.Data_Lessons_Base(
                    sql, db, cid, uid, lversions, 0, isupdate)
    db.destroy()
    return data_course_ini + "！" + data_lesson_ini + "！" + str(mpage)


def GetNew(pdata, self_uid, itype):
    cversions = {}
    lversions = {}
    pam = []
    if itype != 3:
        re_bck = clientVersionDataToJson(pdata)
        cversions = re_bck[0]
        lversions = re_bck[1]
    else:
        arr = pdata.split('$')
        now_page = int(arr[0])
        max_page = int(arr[1])
        pam = [now_page, max_page]
    # 业务执行
    db = DBManager()
    sql_account_type = "select AccountType, Power, distributor from tb_userdata where UID = %s;"
    data = db.fetchone(sql_account_type, self_uid)
    account_type = int(data[0])
    power = int(data[1])
    organization = int(data[2])
    mpage = 0
    if itype == 3:
        mpage = data_course.SHCourseAllCount(db)
    sql = data_course.GetCourseSQLFromTypeNew(itype, db, self_uid, pam, account_type=account_type, power=power)
    arr = data_course.Data_Courses_Base(sql, db, cversions, 0)
    lesson_datas = arr[0]
    data_course_ini = arr[1]
    data_lesson_ini = ""
    for li in lesson_datas:
        cid = li[0]
        uid = li[1]
        p_uid = li[2]
        p_cid = li[3]
        sql = data_lesson.GetLessonSQLFromTypeNew(itype, uid, cid, p_uid, p_cid, teacher=account_type, power=power,
                                                  organization=organization)
        if data_lesson_ini == "":
            data_lesson_ini = str(cid) + "^" + str(uid) + "^" + data_lesson.Data_Lessons_Base(sql, db, cid, uid,
                                                                                              lversions, 0)
        else:
            data_lesson_ini = data_lesson_ini + "*" + str(cid) + "^" + str(uid) + "^" + data_lesson.Data_Lessons_Base(
                    sql, db, cid, uid, lversions, 0)

    db.destroy()
    return data_course_ini + "！" + data_lesson_ini + "！" + str(mpage)


# 删除课程
def Delete(selfuid, db, uid, cid):
    sql = "delete from tb_course_bag where CID = %s and UID = %s"
    # 资源
    params = [str(cid), str(uid)]
    result = db.edit(sql, params)
    if result:
        return True
    return False


# 审核
# shCode 0-拒绝 1-通过
def SH(db, self_uid, uid, cid, shCode):
    # DEBUG_MSG("wid", cid)
    if not interface_global.Global_IsGM(self_uid, db):
        return 0  # 不是GM没有权限
        # DEBUG_MSG("uid", uid)
    if shCode < 0 or shCode > 1:
        return -1  # 参数异常
    list_ccourse_base = data_course.Data_Course_Base(uid, cid, 0, db, 2)  # CheckCourse(cid, uid, shCode)
    if not list_ccourse_base:
        return -2  # 课程不存在
    sign = 2
    if shCode == 1:
        sign = 3
    data_course.UpdateCourseFlag(db, cid, uid, sign)
    wname = list_ccourse_base[1]
    username = list_ccourse_base[19]
    logging.info("审核课程：UserName[%s] 课程名称[%s]" % (username, wname))
    title = ''
    if shCode == 0:
        title = "课程未通过审核"
        tbody = "你的" + wname + "课程未通过审核"
    elif shCode == 1:
        data_course.UpdateToDBNew(db, list_ccourse_base, cid, uid, 1)

        # arr_lesson = ini_lesson_base.split('^')
        pids = data_lesson.CopyToDB_New(db, cid, uid, 1, cid, uid, 0)  # self.PassedLesson(cid, uid)
        # print("审核合成时的本地工程列表：[%s]" % pids)
        if len(pids) > 0:
            for p_arr in pids:
                data__p = data_project.Data_Project_Base(p_arr[0], p_arr[1], 0, db, 2)
                if data__p:
                    interface_project.ProjectToDB(db, p_arr[1], p_arr[0], 1, data__p)
                interface_obj.CopyToDBNew(1, db, p_arr[0], p_arr[1], Global.GetObjTableName(p_arr[0], p_arr[1]))
        # 同步到课程分类里面
        data_course.DoCourseConfig(db, uid, cid, wname)
        title = "课程通过审核"
        tbody = "你的" + wname + "课程通过审核"
    # 发邮件通知
    interface_mail.WriteMail(db, uid, title, tbody)
    return 1


def GetVersion(data, uid, db):
    cid = int(data)
    cversion = data_course.GetVersion(cid, uid, 0, db)
    _back = str(cid) + "^" + str(cversion) + "^" + data_lesson.GetVersion(cid, uid, 0, db)
    return _back


# 上传课程
def UpLoad(l_pdata, uid, db):
    # DEBUG_MSG("课程上传：[%s]" % l_pdata)
    cid = int(l_pdata[1])
    if l_pdata[2] != "":
        project_data = l_pdata[2].split('`')
        project_data[7] = "1"
        data_course.UpdateToDB(db, project_data, cid, uid, 0)
    if l_pdata[3] != "":
        object_data = l_pdata[3]
        _del_data = l_pdata[4]
        data_lesson.UpdateToDB(db, object_data, _del_data, cid, uid, 0)
    return ""


# self_uid 用户自己的UID
# uid 制作者的UID
# cid 市场的课程id
# lid 市场的课程下某一个课时id
# tlong 时长
def BuyNew(db, self_uid, uid, cid, lid, tlong):
    logging.info(
            "赠送课程数据 :" + str(self_uid) + "-" + str(uid) + "-" + str(cid) + "-" + str(uid) + "-" + str(lid) + "-" + str(
                    tlong))

    # 1、 判断一下这个课时是否存在
    # 获取下市场课程数据
    w_data = data_course.Data_Course_Base(uid, cid, 1, db, 2)
    if not w_data:
        return [-1, ""]  # 购买的课程不存在

    # 2、判断课程是否以及购买过
    _cid = data_course.CourseFlag_Buy(self_uid, uid, cid, db)  # 是否购买过

    # 3、如果课程没有买过，先更新课程数据
    if _cid == 0:
        # 分配一个新的课程id
        _cid = interface_global.NewCID(db, self_uid)

        w_data[0] = _cid
        w_data[7] = 0
        w_data[8] = int(time.time())
        w_data[9] = self_uid
        w_data[12] = uid
        w_data[13] = cid

        data_course.UpdateToDB(db, w_data, _cid, self_uid, 0)

    # 课程ini数据
    c_string = data_course.Get_Data_Course_Base_ListToIni(w_data)  # self.GetCString(_cid, self.databaseID)

    # 上面课程处理完了

    # 下面处理课时

    # 4、更新课时
    _now = int(time.time())
    # 获取时长的课时数据
    lessondata_market = data_lesson.Data_Lesson_Base(uid, cid, 1, db, 1)  # self.ComputeBuyLesson(_uid, _cid)
    # 获取自己身上的课时
    myself_lesson = data_lesson.Data_Lesson_Base(self_uid, _cid, 0, db, 1)
    # 要赠送的这个课时数据
    if myself_lesson and lid in myself_lesson:
        selfLesson = myself_lesson[lid]
        logging.info("自身课程获取原日期: %s" % selfLesson["value19"])
        # 版本号+1
        selfLesson["value17"] = int(myself_lesson[lid]["value17"]) + 1
        # 验证已有时间， 判断、加上本次时长 tlong
        selfLesson["value19"] = int(selfLesson["value19"]) + int(tlong)

    else:
        selfLesson = lessondata_market[lid]
        # 版本号为市场的
        selfLesson["value17"] = lessondata_market[lid]["value17"]
        # 时长为现在加上 tlong
        selfLesson["value19"] = _now + tlong
    # 修改课时数据
    # print("buy_datas", buy_datas)
    selfLesson["value9"] = self_uid
    # selfLesson["value10"] = int(time.time())
    buy_ini = data_lesson.Get_Data_Lesson_Base_JsonToIni(selfLesson)
    # 更新
    data_lesson.UpdateToDB(db, buy_ini, "", _cid, self_uid, 0)
    _back = c_string + "！" + str(_cid) + "^" + str(self_uid) + "^" + buy_ini
    return [1, _back]


# 购买课程/赠送课程
# 可单个购买也可多个购买
# lid 0-全部 其他单节
# itype 购买时 0-一年 1-永久 | 赠送时 = 赠送时长
# btype 0-赠送 1-购买
# ctype 0-等级包/权限包(时间叠加) 1-补偿包(时间叠加) 2-机构老师包(时间叠加) 3-购买课程 4 - 客户端多个购买(lid 用#分割)
def Buy(db, self_uid, uid, cid, lid, type, btype, ctype, self_username):
    # self_uid 1466-uid 63-cid 137 -lid 2-type 2592000-btype 0 ctype = 1
    logging.info("Buy Course Datas :" + str(self_uid) + "-" + str(uid) + "-" + str(cid) + "-" + str(uid) + "-" + str(
            lid) + "-" + str(type) + "-" + str(btype) + " ctype = " + str(ctype))

    if uid == self_uid and btype == 1:
        return [0, ""]  # 不能购买自己的
    # print("buy ======= 1")
    # 参数转换
    arr_clientbs = []
    if ctype == 4:
        if len(lid) > 0:
            arr_clientbs = lid.split('#')
        lid = 0
    else:
        lid = int(lid)
    # print("buy ======= 2")
    # 获取下市场课程数据
    w_data = data_course.Data_Course_Base(uid, cid, 1, db, 2)
    if not w_data:
        return [-1, ""]  # 购买的课程不存在
    UserName = w_data[18]  # 发布者
    _ZK1 = float(w_data[15])
    _ZK2 = float(w_data[16])
    _CourseName = w_data[1]
    # print("课程折扣 :", _ZK1,_ZK2)
    # 市场中发布的课时数据
    _bstr2 = "[" + _CourseName + "]("
    market_lessons = data_lesson.Data_Lesson_Base(uid, cid, 1, db, 1, 1)
    if isinstance(market_lessons, str):
        return [-1, ""]  # 购买的课程不存在
    # 购买的数据
    myself_lesson = {}
    _uid = self_uid
    _cid = data_course.CourseFlag_Buy(_uid, uid, cid, db)  # 是否购买过
    if _cid != 0:
        myself_lesson = data_lesson.Data_Lesson_Base(_uid, _cid, 0, db, 1)  # self.ComputeBuyLesson(_uid, _cid)
        ##[一年价格 永久价格 到期时间 是否购买 课时ID 版本号]
    buy_datas = []
    buy_ini = ""
    if lid != 0:  # 按课时购买
        _version = 0
        _pdate = 0
        # print("buy ======= 5")
        if lid not in market_lessons.keys():
            return [-2, ""]  # 课时不存在
        # print("buy ======= 6")
        if lid in myself_lesson.keys():
            # _version = myself_lesson[lid]["value18"]
            if myself_lesson[lid]["value20"] == 1:  # 永久课时
                return [-3, ""]  # 永久课程不能购买
        buy_datas.append(market_lessons[lid])
        # _bstr2 = _bstr2 + " " + market_lessons[lid]["value3"] + ","
    else:
        # print("buy ======= 8")
        _keys = []
        if ctype == 4:  # 同时购买多个课时
            if len(arr_clientbs) == 0:
                _keys = market_lessons.keys()
            else:
                _keys = arr_clientbs
        else:  # 购买整个课程
            # print("market_lessons : " , market_lessons)
            _keys = market_lessons.keys()
        for _lkey in _keys:
            if ctype == 4 and len(arr_clientbs) != 0:
                _lkey = int(_lkey)
            _version = 0
            _pdate = 0
            if _lkey in myself_lesson.keys():
                if myself_lesson[_lkey]["value19"] == 1:  # or (myself_lesson[_lkey][2] == 0 and type == 0)
                    continue
            buy_datas.append(market_lessons[_lkey])
    if len(buy_datas) < 1:
        return [-4, ""]  # 购买异常，没有可购买的

    bBCourse = False
    if len(buy_datas) == len(market_lessons):
        bBCourse = True

    # 计算价钱
    Price = 0
    buys = ""

    for _data in buy_datas:
        if btype == 1:
            if type == 0:
                Price += _data["value15"]
            elif type == 1:
                Price += _data["value18"]
        if buys == "":
            buys = str(_data["value1"])
        else:
            buys = buys + "," + str(_data["value1"])

    _bstr = ""
    _d1 = ""
    if btype == 1:
        _d1 = "购买"
        if type == 0:
            _bstr = "一年"
        else:
            _bstr = "永久"
    else:
        _d1 = "赠送"
        if type == 1:
            _bstr = "永久"
        else:
            _bstr = str(type / (24 * 60 * 60)) + "天"

    desc = ""

    # if btype == 1:
    if lid == 0 and ctype != 4:
        desc = _d1 + "[整个课程](" + _CourseName + ")(" + _bstr + ")"
    else:
        desc = _d1 + "[课程](" + _CourseName + ")-[课时]("
        for arr_data in buy_datas:
            desc += arr_data["value2"]
            desc += ","
        desc += ")"
        desc += "(" + _bstr + ")"

    # 扣钱
    if btype == 1:
        if (lid == 0 and ctype != 4) or (
                lid == 0 and (len(arr_clientbs) == 0 or len(arr_clientbs) == len(market_lessons)) and ctype == 4):
            # 计算折扣
            if _ZK1 == 0:
                _ZK1 = 1
            if _ZK2 == 0:
                _ZK2 = 1
            if type == 0:
                Price = _ZK1 * Price
            else:
                Price = _ZK2 * Price

        Price1 = int(Price)
        if Price1 != 0:
            if Price % Price1 != 0:
                Price1 += 1

        if Price1 > 0:
            if not interface_wit.ReduceWitScore(db, self_uid, int(Price1)):
                return [-5, ""]  # 智慧豆不足
            # 制作者加钱
            _add = Price  # int(Price/2)
    # 增加课程
    c_string = ""
    # DEBUG_MSG("1 _cid [%i] WID:[%i]" % (_cid, self.WID))
    if _cid == 0:
        # DEBUG_MSG("_cid [%i] WID:[%i]" % (_cid,self.WID))
        _cid = interface_global.NewCID(db, self_uid)  # self.HttpInst.GetCID(self.UserName)
        # self.WID = _cid

    # 购买写入数据

    # 修改自己部分数据

    w_data[0] = _cid
    w_data[7] = 0
    w_data[8] = int(time.time())
    w_data[9] = self_uid
    w_data[12] = uid
    w_data[13] = cid

    data_course.UpdateToDB(db, w_data, _cid, self_uid, 0)
    c_string = data_course.Get_Data_Course_Base_ListToIni(w_data)  # self.GetCString(_cid, self.databaseID)

    # 课时数据写入
    _now = int(time.time())
    ipos = 0
    for info in buy_datas:
        info_lid = info["value1"]
        if btype == 1:  # 购买
            if type == 0:  # 一年期限
                if info_lid not in myself_lesson.keys():
                    data_p = _now + 31536000
                else:
                    if myself_lesson[info_lid]["value19"] < _now:
                        data_p = _now + 31536000
                    else:
                        data_p = myself_lesson[info_lid]["value19"] + 31536000
            elif type == 1:
                data_p = 1
            else:
                if info_lid not in myself_lesson.keys():
                    data_p = _now + type
                else:
                    if myself_lesson[info_lid]["value19"] < _now:
                        data_p = _now + type
                    else:
                        data_p = myself_lesson[info_lid]["value19"] + type
        elif btype == 0:  #
            if type == 1:
                data_p = 1
            else:
                if info_lid not in myself_lesson.keys():
                    data_p = _now + type
                else:
                    if myself_lesson[info_lid]["value19"] < _now:
                        data_p = _now + type
                    else:
                        data_p = myself_lesson[info_lid]["value19"] + type
        # 更新数据
        buy_datas[ipos]["value19"] = data_p
        buy_datas[ipos]["value9"] = self_uid
        buy_datas[ipos]["value10"] = int(time.time())
        if buy_ini == "":
            buy_ini = data_lesson.Get_Data_Lesson_Base_JsonToIni(buy_datas[ipos])
        else:
            buy_ini = buy_ini + "!" + data_lesson.Get_Data_Lesson_Base_JsonToIni(buy_datas[ipos])
        ipos += 1
    data_lesson.UpdateToDB(db, buy_ini, "", _cid, self_uid, 0)
    _back = c_string + "！" + str(_cid) + "^" + str(self_uid) + "^" + buy_ini

    # 日志
    if btype != 0:
        if bBCourse:
            interface_solr.Solr_PayLog(str(_cid), _CourseName, 1, 3, 0, Price1, 4, "0", int(time.time()), 0, self_uid,
                                       "pc", 1, self_username)

    return [1, _back]


# 撤销
def CX(db, cid, uid):
    data_course.UpdateCourseFlag(db, cid, uid, 0)
    return 1


# 上架/下架（市场）
def LessonUD(db, cid, uid, lid, status):
    _lids = []

    table_name = Global.GetMLessonTableName(uid, cid)
    if lid == 0:
        sql = "select lid,ID from " + table_name
        data = db.fetchall(sql, None)
        if data:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)
                _lids.append(minfo_list[0])
    else:
        sql = "select lid,ID from " + table_name + " where lid = " + str(lid)
        data = db.fetchone(sql, None)
        _lid = 0
        if data:
            _lid = int(data[0])
        if _lid == 0:
            return 0
        _lids.append(lid)

    if len(_lids) < 1:
        return 0
    for _lid in _lids:

        sql = "select ID from sys_course_res where CID = " + str(cid) + " and uid = " + str(
                uid) + " and mlessonID = " + str(_lid)
        data = db.fetchone(sql, None)
        _id = 0
        if data:
            _id = int(data[0])

        if _id == 0:
            sql = "insert into sys_course_res (cid,uid,mlessonID,flag) values ('" + str(cid) + "','" + str(
                    uid) + "','" + str(_lid) + "','" + str(status) + "')"
        else:
            sql = "update sys_course_res set flag = '" + str(status) + "' where ID = " + str(_id)
        db.edit(sql, None)

    return 1
