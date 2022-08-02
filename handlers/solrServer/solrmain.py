#!/usr/bin/env python
# coding=utf-8

import time
import json
from handlers.base import BaseHandler
from methods.SolrInterface import SolrInst


class SolrRequest(BaseHandler):

    def post(self):
        self.SOLR_VERIFY
        solrdata = self.SolrData

        Code = solrdata["code"]
        Data = solrdata["data"]

        # print("Data", type(Data))
        # print("Data", type(Data) is "dict")
        # print("Data", isinstance(Data,dict))
        # 暂时先屏蔽了 - 等二级平台部署时一起放开
        SolrInst.SolrLog(int(Code), Data)

        # if Code == 1:
        #     #工程项目创建索引
        #     SolrInterface.Log_Cost()
        json_bck = {
                "Code": 1,
                "ERR": 0,
        }
        self.write(json_bck)
