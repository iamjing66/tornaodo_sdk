class WxConfig(object):
    """微信开发--基础配置"""
    # 测试账号
    AppID = 'wx726f99dff3710781'
    AppSecret = '53e436d340bbbe8ba1648d8404b7f41e'

    """微信网页开发域名"""
    AppHost = 'http://www.mrbutfly.com'

    '''获取access_token接口'''
    get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    AppID, AppSecret)

    '''自定义菜单创建接口'''
    menu_create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='

    '''自定义菜单查询接口'''
    menu_get_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token='

    '''自定义菜单删除接口'''
    menu_delete_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='

    '''微信公众号菜单映射页面，参数是page/后面的'''
    wx_menu_state_map = {
        'airkiss': '%s/wx/page/airkiss' % AppHost,
        'test': '%s/wx/page/test' % AppHost
    }