import logging
from handlers.kbeServer.Editor.response import response_vr,response_account,response_global,response_workmark


class Avatar_App:    #继承base.py中的类BaseHandler

    def __init__(self):
        pass



    def Transactions_Code(self,subCode ,self_uid,self_username, json_data):

        json_dback = {}
        logging.info("VR subcode[%i] self_uid[%i] self_username[%s] json_data[%s]" % (subCode ,self_uid,self_username, json_data))
        if subCode == 2001: #买看-作品
            json_dback = response_vr.Transactions_Code_2001(self_uid,self_username,json_data)
        elif subCode == 2002: #买看-SIS
            json_dback = response_vr.Transactions_Code_2002(self_uid,self_username,json_data)
        elif subCode == 2003: #发布-作品
            json_dback = response_vr.Transactions_Code_2003(self_uid,self_username,json_data)
        elif subCode == 2004:   #VR端登录
            json_dback = response_vr.Transactions_Code_2004(self_uid, self_username, json_data)
        elif subCode == 2005:   #修改密码
            json_dback = response_account.Transactions_Code_2005(self_uid, self_username, json_data)
        elif subCode == 2006:   #修改昵称头像
            json_dback = response_account.Transactions_Code_2006(self_uid, self_username, json_data)
        elif subCode == 2007:   #畅想包月
            json_dback = response_global.Transactions_Code_2007(self_uid, self_username, json_data)
        elif subCode == 2008:   #点赞
            json_dback = response_workmark.Transactions_Code_2008(self_uid, self_username, json_data)
        elif subCode == 2009:   #评分/评论
            json_dback = response_workmark.Transactions_Code_2009(self_uid, self_username, json_data)
        elif subCode == 2010:   #获取评分数据
            json_dback = response_workmark.Transactions_Code_2010(self_uid, self_username, json_data)
        elif subCode == 2011:   #获取评论数据
            json_dback = response_workmark.Transactions_Code_2011(self_uid, self_username, json_data)
        elif subCode == 2012:   #VR端登出
            json_dback = response_account.Transactions_Code_1040(self_uid, self_username, json_data)
        elif subCode == 2013: #发布-作品
            json_dback = response_vr.Transactions_Code_2013(json_data)
        return json_dback





AvatarAppInst = Avatar_App()