
import logging
from handlers.kbeServer.XREditor.Response import xr_response_account,xr_response_work,xr_response_gm,xr_response_mail,xr_response_vip
class Avatar_XREditor:    #继承base.py中的类BaseHandler

    def __init__(self):
        pass



    def Transactions_Code(self,subCode ,self_uid,self_username,languageStr, json_data):

        json_dback = {}
        logging.info("opemcode[400]subcode[%i] self_uid[%i] self_username[%s] json_data[%s]" % (subCode ,self_uid,self_username, json_data))
        if subCode == 1001:     #验证码获取
            json_dback = xr_response_account.Transactions_Code_1001(self_uid,self_username,languageStr,json_data)
        elif subCode == 1002:   #注册账号
            json_dback = xr_response_account.Transactions_Code_1002(self_uid, self_username,languageStr, json_data)
        elif subCode == 1003:   #获取微信登录状态
            json_dback = xr_response_account.Transactions_Code_1003(self_uid, self_username,languageStr, json_data)
        elif subCode == 1004:   #微信登录，绑定手机,绑定后自动登录
            json_dback = xr_response_account.Transactions_Code_1004(self_uid, self_username,languageStr, json_data)
        elif subCode == 1005:   #手机验证码登录
            json_dback = xr_response_account.Transactions_Code_1005(self_uid, self_username,languageStr, json_data)
        elif subCode == 1006:   #微信登录
            json_dback = xr_response_account.Transactions_Code_1006(self_uid, self_username,languageStr, json_data)
        elif subCode == 1007:   #账号密码登录
            json_dback = xr_response_account.Transactions_Code_1007(self_uid, self_username,languageStr, json_data)
        elif subCode == 1008:   #忘记密码
            json_dback = xr_response_account.Transactions_Code_1008(self_uid, self_username,languageStr, json_data)
        elif subCode == 1009:   #登录获取用户数据
            json_dback = xr_response_account.Transactions_Code_1009(self_uid, self_username,languageStr, json_data)
        elif subCode == 1010:   #绑定手机号
            json_dback = xr_response_account.Transactions_Code_1010(self_uid, self_username,languageStr, json_data)
        elif subCode == 2001:   #获取资源最新版本号
            json_dback = xr_response_account.Transactions_Code_2001(self_uid, self_username,languageStr, json_data)
        elif subCode == 2002:   #获取资源配表数据
            json_dback = xr_response_account.Transactions_Code_2002(self_uid, self_username,languageStr, json_data)
        elif subCode == 3001:   #软件更新获取
            json_dback = xr_response_account.Transactions_Code_3001(self_uid, self_username,languageStr, json_data)
        elif subCode == 4001:   #新建作品
            json_dback = xr_response_work.Transactions_Code_4001(self_uid, self_username,languageStr, json_data)
        elif subCode == 4002:   #设为模板
            json_dback = xr_response_work.Transactions_Code_4002(self_uid, self_username,languageStr, json_data)
        elif subCode == 4003:   #模板新建
            json_dback = xr_response_work.Transactions_Code_4003(self_uid, self_username,languageStr, json_data)
        elif subCode == 4004:   #作品转移
            json_dback = xr_response_work.Transactions_Code_4004(self_uid, self_username,languageStr, json_data)
        elif subCode == 4005:   #获取资源服务器版本
            json_dback = xr_response_work.Transactions_Code_4005(self_uid, self_username,languageStr, json_data)
        elif subCode == 4006:   #上传作品
            json_dback = xr_response_work.Transactions_Code_4006(self_uid, self_username,languageStr, json_data)
        elif subCode == 4007:  # 作品发布
            json_dback = xr_response_work.Transactions_Code_4007(self_uid, self_username, languageStr, json_data)
        elif subCode == 4008:  # 作品改名
            json_dback = xr_response_work.Transactions_Code_4008(self_uid, self_username, languageStr, json_data)
        elif subCode == 4009:  # 作品删除
            json_dback = xr_response_work.Transactions_Code_4009(self_uid, self_username, languageStr, json_data)
        elif subCode == 4010:  # 作品审核列表
            json_dback = xr_response_work.Transactions_Code_4010(self_uid, self_username, languageStr, json_data)
        elif subCode == 4011:  # 作品审核
            json_dback = xr_response_work.Transactions_Code_4011(self_uid, self_username, languageStr, json_data)
        elif subCode == 4012:  # 购买作品
            json_dback = xr_response_work.Transactions_Code_4012(self_uid, self_username, languageStr, json_data)
        elif subCode == 4013:   #作品复制
            json_dback = xr_response_work.Transactions_Code_4013(self_uid, self_username,languageStr, json_data)
        elif subCode == 4014:   #取消发布
            json_dback = xr_response_work.Transactions_Code_4014(self_uid, self_username,languageStr, json_data)
        elif subCode == 4015:   #下架作品
            json_dback = xr_response_work.Transactions_Code_4015(self_uid, self_username,languageStr, json_data)
        elif subCode == 4016:   #上架作品
            json_dback = xr_response_work.Transactions_Code_4016(self_uid, self_username,languageStr, json_data)
        elif subCode == 5001:  # 作品市场-普通作品/精品市场
            json_dback = xr_response_work.Transactions_Code_5001(self_uid, self_username, languageStr, json_data)
        elif subCode == 5002:  # 个人作品集
            json_dback = xr_response_work.Transactions_Code_5002(self_uid, self_username, languageStr, json_data)
        elif subCode == 7001:  # 写入邮件
            json_dback = xr_response_gm.Transactions_Code_7001(self_uid, self_username, languageStr, json_data)
        elif subCode == 7002:  # 赠送智慧豆
            json_dback = xr_response_gm.Transactions_Code_7002(self_uid, self_username, languageStr, json_data)
        elif subCode == 7003:   #删除账号
            json_dback = xr_response_gm.Transactions_Code_7003(self_uid, self_username,languageStr, json_data)
        elif subCode == 7004:   #删除VIP
            json_dback = xr_response_gm.Transactions_Code_7004(self_uid, self_username,languageStr, json_data)
        elif subCode == 6001:  #获取邮件列表
            json_dback = xr_response_mail.Transactions_Code_6001(self_uid, self_username, languageStr, json_data)
        elif subCode == 6002:  #读邮件
            json_dback = xr_response_mail.Transactions_Code_6002(self_uid, self_username, languageStr, json_data)
        elif subCode == 6003:  #删除邮件
            json_dback = xr_response_mail.Transactions_Code_6003(self_uid, self_username, languageStr, json_data)
        elif subCode == 6004:  #全部已读
            json_dback = xr_response_mail.Transactions_Code_6004(self_uid, self_username, languageStr, json_data)
        elif subCode == 6005:  #删除已读
            json_dback = xr_response_mail.Transactions_Code_6005(self_uid, self_username, languageStr, json_data)
        elif subCode == 8001:  #购买vip
            json_dback = xr_response_vip.Transactions_Code_8001(self_uid, self_username, languageStr, json_data)
        return json_dback







AvatarXREditorInst = Avatar_XREditor()


