#!/usr/bin/env python
# coding=utf-8

import logging
import time

from dateutil.relativedelta import relativedelta
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU
from handlers.kbeServer.Editor.Interface.interface_config import IC
from handlers.kbeServer.Editor.Interface import interface_wit,interface_solr
from handlers.kbeServer.Editor.Data import data_ppackage
from handlers.kbeServer.Editor.Data import data_respackahe
import datetime
from handlers.redisServer.RedisInterface import ServerUserCache



def BaseLogin(DB,username,password):
    sql = "select Enddate, UID, pwd_md5 from tb_userdata where binary username = %s;"
    data = DB.fetchone(sql, username)
    if data:

        enddate = int(data[0])
        UID = int(data[1])
        _password = data[2]

        if _password != password:
            return -1

        if enddate != 1 and int(time.time()) > enddate:
            return -2

        return 1

    else:
        return 0


def PC_lOGON(DB,Username, json_data):

    #基础数据
    uid = 0
    sql = "select * from tb_userdata where binary UserName = '"+str(Username) + "'"
    # print("pc_login :" , sql)
    data = DB.fetchone(sql, None)
    if data:
        uid = int(data[1])
        Phone = data[2]
        Power = int(data[3])
        UPower = int(data[4])
        MainAccount = int(data[5])
        TheName = data[6]
        TheSchool = data[7]
        TheClass = data[8]
        identity = data[9]
        COMID = int(data[10])
        PassDate = int(data[11])
        AccountDesc = data[12]
        BCBag = data[13]
        _add_Wit_Score = int(data[14])
        organization = int(data[16])
        distributor = int(data[17])
        AccountType = int(data[18])
        uversion = int(data[20])
        makec = int(data[21])
        AccountSource = int(data[22])
        ClassID = str(data[24])
        fabricator = int(data[27])
        adminType = int(data[29])
        JGTC_Date = str(data[33])
        AccountPower = int(data[36])
        VipPower = int(data[37])
        VipDate = int(data[38])
        Wit_RMB = int(data[39])
        gmstate = int(data[47])
        save_status = data[58]

    # 班级信息
    class_str = ""
    sclass = ""
    now = (datetime.datetime.now()).strftime("%Y-%m-%d")
    if AccountType == 1:  # 老师
        sql = "select CID,CNAME,isDel FROM tb_class WHERE TID = " + str(uid) + " and end_date >= %s;"
    else:
        sql = "select CID,CNAME,isDel FROM tb_class WHERE find_in_set(CID,'" + ClassID + "') and end_date >= %s;"
    data = DB.fetchall(sql, now)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            _IsDet = minfo_list[2]
            if _IsDet == "1":
                continue
            if class_str == "":
                class_str = str(minfo_list[0])
            else:
                class_str = class_str + "," + str(minfo_list[0])
            if sclass == "":
                sclass = str(minfo_list[0]) + "`" + minfo_list[1]
            else:
                sclass = sclass + "^" + str(minfo_list[0]) + "`" + minfo_list[1]

    # 包裹信息
    Package_Msg = ""
    sql = "select ID,PID,ENDDATE FROM tb_bag WHERE UID = " + str(uid) + ";"
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            if Package_Msg == "":
                Package_Msg = str(minfo_list[0]) + "|" + str(minfo_list[1]) + "|" + str(minfo_list[2])
            else:
                Package_Msg = Package_Msg + "@" + str(minfo_list[0]) + "|" + str(minfo_list[1]) + "|" + str(minfo_list[2])


    #购买的资源数据
    Res_Msg = ""
    sql = "select RESID,DATE FROM respackage WHERE UID = " + str(uid) + ";"
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            if Res_Msg == "":
                Res_Msg = str(minfo_list[0]) + "|" + str(minfo_list[1])
            else:
                Res_Msg = Package_Msg + "@" + str(minfo_list[0]) + "|" + str(minfo_list[1])

    # 购买的场景数据
    Scene_Msg = ""
    sql = "select RESID,DATE FROM scenepackage WHERE UID = " + str(uid) + ";"
    data = DB.fetchall(sql, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            minfo_list = list(minfo)
            if Scene_Msg == "":
                Scene_Msg = str(minfo_list[0]) + "|" + str(minfo_list[1])
            else:
                Scene_Msg = Package_Msg + "@" + str(minfo_list[0]) + "|" + str(minfo_list[1])


    _SEND = Phone + "$" + str(Power) + "$" + str(UPower) + "$" + str(MainAccount) + "$" + TheName + "$" + TheSchool + "$" + TheClass + "$" + identity + "$" + str(COMID) + "$" + str(PassDate) + "$" + AccountDesc + "$" + BCBag + "$" + str(organization) + "$" + str(distributor) + "$" + str(AccountType) + "$" + str(uversion) + "$" + str(makec) + "$" + str(AccountSource) + "$" + class_str + "$" + str(sclass) + "$" + str(fabricator) + "$" + str(adminType) + "$" + str(AccountPower) + "$" + str(VipPower) + "$" + str(VipDate) + "$" + Package_Msg + "$" + str(uid) + "$" + Res_Msg+ "$" + Scene_Msg + "$" + str(gmstate) + "$" + str(save_status)
    #print("_SEND",_SEND)

    #login
    #记录redis缓存
    solr_redis = ServerUserCache.redis_ip_set(Username, json_data)
    if solr_redis:
        #登录的索引库在互动引擎中
        DoLogin(DB,Username, VipDate, "pc")

    return _SEND


#VR登录数据
def VR_LOGIN(DB,VR_USERNAME,json_data):

    _userdata_string = ""
    vipdate = 0
    UPower = 0
    sql = "select UserName,Wit_Score,Wit_RMB,UID,POWER,UPOWER,AccountSource,ClassID,organization,distributor,Phone,NickName,NickUrl,`identity`,admintype,accountPower,VipDate from tb_userdata where UserName = '"+VR_USERNAME+"'"
    # DEBUG_MSG("sql : " , sql)
    data = DB.fetchone(sql, None)
    account_power = 0
    if data:
        # 0-官网注册 1-diy world手机内注册 2-分销平台注册 3-CreateX后台注册
        _userdata_string = str(data[3]) + "^" + data[0] + "^" + str(data[1]) + "^" + str(data[4]) + "^" + str(data[5]) + "^" + str(data[6]) + "^" + str(data[7]) + "^" + str(data[10]) + "^" + str(data[11]) + "^" + str(data[12]) + "^" + str(data[13]) + "^"+ str(data[9]) + "^" + str(data[14]) + "^" + str(data[15]) + "^" + str(data[8])+ "^" + str(data[16])
        vipdate = int(data[16])
        UPower = int(data[4])
        # login
        # 记录redis缓存
    solr_redis = ServerUserCache.redis_ip_set(VR_USERNAME, json_data)
    if solr_redis:
        DoLogin(DB, VR_USERNAME, vipdate, "vr")

    return _userdata_string

    # db = mysqlHander.READDB(False)
    # cursor = db.cursor()
    # # ==用户数据
    # sql = "SELECT POWER,UPOWER,AccountSource,ClassID,organization,distributor,Phone,NickName,NickUrl,`identity`,admintype,accountPower FROM tb_userdata WHERE UID = " + str(self.Editor_UID) + ";"
    # cursor.execute(sql)
    # db.commit()
    # data = cursor.fetchone()
    # if data != None and len(data) > 0:
    #     _Power = int(data[0])
    #     self.Power = _Power
    #     self.UPower = int(data[1])
    #     self.AccountResource = int(data[2])
    #     self.organization = int(data[4])
    #     self.distributor = int(data[5])
    #     self.Editor_Phone = data[6]
    #     self.Editor_NickName = data[7]
    #     self.Editor_NickUrl = data[8]
    #     self.identity = data[9]
    #     self.adminType = int(data[10])
    #     self.accountPower = int(data[11])
    #     # 0-官网注册 1-diy world手机内注册 2-分销平台注册 3-CreateX后台注册
    #     _userdata_string = str(self.Editor_UID) + "^" + self.EditorUserName + "^" + str(self.Wit_Score) + "^" + str(data[0]) + "^" + str(data[1]) + "^" + str(data[2]) + "^" + data[3] + "^" + data[6] + "^" + data[7] + "^" + data[8] + "^" + data[9] + "^" + str(data[5]) + "^" + str(data[10]) + "^" + str(data[11]) + "^" + str(data[4])


    #self.SolrInst.Log_Login(0, self.Editor_UID, self.organization, self.distributor, self.EditorUserName, self.Plat,self.LocalIP,self.VipDate)

    #DEBUG_MSG("LoadData2", self.Editor_UID, self.EditorUserName, self.Wit_Score, appType, self.Power, self.AccountResource)



#登录登出处理
def DoLogin(DB,USERNAME,vipDate,SoftType):

    localip = ""

    solrdata = ServerUserCache.redis_user_get(USERNAME, ['uid', 'Power', 'AccountPower'])
    if solrdata:
        _vip = 0
        if vipDate < int(time.time()):
            _vip = 1
        _long = 0
        _data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_data = {
            #"platform": platform,
            "dateTime": _data,
            "loginState": 0,
            #"organization": solrdata[0],
            #"distributor": solrdata[1],
            "userName": USERNAME,
            "userId": solrdata[0],
            "useTime": _long,
            "SoftType": SoftType,
            "UPower": _vip,
            "Power": solrdata[1],
            "AccountPower": solrdata[2],
        }
        interface_solr.RequestSolr(4,json_data)

        if SoftType == "pc":
            ServerUserCache.redis_state_set(USERNAME, 'state', 1)
            # sql = "update tb_userdata set state = 1 where username = '"+ USERNAME +"'"
        else:
            ServerUserCache.redis_state_set(USERNAME, 'appstate', 1)
            # sql = "update tb_userdata set appstate = 1 where username = '"+ USERNAME +"'"
        # DB.edit(sql, None)



def DoLogout(DB,USERNAME,jsondata):
    vipDate = int(jsondata["vipDate"])
    SoftType = jsondata["SoftType"]
    _long = float(jsondata["long"])

    localip = ""
    solrdata = ServerUserCache.redis_user_get(USERNAME, ['uid', 'Power', 'AccountPower'])
    if solrdata:
        _vip = 0
        if vipDate < int(time.time()):
            _vip = 1
        _data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_data = {
            #"platform": platform,
            "dateTime": _data,
            "loginState": 1,
            #"organization": solrdata[0],
            #"distributor": solrdata[1],
            "userName": USERNAME,
            "userId": solrdata[0],
            "useTime": int(_long),
            "SoftType": SoftType,
            "UPower": _vip,
            "Power": solrdata[1],
            "AccountPower": solrdata[2],
        }
        interface_solr.RequestSolr(4, json_data)

        if SoftType == "pc":
            ServerUserCache.redis_state_set(USERNAME, 'state', 0)
            # sql = "update tb_userdata set state = 0 where username = '"+ USERNAME +"'"
        else:
            ServerUserCache.redis_state_set(USERNAME, 'state', 0)
            # sql = "update tb_userdata set appstate = 0 where username = '"+ USERNAME +"'"
        # DB.edit(sql, None)

    return 1


# ===========================================
# 验证身份信息
# ===========================================
def VerifyIdentity(DB,self_uid,pam,username):

    identity = ""
    thename = ""
    d_arr = pam.split('$')
    _mode = d_arr[0]
    if _mode == "1":
        identity = d_arr[1]
    else:
        thename = d_arr[1]


    sql = "select `identity`,TheName from tb_userdata where UserName = '" + str(username) + "';"
    data = DB.fetchone(sql,None)
    _identity = ""
    _thename = ""
    if data != None:
        _identity = data[0]
        _thename = data[1]
    if _identity == "" and _thename == "":
        return 0
    if identity == "" and thename == "":
        return -1
    if identity != "":
        if _identity != identity:
            return -2
    if thename != "":
        if _thename != thename:
            return -3
    return 1


#获取账号信息
def FabricatorData(DB,self_uid,username):


    sql = "select fabricator,savepnum,power,UID from tb_userdata where username = '" + username + "';"
    data = DB.fetchone(sql,None)
    if data:
        return str(data[0]) + "$" + str(data[1]) + "$" + str(data[2]+1)
    return ""


#type 0-永久 1-一年
#buytype 0-资源 1-场景
def N_ResNuy(DB,UID,ObjID,type,buytype, self_username):

    Info = {}
    buydatas = {}
    ObjectDatas = IC.ObjConfig
    SceneResData = IC.SceneConfig
    objName = ""
    if buytype == 0:
        if ObjID not in ObjectDatas.keys():
            return [-3,""]
        Info = ObjectDatas[ObjID]
        objName = Info[2]
    else:
        if ObjID not in SceneResData.keys():
            return [-3,""]
        Info = SceneResData[ObjID]
        objName = Info[2]
    #判断下资源书否可以购买.
    # isbuy = Info["IsNeedBuy"]
    # if isbuy == 0:
    #     if self.client:
    #         self.client.N_ResNuy_C(-3, 0, 0, 0)  # 资源不需要购买
    #     return
    _price = 0
    _b_date = 0
    if buytype == 0:
        buydatas = data_respackahe.Data_Obj_Base(DB,UID)

    else:
        buydatas = data_respackahe.Data_Obj_Base(DB, UID)

    if ObjID in buydatas.keys():  # 购买过
        _b_date = buydatas[ObjID]

    # 永久
    if _b_date == 1:
        return [-1,""]


    _bstr = ""
    if type == 0:
        _bstr = "永久"
        _b_date = 1
        _price = Info[1]
    else:
        if _b_date == 0:
            _b_date = int(time.time())
        _b_date += 44676000
        _price = Info[0]
        _bstr = "一年"
    #扣钱
    if not interface_wit.ReduceWitScore(DB, UID, _price):
        return [-2, ""]  # 智慧豆不足
    # 修改数据
    if ObjID in buydatas.keys():
        data_respackahe.UpdateToDB(DB,UID,ObjID,buytype,_b_date,False)
    else:
        data_respackahe.UpdateToDB(DB, UID, ObjID, buytype, _b_date, True)

    #写日志
    if buytype == 0:
        sql = "insert into tb_rescost_log (UID,WITE_NUM,RESID,PDATE) VALUE("+str(UID)+","+str(_price)+","+str(ObjID)+","+str(_b_date)+");"
    else:
        sql = "insert into tb_scenecost_log (UID,WITE_NUM,RESID,PDATE) VALUE(" + str(UID) + "," + str(_price) + "," + str(ObjID) + "," + str(_b_date) + ");"
    DB.edit(sql,None)

    if buytype == 0:
        #interface_solr.Solr_Pay(DB,2, "", objName, 10, 1, 9, 0, _price, 7, "0", int(time.time()), 0, UID)
        interface_solr.Solr_PayLog("", objName, 1, 9, 0, _price, 7, "", int(time.time()), 0, UID, "pc", 1, self_username)
            # self.SolrInst.Log_Cost(5, "购买资源", _price, "购买资源[" + objName + "]("+_bstr+")" , 0, "",self.organization, self.distributor, self.UID)
    else:
        #interface_solr.Solr_Pay(DB,2, "", objName, 10, 1, 7, 0, _price, 6, "0", int(time.time()), 0, UID)
        interface_solr.Solr_PayLog("", objName, 1, 7, 0, _price, 6, "", int(time.time()), 0, UID, "pc", 1, self_username)

    return [1,str(type)+"$"+str(ObjID)+"$"+str(buytype)+"$"+str(_b_date)]


#购买包裹位
def BuyPackage(DB,uid,code,bid,num, self_username):

    buydatas = data_ppackage.Data_Buy_Base(DB,uid)
    if bid != 0:
        if bid not in buydatas.keys():
            return [0,""]          #续费包裹不存在
        if  buydatas[bid][1] == 1:
            return [-1,""]          #包裹位已经是永久的
    if num < 1:
        return -4  # 数量异常
    #扣钱
    if IC.DataConfig == None or "bagprice" not in IC.DataConfig or IC.DataConfig["bagprice"] <= 0:
        return -2         #包裹价格异常，购买失败

    price = int(IC.DataConfig["bagprice"]) * num
    if not interface_wit.ReduceWitScore(DB, uid, price):
        return [-3, ""]  # 智慧豆不足

    #添加包裹
    cname = ""
    cdata = ""
    if bid == 0:
        cname = "购买包裹位("+str(num)+")个"
        _date = int(time.time()) + 31536000

        for i in range(num):

            i_id = data_ppackage.InsertToDB(DB,uid,_date)
            #print("i_id:",i_id)
            if cdata == "":
                cdata = str(i_id) + "$" + str(_date)
            else:
                cdata = cdata + "@"+ str(i_id) + "$" + str(_date)

    else:
        _pdate = buydatas[bid][1]
        if _pdate < int(time.time()):
            _pdate = int(time.time())
        _date = _pdate + 31536000
        data_ppackage.UpdateToDB(DB, _date,bid)
        cname = "续费包裹位"
        cdata = str(bid) + "$" + str(_date)

    cdesc = cname + "(价格["+str(price)+"])"

    ##print("self.PackageData:",self.PackageData)


    # 日志
    #interface_solr.Solr_Pay(DB,2, "", "扩展位购买", 10, 7, 2, 0, price*10, 9, "", int(time.time()),_date,uid)
    interface_solr.Solr_PayLog("", "扩展位购买", 7, 2, 0, price , 9, "", int(time.time()), _date, uid, "pc", 1, self_username)
        #self.SolrInst.Log_Cost(13, cname , price,cdesc , 0, "", self.organization,self.distributor, self.UID)

    return [1,cdata]


def PackageBind(DB,UID,bid,PID):

    buydatas = data_ppackage.Data_Buy_Base(DB, UID)
    if bid not in buydatas.keys():
        return [0,""]

    data_ppackage.BindProject(DB, PID, bid)

    _bck = str(bid)+"$"+str(PID)
    return [1,_bck]

def DelPPackage(DB,UID,PID):

    sql = "update tb_bag set PID = 0 where UID = "+str(UID)+" AND PID = " + str(PID)
    DB.edit(sql,None)


# 修改密码
def UpdatePassword_App(DB,UserName, oldPassword, NewPassWord):

    if len(oldPassword) < 1:
        return 0  ## 老密码异常
    if len(NewPassWord) != len(NewPassWord.encode('utf-8')):
         # 只能用英文
        return -1
    if len(NewPassWord) < 6:
        # 密码不能少于6位
        return -2
    data = DB.callprocAll('UpdatePassword', (UserName, oldPassword, NewPassWord))
    if data:
        code = data[0]
        if code != 1:
            return -3  # 原始密码错误
        else:
            return 1  # 密码设置 成功
    else:
        return -4  # 原始密码错误


#修改昵称|头像
def AlterAppPam(DB,uid,atype,pam):

    sql = ""

    if atype == 1:
        if len(pam) > 12:
            # 太长
            return 0
        sql = "select uid from tb_userdata where NickName = '"+pam+"'"
        data = DB.fetchone(sql,None)
        if data:
            if int(data[0]) > 0:
                return -1      # 重名


        sql = "update tb_userdata set NickName = '"+pam+"' where uid = "+str(uid)
    elif atype == 2:
        if len(pam) < 1:
            return 0      # 太短

        sql = "update tb_userdata set NickUrl = '"+pam+"' where uid = "+str(uid)

    DB.edit(sql,None)
    return 1


#注册
def Register(DB,uid,username,data,phone_recode):

    json_data = {
        "code": 0,
        "phone":"",
        "msg": ""
    }

    phonecode = data["phonecode"]
    ##print("phonecode 1 " , phonecode)
    if len(phone_recode) < 1:
        json_data["code"] = -1
        json_data["msg"] = "请先获取验证码"
        return json_data
    if phone_recode == "-99":
        json_data["code"] = -2
        json_data["msg"] = "验证码过期"
        return json_data
    if phone_recode != phonecode:
        json_data["code"] = -3
        json_data["msg"] = "验证码错误"
        return json_data

    accountdata = data["accountdata"]
    _arrPam = accountdata.split('#')
    userName = _arrPam[0]  # 用户名
    phone = userName

    sql = "select UserName from tb_userdata where UserName = '" + str(phone) + "';"
    data = DB.fetchone(sql,None)
    if data:
        json_data["code"] = -4
        json_data["msg"] = "账号已注册"
        return json_data


    passWord = _arrPam[1]   #密码
    power = _arrPam[2]      #账号权限
    if power == "":
        power = "0"
    #C端账号才有
    upower = _arrPam[3]
    if upower == "":
        upower = "0"
    #账号说明
    desc = _arrPam[4]
    if desc == "":
        desc = "未添加说明"
    #到期时间
    #默认一年
    EndDate = _arrPam[5]
    if EndDate == "":
        EndDate = "1"
    #主账号
    #B端账号才有
    #默认为0
    mainAccount = _arrPam[6]
    if mainAccount == "":
        mainAccount = "0"
    #分销商
    organization = "0"
    if len(_arrPam) > 7:
        organization = _arrPam[7]
    #机构
    distributor = "0"
    if len(_arrPam) > 8:
        distributor = _arrPam[8]
    #账号类型(0 - 学生 1 - 老师)
    accountType = "0"
    if len(_arrPam) > 9:
        accountType = _arrPam[9]
    #账号来源(0 - 官网注册
    #1 - diy
    #world手机内注册
    #2 - 分销平台注册
    #3 - CreateX后台注册)
    AccountSource = "0"
    if len(_arrPam) > 10:
        AccountSource = _arrPam[10]
    #平台
    AccountOther = ""
    if len(_arrPam) > 11:
        AccountOther = _arrPam[11]
    #昵称
    NickName = ""
    if len(_arrPam) > 12:
        NickName = _arrPam[12]
    #身份证
    sfz = ""
    if len(_arrPam) > 13:
        sfz = _arrPam[13]
    #电话号码
    phone = ""
    if len(_arrPam) > 14:
        phone = _arrPam[14]
    #学校
    school = ""
    if len(_arrPam) > 15:
        school = _arrPam[15]
    #班级
    _class = ""
    if len(_arrPam) > 16:
        _class = _arrPam[16]
    #账号权限(0 - 试用1 - 正式)
    AccountPower = "1"
    
    # D类账号注册
    d_code = ""
    if len(_arrPam) > 18:
        d_code= _arrPam[18]
        sql_d = "select id, pid from eservices where settlementCode = %s;"
        d_data = DB.fetchone(sql_d, d_code)
        if d_data:
            distributor = d_data[0]
            organization = d_data[1]
            power = "5"
            logging.info("D类账号注册：" + str(d_code))
        
    create_user = DB.callprocAll('CreateUser', (userName, passWord, power, upower, desc, EndDate, mainAccount, organization, distributor, accountType, AccountSource, AccountOther, NickName, sfz, phone, school, _class, AccountPower,'', '', '', '', '0'))
    if create_user:
        json_data["code"] = 1
        json_data["msg"] = "注册成功"
        json_data["phone"] = phone
    else:
        json_data["code"] = -5
        json_data["msg"] = "注册失败"
        json_data["phone"] = phone
    return json_data


def UpdatePD(DB,uid,username,data,phone_recode):
    json_data = {
        "code": 0,
        "phone": "",
        "msg": ""
    }

    phonecode = data["phonecode"]
    #print("phonecode 1 ", phonecode)
    if len(phone_recode) < 1:
        json_data["code"] = -1
        json_data["msg"] = "请先获取验证码"
        return json_data
    if phone_recode == "-99":
        json_data["code"] = -2
        json_data["msg"] = "验证码过期"
        return json_data
    if phone_recode != phonecode:
        json_data["code"] = -3
        json_data["msg"] = "验证码错误"
        return json_data
    pd = data["pd"]
    if len(pd) < 6:
        json_data["code"] = -4
        json_data["msg"] = "密码长度不足6位"
        return json_data
    phone = username
    DB.callprocAll('UpdatePassword', (username,"",pd))
    json_data["code"] = 1
    json_data["msg"] = "修改成功"
    json_data["phone"] = phone
    return json_data


def FindPD(DB,uid,username,data):

    json_data = {
        "code": 0,
        "msg": ""
    }

    pd_old = data["pdo"]
    #print("pd_old" , pd_old)
    if len(pd_old) < 6:
        json_data["code"] = -1
        json_data["msg"] = "原始密码异常"
        return json_data
    pd = data["pd"]
    #print("pd", pd)
    if len(pd) < 6:
        json_data["code"] = -2
        json_data["msg"] = "密码长度不足6位"
        return json_data

    data = DB.callprocAll('UpdatePassword', (username,pd_old,pd))

    code = 0
    if data:
        code = int(data[0])
    if code != 1:
        json_data["code"] = 0
        json_data["msg"] = "原始密码错误"
    else:
        json_data["code"] = 1
        json_data["msg"] = "修改成功"
    # print("json_data", json_data)
    return json_data


def BindPhone(DB,uid, username, data, phone_recode):

    json_data = {
        "code": 0,
        "phone": "",
        "msg": ""
    }

    phonecode = data["phonecode"]
    #print("phonecode 1 ", phonecode)
    if len(phone_recode) < 1:
        json_data["code"] = -1
        json_data["msg"] = "请先获取验证码"
        return json_data
    if phone_recode == "-99":
        json_data["code"] = -2
        json_data["msg"] = "验证码过期"
        return json_data
    if phone_recode != phonecode:
        json_data["code"] = -3
        json_data["msg"] = "验证码错误"
        return json_data
    phone = data["phone"]
    _username = ""
    sql = "select UserName from tb_userdata where Phone = '" + str(phone) + "';"
    data = DB.fetchone(sql,None)
    if data:
        _username = data[0]

    if _username != "":
        json_data["code"] = -4
        json_data["msg"] = "该手机号已绑定其他账号"

        return json_data

    sql = "update tb_userdata set Phone = '" + phone + "' where UserName = '"+username+"'"
    DB.edit(sql,None)
    json_data["code"] = 1
    json_data["msg"] = "绑定成功"
    json_data["phone"] = phone
    return json_data


#获取绑定的手机号
def GetPhoneBind(DB,username):


    phone = ""
    sql = "select Phone from tb_userdata where UserName = '"+str(username)+"';"
    data = DB.fetchone(sql,None)
    if data:
        phone = data[0]

    return phone

def GetPhoneRegister(DB,phone):

    code = 0
    sql = "select Phone from tb_userdata where UserName = '"+str(phone)+"' limit 0,1;"
    data = DB.fetchone(sql,None)
    if data:
        code = 1
    return code


def LoginList(DB):
    json_data = {
        "code": 0,
        "msg": ""
    }

    strSql = "select LOGIN_IP,LOGIN_PORT FROM tb_config_login ORDER BY LVS LIMIT 1"

    _cback = ""
    try:

        data = DB.fetchall(strSql,None)
        if data:
            IP = data[0][0]
            Port = data[0][1]
            _cback = IP + "$" + Port
            if str(IP) != "" :
                if str(Port) != "":
                    strSql = " update  tb_config_login  set  LVS = LVS + 1   where   LOGIN_IP = '"+str(IP)+"' and LOGIN_PORT = '"+str(Port)+"'"
                    DB.edit(strSql,None)
            json_data["code"] = "1"
            json_data["msg"] = _cback
        else:
            json_data["code"] = "0"
            json_data["msg"] = ""
    except:
        json_data["code"] = "0"
        json_data["msg"] = ""
    return json_data


#=====个人信息绑定
def N_WriteRoleData(DB,self_uid,name,iedent,school,_class):

    sql = "update tb_userdata set TheName = '"+name+"',TheSchool = '"+school+"',TheClass = '"+school+"',identity = '"+iedent+"' where uid = "+str(self_uid)
    DB.edit(sql,None)
    return 1

#=====导出视频
def DaochuVedio(DB, tlong, uid, course_type, video_type, self_username):


    if tlong <= 0:
        return 0
    else:
        b_type = ["2","3"]
        sql = "select Power from tb_userdata where UID = %s"
        user_type = DB.fetchone(sql, uid)
        if str(user_type[0]) in b_type:
            # B类账号扣除导出次数
            sql_out_video = "select UsedTimes from tb_userdata where UID = %s and TotalTimes > UsedTimes"
            user_times = DB.fetchone(sql_out_video, uid)
            if user_times:
                sql_update = "update tb_userdata set UsedTimes = %s where UID = %s"
                update_times = DB.edit(sql_update, (int(user_times[0]) + 1, uid))
                if update_times:
                    # 导出次数扣除成功
                    logging.info("用户: %s, 成功导出视频, 已使用次数%i" % (str(uid), int(user_times[0]) + 1))
                    return 1, "导出次数扣除成功"
                else:
                    # 次数扣除失败
                    logging.error("用户: %s, 导出失败, 扣除次数失败" % (str(uid)))
                    return -1, "次数扣除失败"
            else:
                logging.info("用户: %s, 导出次数不足" % uid)
                return -2, "导出次数不足"
        else:
            long = tlong % 5
            sql_price = "select unitPrice from tb_exportvideo_cfg where courseType = %s and videoType = %s"
            price_data = DB.fetchone(sql_price, (course_type, video_type))
            # 课程默认扣费 每五秒五豆
            price_5s = 5
            # 总价
            price = 0
            if price_data:
                # 获取对应课程类型扣费
                price_5s = int(price_data[0])
            
            if long == 0:
                price = tlong/5 * price_5s
            else:
                price = (tlong - long) / 5 * price_5s + price_5s
            if interface_wit.ReduceWitScore(DB,uid,price):
                interface_solr.Solr_PayLog("", "导出视频", 10, 2, 0, price, 9, "", int(time.time()), 0, uid, "pc", 1, self_username)
                return 1
            else:
                return -1

def get_video_price(DB):
    sql = "select id,unitPrice from tb_exportvideo_cfg"
    data = DB.fetchall(sql)
    price_str = ""
    if data:
        l2 = []
        for i in data:
            l2.append(":".join([str(i[0]), str(i[1])]))
        price_str = "|".join(l2)
        # 获取视频定价成功
        return 1, price_str
    # 获取视频定价失败
    return -1, price_str

def get_account_outtimes(DB, uid):
    b_type = ["2","3"]
    sql = "select Power from tb_userdata where UID = %s"
    user_type = DB.fetchone(sql, uid)
    if user_type:
        if str(user_type[0]) in b_type:
            # B类账号扣除导出次数
            sql_out_video = "select TotalTimes, UsedTimes from tb_userdata where UID = %s"
            user_times = DB.fetchone(sql_out_video, uid)
            if user_times:
                return 1, [str(user_times[0]), str(user_times[1])]
            else:
                    logging.info("用户: %s ,次数不够")
                    return -1, ["-1","-1"]
        else:
            # 次数不够
            # 导出视频只能在 10s 以内
            logging.info("用户: %s ,非B类")
            return -1, ["-1","-1"]
    else:
        return -1, ["-1","-1"]


def projectConfig(DB, uid,pid,ismarket):

    _back = ""

    sql = "select t2.ABPATH,t2.RID,t2.`Name`,t2.tid from tb_mproject t1 inner join tb_config_scene t2 on T2.RID = t1.SID AND t1.uid = "+str(uid)+" and t1.pid = "+str(pid)+" limit 0, 1;"
    data = DB.fetchone(sql,None)
    if data:
        _back = data[0] + "$" + str(data[1]) + "$" + data[2] + "$"+ str(data[3]) + "$"
        sql = "select t2.RID,t2.ABPath,t2.tid2,t2.tid from tb_mobj_"+str(uid)+"_"+str(pid)+" t1 inner join tb_config_res t2 on t1.ObjID = t2.RID group by (t2.RID) ;"
        data = DB.fetchall(sql, None)
        if data:
            for info in data:
                _back += str(info[0])+"|"+str(info[1])+"|"+str(info[2])+"|"+str(info[3]) + "&"

            # _back += "$"
            # sql = "select RID,`Path` from tb_config_audio;"
            # data = DB.fetchall(sql, None)
            # if data:
            #     for info in data:
            #         _back += str(info[0]) + "|" + str(info[1]) + "&"
    else:
        _back = ""


    return _back


def GetAudioPath(DB, audioid):

    _back = ""

    sql = "select `Path` from tb_config_audio where RID = "+audioid+" limit 0,1;"
    data = DB.fetchone(sql, None)
    if data:
        _back = audioid + "|" + str(data[0])


    return _back


# 获取目标账户是否存在空闲包裹位
def get_user_bag(DB, username):
    now = int(time.time())
    sql = "select t2.ID from tb_userdata t1 inner join tb_bag t2 on t1.UID = t2.UID and t1.UID = (select UID from tb_userdata where UserName = %s ) and (t2.ENDDATE > %s or t2.ENDDATE = 1) and t2.PID = 0 limit 1;"
    data = DB.fetchone(sql, (username, now))
    if data:
        return data[0]
    return 0


# 转移工程时更新目标账户的包裹位
def update_user_bag(DB, pid, bag_id):
    sql = "update tb_bag set PID = %s where ID = %s"
    DB.edit(sql, (pid, bag_id))


def get_user_power(DB, username):
    sql = "select Power from tb_userdata where USERNAME = %s"
    data = DB.fetchone(sql, username)
    if data:
        return data[0]
    return -1
