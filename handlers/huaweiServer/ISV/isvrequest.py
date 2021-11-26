#!/usr/bin/env python
# coding=utf-8
import time

from handlers.base import BaseHandler
import Global,json
import logging
from handlers.huaweiServer.ISV import AESCBC
from methods.DBManager import DBManager

class ISVHandler(BaseHandler):


    def get(self):

        cryBody = {

        }

        #activity 新购(newInstance) 续费(refresshInstance) 过期(expireInstance) 释放(releaseInstance)
        activity = self.get_argument("activity", "")

        print("activity = ", activity)

        if activity == "newInstance": #新购
            cryBody = self.ISV_NewInstance()
        elif activity == "refreshInstance": #续费
            cryBody = self.ISV_refresshInstance()
        elif activity == "expireInstance": #过期
            cryBody = self.ISV_expireInstance()
        elif activity == "releaseInstance": #释放
            cryBody = self.ISV_releaseInstance()


        encryptBody = self.generateResponseBodySignature(Global.Global_IsvKey, json.dumps(cryBody))
        print("instanceId = ", encryptBody)
        print("cryBody = " , cryBody)
        self.set_header("Body-Sign", "sign_type=\"HMAC-SHA256\",signature=\"" + encryptBody + "\"")

        self.write(cryBody)




    def getArgument(self,Torken_param,key):

        if key not in Torken_param.keys():
            return ""
        return Torken_param[key]

    def timeC(self,edate):
        #edate = "20220929141257"
        sdate = edate[0:4] + "-" + edate[4:6] + "-" + edate[6:8] + " " + edate[8:10] + ":" + edate[10:12] + ":" + edate[12:14]
        print("sdate = ", sdate)
        timeArray = time.strptime(sdate, "%Y-%m-%d %H:%M:%S")
        print(timeArray)
        stime = time.mktime(timeArray)
        return int(stime)


    def ISV_NewInstance(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
            "instanceId": "d5d00dab-186e-478d-a7f2-c6743842f48f",
            "encryptType": "2",
            "appInfo": {
                #"frontEndUrl": "http://www.isvserver.com",
                "adminUrl": "http://www. isvserver.com",
                # "userName": encrypt_text1,
                # "password": "7Bx4DyX7980a59T0qbhnpfhCz82Uc5cZQQtExg=="
            }
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:
            # businessId 云市场业务ID。每一次请求，businessId皆不一致
            businessId = self.getArgument(Torken_param,"businessId")
            # customerId 客户在华为云注册账号的唯一标识
            customerId = self.getArgument(Torken_param,"customerId")
            # customerName 客户在华为云注册的账户名
            customerName = self.getArgument(Torken_param,"customerName")
            # email 客户邮箱。非必传
            email = self.getArgument(Torken_param,"email")
            if len(email) > 0:
                email = AESCBC.DecryptDeveloment(Global.Global_IsvKey, email[0:16], email[16:len(email)])
            # mobilePhone 客户手机号，非必传
            mobilePhone = self.getArgument(Torken_param,"mobilePhone")
            if len(mobilePhone) > 0:
                mobilePhone = AESCBC.DecryptDeveloment(Global.Global_IsvKey, mobilePhone[0:16],
                                                       mobilePhone[16:len(mobilePhone)])
            # orderAmount 订单金额
            orderAmount = self.getArgument(Torken_param,"orderAmount")
            # periodNumber 周期数量
            periodNumber = self.getArgument(Torken_param,"periodNumber")
            # periodType 周期类型
            periodType = self.getArgument(Torken_param,"periodType")
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            productId = self.getArgument(Torken_param,"productId")
            # provisionType 商品实例开通方式。
            provisionType = self.getArgument(Torken_param,"provisionType")
            # testFlag 是否为调试请求
            testFlag = self.getArgument(Torken_param,"testFlag")
            # timeStamp 时间戳
            timeStamp = self.getArgument(Torken_param,"timeStamp")
            # userId 客户以IAM用户认证方式登录时对应子用户的唯一标识。
            userId = self.getArgument(Torken_param,"userId")
            # userName 客户以IAM用户认证方式登录的用户名。
            userName = self.getArgument(Torken_param,"userName")
            expireTime = self.getArgument(Torken_param,"expireTime")
            amount = self.getArgument(Torken_param, "amount")
            logging.info("ISV[NewInstance],businessId=" + businessId + "\n" +
                         ",customerId=" + customerId + "\n" +
                         ",customerName=" + customerName + "\n" +
                         ",email=" + email + "\n" +
                         ",mobilePhone=" + mobilePhone + "\n" +
                         ",orderAmount=" + orderAmount + "\n" +
                         ",periodNumber=" + periodNumber + "\n" +
                         ",periodType=" + periodType + "\n" +
                         ",productId=" + productId + "\n" +
                         ",provisionType=" + provisionType + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp + "\n" +
                         ",userId=" + userId + "\n" +
                         ",expireTime=" + expireTime + "\n" +
                         ",amount=" + amount + "\n" +
                         ",userName=" + userName
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "select 1 from isv_newinstance where businessId = '"+businessId+"' and sf_flag = 0 limit 1;"  #未被释放的实例才可以计算
            data = DB.fetchone(sql,None)
            if data:
                logging.info("[isv_newinstance] 订单已经处理！")
            else:

                # SAAS 服务时间
                #periodType
                #periodNumber
                timelong = 0
                if periodType == "year":    #年服务费
                    timelong = self.timeC(expireTime)


                    sql = "INSERT INTO `isv_newinstance` (`businessId`,`customerId`,`customerName`,`email`,`mobilePhone`,`orderAmount`,`periodNumber`,`periodType`,`productId`,`provisionType`,`testFlag`,`timeStamp`,`userId`,`userName`,`isvend`,`amount`)VALUES(" \
                          "'" + businessId + "'," \
                          "'" + customerId + "'," \
                            "'" + customerName + "'," \
                           "'" + email + "'," \
                           "'" + mobilePhone + "'," \
                           "'" + orderAmount + "'," \
                          "'" + periodNumber + "'," \
                           "'" + periodType + "'," \
                           "'" + productId + "'," \
                           "'" + provisionType + "'," \
                            "'" + testFlag + "'," \
                            "'" + timeStamp + "'," \
                            "'" + userId + "'," \
                            "'" + userName + "'," \
                             "'" + str(timelong) + "'," \
                            "'" + str(amount) + "'" \
                          + ");"
                    data = DB.edit(sql, None)
                    DB.close()
                    if not data:
                        cryBody["resultCode"] = "000005"
                        cryBody["resultMsg"] = "服务商新购存储失败。"
                    else:

                        # 封装-业务处理
                        logging.info("ISV-新购业务")

                else:
                    logging.info("[isv_newinstance]只支持包周期类型")




            # 封装-业务加密
            userName = self.getArgument(Torken_param,"userName")
            if len(userName) > 0:
                print("userName = ", userName)
                iv = self.ISV_IVGet
                print("iv = ", iv)
                encontent = AESCBC.EncryptDeveloment(Global.Global_IsvKey, userName, iv)
                print("fdtest 加密后 = ", encontent)
                encrypt_text1 = iv + encontent
                # 解密
                # decontent = AESCBC.DecryptDeveloment(Global.Global_IsvKey,userName,iv,encontent)
                # print(encontent , " 解密后 = ", decontent)

                # 封装-测试业务加密
                cryBody["appInfo"]["userName"] = encrypt_text1

                # 加密密码
                iv = self.ISV_IVGet
                encrypt_password = iv + AESCBC.EncryptDeveloment(Global.Global_IsvKey, "123456", iv)
                cryBody["appInfo"]["password"] = encrypt_password

        # 封装-消息签名
        cryBody["instanceId"] = businessId
        #cryBody["appInfo"]["frontEndUrl"] = "http://platform.3dbutfly.com"
        cryBody["appInfo"]["adminUrl"] = "http://platform.3dbutfly.com"



        return cryBody



    #续费
    def ISV_refresshInstance(self):
        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            # expireTime=20210930174148&
            # instanceId=huaiweitest123456&
            # orderAmount=100&
            # orderId=CS1906666666ABCDE&
            # periodNumber=1&
            # periodType=year&
            # productId=00301-666666-0--0&
            # testFlag=1&
            # timeStamp=20210927095241549

            # orderAmount 订单金额
            orderAmount = self.getArgument(Torken_param,"orderAmount")
            # periodNumber 周期数量
            periodNumber = self.getArgument(Torken_param,"periodNumber")
            # periodType 周期类型
            periodType = self.getArgument(Torken_param,"periodType")
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            productId = self.getArgument(Torken_param,"productId")
            # provisionType 商品实例开通方式。
            instanceId = self.getArgument(Torken_param,"instanceId")
            # testFlag 是否为调试请求
            testFlag = self.getArgument(Torken_param,"testFlag")
            # timeStamp 时间戳
            timeStamp = self.getArgument(Torken_param,"timeStamp")
            # userId 客户以IAM用户认证方式登录时对应子用户的唯一标识。
            orderId = self.getArgument(Torken_param,"orderId")
            # userName 客户以IAM用户认证方式登录的用户名。
            expireTime = self.getArgument(Torken_param,"expireTime")

            logging.info("ISV[refresshInstance],orderId=" + orderId + "\n" +
                         ",expireTime=" + expireTime + "\n" +
                         ",orderAmount=" + orderAmount + "\n" +
                         ",periodNumber=" + periodNumber + "\n" +
                         ",periodType=" + periodType + "\n" +
                         ",productId=" + productId + "\n" +
                         ",instanceId=" + instanceId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务续费存储
            DB = DBManager()
            sql = "select 1 from isv_newinstance where businessId = '" + instanceId + "' and sf_flag = 0 limit 1;"  # 未被释放的实例才可以计算
            data = DB.fetchone(sql, None)
            if data:
                logging.info("[ISV_refresshInstance] 处理续费订单！")

                isv_end = self.timeC(expireTime)
                sql = "update isv_newinstance set isvend = " + str(isv_end) + " where businessId = '" + instanceId + "' and sf_flag = 0"
                data = DB.edit(sql,None)
                if data:
                    # 封装-业务处理
                    logging.info("ISV-续费业务")

                else:
                    cryBody["resultCode"] = "000005"
                    cryBody["resultMsg"] = "续费写入失败！(" + instanceId + ")"


            else:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "该订单未找到！("+instanceId+")"

            DB.close()


        return cryBody


    #冻结
    def ISV_expireInstance(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            # activity=expireInstance&
            # instanceId=huaiweitest123456&
            # orderId=CS1906666666ABCDE&
            # testFlag=1&
            # timeStamp=20210927095952430

            # orderAmount 订单金额
            instanceId = self.getArgument(Torken_param,"instanceId")
            # periodNumber 周期数量
            orderId = self.getArgument(Torken_param,"orderId")
            # periodType 周期类型
            testFlag = self.getArgument(Torken_param,"testFlag")
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            timeStamp = self.getArgument(Torken_param,"timeStamp")

            logging.info("ISV[expireInstance],orderId=" + orderId + "\n" +
                         ",instanceId=" + instanceId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "select dj_flag from isv_newinstance where businessId = '" + instanceId + "' and sf_flag = 0 limit 1;"  # 未被释放的实例才可以计算
            data = DB.fetchone(sql, None)
            if data:
                logging.info("[ISV_refresshInstance] 处理冻结订单！")

                if int(data[0]) == 0:
                    sql = "update isv_newinstance set dj_flag = 1,dj_date = "+str(int(time.time()))+" where businessId = '" + instanceId + "' and sf_flag = 0"
                    data = DB.edit(sql, None)
                    if data:
                        # 封装-业务处理
                        logging.info("ISV-冻结业务")

                    else:
                        cryBody["resultCode"] = "000005"
                        cryBody["resultMsg"] = "冻结写入失败！(" + instanceId + ")"
                else:
                    cryBody["resultCode"] = "000005"
                    cryBody["resultMsg"] = "该订单已经冻结！(" + instanceId + ")"
            else:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "该订单未找到！(" + instanceId + ")"


        return cryBody


    #释放
    def ISV_releaseInstance(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            # activity=releaseInstance&
            # instanceId=huaiweitest123456&
            # orderAmount=100&
            # orderId=CS1906666666ABCDE&
            # testFlag=1&
            # timeStamp=20210928020832199

            # orderAmount 订单金额
            instanceId = self.getArgument(Torken_param,"instanceId")
            # periodNumber 周期数量
            orderAmount = self.getArgument(Torken_param,"orderAmount")
            # periodType 周期类型
            orderId = self.getArgument(Torken_param,"orderId")
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            testFlag = self.getArgument(Torken_param,"testFlag")
            # provisionType 商品实例开通方式。
            timeStamp = self.getArgument(Torken_param,"timeStamp")

            logging.info("ISV[releaseinstance],instanceId=" + instanceId + "\n" +
                         ",orderAmount=" + orderAmount + "\n" +
                         ",orderId=" + orderId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "select 1 from isv_newinstance where businessId = '" + instanceId + "' and sf_flag = 0 limit 1;"  # 未被释放的实例才可以计算
            data = DB.fetchone(sql, None)
            if data:
                logging.info("[ISV_refresshInstance] 处理释放订单！")

                sql = "update isv_newinstance set sf_flag = 1,sf_date = " + str(int(time.time())) + " where businessId = '" + instanceId + "' and sf_flag = 0"
                data = DB.edit(sql, None)
                if data:
                    # 封装-业务处理
                    logging.info("ISV-释放业务")

                else:
                    cryBody["resultCode"] = "000005"
                    cryBody["resultMsg"] = "释放写入失败！(" + instanceId + ")"
            else:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "该订单未找到！(" + instanceId + ")"


        return cryBody


class XufeiHandler(BaseHandler):


    def get(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            #expireTime=20210930174148&
            # instanceId=huaiweitest123456&
            # orderAmount=100&
            # orderId=CS1906666666ABCDE&
            # periodNumber=1&
            # periodType=year&
            # productId=00301-666666-0--0&
            # testFlag=1&
            # timeStamp=20210927095241549

            # orderAmount 订单金额
            orderAmount = Torken_param["orderAmount"]
            # periodNumber 周期数量
            periodNumber = Torken_param["periodNumber"]
            # periodType 周期类型
            periodType = Torken_param["periodType"]
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            productId = Torken_param["productId"]
            # provisionType 商品实例开通方式。
            instanceId = Torken_param["instanceId"]
            # testFlag 是否为调试请求
            testFlag = Torken_param["testFlag"]
            # timeStamp 时间戳
            timeStamp = Torken_param["timeStamp"]
            # userId 客户以IAM用户认证方式登录时对应子用户的唯一标识。
            orderId = Torken_param["orderId"]
            # userName 客户以IAM用户认证方式登录的用户名。
            expireTime = Torken_param["expireTime"]

            logging.info("ISV[refreshInstance],orderId=" + orderId + "\n" +
                         ",expireTime=" + expireTime + "\n" +
                         ",orderAmount=" + orderAmount + "\n" +
                         ",periodNumber=" + periodNumber + "\n" +
                         ",periodType=" + periodType + "\n" +
                         ",productId=" + productId + "\n" +
                         ",instanceId=" + instanceId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "INSERT INTO `isv_refreshinstance` (`orderAmount`,`periodNumber`,`periodType`,`productId`,`instanceId`,`testFlag`,`timeStamp`,`orderId`,`expireTime`)VALUES(" \
                   "'" + orderAmount + "'," \
                    "'" + periodNumber + "'," \
                   "'" + periodType + "'," \
                 "'" + productId + "'," \
                "'" + instanceId + "'," \
                "'" + testFlag + "'," \
                "'" + timeStamp + "'," \
                "'" + orderId + "'," \
                "'" + expireTime + "'" \
                  + ");"
            data = DB.edit(sql, None)
            DB.close()
            if not data:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "服务商续费存储失败。"
            else:

                # 封装-业务处理
                logging.info("ISV-续费业务")



        encryptBody = self.generateResponseBodySignature(Global.Global_IsvKey, json.dumps(cryBody))
        print("instanceId = ", encryptBody)

        self.set_header("Body-Sign", "sign_type=\"HMAC-SHA256\",signature=\"" + encryptBody + "\"")

        print(cryBody)

        self.write(cryBody)



class DongjieHandler(BaseHandler):


    def get(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            #activity=expireInstance&
            # instanceId=huaiweitest123456&
            # orderId=CS1906666666ABCDE&
            # testFlag=1&
            # timeStamp=20210927095952430

            # orderAmount 订单金额
            instanceId = Torken_param["instanceId"]
            # periodNumber 周期数量
            orderId = Torken_param["orderId"]
            # periodType 周期类型
            testFlag = Torken_param["testFlag"]
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            timeStamp = Torken_param["timeStamp"]


            logging.info("ISV[expireInstance],orderId=" + orderId + "\n" +
                         ",instanceId=" + instanceId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "INSERT INTO `isv_expireinstance` (`orderId`,`instanceId`,`testFlag`,`timeStamp`)VALUES(" \
                "'" + orderId + "'," \
                "'" + instanceId + "'," \
                "'" + testFlag + "'," \
                "'" + timeStamp + "'" \
                  + ");"
            data = DB.edit(sql, None)
            DB.close()
            if not data:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "服务商续费存储失败。"
            else:

                # 封装-业务处理
                logging.info("ISV-过期业务")



        encryptBody = self.generateResponseBodySignature(Global.Global_IsvKey, json.dumps(cryBody))
        print("encryptBody = ", encryptBody)

        self.set_header("Body-Sign", "sign_type=\"HMAC-SHA256\",signature=\"" + encryptBody + "\"")

        print(cryBody)

        self.write(cryBody)



class ShifangHandler(BaseHandler):


    def get(self):

        # 封装-消息响应
        cryBody = {
            "resultCode": "000000",
            "resultMsg": "success.",
        }

        TorkenTr = self.ISV_TorkenCheck
        Torken_code = TorkenTr[0]
        Torken_param = TorkenTr[1]
        if not Torken_code:
            cryBody["resultCode"] = "000005"
            cryBody["resultMsg"] = "请求参数验证异常"
        else:

            #activity=releaseInstance&
            # instanceId=huaiweitest123456&
            # orderAmount=100&
            # orderId=CS1906666666ABCDE&
            # testFlag=1&
            # timeStamp=20210928020832199


            # orderAmount 订单金额
            instanceId = Torken_param["instanceId"]
            # periodNumber 周期数量
            orderAmount = Torken_param["orderAmount"]
            # periodType 周期类型
            orderId = Torken_param["orderId"]
            # productId 产品标识，同一skuCode下，不同周期类型的productId不同。例如：ISV发布产品，新增一个规格，会生成一个skuCode，再配置包年价格，包月价格，会生成两个productId。
            testFlag = Torken_param["testFlag"]
            # provisionType 商品实例开通方式。
            timeStamp = Torken_param["timeStamp"]


            logging.info("ISV[releaseinstance],instanceId=" + instanceId + "\n" +
                         ",orderAmount=" + orderAmount + "\n" +
                         ",orderId=" + orderId + "\n" +
                         ",testFlag=" + testFlag + "\n" +
                         ",timeStamp=" + timeStamp
                         )

            # 业务新购存储
            DB = DBManager()
            sql = "INSERT INTO `isv_releaseinstance` (`instanceId`,`orderAmount`,`orderId`,`testFlag`,`timeStamp`)VALUES(" \
                   "'" + instanceId + "'," \
                    "'" + orderAmount + "'," \
                   "'" + orderId + "'," \
                 "'" + testFlag + "'," \
                "'" + timeStamp + "'" \
                  + ");"
            data = DB.edit(sql, None)
            DB.close()
            if not data:
                cryBody["resultCode"] = "000005"
                cryBody["resultMsg"] = "服务商续费存储失败。"
            else:

                # 封装-业务处理
                logging.info("ISV-释放业务")



        encryptBody = self.generateResponseBodySignature(Global.Global_IsvKey, json.dumps(cryBody))
        print("instanceId = ", encryptBody)

        self.set_header("Body-Sign", "sign_type=\"HMAC-SHA256\",signature=\"" + encryptBody + "\"")

        print(cryBody)

        self.write(cryBody)