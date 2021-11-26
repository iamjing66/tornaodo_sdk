#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_mail


def mailresponse(DB, subCode, uid, data):
    if subCode == 6:
        return interface_mail.GetMail(DB,uid, data)
    elif subCode == 7:
        return interface_mail.UpdateMail(DB,data, uid)
    elif subCode == 9:
        return interface_mail.Sendnotice(DB,data, uid)
    elif subCode == 8:
        return interface_mail.InsertEmilData(DB,data, uid)