import hashlib
import json
import time

import requests
from handlers.kbeServer.XREditor.data import xr_data_work
from handlers.kbeServer.XREditor.Interface import xr_interface_mail
import Global
from handlers.kbeServer.Editor.Interface import interface_sms
import application
import logging
# 注册
from handlers.kbeServer.Editor.Interface.interface_config import IC
from handlers.kbeServer.Editor.Interface import interface_wit
#from handlers.kbeServer.XREditor.data import da

#时序版获取验证码
#code =  401:  # 时序版注册
#code = 402:  # 微信登录绑定手机
#code = 403:  # 手机号登录验证码
#code = 404:  # 忘记密码
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
            expire = 60
            if code == 401:
                expire = 60
            elif code == 402:
                expire = 60
            elif code == 403:
                expire = 60
            elif code == 404:
                expire = 60
            application.App.Redis_SMS.SaveCode(phone, code, json_data["msg"],expire)


    return json_data

# 手机号注册
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
            #sql = "select UserName from tb_userdata where UserName = '" + str(username) + "' or phone = '"+username+"';"
            data = JugeLoginUserExist(DB,username) #DB.fetchone(sql, None)
            if data:
                json_data["code"] = -6
                json_data["msg"] =Global.LanguageInst.GetMsg("SMSGID_1_1",languageStr)

            else:

                createuser = InterfaceRegister(DB,username,passWord,username,"",False)
                if createuser:
                    #删除缓存
                    application.App.Redis_SMS.DetCode(username,401)

                    json_data["code"] = 1
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_10",languageStr)
                else:
                    json_data["code"] = 0
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_11",languageStr)
    return json_data



def InterfaceRegister(DB,username,passWord,nickname = "",headimgurl = "",wechat = False):
    power = "11"
    # C端账号才有
   # upower = "0"
    # 账号说明
    #desc = ""
    # 到期时间
    # 默认永久
    EndDate = "1"
    # 主账号
    # B端账号才有
    # 默认为0
    #mainAccount = "0"
    # 分销商
    #organization = "0"
    # 机构
    #distributor = "0"
    # 账号类型(0 - 学生 1 - 老师)
    #accountType = "0"
    # 账号来源(0 - 官网注册
    # 1 - diy
    # world手机内注册
    # 2 - 分销平台注册
    # 3 - CreateX后台注册)
    # AccountSource = "0"
    # 平台
    # AccountOther = ""
    # 昵称
    NickName =nickname
    #头像
    NickUrl = headimgurl
    # 身份证
    #sfz = ""
    # 电话号码
    if not wechat:
        phone = username
    else:
        phone = ""
    # 学校
    #school = ""
    # 班级
    #_class = ""
    # 账号权限(0 - 试用1 - 正式)
   # AccountPower = "1"

    # D类账号注册
    d_code = ""

    create_user = DB.callprocAll('xrcreateuser', (
        username, passWord, power,EndDate,  NickName, NickUrl, phone))
    if create_user:
        # sql = "update tb_userdata set XREDITOR = 1 where username = '" + username + "';"
        # DB.edit(sql, None)
        return True
    return False


def WechatLogin(DB,state,languageStr):

    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    unionid = application.App.Redis_Wechat.GetUserName(state)
    if unionid:
        if JugePhoneBind(DB,unionid):
            #直接登录
            json_data["code"] = 1
            json_data["msg"] = unionid
        else:
            # 首次登录授权成功，提示用户去绑定手机号
            json_data["code"] = 2
            json_data["msg"] = unionid
    else:
        # 登录授权未通过，请重新登录
        json_data["code"] = 0
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_14", languageStr)

    return json_data


# def JugeWechatState(DB,unionid):
#
#     sql = "select username from tb_userdata where username = '"+unionid+"' limit 0,1"
#     data = DB.fetchone(sql,None)
#     if data:
#         return data[0]
#     else:
#         return None

def JugeLoginUserExist(DB,username):

    sql = "select UID from tb_userdata where username = '"+username+"' or phone = '"+username+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        return data[0]
    else:
        return 0


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


def JugePhoneBind(DB,username):

    sql = "select phone from tb_userdata where username = '"+username+"' limit 0,1"
    data = DB.fetchone(sql,None)
    if data:
        if len(data[0]) > 0:
            return True
        else:
            return False
    else:
        return False


#手机号登录，不存在就注册
def LoginAutoRegester(DB,phone,PCode,languageStr,code):
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
        if phoneCode != PCode:
            json_data["code"] = -1  #验证码错误
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_9", languageStr)

        else:
            #判断账号是否存在
            exist = JugeLoginUserExist(DB,phone)
            if exist == 0:
                #自动注册
                createuser = InterfaceRegister(DB, phone, "111111",phone,"",False)
                if createuser:
                    # 删除缓存
                    application.App.Redis_SMS.DetCode(phone, code)

                    # json_data["code"] = 1
                    # json_data["msg"] = Global.InterfaceLanguage.GetMsg("SMSGID_1_10", languageStr)
                else:
                    json_data["code"] = -2
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_11", languageStr)
                    return json_data

            # if len(unionid) > 0:
            #     # 这里绑定手机号到
            #     sql = "update tb_userdata set username = '"+unionid+"' where UserName = '"+phone+"';"
            #     DB.edit(sql,None)


            json_data = Login(DB,phone,"",languageStr)

    return json_data


#登录接口
def Login(DB,username,password,languageStr):



    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    data = JugeLoginUserExist(DB,username)


    sql = "select Enddate, UID, pwd_md5,`disable` from tb_userdata where binary username = %s;"
    data = DB.fetchone(sql, username)
    if not data:
        # json_data["code"] = -31
        # json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_18", languageStr)
        sql = "select Enddate, UID, pwd_md5,`disable` from tb_userdata where phone = %s;"
        data = DB.fetchone(sql, username)
        if not data:
            json_data["code"] = -31
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_18", languageStr)
            return json_data

    enddate = int(data[0])
    UID = int(data[1])
    disable = int(data[3])
    _password = data[2]

    # if len(password) > 0 and _password != password:
    #     json_data["code"] = -11
    #     json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_12", languageStr)
    #
    # el
    if disable == 1:
        json_data["code"] = -41
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_19", languageStr)
    elif enddate != 1 and int(time.time()) > enddate:
        json_data["code"] = -21
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_13", languageStr)
    else:

        #登录成功，缓存用户数据
        UserCache(DB,username)
        WitCache(DB,UID)

        json_data["code"] = 1
        json_data["msg"] = UID

    return json_data


def BindPhone(DB,phone,PCode,code,UserName,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    # 判断下验证码
    phoneCode = application.App.Redis_SMS.GetCode(phone, code)
    if phoneCode == "-99":
        json_data["code"] = -1  # 请先获取验证码
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_8", languageStr)
    else:
        if phoneCode != PCode:
            json_data["code"] = -2  # 验证码错误
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_9", languageStr)

        else:
            # 判断账号是否存在
            exist = JugeUserExist(DB, UserName)
            if exist == 0:
                json_data["code"] = -3  # 账号不存在
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_16", languageStr)
            else:
                exist = JugePhoneExist(DB, phone)
                if exist != 0:
                    json_data["code"] = -4  # 手机号已绑定
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_20", languageStr)
                else:
                    sql = "update tb_userdata set phone = '" + str(phone) + "' where username = '"+UserName+"'"
                    DB.edit(sql,None)
                    json_data["code"] = 1 # 手机号已绑定
                    json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_21", languageStr)

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
        #application.App.Redis_Wit.AddWit(uid,num,0,1)
        interface_wit.AddWitScoreWithUserName(None,username,num,0)
        json_data["code"] = 1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_17", languageStr)
    return json_data

def UserCache(DB,username):

    if not application.App.Redis_User.Exist(username):
        sql = "select UID, create_time, organization, distributor, Power, AccountPower, state, appstate from tb_userdata where username = %s limit 0,1;"
        data = DB.fetchone(sql, username)
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
        "wit":wit,          #智慧豆
        "cdate":cdate,      #账号注册时间
        "enddate":0,        #账号到期时间,时间戳，1-表示永久账号
        "phone":"",         #手机号
        "username":"",      #用户名
        "nickname":"",      #昵称
        "nickurl":"",       #头像
        "gm":0,             #GM状态 5表示超级权限
        "vipbuyed": 0,      #是否买过vip
        "vipstate":0,       #vip状态 0-不是vip 1-是vip
        "vipdate":0,        #vip到期时间(时间戳) 1-表示永久
        "mailnrnum": 0,     #未读邮件数量
        "config":{  #配置
            "vip":{},   #vip配置 购买的消耗
            "work":{
                "import":100,   #可导入资源数量
                "template":100, #可存储模板数量
                "create":20,     #可以存储的作品数量上限

            },  #作品相关
            "res":{
                "shoucang":100, #可收藏上限
                "stl":1,        #是否可以导出stl文件
            },   #资源相关
        },
        "myworks":{ #我的作品集
            "self":{
                #我创作的
            },
            "template": {
                # 模板
            },
            "buy": {
                # 我购买的
            },
            "publish": {
                # 我发布的
            },
        }
    }

    #vip配置数据
    user["config"]["vip"] = IC.XrVipConfig
    #vip数据
    sql = "select phone,enddate,UserName,TheNAme,NickUrl,GMState,vippower,vipdate from tb_userdata where uid = " + str(self_uid)+" limit 0,1;"
    data = DB.fetchone(sql,None)
    if data:
        user["phone"] = data[0]
        user["enddate"] = int(data[1])
        user["username"] = data[2]
        user["nickname"] = data[3]
        user["nickurl"] = data[4]
        user["gm"] = int(data[5])
        user["vipbuyed"] = int(data[6])
        user["vipdate"] = int(data[7])
    #作品相关配置
    now = int(time.time())
    print("login vipstate = " , user["vipdate"] , now)
    if user["vipdate"] == 1 or user["vipdate"] > now:
        user["config"]["work"]["import"] = IC.XrWorkConfig["vipimport"]
        user["config"]["work"]["create"] += 20
        user["config"]["work"]["template"] = IC.XrWorkConfig["viptemplate"]
        user["config"]["res"]["shoucang"] = IC.XrWorkConfig["vipshoucang"]
        user["config"]["res"]["stl"] = 1
        user["vipstate"] = 1
    else:
        user["vipstate"] = 0
        user["config"]["work"]["import"] = IC.XrWorkConfig["import"]
        user["config"]["work"]["template"] = IC.XrWorkConfig["template"]
        user["config"]["res"]["shoucang"] = IC.XrWorkConfig["shoucang"]
        user["config"]["res"]["stl"] = 0

    #作品集数据
    myworks = xr_data_work.GetDatas(DB, 3, 0, 0, self_uid)
    if myworks:
        user["myworks"] = myworks

    #未读邮件数量
    user["mailnrnum"] = xr_interface_mail.GetNotReadMailState(DB,self_uid)

    json_data["code"] = 1
    json_data["msg"] = json.dumps(user)

    return json_data



