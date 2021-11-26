#!/usr/bin/env python
# coding=utf-8

from methods.WechatPay import WeiXinPay
from urllib.parse import quote
import hashlib
import xml.etree.ElementTree as ET

class Wxpay_server_pub(WeiXinPay):
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self, xml):
        self.xml = xml
        self.data = {}  # 接收到的数据，类型为关联数组
        self.returnParameters = {}  # 返回参数，类型为关联数组
        self.APIKEY_CODE = "3Dbutfly12345678903Dbutfly123456"
        # super(Wxpay_server_pub, self).__init__()  # super(子类名, 子类对象).父类方法(参数1，参数2.。。)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        # 签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String, self.APIKEY_CODE)
        # 签名步骤三：MD5加密
        # String = hashlib.md5(String).hexdigest()
        String = hashlib.md5(String.encode("utf-8")).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def xmlToArray(self):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(self.xml)
        #root = ElementTree.fromstring(self.xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.items():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def saveData(self):
        """将微信的请求xml转换成关联数组，以方便数据处理"""
        self.data = self.xmlToArray()

    def checkSign(self):
        """校验签名"""
        tmpData = dict(self.data)  # make a copy to save sign
        del tmpData['sign']
        sign = self.getSign(tmpData)  # 本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def getData(self):
        """获取微信的通知的数据"""
        return self.data

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def setReturnParameter(self, parameter, parameterValue):
        """设置返回微信的xml数据"""
        self.returnParameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """生成接口参数xml"""
        return self.arrayToXml(self.returnParameters)

    def returnXml(self):
        """将xml数据返回微信"""
        returnXml = self.createXml()
        return returnXml