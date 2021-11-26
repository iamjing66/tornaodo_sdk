from handlers.wechatGZH.wxconfig import WxConfig
from handlers.wechatGZH.wxcache import TokenCache
from handlers.wechatGZH.wxauthorize import WxAuthorServer
from handlers.wechatGZH.wxlogger import logger
import requests
import json


class WxMenuServer(object):
    """这是一个创建自定义菜单的文件，当你需要更新菜单的时候执行这个文件"""
    token_cache = TokenCache()  # 微信token缓存对象
    # 微信网页授权server，目的是为了重定向，类似关卡
    wx_author_server = WxAuthorServer()

    def create_menu(self):
        """
        自定义菜单创建接口,这个非常灵活，
        我们可以设置权限，可以传入参数等等，
        我们这边就直接写死了
        """
        try:
            access_token = self.token_cache.get_cache('access_token')
            if not access_token:
                logger.error('创建菜单 获取 token失败')
                return None
            url = WxConfig.menu_create_url + access_token
            data = self.create_menu_data()
            r = requests.post(url, data.encode('utf-8'))
            if not r.status_code == 200:
                logger.error('创建菜单 网络错误')
                return None
            json_res = json.loads(r.text)
            if 'errcode' in json_res.keys():
                errcode = json_res['errcode']
                return errcode
        except Exception as e:
            logger.error('wxmenu create_menu' + str(e))

    def get_menu(self):
        """自定义菜单查询接口"""
        try:
            access_token = self.token_cache.get_cache('access_token')
            if not access_token:
                return None
            url = WxConfig.menu_get_url + access_token
            r = requests.get(url)
            if not r.status_code == 200:
                return None
            json_res = json.loads(r.text)
            if 'errcode' in json_res.keys():
                errcode = json_res['errcode']
                logger.error('自定义菜单查询失败!')
                return errcode
        except Exception as e:
            logger.error('wxmenu get_menu' + str(e))

    def delete_menu(self):
        """自定义菜单删除接口"""
        try:
            access_token = self.token_cache.get_cache('access_token')
            if not access_token:
                return None
            url = WxConfig.menu_delete_url + access_token
            r = requests.get(url)
            if not r.status_code == 200:
                return None
            json_res = json.loads(r.text)
            if 'errcode' in json_res.keys():
                errcode = json_res['errcode']
                logger.error('自定义菜单删除失败')
                return errcode
        except Exception as e:
            logger.error('wxmenu delete_menu' + str(e))

    def create_menu_data(self):
        """创建菜单数据"""
        menu_data = {'button': []}  # 大菜单
        menu_Index0 = {
            'type': 'click',
            'name': '一级菜单',
            "key": "menu1"
        }
        menu_data['button'].append(menu_Index0)
        menu_Index1 = {
            "name": "二级菜单",
            "sub_button":
                [
                    {
                        "type": "view",
                        "name": "test",
                        "url": self.wx_author_server.get_code_url('test')
                    },
                    {
                        "type": "click",
                        "name": "click",
                        "key": "click"
                    }
                ]
        }
        menu_data['button'].append(menu_Index1)
        # 菜单三 我们让它请求页面，验证js-sdk权限
        menu_Index2 = {
            'type': 'view',
            'name': 'airkiss',
            "url": self.wx_author_server.get_code_url('airkiss')
        }
        menu_data['button'].append(menu_Index2)
        menu_data = json.dumps(menu_data, ensure_ascii=False)
        return menu_data


if __name__ == '__main__':
    wx_menu_server = WxMenuServer()
    wx_menu_server.create_menu()