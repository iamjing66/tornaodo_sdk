#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pymysql
import Global


class mysqlHander:

    def connectDB(self, host, database, user=None, password=None):
        return pymysql.connect(host, user, password, database)

    def DBREAD(self):
        return self.connectDB(**Global.get_config.mysql_options())

    def SISDBREAD(self):
        return self.connectDB(**Global.get_config.mysqlSIS_options())


DbHander = mysqlHander()
