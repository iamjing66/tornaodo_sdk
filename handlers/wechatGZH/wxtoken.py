import tornado.ioloop
import requests
import json
from handlers.wechatGZH.wxconfig import WxConfig
from handlers.wechatGZH.wxcache import TokenCache
from handlers.wechatGZH.wxlogger import logger


class WxShedule(object):
    """负责access_token和jsapi_ticket的更新"""
    _token_cache = TokenCache()  # 微信token缓存实例
    _expire_time_access_token = 7000 * 1000  # token过期时间

    def excute(self):
        """执行定时器任务"""
        # IOLoop.instance().call_later(delay, callback, *args, **kwargs)
        # 延时delay秒之后，将callback加入到tornado的加入到的处理队列里面，异步调用只调用一次
        tornado.ioloop.IOLoop.instance().call_later(0, self.get_access_token)
        # tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)
        # callback设定定时调用的方法 callback_time设定每次调用之间的间隔，单位毫秒
        tornado.ioloop.PeriodicCallback(self.get_access_token, self._expire_time_access_token).start()

    def get_access_token(self):

        print("[do] - get_access_token")

        """获取微信全局唯一票据access_token"""
        try:
            url = WxConfig.get_access_token_url
            r = requests.get(url)

            print("[result] - url = " , url , " r = " , r)

            if r.status_code == 200:
                d = json.loads(r.text)

                print("[result] - d = ", d)

                if 'access_token' in d.keys():
                    access_token = d['access_token']
                    # 添加至redis中
                    self._token_cache.set_access_cache('access_token', access_token)
                    # 获取JS_SDK权限签名的jsapi_ticket
                    self.get_jsapi_ticket()
                else:
                    errcode = d['errcode']
                    # 出现错误10s之后调用一次，获取access_token
                    tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)
            else:
                # 网络错误10s之后调用一次，获取access_token
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)
        except Exception as e:
            logger.error('wxtoken get_access_token' + str(e))

    def get_jsapi_ticket(self):

        print("[do] - get_jsapi_ticket")

        """获取JS_SDK权限签名的jsapi_ticket"""
        try:
            # 从redis中获取access_token
            access_token = self._token_cache.get_cache('access_token')
            if access_token:
                url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
                r = requests.get(url)
                if r.status_code == 200:
                    d = json.loads(r.text)
                    errcode = d['errcode']
                    if errcode == 0:
                        jsapi_ticket = d['ticket']
                        # 添加至redis中
                        self._token_cache.set_js_cache('jsapi_ticket', jsapi_ticket)
                    else:
                        tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
                else:
                    # 网络错误 重新获取
                    tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
            else:
                # access_token已经过期 重新获取
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)
        except Exception as e:
            logger.error('wxtoken get_jsapi_ticket' + str(e))