#!/usr/bin/env python
# coding=utf-8

import pysolr
import datetime
import Global
import json
import time
import logging
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU
from handlers.redisServer.RedisInterface import ServerUserCache


class SolrInterface:
    def __init__(self) -> None:
        self.url = "http://{0}/{1}"
        self.solr_url = Global.get_config.solr_config()

    def Solr_PayLog(self, proId, name, saleModules, costsRoad, transactionType, price, type, courseId, createDate, endDate, userName, userId, userType, SoftType, channelType):

        # proId           商品ID(String)
        # name            商品名称(String)
        # platform        售卖平台(10 - PC ，20 - APP， 30 - VR，50 - TV平台，12 - 二级平台)(int)（见副4）
        # saleModules     售卖模块（见副2）(int)
        # costsRoad       消费途径（见副3）（int）
        # transactionType 交易类型(0 - 智慧豆 ， 1 - 人民币)(int)
        # price           项目价格  （以“分”为单位）(int)
        # type            商品类型（见副1）(int)
        # courseId        商品类型为5时，添加课时对应的课程ID(String)
        # createDate      开通(售卖)时间(Unix时间戳)(int)
        # endDate         到期时间(Unix时间戳 ，没有为空)(int)
        # organization    分销商ID(String)
        # distributor     机构ID(String)
        # userName        用户名称(String)
        # userId          用户ID(String)
        # userType        用户类型(0 - C端自由用户, 1 - C端培训机构, 2 - B端高职高校, 3 - B端K12教育)(String)
        # useIP           ip地址
        json_data = {
                "proId": proId,
                "name": name,
                "saleModules": saleModules,
                "transactionType": transactionType,
                "costsRoad": costsRoad,
                "price": price,
                "type": type,
                "courseId": courseId,
                "createDate": createDate,
                "endDate": endDate,
                "userName": userName,
                "userId": userId,
                "userType": userType,
                "SoftType": SoftType,
                "channelType": channelType,
        }
        self.SolrLog(2, json_data)

    def Solr_Pay(self, Code, proId, name, _from, saleModules, costsRoad, transactionType, price, type, courseId, createDate, endDate, organization, distributor, userName, userId, userType, _ip):

        platform = 0

        platform = self.GetPlatform(_from)
        if platform == 0:
            return

        json_data = {
                "proId": proId,
                "name": name,
                "platform": platform,
                "saleModules": saleModules,
                "transactionType": transactionType,
                "costsRoad": costsRoad,
                "price": price,
                "type": type,
                "courseId": courseId,
                "createDate": createDate,
                "endDate": endDate,
                "organization": organization,
                "distributor": distributor,
                "userName": userName,
                "userId": userId,
                "userType": userType,
                "useIP": _ip,
        }
        self.SolrLog(Code, json_data)

    def GetPlatform(self, _from):
        if _from == "Android":
            return 20
        elif _from == "Pico":
            return 31
        elif _from == "CWVR":
            return 32
        elif _from == "YCVR":
            return 33
        elif _from == "YCMR":
            return 34
        elif _from == "HtcViveFocus":
            return 35
        elif _from == "DP":
            return 36
        elif _from == "EmdoorVR":
            return 37
        elif _from == "Htc":
            return 38
        elif _from == "HXVR":
            return 39
        elif _from == "HWVR":
            return 40
        elif _from == "CloudVR":
            return 41
        elif _from == "AndroidTV":
            return 50
        elif _from == "XRCREATEX":
            return 10
        else:
            return 0

    # 索引库操作
    def SolrLog(self, Code, Data):

        solr = None
        # print("SolrLog = WriteStart - Code[%i]" % Code)
        logging.info("SolrLog - ToDO -> Code[%i],Data[%s]" % (Code, Data))
        _data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        try:
            if Code == 1:  # 工程项目创建索引
                solr = pysolr.Solr(self.url.format(self.solr_url, 'createProject'), timeout=10)
            elif Code == 2:  # 商品交易记录索引库
                solr = pysolr.Solr(self.url.format(self.solr_url, 'dealCore'), timeout=10)
            elif Code == 3:  # 课程播放
                solr = pysolr.Solr(self.url.format(self.solr_url, 'coursePlay'), timeout=10)
            elif Code == 4:  # 在线时长
                solr = pysolr.Solr(self.url.format(self.solr_url, 'userUseCore'), timeout=10)
            # elif Code == 5:         #登录状态
            #     solr = pysolr.Solr('http://' + self.solr_url + '/userDataCore', timeout=10)
            solr.add(self.interface_CData(Code, Data))
            solr.commit()
        except Exception as e:
            logging.error("Log_Cost Error:Code[%i] - exception-[%s]" % (Code, str(e)))
        else:
            logging.info("Log_Cost OK:Code[%i]" % Code)

            # solr写入成功
            if Code == 2:
                if isinstance(Data, dict):
                    json_data = Data
                else:
                    json_data = json.loads(Data)

                DB = DBManager()
                if int(json_data["transactionType"]) == 0:
                    sql = "update tb_userdata set WitPayTotal = WitPayTotal + " + str(json_data["price"]) + " where uid = " + str(json_data["userId"])
                else:
                    sql = "update tb_userdata set RmbPayTotal = RmbPayTotal + " + str(json_data["price"]) + " where uid = " + str(json_data["userId"])
                DB.edit(sql, None)
                DB.destroy()

    def interface_CData(self, Code, SolrData):

        if isinstance(SolrData, dict):
            json_data = SolrData
        else:
            json_data = json.loads(SolrData)
        jdata = {}
        rdata = []

        userId = int(json_data["userId"])
        username = json_data["userName"]
        SoftType = json_data["SoftType"]
        organization = 0
        distributor = 0
        useIP = 0
        platform = 10
        data = ServerUserCache.redis_user_get(username, ["organization", "distributor", "editor_ip", "app_ip"])
        logging.info("redis data: %s" % data)
        if data:
            organization = data[0]
            distributor = data[1]
            if SoftType == "pc":
                useIP = data[2]
                platform = 10
            else:
                useIP = data[3]
                platform = data[4]
        logging.info("platform data ---> %s" % platform)

        if Code == 1:
            # 工程项目创建
            jdata = {
                    "userId": userId,
                    "userName": username,
                    "createDate": int(time.time()),
                    "organization": str(organization),
                    "distributor": str(distributor),
                    "ActionType": json_data["ActionType"],
                    "namep": str(json_data["PName"]),
                    "useIP": useIP,
                    "platform": platform,  # 售卖平台(0-PC ，1-APP， 2-VR，3-二级平台)(int)
            }
            # print("jdata" , jdata)
        elif Code == 2:
            # 商品交易记录索引库
            jdata = {
                    "proId": str(json_data["proId"]),  # 商品ID(String)
                    "name": json_data["name"],  # 商品名称(String)
                    "platform": platform,  # 售卖平台(0-PC ，1-APP， 2-VR，3-二级平台)(int)
                    "saleModules": json_data["saleModules"],  # 售卖模块（见副2）(int)
                    "transactionType": json_data["transactionType"],  # 交易类型(0-智慧豆 ， 1-人民币)(int)
                    "price": json_data["price"],  # 项目价格  （以“分”为单位）(int)
                    "type": json_data["type"],  # 商品类型（见副1）(int)
                    "costsRoad": json_data["costsRoad"],  # 消费途径（见副3）（int）
                    "createDate": int(time.time()),  # 开通(售卖)时间(Unix 时间戳)(int)
                    "endDate": json_data["endDate"],  # 到期时间(Unix 时间戳 ，没有为空)(int)
                    "organization": str(organization),  # 分销商ID(String)
                    "distributor": str(distributor),  # 机构ID(String)
                    "userName": username,  # 用户名称(String)
                    "userType": json_data["userType"],  # 用户类型(0-C端自由用户,1-C端培训机构,2-B端高职高校,3-B端K12教育)(String)
                    "userId": str(userId),  # 用户ID(String)
                    "useIP": useIP,
                    "courseId": json_data["courseId"],  # 商品类型为5时，添加课时对应的课程ID(String)
                    "channelType": json_data["channelType"],  # 渠道类型
            }
        elif Code == 3:
            # 课程播放
            jdata = {
                    "courseId": json_data["courseId"],  # 课程ID(String)
                    "classHourId": json_data["classHourId"],  # 课时ID(String)
                    "platform": platform,  # 售卖平台(0-PC ，1-APP， 2-VR，3-二级平台)(int)
                    "createDate": int(time.time()),  # 开通(售卖)时间(Unix 时间戳)(int)
                    "organization": str(organization),  # 分销商ID(String)
                    "distributor": str(distributor),  # 机构ID(String)
                    "userName": username,  # 用户名称(String)
                    "userId": userId,  # 用户ID(String)
                    "useIP": useIP,
            }
        elif Code == 4:
            # 在线时长
            jdata = {
                    "platform": platform,  # 售卖平台(0-PC ，1-APP， 2-VR，3-二级平台)(int)
                    "loginDate": int(time.time()),  # 开通(售卖)时间(Unix 时间戳)(int)
                    "dateTime": json_data["dateTime"],  # 开通(售卖)时间(Unix 时间戳)(int)
                    "organization": str(organization),  # 分销商ID(String)
                    "distributor": str(distributor),  # 机构ID(String)
                    "userName": username,  # 用户名称(String)
                    "userId": userId,  # 用户ID(String)
                    "power": json_data["Power"],
                    "useTime": json_data["useTime"],  # 用户ID(String)
                    "useIP": useIP,
                    "loginState": json_data["loginState"],
                    "UPower": json_data["UPower"],
                    "AccountPower": json_data["AccountPower"],

            }
        # elif Code == 5:
        #     # 登录登出记录
        #     jdata = {
        #         "UID": json_data["UID"],  # 课程ID(String)
        #         "dateTime": json_data["dateTime"],  # 开通(售卖)时间(Unix 时间戳)(int)
        #         "organization": str(json_data["organization"]),  # 分销商ID(String)
        #         "distributor": str(json_data["distributor"]),  # 机构ID(String)
        #         "UPower": json_data["UPower"],  # 用户名称(String)
        #         "loginState": json_data["loginState"],  # 用户ID(String)
        #         "terminal": json_data["terminal"],  # 用户ID(String)
        #     }

        # print(jdata)
        rdata.append(jdata)
        return rdata

    # 副1
    # 0
    # VIP
    # 1
    # 频道
    # 2
    # 智慧豆
    # 3
    # 课程包
    # 4
    # 课程
    # 5
    # 课时
    # 6
    # 场景
    # 7
    # 资源
    # 8
    # 特效

    # 副2
    # 0
    # 后台标准课程售卖
    # 1
    # PC标准课程售卖
    # 2
    # PC共享大厅售卖
    # 3
    # APP
    # SIS课程售卖
    # 4
    # APP共享大厅售卖
    # 5
    # VR
    # SIS课程售卖
    # 6
    # VR共享大厅售卖

    # 人民币消费日志
    # proType 1:软件内充值  2：购买作品观看权(rmb消费) 3:购买教育中心内容观看权(rmb消费) 4:作品频道包月(RMB消费) 5:教育中心频道包月(RMB消费) 6:vip购买/续费 7-包裹位购买/续费
    # terminal 账号来源 0-PC 1-APP 2-VR
    # proName 项目名称
    # proPay  消费金额
    # supplement 补充
    def Log_Cost(self, UID, organization, distributor, proType, proName, proPay, supplement, cName):

        try:
            solr = pysolr.Solr(self.url.format(self.solr_url, 'rmbDataCore'), timeout=10)
            # How you'd index data.
            _data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            solr.add([
                    {
                            "UID": UID,
                            "dateTime": _data,
                            "organization": organization,
                            "distributor": distributor,
                            "proType": proType,
                            "terminal ": 1,
                            "proName": proName,
                            "proPay": proPay,
                            "cName": cName,
                            "supplement": supplement
                    }
            ])
            solr.commit()
        except:
            logging.error("Log_Cost Error")
        else:
            logging.info("Log_Cost OK")


SolrInst = SolrInterface()
