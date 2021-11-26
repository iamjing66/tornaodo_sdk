#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_class

def classWorkresponse(DB ,subCode ,uid ,data):
    if subCode == 12:
        return interface_class.ClassSchedule(DB ,data)
    elif subCode ==13:
        return interface_class.StudentWork(DB ,uid ,data)
    elif subCode ==14:
        return interface_class.ClassStudentData(DB ,uid ,data)
    elif subCode ==15:
        return interface_class.ClassStudentList(DB ,uid ,data)