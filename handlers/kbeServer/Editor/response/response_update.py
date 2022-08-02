#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_update


def SoftVersionGet(DB, subcode, pam):
    json_data = {
            "code": 0,
            "msg": ""
    }
    if subcode == 23:
        json_data = interface_update.GetUpdateCxVersion(DB)
    elif subcode == 34:
        json_data = interface_update.GetUpdateCxVersionNew(DB, pam)
    return json_data
