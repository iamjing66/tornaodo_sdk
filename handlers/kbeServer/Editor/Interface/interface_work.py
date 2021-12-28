#!/usr/bin/env python
# coding=utf-8

import logging
import time,Global
from handlers.kbeServer.Editor.Data import data_work
from handlers.kbeServer.Editor.Data import data_obj
from handlers.kbeServer.Editor.Data import data_project,data_Look
from handlers.kbeServer.Editor.Interface import interface_mail, interface_global, interface_project, interface_obj, interface_wit,interface_solr,interface_sms
from methods.DBManager import DBManager


#客户端列表(带版本号)转json，用来比对
def clientVersionDataToJson(pdata):
    p_server = {}
    if pdata != None and len(pdata) > 0:
        l_pdata = pdata.split('!')
        for info in l_pdata:
            sdata = info.split('`')
            uid = int(sdata[0])
            pid = int(sdata[1])
            version = int(sdata[2])
            if uid not in p_server.keys():
                p_server[uid] = {}
            p_server[uid][pid] = version
    return p_server

#同步数据
def Get(pdata, self_uid, type):
    p_server = {}
    now_page = 1
    max_page = 1

    if type == 0 or type == 1:
        # 版本验证
        p_server = clientVersionDataToJson(pdata)
    else:
        arr = pdata.split('$')
        now_page = int(arr[0])
        max_page = int(arr[1])
    # 业务执行
    DB = DBManager()
    mpage = 0
    arrpam = []
    if type == 2:
        mpage = data_work.SHWorkAllCount(DB)
        arrpam = [mpage,now_page,max_page]
    sql = data_work.GetWorkSQLFromType(type,self_uid,arrpam)

    #print("work client version : " , p_server)
    arr = data_work.Data_Works_Base(sql, DB, p_server, 0)
    DB.destroy()
    return arr[1] + "！"


def GetNew(pdata, self_uid, type, **kwargs):
    p_server = {}
    now_page = 1
    max_page = 1

    if type == 0 or type == 1:
        # 版本验证
        p_server = clientVersionDataToJson(pdata)
    else:
        arr = pdata.split('$')
        now_page = int(arr[0])
        max_page = int(arr[1])
    # 业务执行
    DB = DBManager()
    mpage = 0
    arrpam = []
    if type == 2:
        mpage = data_work.SHWorkAllCount(DB)
        arrpam = [mpage,now_page,max_page]

    # 判断用户是否为D类
    d_class = data_work.get_utype_uid(DB, self_uid)
    course_level = kwargs.get("course_level", 2)
    sql = data_work.GetWorkSQLFromTypeNew(type, self_uid, arrpam, course_level=course_level, d_class=d_class)

    #print("work client version : " , p_server)
    arr = data_work.Data_Works_Base_New(sql, DB, p_server, 0)
    DB.destroy()
    return arr[1] + "！"


def GetVersion(data,uid,DB):
    wid = int(data)
    wversion = data_work.GetVersion(wid,uid,DB,0)
    _back = str(wid) + "^" + str(wversion)
    return _back


def UpLoad(DB,l_pdata,self_uid,target):

    #'2937`rwqr`1`1`2937`0``1`0`1621405157`5`0`1002`2`0`0````1`0`0`0'
    if l_pdata[1] != "":
        work_data = l_pdata[1].split('`')
        data_work.UpdateToDB(work_data, self_uid, int(work_data[0]), DB, target)
        data_work.new_work_sort(DB, work_data[0], self_uid, work_data[19])


#审核作品
def SH(DB,self_uid,uid,wid,shCode):

    # DEBUG_MSG("wid", wid)
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0 #不是GM没有权限
        # DEBUG_MSG("uid", uid)
    if shCode < 0 or shCode > 1:
        return -1  # 参数异常
    list_work_base = data_work.Data_Work_Base(uid,wid,0,DB,2,sh=True)
    if not list_work_base:
        return -2
    #DEBUG_MSG("cid",cid)
    data_work.UpdateWorkFlag(DB,wid,uid,shCode)
    wname = list_work_base[1]
    username = list_work_base[24]
    #print("审核作品：UserName[%s] 作品名称[%s]" % (username,wname))
    title = ''
    if shCode == 0:
        title = "作品未通过审核"
        tbody = "你的" +wname + "作品未通过审核"
    elif shCode == 1:
        data_work.UpdateToDB(list_work_base,uid,wid,DB,1)
        #作品中的PID 跟 WID相同
        pid = list_work_base[4]
        if pid != 0:
            data__p = data_project.Data_Project_Base(uid,pid, 0, DB, 2)
            if data__p:
                interface_project.ProjectToDB(DB,pid,uid , 1, data__p)
            # self.PassedProject(p_arr[0], p_arr[1], 1)
            data_o = data_obj.Data_Objs_Base(0, DB, pid,uid , {}, 0)
            #print("data_o",data_o)
            if data_o:
                interface_obj.UpdateToDB(1, DB,uid,pid , data_o)
            # self.PassedProject(pid,uid,0)
            # self.PassedObject(pid,uid)
            # self.PassedExtra(pid,uid)
        title = "作品通过审核"
        tbody = "你的" + wname + "作品通过审核"
        #self.WorkSucc(username)
        interface_global.AccountPowerSet(username,DB)
        #增加创作者经验
        #interface_global.AddFabricator(username,1,DB)
    interface_mail.WriteMail(DB,uid, title, tbody)
    return 1


def BuyFlag(DB,self_uid,uid,pid):

    return data_work.BuyFlag(DB,self_uid,uid,pid)



# type 0-表示正常购买 1-APP内购买 2-更新作品
#ptype 0-一年 1-永久
def Buy(DB,self_uid,wid,UID,type,ptype):

    logging.info("buy work wid = %s uid = %s selfuid = %s type = %s ptype = %s" % (str(wid),str(UID),str(self_uid),str(type),str(ptype)))
    if UID == self_uid:
        return [0,""]   #不能购买自己的
    user_power = get_user_power_uid(DB,self_uid)
    d_class = False
    if user_power == 5:
        d_class = True
    list_work_data = data_work.Data_Work_Base(UID,wid,1,DB,2,d_class=d_class)
    if not list_work_data:
        return [-1,""]   #不存在该作品
    pid = list_work_data[4]
    price1 = int(list_work_data[20])
    UserName = list_work_data[26]
    price2 = int(list_work_data[5])
    WorkName = list_work_data[1]

    if ptype == 0:
        price = price1
    else:
        price = price2
    #print("work buy price : ", price1, price2,price)
    #判断下这个作品是否买过了
    arr_back = BuyFlag(DB,self_uid,UID,wid)
    _pdate = arr_back[0]
    _buy_pid = arr_back[2]
    _now = int(time.time())
    logging.info("buy work WorkName = %s pid = %s price1 = %s price2 = %s _pdate = %s" % (
    str(WorkName), str(pid), str(price1), str(price2), str(_pdate)))
    #判断是否是永久了
    if type != 2:
        if _pdate == 1:
                return [-2,""]   #已经永久了
    if type == 2:
        _ptruedate = 1 #_now + 2592000 #_pdate
    else:
        if ptype == 1:
            _ptruedate = 1
        else:
            if _pdate == 0 or _pdate < _now:
                _pdate = _now
            _ptruedate = _pdate + 2592000

    _bstr = ""
    if ptype == 0:
        _bstr = "一年"
    else:
        _bstr = "永久"
    if type != 2:
        # 扣钱
        if price > 0:
            if not interface_wit.ReduceWitScore(DB,self_uid,price):
                return [-3,""] #智慧豆不足
            # 制作者加钱
            #interface_wit.AddWitScoreWithUserName(DB,UserName, price,0)
    # else:
    #     if _pdate > 1:
    #         if _now >= _pdate:
    #             return [-5,""]   #过期了，不需要更新

        # _version = self.GetPorjectVersion(pid,UID,1) #市场的版本号
        # if _version_local >= _version:
        #     self.client.N_BuyWork_C(-5)  # 无需更新
        #     DEBUG_MSG("不需要更新")
        #     return
    if _buy_pid != 0:
        interface_project.DeleteP(DB,self_uid,self_uid,_buy_pid,1)
    # if _buy_pid != 0:
    #     self.N_DeleteProject(_buy_pid)
        #self.client.N_DeleteProject_C(_buy_pid)


    # 增加工程
    _pid = interface_global.NewPID(DB,self_uid)
    data__p = data_project.Data_Project_Base(UID, pid, 1 , DB, 2)
    if data__p:
        data__p[0] = _pid
        data__p[2] = int(time.time())
        data__p[3] = int(time.time())
        data__p[12] = 0
        data__p[19] = pid
        data__p[24] = self_uid
        data__p[25] = UID
        data__p[27] = _ptruedate
        data__p[28] = 105
        data__p[29] = ""
        interface_project.ProjectToDB(DB, _pid, self_uid, 0, data__p)
    # self.PassedProject(p_arr[0], p_arr[1], 1)
    data_o = data_obj.Data_Objs_Base(1, DB, pid, UID, {}, 0)
    if data_o:
        #print("data_o:", data_o)
        #20`场景编程区`1606181993`0.0`0.0`0.0`0.0`0.0`0.0`1.0`1.0`1.0`0``&0,0&```0`0`3```0.0`0.0``0`1`0!5`3D相机`1606181993`-22.99`15.01`79.61`23.777`17.0805`0.0`1.0`1.0`1.0`0``&0,0&```0`0`4```0.0`0.0``0`1`0!5128`鹿`1606182198`-19.6688`10.0`90.606`0.0`197.09`0.0`1.0`1.0`1.0`0``&0,0&```0`0`5```0.0`0.0``0`1`0!5128`鹿1`1606182208`-27.731`10.1608`88.8461`0.0`154.11`0.0`1.0`1.0`1.0`0``1@4@-177.7321,232.9124,0@D:2@@~2@95@@@1$1|1$0|1$52<2e>75|1$0|2$0@&0,0&```0`0`6```0.0`0.0``0`1`0!20426`松树二`1606182930`-32.9981`10.8735`87.6677`0.0`141.34`0.0`1.0`1.0`1.0`0``&0,0&```0`0`7```0.0`0.0``0`1`0!21157`冷杉二`1606182933`-26.4915`10.1025`90.7153`0.0`164.02`0.0`1.0`1.0`1.0`0``&0,0&```0`0`8```0.0`0.0``0`1`0
        interface_obj.CopyToDB(0, DB, self_uid, _pid, Global.GetMObjTableName(UID,wid))
    # self.Project_Buy(pid, UID, self.databaseID, _pid, _ptruedate)
    # self.Object_Buy(pid, UID, self.databaseID, _pid)
    # self.Extra_Buy(pid, UID, _pid, self.databaseID)

    #
    p_string =  data_project.Get_Data_Project_Base_ListToIni(data__p)
    #obj_string = data_obj.GetData_Objs_Ini(data_o)
    #extra_string = self.GetExtraString(_pid,self.databaseID,0)
    _back =   p_string    # + "*" + obj_string + "*" str(pid)+ "！" + str(UID)  + "！0！105" +

    # 日志
    #interface_solr.Solr_Pay(DB,2,"",WorkName,10,2,5,0,price,12,"",int(time.time()),_ptruedate,self_uid)
    interface_solr.Solr_PayLog("", WorkName, 2, 5, 0, price, 12, "", int(time.time()), _ptruedate, self_uid, "pc", 1)
    return [1,_back]


#撤销
def CX(DB,uid,wid,target):

    data_work.Delete(DB,uid,wid,target)
    return 1


#买看
def VR_BuyWork(DB,self_uid,wid,p_uid,buy_type,plat,phone=None):


    UID = self_uid
    if p_uid == UID:
        return [-1,""]  # 不能购买自己的作品
    w_data = data_work.Data_Work_Base(p_uid,wid,1,DB,2) #self.Work_buy(wid, p_uid)

    if not w_data:
        return [0,""]    #作品不存在
    pid = int(w_data[4])
    price = int(w_data[21])
    cname = w_data[1]
    #
    _arr_data = data_work.BuyFlag(DB,UID,p_uid, pid)
    _pdate = _arr_data[0]
    if _pdate == 1:
        return [-2,""]  # 已经永久购买无需重新购买

    _now = int(time.time())
    if _pdate > _now:
        return [-3,""]  # 作品在购买期限内

    if price < 1:
        return [-10,""]  #免费作品，无需购买

    if buy_type == 0 or buy_type == 2:
        if buy_type == 0:
            # 扣钱
            #print("w_data,",UID,price)
            if not interface_wit.ReduceWitScore(DB,UID,price):
                return [-4,""]  #智慧豆不足

        data_w_list = data_Look.Data_W_Base(DB,UID,p_uid,wid,2)
        _cpdate = 0
        if data_w_list:
            _cpdate = int(data_w_list[3])
        if _cpdate == 0:
            _cpdate = _now
        if _cpdate < _now:
            _cpdate = _now
        _ptruedate = _cpdate + 2592000

        if not data_w_list:
            sql = "insert INTO `tb_work_look_B` (UID, W_UID, W_CID, P_DATE, C_TYPE) values ("+str(UID)+","+str(p_uid)+","+str(wid)+","+str(_ptruedate)+",0)"
        else:
            sql = "update `tb_work_look_B` set P_DATE = "+str(_ptruedate)+" WHERE UID = "+str(UID) + " AND W_UID = "+str(p_uid) + " and w_cid = "+str(wid)
        DB.edit(sql,None)

        if plat == 20:
            _from = 4
        else:
            _from = 6
        if not phone:
            #interface_solr.Solr_Pay(DB,2, "", cname, plat , _from , 8 , 0, price, 10, "", int(time.time()), _ptruedate,UID)
            interface_solr.Solr_PayLog("", cname, _from, 8, 0, price, 10, "", int(time.time()), _ptruedate, self_uid, "vr", 2)
        #wid#uid#buy_type#到期时间
        return [1,str(wid)+"#"+str(p_uid)+"#"+str(buy_type)+"#"+str(_ptruedate),str(p_uid)+"$"+str(wid)+"$"+str(_ptruedate)]

    elif buy_type == 1:
        sql = "select Phone from tb_userdata where UID = " + str(UID) +";"
        data = DB.fetchone(sql,None)
        _phone = ""
        if data:
            _phone = data[0]
        if _phone == "":
            return [-7,""]  #未绑定手机号
        pay_url = str(p_uid) + "@" + str(wid)  # + "$" + str(UID)
        interface_sms.SendSms(1,UID,_phone,pay_url)

        #DEBUG_MSG(res)
        return [99,""]


#VR端分享作品
def VR_ShareWork(DB,self_uid,pid,data):

    #WID,`Name`,Platform,Stars,Pid,price,`desc`,State,NewPid,CreateDate,UID,Vision,Sid,Version,Game,GameStage,SNUM,`identity`,SNAME,ct,price1,price2,Free
    pam = data.split('`')
    wid = pid
    data_work.UpdateToDB(pam,self_uid,wid,DB,0)
    data_project.SetTemplate(DB,self_uid,pid,4)

    return 1


def GetWorkFreetime(DB,pam):

    json_data = {
        "code": "0",
        "msg": "false"
    }
    if pam == "":
        return json_data
    uid = pam.split(',')[0]
    wid = pam.split(',')[1]

    strSql = "select stime,etime from tb_workmarket where UID = %s and  WID = %s limit 1;"
    data = DB.fetchone(strSql, (uid, wid))
    if data:
        stime = data[0]
        etime = data[1]
        Nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if stime < Nowtime < etime:
            json_data["code"] = "1"
            json_data["msg"] = "true"
    return json_data


def get_course_slide(DB, uid, pid, market):
    sql = "select jj from tb_vrfl where uid = %s and pid = %s and ISMARKET = %s"
    data = DB.fetchone(sql, (uid, pid, market))
    if data:
        return 1, float(data[0])
    else:
        sql_insert = "insert into tb_vrfl (uid, pid, ISMARKET, jj) values (%s, %s, %s, %s)"
        DB.edit(sql_insert, (uid, pid, market, float(0.06)))
        return 1, 0.06


def get_user_power_uid(DB, uid):
    sql = "select Power from tb_userdata where UID = %s"
    data = DB.fetchone(sql, uid)
    if data:
        return int(data[0])
    return -1
