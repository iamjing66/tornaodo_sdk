from handlers.wechatGZH.wxlogger import logger

"""这是一个处理客户发送信息的文件"""


def reply_text(FromUserName, ToUserName, CreateTime, Content):
    """回复文本消息模板"""
    textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
    out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
    return out


def receive_msg(msg):
    # 这是一个将疑问改成成熟句子的函数，例如：你好吗 公众号回复：你好
    if msg[-1] == u'吗':
        return msg[:len(msg) - 1]
    elif len(msg) > 2 and msg[-2] == u'吗':
        return msg[:len(msg) - 2]
    else:
        return "你说的话我好像不明白？"


def receive_event(event, key):
    # 如果是关注公众号事件
    if event == 'subscribe':
        return "感谢关注！"
    # 如果是点击菜单拉取消息事件
    elif event == 'CLICK':
        # 接下来就是根据你点击不同的菜单拉去不同的消息啦
        # 我为了省事，不进行判断啦，如果需要判断请根据 key进行判断
        return "你点击了菜单" + key
    # 如果是点击菜单跳转Url事件，不做任何处理因为微信客户端会自行处理
    elif event == 'VIEW':
        return None