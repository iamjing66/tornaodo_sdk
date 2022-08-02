#!/usr/bin/env python
# coding=utf-8

import time
import json

import qrcode
from alipay.aop.api.request.AlipayTradePrecreateRequest import AlipayTradePrecreateRequest

from handlers.base import BaseHandler
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from datetime import datetime
from methods.WechatPay import WeiXinPay
from methods.Wxpay_server_pub import Wxpay_server_pub


class Ali_PayHandler(BaseHandler):

    def get(self):
        # """
        # 设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
        # """
        # alipay_client_config = AlipayClientConfig()
        # alipay_client_config.server_url = "https://openapi.alipay.com/gateway.do"
        # alipay_client_config.app_id = "2021001160668207"
        # alipay_client_config.app_private_key = "MIIEpQIBAAKCAQEAuIdOisWAzBnuE4V93jxgaQgyBrkuMnToGCQGx9Dj2yo/2n8ET3yVWd0As/2phI6aXtYAUHXiS7JkSd2naXVSlgjgtgZ28LSplJdvI4YQfYTfwYg1J9LXRI4zu9h7khk0JGrrVrOW1C7xvmywOyHlJ+V8Wf44MUbjvmojU0OTOEZNV3O9rVx4vxaPCF9RGQtAIKnLQGFwDu+B7Fu37HuxL6gvkd1XQPI8cs8FZDcLMHrYLyr79+MjLZx6phPPL4ZsptOCAPS9ty/6EGSACf4ad27byWHL8iu9LpkWbalAnBSisZJPDcN82Q4AHewJ8k02fkS1B4MGybotpXsga3a+jQIDAQABAoIBAGpVJhBXcTmrs4IySW63sgK0Q0eWjCVtMpU+pV2dZL/VX8hDqzM2okWPUalmgbmuBwyhGrtCwu1F1f6uqJrfjYCBiyO5I+7e3F2Qye1ZgsUhvWKjX6YcHAoYO32CaOqudVqK9iQXBtIsXweRUBgzFv7fgcHF+ZGDvRbryIFhjkM9XIBtGmBT1gnLigVoUWQvuD7rXA6P/Jys29b3EK8UDTe1o0sJUreTNNAlGOLa2AefNvLDYt5fqmYjJ3U9sWJvB+UfHGO+I3EhMxvHWTgXptaZ2jH/0SDRnVKAtQwyTMG9w77NKs5jDaYKCFtsnSTR5zrI0h+mMGEeG0QK1W3Nom0CgYEA6kEWKWhpFXeroavqk1k06Obp0/UYUkHLbw5jmtz70TRUda6WSzv0sFEwqwn++52+eyMbeXRut0SgdgfDiZPLjtnLTmlNBI1WjDKglMVnfASFkEHyURpYT9YMHWmu6RYTzDcwUfyscmdTfFQ3fOWm2NpEZd89aexNSB8JPvXmzDsCgYEAyaiEs2T+FQw6d5EjZby9Fj8urUp1U4n0Ed1w65TVMnzZkOYZn8biR9N8tbCWy3ozqLf2ArcQjTH1+xyl+nVFbctbjngw/DeZXkS7S+OxjudI0ON/be6XOVajjI5Ugaxr+Q19Qx1fw1yMDqeRT6T5osJPCBekOUhnjyD6ycbVG9cCgYEArf173XOcoYJKK4HKcHkQsHBaesEPuID//dO9LZg3PXLVzLbJEMZOfus+77sz9WV7xnAUBwjw9xR07lXj6Xqp9cdUlz/lIZ1tDCLKXNWmgFnHbpdcyNp9f4bnZq1Jafyo5cSUEkFPQIX4X18Z+52DaIvtw5ClR9hoqknLD0WLkGMCgYEAmvVbw15/wDy9UNO+l5cI1eeHPrJQpfkEDBZVhzG/AiTeKnImjpiNmRPyaMthlMo6mBOEf2Gc3mLd2jCRenxS9aOmnzvMqIMw3zeBlTdKYb1oPtwSN693lR/2XTOhzGNqNN8gukoAJGchWMF67/Cdw2v8vwMrtrjkmx+Elziq2dECgYEA4ao+0YAriMbbYCRGvsf8fGIQbe0n0NC4sh4JiFmrsF9BjAWxdu/dYkp5OKFnoYhxyxFEisIQETXa/mD06M68htnQqSWgAlI3z7zUR3nFe6lhUbgwQj0aoUTrYEqr3i1MDvsGv+OdQWzERK/igyiP3p8sW/rPZpU8ztdtnKej3Ig="
        # alipay_client_config.alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuIdOisWAzBnuE4V93jxgaQgyBrkuMnToGCQGx9Dj2yo/2n8ET3yVWd0As/2phI6aXtYAUHXiS7JkSd2naXVSlgjgtgZ28LSplJdvI4YQfYTfwYg1J9LXRI4zu9h7khk0JGrrVrOW1C7xvmywOyHlJ+V8Wf44MUbjvmojU0OTOEZNV3O9rVx4vxaPCF9RGQtAIKnLQGFwDu+B7Fu37HuxL6gvkd1XQPI8cs8FZDcLMHrYLyr79+MjLZx6phPPL4ZsptOCAPS9ty/6EGSACf4ad27byWHL8iu9LpkWbalAnBSisZJPDcN82Q4AHewJ8k02fkS1B4MGybotpXsga3a+jQIDAQAB"
        # alipay_client_config.sign_type = "RSA2"

        orderString = ""

        # """
        # 得到客户端对象。
        # 注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
        # logger参数用于打印日志，不传则不打印，建议传递。
        # """
        # client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        #
        # # SDK已经封装掉了公共参数，这里只需要传入业务参数。以下方法为sdk的model入参方式(model和biz_content同时存在的情况下取biz_content)。
        json_bck = {
                "Code": "OK",
                "ORDERSTR": ""
        }

        pay_type = int(self.get_argument("pay_type"))
        wid = self.get_argument("wid")
        b_uid = int(self.get_argument("b_uid"))
        uid = self.get_argument("uid")
        apptype = int(self.get_argument("apptype"))  # apptype 0-支付宝支付 1-微信支付 2-支付宝扫码支付 3-微信扫码支付
        _ip = self.get_argument("ip")
        # print("pay_type:", type(pay_type))
        # print("AppPay-pay_type:", pay_type)
        # print("AppPay-wid:", wid)
        # print("AppPay-b_uid:", b_uid)
        # print("AppPay-uid:", uid)
        # print("AppPay-apptype:", apptype)
        # print("AppPay-_ip:", _ip)
        sql_str = ""
        # 这里的订单号要动态生成
        if pay_type == 0:
            # wid = 10
            # b_uid = 380
            sql_str = "select ID,price2,`Name` from tb_workmarket where WID = " + str(wid) + " AND UID = " + str(b_uid) + ";"
        elif pay_type == 1:  # SIS教育产品
            # wid产品ID
            # b_uid 0 - 一天 1 - 一年
            # uid
            print("b_uid:", type(b_uid))
            if b_uid == 0 or b_uid == "0":
                sql_str = "select id,coursePrice,`name` from new_coursedetails where courseId = " + wid + ";"
            else:
                sql_str = "select id,courseYearPrice,`name` from new_coursedetails where courseId = " + wid + ";"
        print("sql_str", sql_str)
        self.db_ping
        self.Cur.execute(sql_str)
        self.db.commit()
        data = self.Cur.fetchone()
        _id = 0
        _price2 = 0
        _name = ""
        if data != None and len(data) > 0:
            _id = int(data[0])
            _price2 = int(data[1])
            _name = data[2]
        print("AppPay-_name:", _name)
        print("AppPay-Price:", _price2)
        if _id == 0 or _price2 < 0:
            json_bck["Code"] = "Err"
            self.write(json_bck)
            return

        if _price2 != 0:
            _price2 = _price2 / 10  # 元
            _order = self.Ali_Order
            _order += 1
            self.application.Ali_Order = _order
            # sql_str = "select ali_order from clive where ID = 1;"
            # self.Cur.execute(sql_str)
            # self.db.commit()
            # data = self.Cur.fetchone()
            # if data != None and len(data) > 0:
            #     _order = int(data[0])
            # _order+=1
            # sql_str = "update clive set ali_order = "+str(_order)+" where ID = 1;"
            # self.Cur.execute(sql_str)
            # self.db.commit()
            _now = int(time.time())

            if apptype == 0 or apptype == 2:

                # model = self.ali_model
                # model.subject = _name  # 商品标题
                # _out_trade_no = "Ali" + str(_now) + str(_order)
                # model.out_trade_no = _out_trade_no  # 商家订单编号
                # model.timeout_express = "30m"  # 超时关闭该订单时间
                # model.total_amount = str(_price2)  # 订单总金额
                # _price3 = _price2*100

                model = self.ali_model
                model.subject = _name  # 商品标题
                _out_trade_no = "AliD" + str(_now) + str(_order)
                model.out_trade_no = _out_trade_no  # 商家订单编号
                model.timeout_express = "30m"  # 超时关闭该订单时间
                # model.total_amount = str(100)  # 订单总金额
                model.product_code = "FACE_TO_FACE_PAYMENT"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
                model.format = "JSON"
                model.charset = "utf-8"
                model.total_amount = str(_price2)  # 订单总金额
                _price3 = _price2 * 100

                if apptype == 0:
                    model.product_code = "QUICK_MSECURITY_PAY"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
                else:
                    model.product_code = "FACE_TO_FACE_PAYMENT"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY

                model.passback_params = str(pay_type) + "$" + str(wid) + "$" + str(b_uid) + "$" + str(uid) + "$" + _out_trade_no + "$" + str(_price2) + "$" + str(apptype) + "$" + str(
                    _price3) + "$" + _name
                # 实例化具体API对应的request类, 类名称和接口名称对应, 当前调用接口名称：alipay.trade.app.pay
                if apptype == 0:
                    request = AlipayTradeAppPayRequest(biz_model=model)
                else:
                    request = AlipayTradePrecreateRequest(biz_model=model)
                request.notify_url = "http://www.bestbutfly.com:8082/alipaybck"
                print(model)
                if apptype == 0:
                    response = self.ali_client.sdk_execute(request)
                    orderString = str(response)
                    # print(orderString)
                    json_bck["ORDERSTR"] = orderString
                else:
                    response = self.ali_client.execute(request)
                    json_response = json.loads(response)
                    print("ali response : ", json_response, type(json_response))
                    print("msg : ", json_response["msg"])

                    if json_response["msg"] == "Success":
                        json_bck["ORDERSTR"] = json_response["qr_code"]
                    else:
                        json_bck["ORDERSTR"] = "异常"
            else:
                _out_trade_no = "Wechat" + str(_now) + str(_order)
                _payInst = WeiXinPay()
                _price2 = _price2 * 100
                passback_params = str(pay_type) + "$" + str(wid) + "$" + str(b_uid) + "$" + str(uid) + "$" + _out_trade_no + "$" + str(_price2) + "$" + str(apptype) + "$" + str(_price2) + "$" + _name
                if apptype == 1:
                    _payInst.get_parameter(_out_trade_no, _name, _price2, _ip, passback_params, "http://www.bestbutfly.com:8082/wechatpaybck", "APP")
                else:
                    _payInst.get_parameter(_out_trade_no, _name, _price2, _ip, passback_params, "http://www.bestbutfly.com:8082/wechatpaybck", "NATIVE")
                try:
                    _wbck = _payInst.re_finall()
                    print("_wbck : ", _wbck)
                    if _wbck == "Err":
                        print("Wechat订单创建失败2！:")
                        json_bck["Code"] = "ERR"
                    else:
                        json_bck["ORDERSTR"] = str(_wbck)
                    # print("_wbck , ", _wbck)
                except Exception as e:
                    print("订单创建失败1！:" + str(e))
                    json_bck["Code"] = "ERR"
        else:
            # 无需购买
            if pay_type == 0:  # 编程产品
                sql = "INSERT INTO `tb_work_look`(`UID`,`W_UID`,`W_CID`,`price`)VALUES(" + str(uid) + "," + str(b_uid) + "," + str(wid) + ",0);"
            else:
                courseId = wid
                buytype = b_uid
                userId = uid
                sql = "INSERT INTO `tb_work_look`(`userId`,`buytype`,`courseId`,`price`,`courseBuyTime`)VALUES(" + str(userId) + "," + str(buytype) + "," + str(
                    courseId) + ",0," + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ");"
            print("无需购买:", sql)
            self.Cur.execute(sql)
            self.db.commit()

        self.write(json_bck)


class Ali_PayBckHandler(BaseHandler):

    def post(self):
        """
        支付宝内部支付完成后，异步通知到这个接口，返回支付宝状态，同步到数据库中
        """
        """处理不同得参数，必须返回success"""
        # 我这里是用的Django所以取值使用request.POST,具体怎么取值取决于使用者的框架
        _body = self.request.body_arguments

        _passback_params = self.get_body_argument("passback_params", "")
        # print("_passback_params",_passback_params)

        #         # 1. 商户需要验证该通知数据中的 out_trade_no 是否为商户系统中创建的订单号
        #         # 2. 判断 total_amount 是否确实为该订单的实际金额（即商户订单创建时的金额），
        #         # 3. 校验通知中的 seller_id（或者 seller_email ) 是否为 out_trade_no 这笔单据的对应的操作方（有的时候，一个商户可能有多个seller_id/seller_email）
        #         # 4. 验证 app_id 是否为该商户本身。上述 1、2、3、4有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。在支付宝的业务通知中，只有交易通知状态为 TRADE_SUCCESS 或 TRADE_FINISHED 时，支付宝才会认定为买家付款成功
        #
        #         # 1-4的验证需要自己加
        json_bck = {
                "Code": "OK",
        }

        notify_type = self.get_body_argument('notify_type', "")  # 通知类型
        trade_status = self.get_body_argument('trade_status', "")  # 订单状态
        out_trade_no = self.get_body_argument('out_trade_no', "")  # 订单状态
        total_amount = self.get_body_argument('total_amount', "")  # 订单状态
        # print("notify_type", notify_type)
        # print("trade_status", trade_status)
        # print("out_trade_no", out_trade_no)
        # print("total_amount", total_amount)
        _arr_pam = _passback_params.split('$')
        if len(_arr_pam) != 9:
            json_bck["Code"] = "Err"
        else:
            if _arr_pam[4] != out_trade_no or float(_arr_pam[5]) != float(total_amount):
                json_bck["Code"] = "Err1"  # 回调的订单不是请求的，考虑是 假链接
            else:
                if notify_type == 'trade_status_sync':
                    pay_success = False
                    if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                        pay_success = True
                    if pay_success:
                        # 如果支付成功一定是success这个单词，其他的alipay不认
                        self.db_ping
                        PayBackDo(_arr_pam, total_amount, self.Cur, self.db, self.SolrInst)
                        json_bck["Code"] = "OK"
                else:
                    json_bck["Code"] = "Err2"

        self.write(json_bck)

        # data = self.request.POST.dict()
        # # sign, sign_type 都要从数据中取出，否则签名通不过
        # sign, sign_type = data.pop('sign'), data.pop('sign_type')
        # # 排序
        # params = sorted(data.items(), key=lambda e: e[0], reverse=False)
        # # 拼接成字符串
        # message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()
        # alipay_public_key = settings.alipay_public_key
        # try:
        #     if verify_with_rsa(alipay_public_key.encode('utf-8').decode('utf-8'), message, sign):
        #         # 1. 商户需要验证该通知数据中的 out_trade_no 是否为商户系统中创建的订单号
        #         # 2. 判断 total_amount 是否确实为该订单的实际金额（即商户订单创建时的金额），
        #         # 3. 校验通知中的 seller_id（或者 seller_email ) 是否为 out_trade_no 这笔单据的对应的操作方（有的时候，一个商户可能有多个seller_id/seller_email）
        #         # 4. 验证 app_id 是否为该商户本身。上述 1、2、3、4有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。在支付宝的业务通知中，只有交易通知状态为 TRADE_SUCCESS 或 TRADE_FINISHED 时，支付宝才会认定为买家付款成功
        #
        #         # 1-4的验证需要自己加
        #
        #         notify_type = data['notify_type']  # 通知类型
        #         trade_status = data['trade_status']  # 订单状态
        #         if notify_type == 'trade_status_sync':
        #             pay_success = False
        #             if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
        #                 pay_success = True
        #             if pay_success:
        #                 # 如果支付成功一定是success这个单词，其他的alipay不认
        #                 return 'success'
        #         return 'failure'
        #     else:
        #         return 'failure'
        # except:
        #     return 'failure'


def PayBackDo(_arr_pam, total_amount, Cur, Db, SolrInst):
    _pay_type = int(_arr_pam[0])
    _pay_num = _arr_pam[7]
    UID = 0
    proType = 0
    proName = ""
    supplement = ""
    cName = _arr_pam[8]
    classification = 0

    if _pay_type == 0:  # 编程产品
        wid = int(_arr_pam[1])
        b_uid = int(_arr_pam[2])
        uid = int(_arr_pam[3])
        sql = "INSERT INTO `tb_work_look`(`UID`,`W_UID`,`W_CID`,`price`)VALUES(" + str(uid) + "," + str(b_uid) + "," + str(wid) + "," + total_amount + ");"
        sql1 = "INSERT INTO `tb_pay_log`(`UID`,`PAY_NUM`,`terminal`,`proType`)VALUES(" + str(uid) + "," + str(_pay_num) + ",9,1);"
        UID = uid
        proType = 2
        classification = 2
        proName = "购买作品观看权"
    else:
        courseId = _arr_pam[1]
        buytype = int(_arr_pam[2])
        userId = int(_arr_pam[3])
        sql = "INSERT INTO `buylog`(`userId`,`buytype`,`courseId`,`buyprice`,`courseBuyTime`,`IsNewBuy`)VALUES(" + str(userId) + "," + str(buytype) + "," + str(
            courseId) + "," + total_amount + ",'" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "','1');"
        sql1 = "INSERT INTO `tb_pay_log`(`UID`,`PAY_NUM`,`terminal`,`proType`)VALUES(" + str(userId) + "," + str(_pay_num) + ",10,1);"
        UID = userId
        proType = 3
        classification = 1
        proName = "购买教育中心内容观看权"

    print("sql,", sql)
    print("sql1,", sql1)
    Cur.execute(sql)
    Db.commit()
    Cur.execute(sql1)
    Db.commit()

    sql = "select organization,distributor from tb_userdata where UID = " + str(UID)
    Cur.execute(sql)
    Db.commit()
    data = Cur.fetchone()
    organization = 0
    distributor = 0
    if data != None and len(data) > 0:
        organization = int(data[0])
        distributor = int(data[1])

    if SolrInst != None:
        print("记录手机支付log : ", UID, organization, distributor, proType, proName, _pay_num, cName, classification)
        SolrInst.Log_Cost(UID, organization, distributor, proType, proName, _pay_num, cName, "")


class Wechat_PayBckHandler(BaseHandler):

    def post(self):
        params = self.request.body.decode('utf-8')
        # print("params",params)
        returnXml = ""
        try:
            Wxpay_server_pub(params).xmlToArray()  # 判断是否xml数据格式
        except Exception as e:
            # 其他需求比如 和alipay 支付同一回调地址
            print("Wechat_PayBck Resut:", str(e))
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
                    # print("amount" , amount)
                    # print("order_no", order_no)
                    # print("_passback_params", _passback_params)
                    # print("result_code", result_code)
                    # 时间格式转换
                    # datetime_struct = parser.parse(time_string)
                    # time_paid = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
                    # 返回微信数据
                    wxpay.setReturnParameter("return_code", "SUCCESS")
                    wxpay.setReturnParameter("return_msg", "OK")
                    returnXml = wxpay.returnXml()

                    if result_code == wxpay.SUCCESS:
                        # 根据自己需求码代码
                        # 验证一下订单号，随机码，金额验证
                        _arr_pam = _passback_params.split('$')
                        if len(_arr_pam) != 9:
                            print("支付回调异常，参数长度不足！")
                        else:
                            if _arr_pam[4] != order_no or float(_arr_pam[5]) != float(amount):
                                print("支付回调异常，参数验证未通过！")
                            else:
                                self.db_ping
                                PayBackDo(_arr_pam, amount, self.Cur, self.db, self.SolrInst)
        self.write(returnXml)


#
# class AppPay_Monthly(BaseHandler):
#
#     def get(self):
#
#         json_bck = {
#             "Code": "OK",
#             "ORDERSTR": ""
#         }
#
#         pam = self.get_argument("pam")
#         pam_arr = pam.split('^')
#         _code = int(pam_arr[0])
#
#         channel = pam_arr[1]
#         month = int(pam_arr[2])
#         apptype = int(pam_arr[3])    #apptype 0-支付宝支付 1-微信支付
#         uid = int(pam_arr[4])
#         _ip = pam_arr[5]
#         # print("channel:", channel)
#         # print("month:", month)
#         # print("apptype:", apptype)
#         # print("_ip:", _ip)
#         CIDS = ""
#         sql_str = ""
#         #这里的订单号要动态生成
#         sql_str = "select Price,`Desc`,WTYPE,CID from tb_channel where CID in (" + channel + ");"
#         self.db_ping
#         self.Cur.execute(sql_str)
#         self.db.commit()
#         data = self.Cur.fetchall()
#         _price2 = 0
#         _name = ""
#         _wtype = ""
#         _price_record = ""
#         if data != None and len(data) > 0:
#             list_data = list(data)
#             for minfo in list_data:
#                 if _price_record == "":
#                     _price_record = str(minfo[0])
#                 else:
#                     _price_record = _price_record + "#" + str(minfo[0])
#                 _price2 += int(minfo[0])
#                 if _name == "":
#                     _name = minfo[1]
#                 else:
#                     _name = _name + "#" + minfo[1]
#                 if _wtype == "":
#                     _wtype = str(minfo[2])
#                 else:
#                     _wtype = _wtype + "#" + str(minfo[2])
#                 if CIDS == "":
#                     CIDS = str(minfo[3])
#                 else:
#                     CIDS = CIDS + "#" + str(minfo[3])
#         # print("AppPay-_name:", _name)
#         # print("AppPay-Price:", _price2 )
#         # print("AppPay-_wtype:", _wtype)
#         if _price2 <= 0:
#             json_bck["Code"] = "Not Channel"
#             self.write(json_bck)
#             return
#
#         sql_str = "select Days,`Discount` from tb_discount where CID = " + str(month) + ";"
#         self.Cur.execute(sql_str)
#         self.db.commit()
#         data = self.Cur.fetchone()
#         _price3 = 0
#         days = 0
#         if data != None and len(data) > 0:
#             days = int(data[0])
#             _price3 = float(data[1])
#         # print("AppPay-days:", days)
#         # print("AppPay-_price3:", _price3)
#         if days == 0:
#             json_bck["Code"] = "Not MonthID"
#             self.write(json_bck)
#             return
#         _price = int(int((days/30))*_price2*_price3)
#         if _price < 0:
#             json_bck["Code"] = "Not Price"
#             self.write(json_bck)
#             return
#         # print("AppPay-days:", days)
#         _order = self.Ali_Order
#         _order+=1
#         self.application.Ali_Order = _order
#         _now = int(time.time())
#         _name = ""
#         if apptype == 0:
#             model = self.ali_model
#             model.subject = "频道畅享"  # 商品标题
#             _out_trade_no = "AliB" + str(_now) + str(_order)
#             model.out_trade_no = _out_trade_no  # 商家订单编号
#             model.timeout_express = "30m"  # 超时关闭该订单时间
#             _price_a = _price/100
#             model.total_amount = str(_price_a)  # 订单总金额
#             model.product_code = "QUICK_MSECURITY_PAY"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
#             model.passback_params = str(channel) + "$"+str(month) + "$"+str(apptype)+"$"+str(_price_a)+ "$"+_name+"$"+_out_trade_no +"$"+str(_wtype)+"$"+str(uid) + "$" + _price_record+"$"+str(_price)
#             # 实例化具体API对应的request类, 类名称和接口名称对应, 当前调用接口名称：alipay.trade.app.pay
#             request = AlipayTradeAppPayRequest(biz_model=model)
#             request.notify_url = "http://www.bestbutfly.com:8082/monthpaybck"
#
#             try:
#                 response = self.ali_client.sdk_execute(request)
#                 orderString = str(response)
#                 #print(orderString)
#                 json_bck["ORDERSTR"] = orderString
#                 # orderString = response.getBody()
#                 # print("orderString", orderString)
#             except Exception as e:
#                 print("订单创建失败！:" + str(e))
#                 json_bck["Code"] = "ERR"
#         else:
#             _out_trade_no = "WechatB" + str(_now) + str(_order)
#             _payInst = WeiXinPay()
#             #_price = _price*100
#             _price_a = _price
#             passback_params = str(channel) + "$"+str(month) + "$"+str(apptype)+"$"+str(_price_a)+ "$"+_name+"$"+_out_trade_no+"$"+str(_wtype)+"$"+str(uid) + "$" + _price_record+"$"+str(_price_a)
#             _payInst.get_parameter(_out_trade_no,"频道畅享",_price_a,_ip,passback_params,"http://www.bestbutfly.com:8082/wxmonthpaybck","APP")
#             try:
#                 _wbck = _payInst.re_finall()
#                 if _wbck == "Err":
#                     print("Wechat订单创建失败2！:")
#                     json_bck["Code"] = "ERR"
#                 else:
#                     json_bck["ORDERSTR"] = str(_wbck)
#                 print("_wbck , ", _wbck)
#             except Exception as e:
#                 print("订单创建失败1！:" + str(e))
#                 json_bck["Code"] = "ERR"
#
#
#         self.write(json_bck)

class Ali_MonthPayBckHandler(BaseHandler):

    def post(self):
        """
        支付宝内部支付完成后，异步通知到这个接口，返回支付宝状态，同步到数据库中
        """
        """处理不同得参数，必须返回success"""
        # 我这里是用的Django所以取值使用request.POST,具体怎么取值取决于使用者的框架
        _body = self.request.body_arguments

        _passback_params = self.get_body_argument("passback_params", "")
        print("_passback_params", _passback_params)

        #         # 1. 商户需要验证该通知数据中的 out_trade_no 是否为商户系统中创建的订单号
        #         # 2. 判断 total_amount 是否确实为该订单的实际金额（即商户订单创建时的金额），
        #         # 3. 校验通知中的 seller_id（或者 seller_email ) 是否为 out_trade_no 这笔单据的对应的操作方（有的时候，一个商户可能有多个seller_id/seller_email）
        #         # 4. 验证 app_id 是否为该商户本身。上述 1、2、3、4有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。在支付宝的业务通知中，只有交易通知状态为 TRADE_SUCCESS 或 TRADE_FINISHED 时，支付宝才会认定为买家付款成功
        #
        #         # 1-4的验证需要自己加
        json_bck = {
                "Code": "OK",
        }

        notify_type = self.get_body_argument('notify_type', "")  # 通知类型
        trade_status = self.get_body_argument('trade_status', "")  # 订单状态
        out_trade_no = self.get_body_argument('out_trade_no', "")  # 订单状态
        total_amount = self.get_body_argument('total_amount', "")  # 订单状态
        # print("notify_type", notify_type)
        # print("trade_status", trade_status)
        # print("out_trade_no", out_trade_no)
        # print("total_amount", total_amount)
        _arr_pam = _passback_params.split('$')
        if len(_arr_pam) != 8:
            json_bck["Code"] = "Err"
        else:
            if _arr_pam[5] != out_trade_no or float(_arr_pam[3]) != float(total_amount):
                json_bck["Code"] = "Err1"  # 回调的订单不是请求的，考虑是 假链接
            else:
                if notify_type == 'trade_status_sync':
                    pay_success = False
                    if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                        pay_success = True
                    if pay_success:
                        # 如果支付成功一定是success这个单词，其他的alipay不认
                        self.db_ping
                        MonthPayBackDo(_arr_pam, total_amount, self.Cur, self.db, self.SolrInst)
                        json_bck["Code"] = "OK"
                else:
                    json_bck["Code"] = "Err2"

        self.write(json_bck)


class Wechat_MonthPayBckHandler(BaseHandler):

    def post(self):
        params = self.request.body.decode('utf-8')
        print("params", params)
        returnXml = ""
        try:
            Wxpay_server_pub(params).xmlToArray()  # 判断是否xml数据格式
        except Exception as e:
            # 其他需求比如 和alipay 支付同一回调地址
            print("Wechat_PayBck Resut:", str(e))
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
                    # print("amount", amount)
                    # print("order_no", order_no)
                    # print("_passback_params", _passback_params)
                    # print("result_code", result_code)
                    # 时间格式转换
                    # datetime_struct = parser.parse(time_string)
                    # time_paid = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
                    # 返回微信数据
                    wxpay.setReturnParameter("return_code", "SUCCESS")
                    wxpay.setReturnParameter("return_msg", "OK")
                    returnXml = wxpay.returnXml()

                    if result_code == wxpay.SUCCESS:
                        # 根据自己需求码代码
                        # 验证一下订单号，随机码，金额验证
                        _arr_pam = _passback_params.split('$')
                        if len(_arr_pam) != 10:
                            print("支付回调异常，参数长度不足！")
                        else:
                            if _arr_pam[5] != order_no or float(_arr_pam[3]) != float(amount):
                                print("支付回调异常，参数验证未通过！")
                            else:
                                self.db_ping
                                MonthPayBackDo(_arr_pam, amount, self.Cur, self.db, self.SolrInst)
        self.write(returnXml)


def MonthPayBackDo(_arr_pam, total_amount, Cur, Db, SolrInst):
    # str(channel) + "$"+str(month) + "$"+str(apptype)+"$"+str(_price)+ "$"+_name+"$"+_out_trade_no
    channel = _arr_pam[0]
    month = int(_arr_pam[1])
    apptype = int(_arr_pam[2])
    _pay_num = int(_arr_pam[3])
    _pay_type = _arr_pam[6]
    UID = int(_arr_pam[7])
    _price_s = _arr_pam[8]
    _price_pay = int(_arr_pam[9])
    proType = 0
    proName = ""
    supplement = ""
    cName = _arr_pam[4]
    classification = 0

    sql = "select organization,distributor from tb_userdata where UID = " + str(UID)
    Cur.execute(sql)
    Db.commit()
    data = Cur.fetchone()
    organization = 0
    distributor = 0
    if data != None and len(data) > 0:
        organization = int(data[0])
        distributor = int(data[1])

    _channel_arr = channel.split('#')
    _paytype_arr = _pay_type.split('#')
    _price_arr = _price_s.split('#')
    # _name_arr = cName.split('#')
    # print("_channel_arr",_channel_arr)
    # print("_paytype_arr", _paytype_arr)
    # print("_price_arr", _price_arr)
    # print("_name_arr", _name_arr)
    _pos = 0
    for channel_id in _channel_arr:
        _pay_type = _paytype_arr[_pos]
        _paynum = _price_arr[_pos]
        # cName = _name_arr[_pos]
        if _pay_type == 1:  # 编程产品
            proType = 4
            classification = 2
            proName = "作品频道包月"
        else:
            proType = 5
            classification = 1
            proName = "教育中心频道包月"

        sql = "Insert Into tb_channel_log (CID,DID,UID,PRICE,APPTYPE) values (" + channel_id + "," + str(month) + "," + str(UID) + "," + str(_pay_num) + "," + str(apptype) + ");"
        Cur.execute(sql)
        Db.commit()

        if SolrInst != None:
            print("记录手机支付log : ", UID, organization, distributor, proType, proName, _price_pay, channel_id, classification)
            SolrInst.Log_Cost(UID, organization, distributor, proType, proName, _price_pay, "频道[" + channel_id + "]包月", channel_id)

        _pos += 1


class CxNative_Pay(BaseHandler):

    def get(self):

        json_bck = {
                "Code": "OK",
                "ORDERSTR": ""
        }

        # 扫码支付 - 参数
        model = int(self.get_argument("model"))  # 0-VIP升级/续费 1-工程拓展位
        apptype = int(self.get_argument("paytype"))  # 0-微信 1-支付宝
        uid = int(self.get_argument("uid"))  # UID
        ip = self.get_argument("ip")  # IP本地
        extra = self.get_argument("extra")  # vip购买 表示购买的期限 存储位0-表示新购 其他-表示续费
        # vip
        b_date = 0
        # 存储位
        b_id = 0
        b_num = 0
        if model == 0:
            b_date = int(extra)
        elif model == 1:
            _arr = extra.split('$')
            b_id = int(_arr[0])
            b_num = int(_arr[1])

        bagID = 0
        pdate = 0
        # 验证下参数
        sql = ""
        if model == 0:
            sql = "select VIPDATE FROM Tb_Userdata where uid = " + str(uid)
        else:
            if b_id != 0:
                sql = "select ENDDATE,ID FROM TB_BAG where ID = " + str(b_id)
        self.db_ping
        if sql != "":
            self.Cur.execute(sql)
            self.db.commit()
            data = self.Cur.fetchone()
            if data != None and len(data) > 0:
                _pam = int(data[0])
                if model == 0:
                    if _pam == 1:
                        json_bck["Code"] = "Err"
                        json_bck["ORDERSTR"] = "永久VIP,无需续费"
                        print("永久VIP,无需续费")
                        self.write(json_bck)
                        return
                    pdate = _pam
                else:
                    if extra != 0:
                        if _pam == 1:
                            json_bck["Code"] = "Err"
                            json_bck["ORDERSTR"] = "永久包裹位,无需续费"
                            print("永久VIP,无需续费")
                            self.write(json_bck)
                            return
                        bagID = int(data[1])
                        pdate = _pam
        # 计算价格
        price = 0  # 分为单位
        sql = "select VIPPrice,WorksAPrice,(select DiscountRate from tb_new_vipdiscount where ThePurchaseTime = " + str(b_date) + ") as rate from tb_new_config;"
        self.Cur.execute(sql)
        self.db.commit()
        data = self.Cur.fetchone()
        _id = 0
        _price2 = 0
        _name = ""
        if data != None and len(data) > 0:
            print("data", data)
            if model == 0:
                price = int(data[0] * data[2] * b_date)
            else:
                price = int(data[1]) * b_num
        print("price:", price)
        if price <= 0:
            json_bck["Code"] = "Err"
            json_bck["ORDERSTR"] = "价格异常"
        else:

            # 这里的订单号要动态生成
            _order = self.Ali_Order
            _order += 1
            self.application.Ali_Order = _order
            _now = int(time.time())
            if model == 0:
                _name = "VIP开通/续费"
            else:
                _name = "包裹位"

            if apptype == 1:

                # 支付宝-扫码
                alimodel = self.ali_model
                alimodel.subject = _name  # 商品标题
                _out_trade_no = "AliD" + str(_now) + str(_order)
                alimodel.out_trade_no = _out_trade_no  # 商家订单编号
                alimodel.timeout_express = "30m"  # 超时关闭该订单时间
                alimodel.total_amount = str(price / 100)  # 订单总金额
                alimodel.product_code = "FACE_TO_FACE_PAYMENT"  # 销售产品码，商家和支付宝签约的产品码，为固定值QUICK_MSECURITY_PAY
                _passback_params = str(uid) + "*" + str(price) + "*" + str(model) + "*" + str(apptype) + "*" + str(extra) + "*" + _out_trade_no + "*" + str(bagID) + "*" + str(pdate)
                alimodel.format = "JSON"
                alimodel.charset = "utf-8"
                self.RecodeOrder_ALI(_out_trade_no, _passback_params)
                # 实例化具体API对应的request类, 类名称和接口名称对应, 当前调用接口名称：alipay.trade.app.pay
                # request = AlipayTradeAppPayRequest(biz_model=model)
                request = AlipayTradePrecreateRequest(biz_model=alimodel)
                request.notify_url = "http://www.bestbutfly.com:8082/smalipaybck"

                try:
                    response = self.ali_client.execute(request)
                    json_response = json.loads(response)
                    print("ali response : ", json_response, type(json_response))
                    print("msg : ", json_response["msg"])

                    if json_response["msg"] == "Success":
                        json_bck["ORDERSTR"] = json_response["qr_code"]
                    else:
                        print("订单创建失败！:" + json_response["msg"] + " Code :" + json_response["code"])
                        json_bck["Code"] = "ERR"
                    # json_bck["ORDERSTR"] = orderString

                    # orderString = response.getBody()

                    # print("orderString", orderString)

                except Exception as e:
                    print("订单创建失败！:" + str(e))
                    json_bck["Code_ALI"] = "ERR"
            else:

                # 微信-扫码
                _out_trade_no = "WechatC" + str(_now) + str(_order)
                _payInst = WeiXinPay()
                passback_params = str(uid) + "*" + str(price) + "*" + str(model) + "*" + str(apptype) + "*" + str(extra) + "*" + _out_trade_no + "*" + str(bagID) + "*" + str(pdate)
                _payInst.get_parameter(_out_trade_no, _name, price, ip, passback_params, "http://www.bestbutfly.com:8082/smwechatpaybck", "NATIVE")
                try:
                    _wbck = _payInst.re_finall()
                    if _wbck == "Err":
                        print("Wechat订单创建失败2！:")
                        json_bck["Code"] = "ERR"
                    else:
                        json_bck["ORDERSTR"] = _wbck
                    print("_wbck , ", _wbck)
                except Exception as e:
                    print("订单创建失败1！:" + str(e))
                    json_bck["Code"] = "ERR"

        self.write(json_bck)

    def CreateQRCode(self, code_url, file):

        img = qrcode.make(code_url)
        # 写入文件
        with open(file, 'wb') as f:
            img.save(f)


class CxNative_WechatPayBck(BaseHandler):

    def post(self):
        params = self.request.body.decode('utf-8')
        # print("params",params)
        returnXml = ""
        try:
            Wxpay_server_pub(params).xmlToArray()  # 判断是否xml数据格式
        except Exception as e:
            # 其他需求比如 和alipay 支付同一回调地址
            print("Wechat_PayBck Resut:", str(e))
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
                    # print("amount" , amount)
                    # print("order_no", order_no)
                    # print("_passback_params", _passback_params)
                    # print("result_code", result_code)
                    # 时间格式转换
                    # datetime_struct = parser.parse(time_string)
                    # time_paid = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
                    # 返回微信数据
                    wxpay.setReturnParameter("return_code", "SUCCESS")
                    wxpay.setReturnParameter("return_msg", "OK")
                    returnXml = wxpay.returnXml()

                    if result_code == wxpay.SUCCESS:
                        # 根据自己需求码代码
                        print("支付成功")
                        # 验证一下订单号，随机码，金额验证
                        _arr_pam = _passback_params.split('*')
                        # str(uid)+"$"+str(price)+"$"+str(model)+"$"+str(apptype)+"$"+str(extra)+ "$" + _out_trade_no
                        # UID 价格(分) 类型(0-VIP 1-拓展包裹) 支付类型(0-微信 1-支付宝) 期限(VIP购买有) 订单号
                        if _arr_pam[5] != order_no or float(_arr_pam[1]) != float(amount):
                            print("支付回调异常，参数验证未通过！")
                        else:
                            self.db_ping
                            SMPayBackDo(_arr_pam, amount, self.Cur, self.db, self.SolrInst)
        self.write(returnXml)


class CxNative_AliPayBck(BaseHandler):

    def post(self):
        """
               支付宝内部支付完成后，异步通知到这个接口，返回支付宝状态，同步到数据库中
               """
        """处理不同得参数，必须返回success"""
        # 我这里是用的Django所以取值使用request.POST,具体怎么取值取决于使用者的框架
        _body = self.request.body_arguments

        #         # 1. 商户需要验证该通知数据中的 out_trade_no 是否为商户系统中创建的订单号
        #         # 2. 判断 total_amount 是否确实为该订单的实际金额（即商户订单创建时的金额），
        #         # 3. 校验通知中的 seller_id（或者 seller_email ) 是否为 out_trade_no 这笔单据的对应的操作方（有的时候，一个商户可能有多个seller_id/seller_email）
        #         # 4. 验证 app_id 是否为该商户本身。上述 1、2、3、4有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。在支付宝的业务通知中，只有交易通知状态为 TRADE_SUCCESS 或 TRADE_FINISHED 时，支付宝才会认定为买家付款成功
        #
        #         # 1-4的验证需要自己加
        json_bck = {
                "Code": "OK",
        }

        notify_type = self.get_body_argument('notify_type', "")  # 通知类型
        trade_status = self.get_body_argument('trade_status', "")  # 订单状态
        out_trade_no = self.get_body_argument('out_trade_no', "")  # 订单状态
        total_amount = self.get_body_argument('total_amount', "")  # 订单状态

        _passback_params = self.GetOrder_ALI(out_trade_no)
        print("_passback_params", _passback_params)
        if _passback_params == None and len(_passback_params) < 1:
            json_bck["Code"] = "Err2"
        else:
            _arr_pam = _passback_params.split('*')
            # str(uid)+"$"+str(price)+"$"+str(model)+"$"+str(apptype)+"$"+str(extra)+ "$" + _out_trade_no
            # UID 价格(分) 类型(0-VIP 1-拓展包裹) 支付类型(0-微信 1-支付宝) 期限(VIP购买有) 订单号
            if notify_type == 'trade_status_sync':
                pay_success = False
                if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                    pay_success = True
                if pay_success:
                    # 如果支付成功一定是success这个单词，其他的alipay不认
                    self.db_ping
                    SMPayBackDo(_arr_pam, total_amount, self.Cur, self.db, self.SolrInst)
                    json_bck["Code"] = "OK"
            else:
                json_bck["Code"] = "Err2"

        self.write(json_bck)


def SMPayBackDo(_arr_pam, total_amount, Cur, Db, SolrInst):
    # str(uid)+"$"+str(price)+"$"+str(model)+"$"+str(apptype)+"$"+str(extra)+ "$" + _out_trade_no
    # UID 价格(分) 类型(0-VIP 1-拓展包裹) 支付类型(0-微信 1-支付宝) 期限(VIP购买有) 订单号
    uid = int(_arr_pam[0])
    price = int(_arr_pam[1])
    model = int(_arr_pam[2])
    pam_apptype = int(_arr_pam[3])
    extra = _arr_pam[4]
    _out_trade_no = _arr_pam[5]
    _bagid = int(_arr_pam[6])
    _pdate = int(_arr_pam[7])
    # 64*10*1*0*0$1*WechatC16062229482*0*0
    # vip
    b_date = 0
    # 存储位
    b_id = 0
    b_num = 0
    if model == 0:
        b_date = int(extra)
    elif model == 1:
        _arr = extra.split('$')
        b_id = int(_arr[0])
        b_num = int(_arr[1])

    proType = 0
    proName = ""
    supplement = ""
    cName = ""
    classification = 0

    sql = "select organization,distributor from tb_userdata where UID = " + str(uid)
    Cur.execute(sql)
    Db.commit()
    data = Cur.fetchone()
    organization = 0
    distributor = 0
    if data != None and len(data) > 0:
        organization = int(data[0])
        distributor = int(data[1])
    else:
        print("账号不存在。")
        return

    cdata = ""
    if model == 0:
        proType = 6
        proName = "VIP购买"
        supplement = "VIP购买(一年)"
        cName = "vip"
        if _pdate < int(time.time()):
            _pdate = int(time.time())
        _date = _pdate + b_date * 30 * 86400
        sql = "update tb_userdata set VIPPOWER = 2,VIPDATE = " + str(_date) + " where UID = " + str(uid)
        Cur.execute(sql)
        Db.commit()
        cdata = str(_date)
        InsertSyncData("editor", 101, cdata, 0, 1, uid, Cur, Db)
    else:
        proType = 7
        proName = "包裹位购买"
        supplement = "包裹位购买(一年)"
        cName = "包裹位"
        if _bagid == 0:
            _date = int(time.time()) + 31536000
            sql1 = "INSERT INTO tb_bag (UID,ENDDATE) VALUES (" + str(uid) + "," + str(_date) + ");"
            sql = "select last_insert_id();"
            for i in range(b_num):

                Cur.execute(sql1)
                Db.commit()

                Cur.execute(sql)
                Db.commit()
                data = Cur.fetchone()
                if data != None and len(data) > 0:
                    if cdata == "":
                        cdata = str(data[0]) + "$" + str(_date)
                    else:
                        cdata = cdata + "@" + str(data[0]) + "$" + str(_date)
            InsertSyncData("editor", 102, cdata, 0, 1, uid, Cur, Db)
        else:
            if _pdate < int(time.time()):
                _pdate = int(time.time())
            _date = _pdate + 31536000
            sql = "update tb_bag set ENDDATE = " + str(_date) + " where uid = " + str(uid) + " AND ID = " + str(_bagid) + ";"
            Cur.execute(sql)
            Db.commit()
            cdata = str(_bagid) + "$" + str(_date)
            InsertSyncData("editor", 102, cdata, 0, 1, uid, Cur, Db)

    # 订单记录
    sql = "Insert Into tb_saomazhifu (model,uid,paytype,price,`desc`,`Order`) values (" + str(model) + "," + str(uid) + "," + str(pam_apptype) + "," + str(price) + ",'" + str(
        extra) + "','" + _out_trade_no + "');"
    Cur.execute(sql)
    Db.commit()

    if model == 0:
        sql = "update tb_userdata set AccountPower = 1, EndDate = 1 where uid = " + str(uid) + ";"
        Cur.execute(sql)
        Db.commit()

    # 日志记录
    if SolrInst != None:
        print("扫码支付日志记录 : ", uid, organization, distributor, proType, proName, price, model, pam_apptype)
        SolrInst.Log_Cost(uid, organization, distributor, proType, proName, price, supplement, cName)


def InsertSyncData(pam_apptype, code, pam, doserver, doclient, uid, Cur, Db):
    _now = int(time.time())
    sql = "INSERT INTO TB_DATAQUEUE ( `APPTYPE`,`CODE`,BODY,DOSERVER,DOCLIENT,UID,CDATE ) VALUES ('" + str(pam_apptype) + "'," + str(code) + ",'" + pam + "'," + str(doserver) + "," + str(
        doclient) + "," + str(uid) + "," + str(_now) + ")"
    print("sql,", sql)
    Cur.execute(sql)
    Db.commit()
