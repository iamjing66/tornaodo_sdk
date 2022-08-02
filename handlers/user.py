#!/usr/bin/env python
# coding=utf-8

import tornado.web
import tornado.escape
import Global
import time
from handlers.base import BaseHandler
from AgaraTorken.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from handlers.smsServer.SmsInterface import SmsInst


class UserHandler(BaseHandler):

    def get(self):
        pamam = "{\"name\":'1@1@2'}"
        SmsInst.SendSms("18092973675", "SMS_198665133", pamam)
