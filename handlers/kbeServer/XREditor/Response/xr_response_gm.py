import Global
from methods.DBManager import DBManager
from handlers.kbeServer.XREditor.Interface import xr_interface_mail,interface_account

#验证码获取
def Transactions_Code_7001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    channel = int(json_data["channel"])       #0-系统邮件 UID-单用户邮件
    title = json_data["title"]               #标题
    body = json_data["body"]                  #内容
    #talker = int(json_data["talker"])           #发送部门 传0

    if channel < 0 or len(title) < 1 or len(body) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:
        # 获取下db的句柄，如果需要操作数据库的话
        DB = DBManager()
        json_back = xr_interface_mail.writemail(DB,channel,title,body,languageStr)
        DB.destroy()

    return json_back


def Transactions_Code_7002(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }
    #logging.info("getphone code：[%s] - [%s] " % (phone, code))
    #json_data 结构
    num = int(json_data["num"])                 #赠送数量
    username = json_data["username"]            #用户

    if num < 0 or len(username) < 1 :
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    else:
        # 获取下db的句柄，如果需要操作数据库的话
        DB = DBManager()
        json_back = interface_account.GiveWit(username,num,languageStr)
        DB.destroy()

    return json_back

#删除账号
def Transactions_Code_7003(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #json_data 结构
    username = json_data["username"]

    #type = int(json_data["type"])  #
    if len(username) < 1:
        json_back["code"] = 0  #参数异常
        json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
        return json_back
    # 获取下db的句柄，如果需要操作数据库的话
    DB = DBManager()
    json_back = interface_account.DeleteAccount(DB,username, languageStr)
    DB.destroy()
    return json_back
