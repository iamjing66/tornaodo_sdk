class kfz_WxConfig(object):
    """微信开发--基础配置"""
    # 测试账号
    AppID = "wx74b1fd3e0df1b73a"
    AppSecret = "3394704c3f91a9eadc1f8e1863bf7bfd"
    OPENID = ""
    """微信网页开发域名"""
    AppHost = 'http://29w1v17148.qicp.vip'

    '''获取access_token接口'''
    get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)

