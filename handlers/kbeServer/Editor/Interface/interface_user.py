#!/usr/bin/env python
# coding=utf-8

import logging

import requests

from handlers.SyncServer.sockect import pro_status
from handlers.redisServer.RedisInterface import C_ServerAddressCache


def IUser_Diffusion(subcode, uid, username, data, cmode):

    json = {
        "opencode": 300,
        "subcode": subcode,
        "UID": uid,
        "username": username,
        "data": data
    }
    json["data"]["cmode"] = cmode

    Adresse = C_ServerAddressCache.GetAddress(username, cmode)
    if Adresse:
        url = "http://" + str(Adresse.decode('utf-8')) + "/postinterface"
        logging.info("[IUser_Diffusion] url = %s" % url)
        headers = {
            'Connection': 'close',
        }
        res = requests.post(url=url, json=json)
        logging.info("DiffusionDo opencode = %s ,subcode = %s, username = %s, res = %s" % (300, subcode, username, data))
    pro_status.user_connect(username, uid, cmode)


def IUser_DiffusionDo(subcode, uid, username, data):
    logging.info("DiffusionDo opencode = %s ,subcode = %s, username = %s, res = %s" % (300, subcode, username, data))
    if subcode == 1:
        # 顶号
        pro_status.user_kick(uid, data["cmode"])
