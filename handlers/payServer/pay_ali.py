#!/usr/bin/env python
# coding=utf-8

import json

from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest

import Global
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePrecreateRequest import AlipayTradePrecreateRequest

from handlers.payServer.pay_pam import payPamClass

class pay_ali:

    def __init__(self):
        #支付宝支付
        pass


    def PayMain(self,AppType,UID,UserName,AppCode,PayData,_out_trade_no,DB,ali_client,ali_model,CB):

        if AppType == 1:
            return self.AppPay(UID,UserName,AppCode,PayData,_out_trade_no,DB,ali_client,ali_model,CB)
        elif AppType == 2:
            return self.SaomaPay(UID,UserName, AppCode, PayData,_out_trade_no,DB,ali_client,ali_model,CB)
        else:
            return self.MobileH5(UID, UserName, AppCode, PayData, _out_trade_no, DB, ali_client, ali_model,CB)


    #APP支付
    def AppPay(self,UID,UserName,AppCode,PayData,_out_trade_no,DB,ali_client,ali_model,CB):

        json_bck = {
            "Code": 1,
            "price":0,
            "ERR": 0,
            "ORDERSTR": "",
            "plen":0
        }

        Json_Request = payPamClass.GetPayPam(UID,AppCode,PayData,DB)
        if Json_Request["Code"] == 1:
            Json_Data = Json_Request["Data"]

            model = ali_model
            model.subject = Json_Data["name"]  # 商品标题
            model.out_trade_no = _out_trade_no  # 商家订单编号
            model.timeout_express = "30m"  # 超时关闭该订单时间
            model.product_code = "QUICK_MSECURITY_PAY"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
            model.format = "JSON"
            model.charset = "utf-8"
            model.total_amount = str(Json_Data["price"]/100)  # 订单总金额
            #print(Json_Data["price"])
            #print(model.total_amount)
            #基础数据是8个长度
            model.passback_params = "1@1@" + str(AppCode) + "@"+ _out_trade_no + "@" + str(Json_Data["price"]) + "@"+ Json_Data["name"]+ "@"+ str(UID)+ "@"+ str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(model.passback_params.split('@'))

            request = AlipayTradeAppPayRequest(biz_model=model)
            request.notify_url = CB + "/alipaycallback"
            #request.notify_url = "http://www.bestbutfly.com:8082/alipaybck"
            response = ali_client.sdk_execute(request)
            orderString = str(response)
            json_bck["ORDERSTR"] = orderString
            json_bck["price"] = Json_Data["price"]


        else:
            #无需购买 这里后续需要处理一下
            json_bck["Code"] = 0
            json_bck["ERR"] = 99


        return json_bck



    #扫码支付
    def SaomaPay(self,UID,UserName,AppCode,PayData,_out_trade_no,DB,ali_client,ali_model,CB):

        json_bck = {
            "Code": 1,
            "ERR": 0,
            "price": 0,
            "ORDERSTR": "",
            "plen": 0
        }

        Json_Request = payPamClass.GetPayPam(UID,AppCode, PayData,DB)
        if Json_Request["Code"] == 1:
            Json_Data = Json_Request["Data"]

            model = ali_model
            model.subject = Json_Data["name"]  # 商品标题
            model.out_trade_no = _out_trade_no  # 商家订单编号
            model.timeout_express = "30m"  # 超时关闭该订单时间
            model.product_code = "FACE_TO_FACE_PAYMENT"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
            model.format = "JSON"
            model.charset = "utf-8"
            model.total_amount = str(Json_Data["price"] / 100)  # 订单总金额
            model.passback_params = "1@2@" + str(AppCode) + "@" + _out_trade_no + "@" + str(Json_Data["price"]) + "@" + Json_Data["name"] + "@" + str(UID) + "@" + str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(model.passback_params.split('@'))

            request = AlipayTradePrecreateRequest(biz_model=model)
            request.notify_url = CB + "/alipaycallback"
            response = ali_client.execute(request)
            json_response = json.loads(response)
            if json_response["msg"] == "Success":
                json_bck["ORDERSTR"] = json_response["qr_code"]
                json_bck["price"] = Json_Data["price"]
            else:
                json_bck["Code"] = 0
                json_bck["ERR"] = 1


        else:
            # 无需购买 这里后续需要处理一下
            json_bck["Code"] = Json_Request["Code"]
            json_bck["ERR"] = 99

        return json_bck

    # 手机网站支付
    def MobileH5(self, UID, UserName, AppCode, PayData, _out_trade_no,DB , ali_client, ali_model,CB):

        json_bck = {
            "Code": 1,
            "price": 0,
            "ERR": 0,
            "ORDERSTR": "",
            "plen": 0
        }

        Json_Request = payPamClass.GetPayPam(UID, AppCode, PayData,DB)
        if Json_Request["Code"] == 1:
            Json_Data = Json_Request["Data"]

            model = ali_model
            model.subject = Json_Data["name"]  # 商品标题
            model.out_trade_no = _out_trade_no  # 商家订单编号
            model.timeout_express = "30m"  # 超时关闭该订单时间
            model.product_code = "QUICK_MSECURITY_PAY"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
            model.format = "JSON"
            model.charset = "utf-8"
            model.total_amount = str(Json_Data["price"] / 100)  # 订单总金额
            # print(Json_Data["price"])
            # print(model.total_amount)
            # 基础数据是8个长度
            model.passback_params = "1@1@" + str(AppCode) + "@" + _out_trade_no + "@" + str(Json_Data["price"]) + "@" + Json_Data["name"] + "@" + str(UID) + "@" + str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(model.passback_params.split('@'))

            request = AlipayTradeWapPayRequest(biz_model=model)
            #request = AlipayTradeAppPayRequest(biz_model=model)
            request.notify_url = CB + "/alipaycallback"
            # request.notify_url = "http://www.bestbutfly.com:8082/alipaybck"
            # response = ali_client.pageExecute(request)
            # orderString = str(response)



            json_bck["price"] = Json_Data["price"]

            #form = None
            form = ali_client.page_execute(request,http_method="GET")  # .getBody()  #调用SDK生成表单
            json_bck["ORDERSTR"] = form
            #print("form : " + form)

        else:
            # 无需购买 这里后续需要处理一下
            json_bck["Code"] = 0
            json_bck["ERR"] = 99

        return json_bck



AliClass = pay_ali()
