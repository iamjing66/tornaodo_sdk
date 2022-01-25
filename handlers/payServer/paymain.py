#!/usr/bin/env python
# coding=utf-8

import json
import time
import logging
import Global
import application
from handlers.base import BaseHandler
from handlers.payServer.pay_ali import AliClass
from handlers.payServer.pay_wechat import WechatClass
from handlers.payServer.payback_ali import PayBackAliClass
from methods.Wxpay_server_pub import Wxpay_server_pub
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_order
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU



class PayOrder(BaseHandler):

    def post(self):

        json_back = {}

        self.SOLR_VERIFY

        paydata = self.SolrData
        DB = DBManager()
        PayType = int(paydata["PayType"])           #1-支付宝          2-微信
        AppType = int(paydata["AppType"])           #1-APP支付         2-扫码支付  3-VR支付
        UID = paydata["UID"]                        #UID
        #print("1============",type(paydata["PayData"]) )
        UserName = paydata["UserName"]              #用户名
        AppCode = int(paydata["AppCode"])           #1-编程作品买看 2-SIS课程购买 3-频道畅享 4-VIP 5-包裹位
        pdata = paydata["PayData"]
        if isinstance(pdata,dict):
            PayData = pdata
        else:
            PayData = json.loads(pdata)  # 支付数据
        #CB = paydata["cb"]                          #支付回调


        #这里处理xreditor的新接口
        if "from" not in PayData.keys():
            PayData["from"] = paydata["from"]
            PayData["ip"] = paydata["ip"]

        #if len(CB) < 1:
        CB = Global.get_config.pay_config()

        logging.info("PayOrder -> post -> UID[%s],UserName[%s],PayType[%i],AppType[%i],AppCode[%i],CB[%s]" % (UID,UserName,PayType,AppType,AppCode, CB))

        _order = self.Ali_Order
        _order += 1
        self.application.Ali_Order = _order
        _now = int(time.time())
        _out_trade_no = str(PayType) + str(AppType) + str(AppCode) + str(_now) + str(_order)

        logging.info("支付参数：PayType[%i],AppType[%i],UID[%s],UserName[%s],AppCode[%i],PayData[%s]" % (PayType,AppType,UID,UserName,AppCode,PayData))

        if PayType == 1:
            json_back = AliClass.PayMain(AppType,UID,UserName,AppCode,PayData,_out_trade_no,DB,self.ali_client,self.ali_model,CB)
        else:
            json_back = WechatClass.PayMain(AppType, UID,UserName, AppCode, PayData,_out_trade_no,DB,CB)

        if json_back["Code"] == 1:
            spaydata = paydata["PayData"]
            if isinstance(PayData,dict):
                spaydata = json.dumps(PayData)
            #print("PayData",_out_trade_no,str(UID),UserName,PayData["from"],PayType,json_back["price"],PayData,PayData["ip"],AppType)
            interface_order.InsertPayOrder(_out_trade_no,str(UID),UserName,PayData["from"],PayType,json_back["price"],spaydata,PayData["ip"],AppType,DB)


        # self.SetPCodeLen(AppCode,json_back["plen"])

        DB.destroy()

        logging.info(json_back)

        self.write(json_back)

    def get(self):

        Pdata = self.get_argument("PayData")
        PayType = int(self.get_argument("PayType"))  # 1-支付宝          2-微信
        # PayData=3@2116@2@1&PayType=1


        arr_pam = Pdata.split('@')
        AppCode = int(arr_pam[0])  # 1-编程作品买看 2-SIS课程购买 3-频道畅享 4-VIP 5-包裹位
        UID = arr_pam[1]  # UID

        CB = globalRedisU.redisurl_get(UID,"app")  # 支付回调

        if not CB:
            CB = Global.get_config.pay_config()


        AppType = 3  # 1-APP支付        2-扫码支付       3-手机网站支付
        UserName = ""
        organization = ""
        distributor = ""
        _power = 0
        PayData = {}
        logging.info("PayOrder -> get -> UID[%s],UserName[%s],PayType[%i],AppType[%i],AppCode[%i]" % (UID,UserName,PayType,AppType,AppCode))
        DB = DBManager()
        sql = "select UserName,organization,distributor,`Power` from tb_userdata where uid = " + str(UID)

        data = DB.fetchone(sql,None)
        if data:
            UserName = data[0]
            organization = int(data[1])
            distributor = int(data[2])
            _power = int(data[3])

        if AppCode == 1:  # 买看
            # 1@9@62@5457
            p_uid = int(arr_pam[2])
            p_cid = int(arr_pam[3])
            PayData = {
                "wid": p_cid, "b_uid": p_uid, "organization": organization, "distributor": distributor,"from":"VR" , "ip": "127.0.0.1","power":_power
            }
        elif AppCode == 2:  # SIS课程
            # 2@9@1010003
            p_cid = arr_pam[2]
            PayData = {
                "wid": p_cid, "b_uid": 0, "organization": organization, "distributor": distributor, "from": "VR","ip": "127.0.0.1","power":_power
            }
        elif AppCode == 3:  # 频道包月
            # 3@9@1@1
            chanelid = arr_pam[2]
            monthid = int(arr_pam[3])
            PayData = {
                "changel": str(chanelid) , "month": monthid, "organization": organization, "distributor": distributor, "from": "VR","ip": "127.0.0.1","power":_power, "WType": "0"
            }

        _order = self.Ali_Order
        _order += 1
        self.application.Ali_Order = _order
        _now = int(time.time())
        _out_trade_no = str(PayType) + str(AppType) + str(AppCode) + str(_now) + str(_order)
        if PayType == 1:
            json_back = AliClass.PayMain(AppType,UID,UserName,AppCode,PayData,_out_trade_no,DB,self.ali_client,self.ali_model,CB)
        else:
            json_back = WechatClass.PayMain(AppType, UID,UserName, AppCode, PayData,_out_trade_no,DB,CB)

        if json_back["Code"] == 1:
            interface_order.InsertPayOrder(_out_trade_no,str(UID),UserName,PayData["from"],PayType,json_back["price"],Pdata,PayData["ip"],AppType,DB)


        # self.SetPCodeLen(AppCode,json_back["plen"])

        DB.destroy()

        logging.info("订单详情：%s" % json_back)

        if AppType == 3:
            _from = json_back["ORDERSTR"]
            #print("_from" , _from)
            # httpResponse.setContentType("text/html;charset=utf-8");
            # httpResponse.getWriter().write(form); // 直接将完整的表单html输出到页面
            # httpResponse.getWriter().flush();
            #self.write(_from)

            #_from = "<!DOCTYPE html>"+"<html lang=\"en\">"+ "<head>"+"    <meta charset=\"UTF-8\">"+"   <title>重定向测试页面</title>"+"</head>"+"<body>"+"</body>"+"</html>"

            # print("这里需要重定向")
            self.set_header("Content-Type", "text/html")
            self.set_header("charset", "UTF-8")
            self.redirect(_from)
            #self.write("pay2.html")
            #self.set_header("Content-Type", "text/html","")
            #self.
            #self.redirect("/test")
        else:
            self.write(json_back)



class AliPayCallBack(BaseHandler):

    def post(self):
        json_bck = {
            "code": "SUCCESS",
            "message": ""
        }

        _body = self.request.body_arguments
        _passback_params = self.get_body_argument("passback_params", "")
        notify_type = self.get_body_argument('notify_type', "")  # 通知类型
        trade_status = self.get_body_argument('trade_status', "")  # 订单状态
        out_trade_no = self.get_body_argument('out_trade_no', "")  # 订单状态
        total_amount = self.get_body_argument('total_amount', "")  # 订单状态

        _arr_pam = _passback_params.split('@')
        logging.info("body pam --> %s" % _body)
        logging.info("payback pam -> %s" % _arr_pam)
        if len(_arr_pam) < 5:
            json_bck["code"] = "Err1"
            logging.info("payback 参数缺失")
        else:
            AppCode = int(_arr_pam[2])
            _order = _arr_pam[3]
            _price = int(_arr_pam[4])

            DB = DBManager()
            if interface_order.GetPayFlag(_order, DB) != 0:
                logging.info("Err_repit")
                json_bck["code"] = "Err_repit"
            elif _order != out_trade_no or float(_price/100) != float(total_amount):
                json_bck["code"] = "Err3"  # 回调的订单不是请求的，考虑是 假链接
            else:
                if notify_type == 'trade_status_sync':
                    pay_success = False
                    if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                        pay_success = True
                    if pay_success:
                        # 如果支付成功一定是success这个单词，其他的alipay不认
                        PayBackAliClass.Do(AppCode,_passback_params,_order,DB)
                        #self.SetPayOrders(_order)
                        interface_order.UpdatePayOrder(_order,1,DB)
                        json_bck["code"] = "SUCCESS"
                else:
                    logging.error("notify_type 不是 trade_status_sync")
                    json_bck["code"] = "Err2"
            DB.destroy()
        logging.info(json_bck)
        self.write(json_bck)


class WechatPayCallBack(BaseHandler):

    def post(self):
        json_bck = {
            "code": "SUCCESS",
            "message":""
        }

        params = self.request.body.decode('utf-8')
        #print("params",params)
        returnXml = ""
        try:
            Wxpay_server_pub(params).xmlToArray()  # 判断是否xml数据格式
        except Exception as e:
            # 其他需求比如 和alipay 支付同一回调地址
            logging.error("Wechat_PayBck Resut: %s" % str(e))
        else:
            wxpay_params = params  # xml 字符串
            wxpay = Wxpay_server_pub(wxpay_params)  # 创建对象
            wxpay.saveData()
            wxpay_dict = wxpay.getData()
            return_code = wxpay_dict.get('return_code')
            if return_code == wxpay.SUCCESS:
                ret = wxpay.checkSign()  # 校验签名
                channel = "微信支付"
                subject = None
                if ret:  # 成功则继续后续操作
                    wxpay_dict = wxpay.xmlToArray()
                    amount = wxpay_dict.get('total_fee')
                    order_no = wxpay_dict.get('out_trade_no')
                    # nonce_str = wxpay_dict.get('nonce_str')
                    result_code = wxpay_dict.get('result_code')
                    _passback_params = wxpay_dict.get('attach')
                    #print("amount" , amount)
                    #print("order_no", order_no)
                    #print("_passback_params", _passback_params)
                    #print("result_code", result_code)
                    # 时间格式转换
                    # datetime_struct = parser.parse(time_string)
                    # time_paid = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
                    # 返回微信数据
                    wxpay.setReturnParameter("return_code", "SUCCESS")
                    wxpay.setReturnParameter("return_msg", "OK")
                    returnXml = wxpay.returnXml()

                    if result_code == wxpay.SUCCESS:
                        _arr_pam = _passback_params.split('@')
                        #print("_arr_pam",_arr_pam)
                        if len(_arr_pam) < 5:
                            json_bck["code"] = "Err1"
                        else:
                            AppCode = int(_arr_pam[2])
                            _order = _arr_pam[3]
                            _price = int(_arr_pam[4])
                            DB = DBManager()
                            if application.App.Redis_PayOrder.GetOrder(_order):

                            #if interface_order.GetPayFlag(_order,DB) != 0:
                                logging.error("Err_repit")
                                json_bck["code"] = "Err_repit"
                            elif _order != order_no or _price != int(amount):
                                json_bck["code"] = "Err3"  # 回调的订单不是请求的，考虑是 假链接
                            else:
                                PayBackAliClass.Do(AppCode, _passback_params,_order,DB)
                                #self.SetPayOrders(_order)
                                #interface_order.UpdatePayOrder(_order, 1, DB)
                                application.App.Redis_PayOrder.SaveOrder(_order)
                                json_bck["code"] = "SUCCESS"
                            DB.destroy()
                    else:
                        logging.error("WX pay fail")
                        json_bck["code"] = "Err4"

        #22416091436362
        #22416091436362
        #logging.info("wechatpayback = " + json_bck)
        logging.info(f"wx payback -> {json_bck}")
        self.write(returnXml)