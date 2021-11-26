#!/usr/bin/env python
# coding=utf-8


from handlers.base import BaseHandler
from handlers.kbeServer.Editor.Interface import interface_sms
from methods.DBManager import DBManager
import json
import uuid

class SmsPayRequest(BaseHandler):

    def get(self):


        pdata = self.get_argument("str")
        arr_pam = pdata.split('@')
        AppCode = int(arr_pam[0])  # 1-编程作品买看 2-SIS课程购买 3-频道畅享 4-VIP 5-包裹位
        # PayType = int(arr_pam[1])  # 1-支付宝          2-微信
        UID = arr_pam[1]  # UID
        DB = DBManager()
        sql = ""
        sql1 = ""
        Name = ""
        PICPATH = ""
        price = 0
        if AppCode == 1:  # 买看
            # 1@9@62@5457
            p_uid = int(arr_pam[2])
            p_cid = int(arr_pam[3])
            sql = "select t1.`Name`,t1.price2,t2.`PICPATH` from tb_workmarket t1 inner join tb_config_scene t2 on t1.SID = t2.RID AND t1.uid = " + str(p_uid) + " and t1.wid = " + str(p_cid)
        elif AppCode == 2:  # SIS课程
            # 2@9@1010003
            p_cid = arr_pam[2]
            sql = "select `name`,coursePrice,iconName from new_coursedetails where courseId = '" + p_cid + "'"
        elif AppCode == 3:  # 频道包月
            # 3@9@1@1
            #3@1378@1@11001%E6%94%AF%E4%BB%98%E7%95%8C%E9%9D%A2
            #/smspay?str=3@1378@1@11001%E6%94%AF%E4%BB%98%E7%95%8C%E9%9D%A2
            ##3@1378@3@1
            chanelid = int(arr_pam[2])
            #print("chanelid",chanelid)
            monthid = int(arr_pam[3])
            if chanelid in (1,2,3):
                sql = "select t1.`Desc`,t1.Price,t2.`courseUrl` from tb_channel t1 inner join new_coursetype t2 on t1.WID = t2.courseTypeId AND t1.CID = " + str(chanelid)
            else:
                sql = "select t1.`Desc`,t1.Price,t2.`cIconPath` from tb_channel t1 inner join tb_work_type t2 on t1.WID = t2.WID AND t1.CID  = " + str(chanelid)
            sql1 = "select Days,`Discount` from tb_discount where CID = " + str(monthid) + ";"
        print("sql :" , sql)
        print("sql1 :", sql1)
        data = DB.fetchone(sql,None)
        if data:
            Name = data[0]
            price = int(data[1])
            if AppCode == 1:
                PICPATH = "https://createx.oss-cn-beijing.aliyuncs.com/createx_pc/" + data[2]
            elif AppCode == 2:
                PICPATH = "https://createx.oss-accelerate.aliyuncs.com/CourseImage/"+data[2]+".png"
            elif AppCode == 3:
                PICPATH = "https://createx.oss-cn-beijing.aliyuncs.com/createx_pc/" + data[2]
        if AppCode == 3:
            data = DB.fetchone(sql1, None)
            _price3 = 0
            days = 0
            if data:
                days = int(data[0])
                _price3 = float(data[1])
                price = int(int((days / 30)) * price * _price3)
                print("price",price,days,_price3)
        #print(PICPATH)
        sdata = {
            "name":Name,
            "price": price,
            "url":PICPATH,
            "data":pdata,
        }

        self.render("pay1.html",sdata = sdata)
        #self.redirect("/payorder")

#
# class TEstRequest(BaseHandler):
#
#     def get(self):
#
#         print("test 进来了啊！")
#         self.render("pay2.html")



class SmsRequest(BaseHandler):

    def post(self):

        json_back = {}

        #print(self.get_argument("data"))
        #self.SOLR_VERIFY
        # AppCode = 2 & phone = 18740487328 & organization = 0 & distributor = 0 & UID = 9 & UserName = lyy &
        # from=VR & data = 1010004 % 249 % 241

        #paydata = self.SolrData
        self.SOLR_VERIFY
        solrdata = self.SolrData
        print("SmsPost" , solrdata)
        # PayType = int(paydata["PayType"])           #1-支付宝          2-微信
        # AppType = int(paydata["AppType"])           #1-APP支付         2-扫码支付
        UID = solrdata["UID"]                   #UID
        #UserName = self.get_argument("UserName")           #用户名
        AppCode = int(solrdata["AppCode"])          #1-编程作品买看 2-SIS课程购买 3-频道畅享 4-VIP 5-包裹位
        #organization =int(self.get_argument("organization"))
        #distributor = int(self.get_argument("distributor"))
        phone = solrdata["phone"]
        PayData = solrdata["data"]    #支付数据

        pay_data = str(AppCode) + "@" + str(UID) + "@" + PayData
        print("pay_data",pay_data , "phone" ,phone)
        pamam = "{\"name\":'"+pay_data+"'}"
        smsResponse = interface_sms.SendSms(UID,phone, pamam)
        print(smsResponse.decode())

        self.write("ok")



class SendSmsRequest(BaseHandler):

    def set_default_headers(self):
        self.allowMyOrigin()


    def post(self):

        no = self.get_argument("smsNo")
        phone = self.get_argument("phone")
        print("no = ", no)
        print("phone = ", phone)
        # pdata = self.request.body.decode('utf-8')
        # print("pdata = " , pdata)
        # post_data = json.loads(pdata)

        #pdata = {"smsNo":1 , "phone" : "123123123"}

        json_bck = interface_sms.interface_sendSMS(None,int(no),0,"",phone)


        self.write(json_bck)

