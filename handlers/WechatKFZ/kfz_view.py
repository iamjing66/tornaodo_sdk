import logging

import application
from handlers.WechatKFZ import kfz_authorize
from handlers.base import BaseHandler
from handlers.kbeServer.XREditor.Interface import interface_account
from methods.DBManager import DBManager


class WechatLoginCallBackRequest(BaseHandler):

    def get(self):


        print("self.get_argument = " , self.get_arguments)
        code = self.get_argument("code",None)
        state = self.get_argument("state",None)
        logging.info("[wechatLogin] wechat callback - code = %s , state = %s " % (code,state))
        if code and state:
            json_torken = application.App.WechatLogin.get_auth_access_token(code)
            #{'access_token': '52_tp1kOT1pOjtxGv5vgXeOSAgex8WNUNPfoGe3j8VJ0X7tEdTgqYyUoRwyrAvhXmAvlzJ56yqaXRt2yt-s0tbdpJyFrSRjsfx4IU9qi3w89Hs', 'expires_in': 7200,
            # 'refresh_token': '52_hpYcSsUJanzgI1yQzN8LpFXt_9yexg0m6oCO4uSkVi5tslIWlfY-AxeKOIoVPyFckaxodkUGNnur2128Gqfxre8fYdAx679tpV_lQwkvl08',
            #  'openid': 'oWlIt5unXOcY1NxIMZkButjOPbqs', 'scope': 'snsapi_login', 'unionid': 'o8eNzw__wuk6KgOWP43xEep4QtxQ'}
            if json_torken:
                access_token = json_torken["access_token"]
                unionid = json_torken["unionid"]
                openid = json_torken["openid"]
                #o8eNzw__wuk6KgOWP43xEep4QtxQ
                #o8eNzw__wuk6KgOWP43xEep4QtxQ
                #openid = oWlIt5unXOcY1NxIMZkButjOPbqs
                #{'openid': 'oWlIt5unXOcY1NxIMZkButjOPbqs', 'nickname': 'lyyym', 'sex': 0, 'language': '', 'city': '', 'province': '', 'country': '', 'headimgurl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOjmsCYpuqtJZ7LTnkYQfaoGic651kicHlTLiaLicfSxfJuLYAuJDib6n8f1oc5Cicj6NKSOdHHzjpCulw/132', 'privilege': [], 'unionid': 'o8eNzw__wuk6KgOWP43xEep4QtxQ'}
                logging.info("[gettorken] openid = %s , unionid = %s"% (openid ,unionid))
                DB = DBManager()
                username = interface_account.JugeUserExist(DB,unionid)

                if not username:
                    #获取用户信息
                    json_userinfo = application.App.WechatLogin.get_WechatUserInfo(access_token,openid)
                    if json_userinfo:

                        nickname = json_userinfo["nickname"]
                        headimgurl = json_userinfo["headimgurl"]
                        sex = json_userinfo["sex"]
                        print("nickname = " , nickname)
                        print("headimgurl = ", headimgurl)
                        print("sex = ", sex)

                        #这里注册
                        interface_account.InterfaceRegister(DB,unionid,'111111',nickname,headimgurl,True)

                        #logging.info("[userinfo]nickname = %s, , headimgurl = %s , sex = %s " % (nickname,headimgurl,str(sex)))
                        #application.App.Redis_Wechat.SaveCode(state,nickname,headimgurl,str(sex),unionid)
                        application.App.Redis_Wechat.SavUserName(state, unionid)
                        self.write("Wechat Login To Bind Phone")
                    else:
                        self.write("Wechat Login Error 1")
                else:
                    self.write("Wechat Login Succ")
                    application.App.Redis_Wechat.SavUserName(state,unionid)
                #{'openid': 'oWlIt5unXOcY1NxIMZkButjOPbqs', 'nickname': 'lyyym', 'sex': 0, 'language': '', 'city': '', 'province': '', 'country': '',
                #  'headimgurl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOjmsCYpuqtJZ7LTnkYQfaoGic651kicHlTLiaLicfSxfJuLYAuJDib6n8f1oc5Cicj6NKSOdHHzjpCulw/132', 'privilege': [],
                # 'unionid': 'o8eNzw__wuk6KgOWP43xEep4QtxQ'}
                #logging.info("[userinfo]json_userinfo = %s" % json_userinfo)
                DB.close()
            else:
                self.write("Wechat Login Error 2")
        else:
            self.write("Wechat Login Error 3")
        #print("call back get code = " , code)



    def post(self):

        print("call back post")

class WechatLoginRequest(BaseHandler):

    def get(self):

        #json_data = interface_account.WechatLogin()

        #self.write(json_data)

        state = self.get_argument("state")

        codeUrl = application.App.WechatLogin.get_code_url(state)

        logging.info("[wechatLogin] codeUrl = %s , state = %s" % (codeUrl,state))
        #codeUrl = https://open.weixin.qq.com/connect/qrconnect?appid=wx74b1fd3e0df1b73a&redirect_uri=http%3A%2F%2F29w1v17148.qicp.vip%2Fwechatkfz%2Fcodeget&response_type=code&scope=snsapi_login&state=18740487328 ,
        #  state = 18740487328
        self.redirect(codeUrl)
