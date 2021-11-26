import time
import random
import string
import hashlib
from handlers.wechatGZH.wxcache import TokenCache
from handlers.wechatGZH.wxlogger import logger


def get_js_sdk_sign(url):
    """获取调用js-sdk必要的数据 nonceStr timestamp signature"""
    try:
        _token_cache = TokenCache()  # 微信token缓存实例
        jsapi_ticket = _token_cache.get_cache('jsapi_ticket')  # 从redis中提取jsapi_ticket
        if jsapi_ticket:
            nonceStr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            timestamp = int(time.time())
            url = url
            ret = {
                'nonceStr': nonceStr,
                'jsapi_ticket': jsapi_ticket,
                'timestamp': timestamp,
                'url': url
            }
            _string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
            ret['signature'] = hashlib.sha1(_string.encode('utf-8')).hexdigest()
            return ret
    except Exception as e:
        logger.error('wxsign get_js_sdk_sign' + str(e))