#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_fullview


def FullViewResponse(DB, subcode, params):
    if subcode == 26:
        return interface_fullview.GetQjtTypeList(DB)
    elif subcode == 27:
        Pam = params["Pam"]
        return interface_fullview.GetQjtDetailList(DB,Pam)