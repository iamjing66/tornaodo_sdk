import hashlib
import json
import time

import requests

import Global
from handlers.kbeServer.XREditor.data import xr_data_work,xr_data_obj
from handlers.kbeServer.XREditor.Interface import interface_account
import application
import logging


def Upload(DB,self_uid,pid,obj,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        if workData["state"] == 1:
            json_data["code"] = -2
            json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_8", languageStr)
        else:
            code = xr_data_obj.Update(DB, self_uid, pid, 0,obj)
            if code == 1:
                json_data["code"] = 1
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_6", languageStr)
            else:
                json_data["code"] = -3
                json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_7", languageStr)

    return json_data


def XrObjVersion(DB,self_uid,pid,languageStr):
    json_data = {
        "code": 0,
        "pam": "",
        "msg": ""
    }

    workData = xr_data_work.GetData(DB, 0, 0, self_uid, pid, 0)
    if not workData:
        json_data["code"] = -1
        json_data["msg"] = Global.LanguageInst.GetMsg("SMSGID_2_2", languageStr)
    else:
        json_data["code"] = 1
        json_data["msg"] = xr_data_obj.GetVersion(DB,self_uid,pid,0)

    return json_data
