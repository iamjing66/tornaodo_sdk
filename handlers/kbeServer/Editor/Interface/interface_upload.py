#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_course

#数据上传
def UpdateLoad(pdata,uid):

    #print("pdata",pdata )
    # 开始解析数据
    l_pdata = pdata.split('^')  #工程数据！资源数据！动态库
    #print("l_pdata",l_pdata)
    data_type = int(l_pdata[0])
    if data_type == 1:  #工程上传
        self.DoProjectDSave(l_pdata,uid)
    elif data_type == 2:  #作品上传
        self.DoWorkDSave(l_pdata,0,uid)
    elif data_type == 3:  #课程上传
        interface_course.UpLoad(l_pdata,uid)

    return str(data_type)