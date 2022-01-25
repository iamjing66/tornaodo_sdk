
import Global
from methods.DBManager import DBManager
from handlers.kbeServer.XREditor.Interface import xr_interface_mail,interface_account

#验证码获取
def Transactions_Code_8001(self_uid,self_username,languageStr,json_data):

    #回调json
    json_back = {
        "code" : 0,
        "msg": "",
        "pam": ""
    }

    #flag = int(json_data["channel"])  # 0-系统邮件 UID-单用户邮件

    # if channel < 0 or len(title) < 1 or len(body) < 1:
    #     json_back["code"] = 0  #参数异常
    #     json_back["msg"] =  Global.LanguageInst.GetMsg("SMSGID_0_1",languageStr)
    # else:
    #     # 获取下db的句柄，如果需要操作数据库的话
    #     DB = DBManager()
    #     json_back = xr_interface_mail.writemail(DB,channel,title,body,languageStr)
    #     DB.destroy()

    return json_back
