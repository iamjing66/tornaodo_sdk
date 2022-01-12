from handlers.WechatKFZ.kfs_config import kfz_WxConfig
from urllib import parse
from handlers.wechatGZH.wxlogger import logger
import requests
import json

""" 用于拦截 对页面的请求 提取用户信息"""


class WxAuthorKFZServer(object):
    """微信网页授权server"""

    """对与请求连接进行重定向，获取用户信息进行网页授权"""
    redirect_uri = '%s/wechatkfz/codeget' % kfz_WxConfig.AppHost
    """
    应用授权作用域
    snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid）
    snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
    """
    SCOPE = 'snsapi_login'

    """通过code换取网页授权access_token"""
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
    #https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
    """拉取用户信息"""
    get_userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?'

    def get_code_url(self, state):
        """获取code的url"""
        _dict = {'redirect_uri': self.redirect_uri}
        redirect_uri = parse.urlencode(_dict)
        author_get_code_url = 'https://open.weixin.qq.com/connect/qrconnect?appid=%s&%s&response_type=code&scope=%s&state=%s' % (
            kfz_WxConfig.AppID, redirect_uri, self.SCOPE, state)
        return author_get_code_url

    def get_auth_access_token(self, code):
        """通过code换取网页授权access_token"""
        try:
            url = self.get_access_token_url + 'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
                kfz_WxConfig.AppID, kfz_WxConfig.AppSecret, code)
            r = requests.get(url)
            if r.status_code == 200:
                json_res = json.loads(r.text)
                #print("json_res torken = ",json_res)
                if 'access_token' in json_res.keys():
                    return json_res
                elif 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    logger.error('通过code换取网页授权access_token:' + errcode)
        except Exception as e:
            logger.error('get_auth_access_token:' + str(e))

        return None

    def get_WechatUserInfo(self, torken,openid):
        """通过code换取网页授权access_token"""
        try:
            #https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID
            url = self.get_userinfo_url + 'access_token=%s&openid=%s' % (
                torken, openid)
            r = requests.get(url)
            if r.status_code == 200:
                json_res = json.loads(r.text)

                #print("json_res USERINFO = ",json_res)
                return json_res
                # if 'access_token' in json_res.keys():
                #     return json_res
                # elif 'errcode' in json_res.keys():
                #     errcode = json_res['errcode']
                #     logger.error('通过code换取网页授权access_token:' + errcode)
        except Exception as e:
            logger.error('get_WechatUserInfo:' + str(e))

        return None