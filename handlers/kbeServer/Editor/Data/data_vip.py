#!/usr/bin/env python
# coding=utf-8


def UpdateToDB(db, _date, uid):
    sql = "update tb_userdata set VIPPOWER = 2,VIPDATE = " + str(_date) + " where UID = " + str(uid)
    db.edit(sql, None)
