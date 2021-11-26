#!/usr/bin/env python
# coding=utf-8

import json
from methods.SolrInterface import SolrInst
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU

def Solr_PayLog(proId, name, saleModules, costsRoad, transactionType, price, type, courseId,createDate, endDate, userId, SoftType, channelType):

    userName = ""
    userType = 0
    data = globalRedisU.redis_user_u_get(userId)
    if data != None:
        userName = data[7]
        userType = data[6]
    SolrInst.Solr_PayLog(proId, name, saleModules, costsRoad, transactionType, price, type, courseId,createDate, endDate,  userName, userId, userType, SoftType, channelType)


def RequestSolr( Code, Data):

    SolrInst.SolrLog(int(Code), Data)

    # url = mysqlHander.PAY_URL + "/solr"
    # json_Data = {'code': Code, "data": Data}  # subPackage
    # headers = {'Connection': 'close', }
    # res = requests.post(url=url, json=json_Data,headers=headers)
    # DEBUG_MSG(res.text)