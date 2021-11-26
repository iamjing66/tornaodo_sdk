# 缓存 access_token 和 jsapi_ticket,并且即使更新，防止过期
# access_token是公众号的全局唯一票据，公众号调用各接口时都需使用access_token。
# 开发者需要进行妥善保存。access_token的存储至少要保留512个字符空间。access_token的有效期目前为2个小时
# jsapi_ticket是公众号用于调用微信JS接口的临时票据。正常情况下，jsapi_ticket的有效期为7200秒，通过access_token来获取
# 我们用redis去存数据，并设置过期时间
import redis
from handlers.wechatGZH.wxlogger import logger


class BaseCache(object):
    """缓存类父类"""
    _host = '127.0.0.1'
    _port = 6379
    _database = 0
    _password = ''

    @property
    def redis_ctl(self):
        """redis控制句柄,就是连接对象"""
        redis_ctl = redis.Redis(host=self._host, port=self._port, db=self._database, password=self._password)
        return redis_ctl


class TokenCache(BaseCache):
    """微信token缓存"""
    _expire_access_token = 7200  # 微信access_token过期时间, 2小时
    _expire_js_token = 7200  # 微信jsapi_ticket, 过期时间, 7200秒

    def set_access_cache(self, key, value):
        """添加微信access_token验证相关redis"""
        self.redis_ctl.set(key, value)
        # 设置过期时间
        self.redis_ctl.expire(key, self._expire_access_token)
        logger.info('更新了 access_token')

    def set_js_cache(self, key, value):
        """添加网页授权相关redis"""
        self.redis_ctl.set(key, value)
        # 设置过期时间
        self.redis_ctl.expire(key, self._expire_js_token)
        logger.info('更新了 js_token')

    def get_cache(self, key):
        """获取redis"""
        try:
            v = (self.redis_ctl.get(key)).decode('utf-8')
            return v
        except Exception as e:
            logger.error('wxcache' + str(e))
            return None
