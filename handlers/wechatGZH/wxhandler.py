import tornado.web
# 这是python 标准库 用来处理 xml文件的
import xml.etree.ElementTree as ET
import hashlib
import time
# wxreply文件是我写关于处理回复的函数，我们导出来必要的函数
from handlers.wechatGZH.wxreply import receive_msg, receive_event, reply_text
from handlers.wechatGZH.wxconfig import WxConfig
from handlers.wechatGZH.wxcache import TokenCache
from handlers.wechatGZH.wxauthorize import WxAuthorServer
from handlers.wechatGZH.wxlogger import logger
from handlers.wechatGZH.wxsign import get_js_sdk_sign


class wxStartHandler(tornado.web.RequestHandler):
    """
    微信服务器签名验证和消息回复
    check_signature: 校验signature是否正确
    """

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        # 这个是token 和我们在微信公众平台配置接口填写一致
        token = 'iotbird'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        # 对于验证结果返回true or false
        return sha1 == signature

    #
    def get(self):
        """这是get请求，处理配置接口验证的"""
        try:
            # 获取参数
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            # 调用验证函数
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                self.write(echostr)
            else:
                logger.error('微信sign校验,---校验失败')
        except Exception as e:
            logger.error('wxhandler get' + str(e))

    def post(self):
        """ 这是post请求 接收消息，获取参数 """
        body = self.request.body
        # 返回的bodys是xml格式，通过ET转换为键值对格式，方便提取信息
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text
        # 如果发送的是消息请求，判断是文字还是语音，因为我们取发送的内容位置不一样
        if MsgType == 'text' or MsgType == 'voice':
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                elif MsgType == 'voice':
                    Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
                # 调用回复函数判断接受的信息，然后返回对应的内容
                reply_content = receive_msg(Content)
                CreateTime = int(time.time())
                # 调用回复信息封装函数，要指定用户，时间和回复内容
                out = reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                self.write(out)
            except Exception as e:
                logger.error('wxStartHandler post' + str(e))
        # 如果接收的是事件，我们也要处理
        elif MsgType == 'event':
            try:
                Event = data.find('Event').text
                Event_key = data.find('EventKey').text
                CreateTime = int(time.time())
                # 判断事件，并返回内容
                reply_content = receive_event(Event, Event_key)
                if reply_content:
                    out = reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
            except Exception as e:
                logger.error('wxStartHandler post' + str(e))


class wechatShareHandler(tornado.web.RequestHandler):

    wx_config = WxConfig()
    wx_token_cache = TokenCache()

    def get(self):
        print("AppHost = ", self.wx_config.AppHost)
        print("AppID = ", self.wx_config.AppID)

        # 调用微信js-sdk接口功能 需要签名
        sign = get_js_sdk_sign('%s/wx/page/airkiss' % self.wx_config.AppHost)
        sign['appId'] = self.wx_config.AppID

        self.render("share.html",sign=sign)
        #self.write(sign)



class pageHandler(tornado.web.RequestHandler):
    '''页面跳转控制路由'''
    wx_config = WxConfig()
    '''微信网页授权server'''
    wx_author_server = WxAuthorServer()




    def get(self, flag):
        print("flag = ", flag)
        try:
            if flag == '/wxauthor':
                '''微信网页授权'''
                code = self.get_argument('code')
                state = self.get_argument('state')
                # 获取重定向的url
                redirect_url = self.wx_config.wx_menu_state_map[state]
                if code:
                    # 通过code换取网页授权access_token
                    data = self.wx_author_server.get_auth_access_token(code)
                    openid = data['openid']
                    if openid:
                        # 跳到自己的业务界面
                        self.redirect(redirect_url)
                    else:
                        # 获取不到openid
                        logger.error('获取不到openid')
            # 如果请求的是airkiss页面
            elif flag == '/airkiss':
                tdata = {
                    "url" : self.get_argument('url')
                }
                self.render('airkiss.html',tdata=tdata)
            elif flag == '/test':
                self.render('test.html')
        except Exception as e:
            logger.error('pageHandler post' + str(e))


class getSignHandler(tornado.web.RequestHandler):
    """返回js-sdk签名数据"""
    wx_config = WxConfig()
    wx_token_cache = TokenCache()


    def get(self):

        print("AppHost = " , self.wx_config.AppHost)
        print("AppID = " , self.wx_config.AppID)

        # 调用微信js-sdk接口功能 需要签名
        sign = get_js_sdk_sign('%s/wx/page/airkiss' % self.wx_config.AppHost)
        sign['appId'] = self.wx_config.AppID
        self.write(sign)
