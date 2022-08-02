#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_res


def ResVersionResponse(DB, subCode, uid, data):
    if subCode == 10:
        return interface_res.GetUpdateVersion(DB, uid, data)
    elif subCode == 11:
        return interface_res.AnlyzeCode(DB, uid, data)
    elif subCode == 40:
        # 新版获取资源版本号
        return interface_res.new_get_update_version(DB, data)
    elif subCode == 41:
        return interface_res.new_anlyze_code(DB, data)


def ConfigGet_Server(DB, params):
    return interface_res.Server_ConfigGet(DB, params)
