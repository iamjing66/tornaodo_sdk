#!/usr/bin/env python
# coding=utf-8

import json
from handlers.kbeServer.XREditor.Response import xr_response_pay
from handlers.kbeServer.Editor.Interface import interface_wit
from handlers.kbeServer.Editor.Data import data_ppackage,data_sis,data_work,data_channel
class pay_pam:

    def __init__(self):
        #支付参数获取
        pass


    def GetPayPam(self,UID,AppCode,PayData,DB):

        json_data = {}

        if AppCode == 1:
            json_data = data_work.PAYPAM_WorkMK(PayData,DB)
            # {"PayType": 2, "AppType": 1, "UID": 9, "UserName": "lyy", "AppCode": 1,
            #  "PayData": {"wid": 4162, "b_uid": 283, "organization": 1, "distributor": 1, "ip": "192.168.0.22"}}
        elif AppCode == 2:
            json_data = data_sis.PAYPAM_SISCourse(PayData,DB)
            # {"PayType": 1, "AppType": 1, "UID": 9, "UserName": "lyy", "AppCode": 2,
            #  "PayData": {"wid": "1010003", "b_uid": 0, "organization": 1, "distributor": 1}}
        elif AppCode == 3:
            json_data = data_channel.PAYPAM_Changxiang(PayData,DB)
            # {"PayType": 1, "AppType": 1, "UID": 9, "UserName": "lyy", "AppCode": 3,
            #  "PayData": {"changel": "1,2,3", "month": 2, "organization": 1, "distributor": 1}}
        elif AppCode == 4:
            json_data = data_ppackage.PAYPAM_VIPANDPPACKAGE(UID,PayData,DB)
            #VIP
            # {"PayType": 2, "AppType": 2, "UID": 9, "UserName": "lyy", "AppCode": 4,
            #  "PayData": {"model": 0, "extra": 3, "organization": 1, "distributor": 1, "ip": "192.168.0.22"}}
            #包裹
            # {"PayType": 2, "AppType": 2, "UID": 9, "UserName": "lyy", "AppCode": 4,
            #  "PayData": {"model": 1, "extra": "0$3", "organization": 1, "distributor": 1, "ip": "192.168.0.22"}}
        elif AppCode == 5:
            json_data = interface_wit.PAYPAM_WitScore(UID,PayData,DB)
            # {"PayType": 1, "AppType": 1, "UID": 9, "UserName": "lyy", "AppCode": 3,
            # "PayData": {"rmb":  2, "organization": 1, "distributor": 1}}
        elif AppCode == 6:
            json_data = data_sis.PAYPAM_ProjectSisData(UID,PayData,DB)
        elif AppCode == 401: #时序版-智慧豆充值
            json_data = xr_response_pay.GetPay_401(UID, PayData, DB)
        elif AppCode == 402:  # 时序版-购买作品
            json_data = xr_response_pay.GetPay_402(UID, PayData, DB)
        elif AppCode == 403:  # 时序版-购买vip
            json_data = xr_response_pay.GetPay_403(UID, PayData, DB)
            #"PayData": {"ptype": 2, "organization": 1, "distributor": 1,"cid": 2,"lid": 2,"wid": 2，"ptype": 2,"ip": localip,"from": "SIS"}

        # 测试用支付价格
        json_data["Data"]["price"] = 1
        return json_data







payPamClass = pay_pam()