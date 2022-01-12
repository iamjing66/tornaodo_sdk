#!/usr/bin/env python
# coding=utf-8

import json
import random
import uuid
import logging

import Global
import application
from handlers.kbeServer.Editor.Interface import interface_account
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from handlers.kbeServer.XREditor.Interface import interface_account as ia


def interface_sendSMS(DB,subCode, uid, username, data,languageStr = "ch"):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    phone = ""
    uname = ""
    if subCode == 0:
        phone = interface_account.GetPhoneBind(DB,username)
        if len(phone) <= 0:
            json_data["code"] = 0  # 未绑定手机号
            json_data["msg"] = "未绑定手机号"
            return json_data
        #uname = username
    elif subCode == 1:  # 手机注册账号
        phone = username
        code = interface_account.GetPhoneRegister(DB,username)
        if code == 1:
            json_data["code"] = 0  # 手机号已注册
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_1",languageStr)
            return json_data
            #uname = username
    elif subCode == 2:  # VR注册账号
        phone = username
        code = interface_account.GetPhoneRegister(DB,username)
        if code == 1:
            json_data["code"] = 0  # 手机号已注册
            json_data["msg"] = "手机号已注册"
            return json_data
            #uname = username
    elif subCode == 33:  # PC端绑定手机号
        phone = interface_account.GetPhoneBind(DB,username)
        if len(phone) > 0:
            json_data["code"] = 0  # 未绑定手机号
            json_data["msg"] = "已绑定手机号"
            return json_data
        phone = data["phone"]
        #uname = username
    elif subCode == 11:  # 后台
        phone = data
    elif subCode == 12:  # 后台
        phone = data
    elif subCode == 401:    #时序版注册
        phone = username
        code = interface_account.GetPhoneRegister(DB, username)
        if code == 1:
            json_data["code"] = 0  # 手机号已注册
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_1",languageStr)
            return json_data
    elif subCode == 402:    #微信登录绑定手机
        phone = username    #手机号未注册，自动注册， 如果注册了，那么直接绑定登录
    elif subCode == 403:    #手机号登录验证码
        phone = username    #手机号未注册，自动注册， 如果注册了，那么直接登录
    elif subCode == 404:    #忘记密码
        phone = username
        code = ia.JugePhoneExist(DB, phone)
        if not code:
            json_data["code"] = 0  # 该手机号未绑定
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_1_15",languageStr)
            return json_data
    else:
        phone = data["phone"]
        #uname = username

    sms_code = ""
    if subCode == 0:
        sms_code = "SMS_169641656"
    elif subCode == 1 or subCode == 401 or subCode == 402 or subCode == 403 or subCode == 404:
        sms_code = "SMS_169641656"
    elif subCode == 2:
        sms_code = "SMS_169641656"
    elif subCode == 33:
        sms_code = "SMS_169641656"
    elif subCode == 11:
        sms_code = "SMS_166779892"
    elif subCode == 12:
        sms_code = "SMS_166779892"
    #print("手机号：", phone)
    phoneCode = RandomCode()
    pamam = "{\"code\":'" + phoneCode + "'}"
    __business_id = uuid.uuid1()
    business_id = "sms" + str(__business_id)
    sign_name = "西安飞蝶"
    smsResponse = send_sms(business_id, phone, sign_name, sms_code, pamam)
    #print("smsResponse", smsResponse)
    json_back = json.loads(smsResponse.decode("utf-8"))
    if json_back["Message"] == "OK":
        json_data["code"] = 1
        json_data["msg"] = phoneCode
        #json_data["phone"] = phone
    else:
        if json_back["Code"] == "isv.MOBILE_NUMBER_ILLEGAL":
            json_data["code"] = -1  # 手机号错误
        elif json_back["Code"] == "isv.BUSINESS_LIMIT_CONTROL":
            json_data["code"] = -2  # 操作频繁
        else:
            json_data["code"] = -3  # 操作频繁
        json_data["msg"] = json_back["Code"]

    logging.info("[phonecode] GetPhone phone = %s , code = %s data = %s"  % (phone,phoneCode,str(json_data)))
    return json_data


def RandomCode():
    str = ""
    for i in range(6):
        code = 2 #random.randrange(3)
        if code == 0:
            # 随机生成一个大写字母
            ch = chr(random.randrange(ord("A"), ord("Z") + 1))
            str += ch
        elif code == 1:
            # 随机生成一个小写字母
            ch = chr(random.randrange(ord("a"), ord("z") + 1))
            str += ch
        elif code == 2:
            # 随机生成一个数字
            ch = chr(random.randrange(ord("0"), ord("9") + 1))
            str += ch
    return str


#发送短信接口
def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):

    #print("send_sms",business_id, phone_numbers, sign_name, template_code, template_param)
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = application.App.acs_client.do_action_with_exception(smsRequest)

    #print("发送成功！")
    # TODO 业务处理

    return smsResponse


#拼接数据发送短信
def SendSms(AppCode,uid,phone,pay_url):

    pay_data = str(AppCode)+"@" + str(uid) + "@" + pay_url
    logging.info("pay_data --> %s" % pay_data)
    pamam = "{\"name\":'" + pay_data + "'}"
    __business_id = uuid.uuid1()
    business_id = "sms" + str(__business_id)
    sign_name = "西安飞蝶"
    smsResponse = send_sms(business_id, phone, sign_name, "SMS_225335134", pamam)
    #print(smsResponse.decode())
    return 1
