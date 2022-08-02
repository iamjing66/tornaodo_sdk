#!/usr/bin/env python
# coding=utf-8

import requests
from urllib.parse import quote
import hashlib
import time
import xmltodict


class WeiXinPay(object):
    """配置账号信息"""

    # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看

    def __init__(self, AppType):
        if AppType == 3:
            # 开发者调用支付统一下单API生成预交易单
            self.APPID = "wx726f99dff3710781"
            # 商户id
            self.MCHID = "1366971302"
            # 异步通知url，商户根据实际开发过程设定
            # self.NOTIFY_URL = "http://www.bestbutfly.com:8082/wechatpaybck"
            # 交易类型
            self.TRADE_TYPE = "MWEB"
            self.Code_Url = ""
            self.MWEB_URL = ""
            self.APIKEY = "3Dbutfly12345678903Dbutfly123456"
            self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"  # 微信请求url
            self.error = None
            self.params = None
        else:
            # 开发者调用支付统一下单API生成预交易单
            self.APPID = "wx1b80d8e34c0ad13a"
            # 商户id
            self.MCHID = "1366971302"
            # 异步通知url，商户根据实际开发过程设定
            # self.NOTIFY_URL = "http://www.bestbutfly.com:8082/wechatpaybck"
            # 交易类型
            self.TRADE_TYPE = "APP"
            self.Code_Url = ""
            self.MWEB_URL = ""
            self.APIKEY = "3Dbutfly12345678903Dbutfly123456"
            self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"  # 微信请求url
            self.error = None
            self.params = None

    def get_parameter(self, order_id, body, total_fee, spbill_create_ip, attach, notify_url, trade_type):
        self.params = {
                'appid': self.APPID,  # appid
                'mch_id': self.MCHID,  # 商户号
                'nonce_str': self.getNonceStr(),
                'body': body,  # 商品描述
                'out_trade_no': str(order_id),  # 商户订单号
                'total_fee': str(int(total_fee)),
                'spbill_create_ip': spbill_create_ip,  # 127.0.0.1
                'trade_type': trade_type,  # 交易类型
                'notify_url': notify_url,  # 微信支付结果异步通知地址
                'receipt': 'Y',
                'attach': attach
        }
        self.TRADE_TYPE = trade_type
        if trade_type == "MWEB":
            self.params["scene_info"] = "{\"h5_info\":{\"type\": \"Wap\",\"wap_url\": \"\",\"wap_name\": \"飞蝶支付\"}}"
            # {"h5_info":{
            #     "type": "Wap",                              #场景类型
            #     "wap_url": "",                              #WAP网站URL地址
            #     "wap_name": "飞蝶支付"                      #WAP 网站名
            # }}
        # print(self.params)
        return self.params

    def getNonceStr(self, length=32):
        """生成随机字符串"""
        import random
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def key_value_url(self, value, urlencode):
        """
        将键值对转为 key1=value1&key2=value2
        对参数按照key=value的格式，并按照参数名ASCII字典序排序
        """
        # print("lyyym 1 : ASCII字典排序 ： 原始 ： " ,value)
        slist = sorted(value)
        buff = []
        for k in slist:
            v = quote(value[k]) if urlencode else value[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def get_sign(self, params):
        """
        生成sign
        拼接API密钥
        """
        stringA = self.key_value_url(params, False)
        # print("lyyym 2 : ASCII字典排序 ： 排序后 ： ", stringA)
        stringSignTemp = stringA + '&key=' + self.APIKEY  # APIKEY, API密钥，需要在商户后台设置
        # print("lyyym 3 : 拼接API密钥 ： ", stringSignTemp)
        sign = (hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()).upper()
        # print("lyyym 4 : 第一次签名 ： ", sign)
        params['sign'] = sign
        return params

    def get_req_xml(self):
        """
        拼接XML
        """
        self.get_sign(self.params)
        xml = "<xml>"
        for k, v in self.params.items():
            # v = v.encode('utf8')
            # k = k.encode('utf8')
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        return xml.encode("utf-8")

    def get_prepay_id(self):
        """
        请求获取prepay_id
        """
        xml = self.get_req_xml()
        # print("lyyym 5 : 第一次签名后 回调的订单号xml ： ", xml)
        respone = requests.post(self.url, xml, headers={'Content-Type': 'application/xml'})
        msg = respone.text.encode('ISO-8859-1').decode('utf-8')
        xmlresp = xmltodict.parse(msg)
        # print("xmlresp , ", xmlresp)
        if xmlresp['xml']['return_code'] == 'SUCCESS':
            if xmlresp['xml']['result_code'] == 'SUCCESS':
                prepay_id = xmlresp['xml']['prepay_id']
                self.params['prepay_id'] = prepay_id
                self.params['package'] = "Sign=WXPay"
                self.params['timestamp'] = str(int(time.time()))
                if self.TRADE_TYPE == "NATIVE":
                    self.Code_Url = xmlresp['xml']['code_url']
                elif self.TRADE_TYPE == "MWEB":
                    self.MWEB_URL = xmlresp['xml']['mweb_url']

                return self.params
            else:
                return 'failure'
        else:
            return 'failure'

    def re_finall(self):
        """得到prepay_id后再次签名，返回给终端参数
        """
        get_prepay_id = self.get_prepay_id()
        # print(self.error)
        print(get_prepay_id)
        if self.error or get_prepay_id == "failure":
            return "Err"
        if self.TRADE_TYPE == "NATIVE":
            return self.Code_Url
        elif self.TRADE_TYPE == "MWEB":
            return self.MWEB_URL
        else:
            # print("prepay_id , " , get_prepay_id)
            sign_again_params = {
                    'appid': self.params['appid'],
                    'noncestr': self.getNonceStr(),  # self.params['nonce_str'],
                    'package': self.params['package'],
                    'partnerid': self.params['mch_id'],
                    'timestamp': str(int(time.time())),  # self.params['timestamp'],
                    'prepayid': self.params['prepay_id']
                    # 'code_url': self.params['code_url']
            }
            # print( "sign - data : " , sign_again_params)
            self.get_sign(sign_again_params)
            sign_again_params['sign'] = sign_again_params['sign']

            return sign_again_params  # 返回给app

    def get_notifypay(self, data):
        dictdata = dict(data)
        _dictdata = dict(dictdata['xml'])
        success = self.get_sign(_dictdata)
        # print('success', success)
        if success:
            success.pop("sign", None)
            success.pop("sign_type", None)
            return success
        else:
            return None

    @staticmethod
    def xml_to_dict(params):
        """
        拼接XML
        """
        if not isinstance(params, dict):
            return None
        xml = "<xml>"
        for k, v in params.items():
            # v = v.encode('utf8')
            # k = k.encode('utf8')
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        return xml
