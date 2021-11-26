#!/usr/bin/env python
# coding=utf-8

from handlers.kbeServer.Editor.Interface import interface_collect


def CollectResponse(DB, subcode, UID, params):
    Pam = params["Pam"]
    if subcode == 28:
        return interface_collect.GetCollectData(DB, UID, Pam)
    elif subcode == 29:
        return interface_collect.CollectDelete(DB, UID, Pam)


