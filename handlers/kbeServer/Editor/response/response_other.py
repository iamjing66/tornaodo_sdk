#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_other


def DataOperate(DB, subcode, params):
    pam = params["Pam"]
    if subcode == 16:
        return interface_other.DoOperate_GetClientName(DB ,pam)
    elif subcode == 17:
        return interface_other.DbGetApkVersionFromDeveceName(DB ,pam)
    elif subcode == 19:
        return interface_other.DoSaveModeGroup(DB ,pam)
    elif subcode == 20:
        return interface_other.ProblemFeedback(DB ,pam)
    elif subcode == 21:
        return interface_other.GetActiveUserFeedback(DB ,pam)
    elif subcode == 35:
        return interface_other.GetLocalFullViewPath(DB ,pam)
    elif subcode == 36:
        return interface_other.DoOperate_GetClientName_new(DB ,pam)
