#!/usr/bin/env python
# coding=utf-8


def UpdateToDB(DB,_date,uid):

    sql = "update tb_userdata set VIPPOWER = 2,VIPDATE = " + str(_date) + " where UID = " + str(uid)
    DB.edit(sql, None)

