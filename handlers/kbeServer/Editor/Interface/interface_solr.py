#!/usr/bin/env python
# coding=utf-8

import json
from methods.SolrInterface import SolrInst
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU
from handlers.redisServer.RedisInterface import ServerUserCache


def Solr_PayLog(proId, name, saleModules, costsRoad, transactionType, price, type, courseId, createDate, endDate, userId, SoftType, channelType, self_username):
    # userName = ""
    # userName = self_username
    userType = 0
    # TODO
    data = ServerUserCache.redis_user_get(self_username, ["Power"])
    # data = globalRedisU.redis_user_u_get(userId)
    if data != None:
        # userName = data[7]
        userType = int(data[0])
    SolrInst.Solr_PayLog(proId, name, saleModules, costsRoad, transactionType, price, type, courseId, createDate, endDate, self_username, userId, userType, SoftType, channelType)


def RequestSolr(Code, Data):
    SolrInst.SolrLog(int(Code), Data)

    # url = mysqlHander.PAY_URL + "/solr"
    # json_Data = {'code': Code, "data": Data}  # subPackage
    # headers = {'Connection': 'close', }
    # res = requests.post(url=url, json=json_Data,headers=headers)
    # DEBUG_MSG(res.text)
