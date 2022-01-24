import hashlib
import json
import time

import requests

import Global
from handlers.kbeServer.Editor.Interface import interface_sms
import application
import logging
# 注册
def account_phonecode(DB, self_uid,self_username, languageStr,phone , code):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    phoneCode = application.App.Redis_SMS.GetCode(phone, code)
    print("phoneCode = ",phoneCode)
    if phoneCode != "-99":
        json_data["code"] = -5
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_5",languageStr)
    else:

        json_data = interface_sms.interface_sendSMS(DB, code, self_uid , phone, phone,languageStr)

        if json_data["code"] == 1:
            #缓存
            application.App.Redis_SMS.SaveCode(phone, code, json_data["msg"])


    return json_data

# 注册
def Register(DB, languageStr, username , passWord , code):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    print("==========================")
    phoneCode = application.App.Redis_SMS.GetCode(username,401)
    if phoneCode == "-99":
        json_data["code"] = -4
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_8",languageStr)
    else:
        if phoneCode != code:
            json_data["code"] = -5
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_9",languageStr)
        else:
            sql = "select UserName from tb_userdata where UserName = '" + str(username) + "';"
            data = DB.fetchone(sql, None)
            if data:
                json_data["code"] = -6
                json_data["msg"] =Global.LanguageInst.GetMsg("SMSGID_1_1",languageStr)

            else:

                createuser = InterfaceRegister(DB,username,passWord)
                if createuser:
                    #删除缓存
                    application.App.Redis_SMS.DetCode(username,401)

                    json_data["code"] = 1
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_10",languageStr)
                else:
                    json_data["code"] = 0
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_11",languageStr)
    return json_data



def InterfaceRegister(DB,username,passWord):
    power = "0"
    # C端账号才有
    upower = "0"
    # 账号说明
    desc = ""
    # 到期时间
    # 默认一年
    EndDate = "1"
    # 主账号
    # B端账号才有
    # 默认为0
    mainAccount = "0"
    # 分销商
    organization = "0"
    # 机构
    distributor = "0"
    # 账号类型(0 - 学生 1 - 老师)
    accountType = "0"
    # 账号来源(0 - 官网注册
    # 1 - diy
    # world手机内注册
    # 2 - 分销平台注册
    # 3 - CreateX后台注册)
    AccountSource = "0"
    # 平台
    AccountOther = ""
    # 昵称
    NickName = ""
    # 身份证
    sfz = ""
    # 电话号码
    phone = username
    # 学校
    school = ""
    # 班级
    _class = ""
    # 账号权限(0 - 试用1 - 正式)
    AccountPower = "1"

    # D类账号注册
    d_code = ""

    create_user = DB.callprocAll('CreateUser', (
        username, passWord, power, upower, desc, EndDate, mainAccount, organization, distributor, accountType,
        AccountSource, AccountOther, NickName, sfz, phone, school, _class, AccountPower, '', '', '', '', '0'))
    if create_user:
        sql = "update tb_userdata set XREDITOR = 1 where username = '" + username + "';"
        DB.edit(sql, None)
        return True
    return False


def WechatLogin(state,languageStr):

    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    unionid = application.App.Redis_Wechat.GetUserName(state)
    if unionid:
        #直接登录
        json_data["code"] = 1
        json_data["msg"] = unionid
    else:
        unionid = application.App.Redis_Wechat.GetCode(state,"unionid")
        if not unionid:
            #登录授权未通过，请重新登录
            json_data["code"] = 0
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_14",languageStr)
        else:
            #首次登录授权成功，提示用户去绑定手机号
            json_data["code"] = 2
            json_data["msg"] = unionid

    return json_data


def JugeWechatState(DB,unionid):

    sql = "select username from tb_userdata where unionid = '"+unionid+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        return data[0]
    else:
        return None


def JugeUserExist(DB,username):

    sql = "select UID from tb_userdata where username = '"+username+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        return data[0]
    else:
        return 0

def JugePhoneExist(DB,phone):

    sql = "select UID from tb_userdata where phone = '"+phone+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        return True
    else:
        return False

def LoginAutoRegester(DB,phone,phoneCode,unionid,languageStr,code,password = "null"):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    #判断下验证码
    phoneCode = application.App.Redis_SMS.GetCode(phone, code)
    if phoneCode == "-99":
        json_data["code"] = -3   #请先获取验证码
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_8", languageStr)
    else:
        if phoneCode != phoneCode:
            json_data["code"] = -1  #验证码错误
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_9", languageStr)

        else:
            #判断账号是否存在
            exist = JugeUserExist(DB,phone)
            if exist == 0:
                #自动注册
                createuser = InterfaceRegister(DB, phone, password)
                if createuser:
                    # 删除缓存
                    application.App.Redis_SMS.DetCode(phone, code)

                    # json_data["code"] = 1
                    # json_data["msg"] = Global.InterfaceLanguage.GetMsg("SMSGID_1_10", languageStr)
                else:
                    json_data["code"] = -2
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_11", languageStr)
                    return json_data

            if len(unionid) > 0:
                # 这里绑定手机号到
                sql = "update tb_userdata set unionid = '"+unionid+"' where UserName = '"+phone+"';"
                DB.edit(sql,None)


            json_data = Login(DB,phone,"",languageStr)

    return json_data


def Login(DB,username,password,languageStr):



    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    sql = "select Enddate, UID, pwd_md5 from tb_userdata where binary username = %s;"
    data = DB.fetchone(sql, username)
    if data:
        enddate = int(data[0])
        UID = int(data[1])
        _password = data[2]

        # if len(password) > 0 and _password != password:
        #     json_data["code"] = -11
        #     json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_12", languageStr)
        #
        # el
        if enddate != 1 and int(time.time()) > enddate:
            json_data["code"] = -21
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_13", languageStr)
        else:

            #登录成功，缓存用户数据
            UserCache(DB,username)
            WitCache(DB,UID)

            json_data["code"] = 1
            json_data["msg"] = UID

    else:
        json_data["code"] = -31
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_0_2", languageStr)
    return json_data


def FindPassword(DB,phone,phonecode,password, languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 判断下验证码
    phoneCode = application.App.Redis_SMS.GetCode(phone, 404)
    if phoneCode == "-99":
        json_data["code"] = -1  # 请先获取验证码
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_8", languageStr)
    else:
        if phoneCode != phonecode:
            json_data["code"] = -2  # 验证码错误
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_9", languageStr)
        else:

            state = JugePhoneExist(DB,phone)
            if not state:
                json_data["code"] = -3 #手机号未绑定
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_15", languageStr)
            else:
                #print("password = " , password)
                m = hashlib.md5(password.encode())
                result = m.hexdigest()  # 获取加密后的结果
                print("result = " , result)
                sql = "update tb_userdata set pwd = '"+password+"',pwd_md5 = '"+result+"' where phone = '"+phone+"';"
                DB.edit(sql)
                json_data["code"] = 1  # 密码修改成功
                json_data["msg"] = ""

                # 删除缓存
                application.App.Redis_SMS.DetCode(phone, 404)


    return json_data



def AlterPassword(DB,username,password,passwordnew):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }


    sql = "select pwd,pwd_md5 from tb_userdata where binary username = %s;"
    data = DB.fetchone(sql, username)
    if data:
        _password_n = data[0]
        _password = data[1]

        if _password != password:
            json_data["code"] = -1 #原始密码错误
        else:
            sql = "update tb_userdata set pwd_md5 = '"+passwordnew+"',pwd = '"+passwordnew+"' where binary username = %s;"
            DB.edit(sql,username)
            json_data["code"] = 1
    else:
        json_data["code"] = 0   #修改密码失败

    return json_data


def DeleteAccount(DB,username, languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    data = DB.callprocAll('New_XRDeleteAccount', (username, Global.get_config.mysql_options()["database"],1))
    if not data:
        json_data["code"] = -1  # 手机号未绑定
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_24", languageStr)
    else:
        json_data["code"] = 1  # 删除成功
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_25", languageStr)

    return json_data



def GiveWit(username,num,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }
    uid = application.App.Redis_User.GetData(username,"uid")
    if not uid:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_16", languageStr)
    else:
        application.App.Redis_Wit.AddWit(uid,num,0,1)
        json_data["code"] = 1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_17", languageStr)
    return json_data

def UserCache(DB,username):

    if not application.App.Redis_User.Exist(username):
        sql = "select UID, create_time, organization, distributor, Power, AccountPower from tb_userdata where username = '"+username+"' limit 0,1;"
        data = DB.fetchone(sql,None)
        if data:
            application.App.Redis_User.SaveUser(username,data)

    return True

def WitCache(DB,uid):

    exist = application.App.Redis_Wit.Exist(uid)
    sql = "select Wit_Score,Wit_Rmb,moneyg,moneyz from tb_userdata where uid = " + str(uid) + " limit 0,1;"
    data = DB.fetchone(sql, None)
    if data:
        Wit_Score = int(data[0])
        Wit_Rmb = int(data[1])
        moneyg = int(data[2])
        moneyz = int(data[3])
        if not exist:
            application.App.Redis_Wit.SaveWit(uid,moneyg,moneyz,0)

        if Wit_Score > 0 or Wit_Rmb > 0:
            sql = "update tb_userdata set Wit_Score = 0,Wit_Rmb = 0 where uid = " + str(uid)
            data = DB.edit(sql,None)
            if data:
                if Wit_Score > 0:
                    application.App.Redis_Wit.AddWit(uid, Wit_Score, 0, 1)
                if Wit_Rmb > 0:
                    application.App.Redis_Wit.AddWit(uid, 0, Wit_Rmb, 2)


    return True





def Logined(DB, self_uid,username, languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    #uid = application.App.Redis_User.GetData(username, "uid")
    #智慧豆
    wit = application.App.Redis_Wit.GetWit(self_uid,0)
    #注册时间
    cdate = application.App.Redis_User.GetData(username,"cdate")

    user = {
        "wit":wit,
        "cdate":cdate
    }
    json_data["code"] = 1
    json_data["msg"] = json.dumps(user)

    return json_data



