#!/usr/bin/env python
# coding=utf-8

import json
import logging
import Global
from handlers.payServer.pay_pam import payPamClass
from methods.WechatPay import WeiXinPay


class pay_wechat:

    def __init__(self):
        pass


    def PayMain(self,AppType,UID,UserName,AppCode,PayData,_out_trade_no,DB,CB):

        if AppType == 1:
            return self.AppPay(UID,UserName,AppCode,PayData,_out_trade_no,DB,CB)
        elif AppType == 2:
            return self.SaomaPay(UID,UserName, AppCode, PayData,_out_trade_no,DB,CB)
        else:
            return self.MobileH5(UID, UserName, AppCode, PayData, _out_trade_no,DB,CB)


    def AppPay(self, UID, UserName, AppCode, PayData, _out_trade_no,DB,CB):

        json_bck = {
            "Code": 1,
            "ERR": 0,
            "price":0,
            "ORDERSTR": "",
            "plen": 0
        }

        Json_Request = payPamClass.GetPayPam(UID,AppCode, PayData,DB)
        if Json_Request["Code"] == 1:
            Json_Data = Json_Request["Data"]

            _payInst = WeiXinPay(1)
            passback_params = "2@1@" + str(AppCode) + "@" + _out_trade_no + "@" + str(Json_Data["price"]) + "@" + Json_Data["name"] + "@" + str(UID) + "@" + str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(passback_params.split('@'))
            #print("_out_trade_no",_out_trade_no)
            #print("_out_trade_no1", Json_Data["name"])
            #print("_out_trade_no2", Json_Data["price"])
            #print("_out_trade_no3", PayData["ip"])
            urlback = CB + "/wechatpaycallback"
            _payInst.get_parameter(_out_trade_no, Json_Data["name"], Json_Data["price"], PayData["ip"], passback_params,urlback , "APP")
            try:
                _wbck = _payInst.re_finall()
                if _wbck == "Err":
                    print("Wechat订单创建失败2！:")
                    json_bck["Code"] = 0
                    json_bck["ERR"] = 1
                else:
                    json_bck["ORDERSTR"] = str(_wbck)
                    json_bck["price"] = Json_Data["price"]
                # print("_wbck , ", _wbck)
            except Exception as e:
                print("订单创建失败1！:" + str(e))
                json_bck["Code"] = 0
                json_bck["ERR"] = 2

        else:
            # 无需购买 这里后续需要处理一下
            json_bck["Code"] = 0
            json_bck["ERR"] = 99


        return json_bck

    def SaomaPay(self, UID, UserName, AppCode, PayData, _out_trade_no,DB,CB):

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

            _payInst = WeiXinPay(2)
            passback_params = "2@2@" + str(AppCode) + "@" + _out_trade_no + "@" + str(Json_Data["price"] )+ "@" + Json_Data["name"] + "@" + str(UID) + "@" + str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(passback_params.split('@'))
            pback = CB + "/wechatpaycallback"
            _payInst.get_parameter(_out_trade_no, Json_Data["name"], Json_Data["price"], PayData["ip"],passback_params,pback, "NATIVE")

            try:
                _wbck = _payInst.re_finall()
                if _wbck == "Err":
                    logging.warn("Wechat订单创建失败2！:")
                    json_bck["Code"] = 0
                    json_bck["ERR"] = 1
                else:
                    json_bck["ORDERSTR"] = str(_wbck)
                    json_bck["price"] = Json_Data["price"]
                # print("_wbck , ", _wbck)
            except Exception as e:
                logging.warn("订单创建失败1！:" + str(e))
                json_bck["Code"] = 0
                json_bck["ERR"] = 2

        else:
            # 无需购买 这里后续需要处理一下
            json_bck["Code"] = 0
            json_bck["ERR"] = 99
        logging.info("SaomaPay -> json_bck[%s]" % json_bck )
        return json_bck


    def MobileH5(self, UID, UserName, AppCode, PayData, _out_trade_no,DB,CB):

        json_bck = {
            "Code": 1,
            "ERR": 0,
            "price":0,
            "ORDERSTR": "",
            "plen": 0
        }

        Json_Request = payPamClass.GetPayPam(UID,AppCode, PayData,DB)
        if Json_Request["Code"] == 1:
            Json_Data = Json_Request["Data"]

            _payInst = WeiXinPay(3)
            passback_params = "2@1@" + str(AppCode) + "@" + _out_trade_no + "@" + str(Json_Data["price"]) + "@" + Json_Data["name"] + "@" + str(UID) + "@" + str(UserName) + "@" + Json_Data["params"]
            json_bck["plen"] = len(passback_params.split('@'))
            #print("_out_trade_no",_out_trade_no)
            #print("_out_trade_no1", Json_Data["name"])
            #print("_out_trade_no2", Json_Data["price"])
            #print("_out_trade_no3", PayData["ip"])
            urlback = CB + "/wechatpaycallback"
            #PayData["ip"] = "192.168.0.23"
            _payInst.get_parameter(_out_trade_no, Json_Data["name"], Json_Data["price"], PayData["ip"], passback_params,urlback , "MWEB")
            try:
                _wbck = _payInst.re_finall()
                if _wbck == "Err":
                    print("Wechat订单创建失败2！:")
                    json_bck["Code"] = 0
                    json_bck["ERR"] = 1
                else:
                    json_bck["ORDERSTR"] = str(_wbck)
                    json_bck["price"] = Json_Data["price"]
                print("_wbck , ", _wbck)
            except Exception as e:
                print("订单创建失败1！:" + str(e))
                json_bck["Code"] = 0
                json_bck["ERR"] = 2

        else:
            # 无需购买 这里后续需要处理一下
            json_bck["Code"] = 0
            json_bck["ERR"] = 99


        return json_bck


WechatClass = pay_wechat()
