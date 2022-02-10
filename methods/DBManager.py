#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import pymysql
import Global


class DBManager:

    def connectDB(self, host, database, user=None, password=None):
        return pymysql.connect(host, user, password, database)

    def __init__(self):
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = self.connectDB(**Global.get_config.mysql_options())
        except:
            logging.error("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        pass
        # 如果数据打开，则关闭；否则没有操作
        # if self.conn and self.cur:
        #     self.cur.close()
        #     self.conn.close()
        # return True

    def destroy(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=False):
        # 连接数据库
        res = self.connectDatabase()

        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            logging.error("execute failed: " + sql)
            logging.error("params: " + str(params))
            self.close()
            return False
        return rowcount

    # 执行数据库的sq语句,主要用来做插入操作
    def callprocDo(self, sql, params=None, commit=False):
        # 连接数据库
        res = self.connectDatabase()

        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.callproc(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            logging.error("execute failed: " + sql)
            logging.error("params: " + str(params))
            self.close()
            return False
        return rowcount

    # 查询所有数据
    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            logging.info("查询失败:" + sql)
            return False
        self.close()
        results = self.cur.fetchall()
        logging.info("查询成功")
        return results

    # 查询一条数据
    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        # print("res",res,type(res))
        # if isinstance(res,int) and res == 0:
        #     logging.info("DoSql - fetchone:No rowcount : " + sql)
        #     return True
        if not res:
            logging.info("DoSql - fetchone:Error:" + sql)
            return False
        self.close()
        result = self.cur.fetchone()
        logging.info("DoSql - fetchone:Succ")
        return result

    # 执行存储过程
    def callprocAll(self, sql, params=None):
        res = self.callprocDo(sql, params, True)
        if not res:
            logging.info("查询失败:" + sql)
            return False
        self.close()
        result = self.cur.fetchone()
        logging.info("查询成功")
        return result

    # 增删改数据
    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        # print("DoSql - edit: Res:",res,type(res))
        # if res == 0:
        #     logging.info("DoSql - edit:No rowcount : " + sql)
        #     return True

        if not res:
            logging.info("DoSql - edit:Error:" + sql)
            return False
        self.conn.commit()
        self.close()
        logging.info("DoSql - edit:Succ")

        return True

    # 数据转换json
    def fetchone_json(self, result):

        json_data = {}
        pos = 1

        if result and len(result) > 0:
            for value in result:
                json_data["value" + str(pos)] = value
                pos += 1

        return json_data

    # 数据转换json
    def fetchall_json(self, result, key):

        json_data = {}

        if result and len(result) > 0:
            for info in result:
                pos_two = 0
                line_name = info[key]
                json_data[line_name] = {}
                for value in info:
                    if pos_two > 0:
                        json_data[line_name]["value" + str(pos_two)] = value
                    pos_two += 1

        return json_data


DB = DBManager()
