#!/usr/bin/env python
# coding=utf-8

import Global
from handlers.kbeServer.Editor.Interface import interface_global


# 本地课时表中的pdate字段之前没有用，现在用来存储课时隐藏数据
# 删除课时(实际上做隐藏处理),全部删除
# selfuid用户自己的UID
# optype 0-删除本地制作课程 目前只能删除该类型课程
def Delete(selfuid, DB, uid, cid, lid, optype=0):
    # 本地课时表中的pdate字段之前没有用，现在用来存储课时隐藏数据

    # 本地课时表
    table_name = Global.GetLessonTableName(uid, cid)
    #
    if not interface_global.Global_TableExist(table_name, DB):
        return 0  # 课时不存在
    if lid == 0:
        sql = "drop from " + table_name
    else:
        sql = "update " + table_name + " set buy = 1 where LID = " + str(lid)
    if DB.edit(sql, None):
        return 1  # 操作成功
    return -1  # 数据库操作失败
