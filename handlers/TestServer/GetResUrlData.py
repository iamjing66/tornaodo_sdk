#!/usr/bin/env python
# coding=utf-8


from handlers.base import BaseHandler
from methods.db_mysql import DbHander


class PostResUrlRequest(BaseHandler):

    def get(self):
        json_back = {}
        json_back = self.GetTestUrl()
        self.write(json_back)


    def GetTestUrl(self):
        strSql = "select * from tb_restest_db"
        db = DbHander.DBREAD()
        Cur = db.cursor()
        _cback = ""
        try:
            Cur.execute(strSql)
            data = Cur.fetchall()
            if data != None and len(data) > 0:
                _cback = str(data[0][1]) + "|" + str(
                    data[0][2]) + "|" + str(data[0][3]) + "|" + str(data[0][4]) + "|" + str(data[0][5]) + "|" + str(
                    data[0][6]) + "|" + str(data[0][7]) + "|" + str(data[0][8]) + "|" + str(data[0][9])
            else:
                _cback = ""
        except:
            _cback = ""
        db.commit()
        db.close()
        return _cback