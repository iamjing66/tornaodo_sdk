#!/usr/bin/env python
# coding=utf-8

import logging

from handlers.kbeServer.Editor.Interface import interface_course
from handlers.kbeServer.Editor.Interface import interface_project, interface_work
from methods.DBManager import DBManager


def UpLoad(pdata, self_uid):
    DB = DBManager()
    l_pdata = pdata.split('^')  # 工程数据！资源数据！动态库
    # print("l_pdata",l_pdata)

    data_type = int(l_pdata[0])
    # UpLoad[2]��datas��[['2', '2937`rwqr`1`1`2937`0``1`0`1621405157`5`0`1002`2`0`0````1`0`0`0']]
    logging.info("UpLoad[%i],datas:[%s]" % (data_type, l_pdata))
    if data_type == 1:  # 工程上传
        interface_project.UpLoad(l_pdata, self_uid, DB)
    elif data_type == 2:  # 作品上传
        interface_work.UpLoad(DB, l_pdata, self_uid, 0)
    elif data_type == 3:  # 课程上传
        interface_course.UpLoad(l_pdata, self_uid, DB)
    DB.destroy()


# 获取版本号
def GetVersion(data, uid):
    DB = DBManager()
    p_data = data.split('*')
    p_type = int(p_data[0])
    _back = ""
    if p_type == 1:  # 工程版本号
        _back = "1*" + interface_project.GetVersion(p_data[1], uid, DB)
    elif p_type == 2:  # 作品版本号
        _back = "2*" + interface_work.GetVersion(p_data[1], uid, DB)
    elif p_type == 3:  # 课程版本号
        _back = "3*" + interface_course.GetVersion(p_data[1], uid, DB)
    DB.destroy()
    return _back
