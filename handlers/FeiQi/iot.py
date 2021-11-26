#!/usr/bin/env python
# coding=utf-8

from handlers.base import BaseHandler

class IotHelloHandler(BaseHandler):

    def get(self):

        _body = {"Code":"OK"}

        set_type = int(self.get_argument("connect"))
        _connect = self.IsConnect
        if set_type == 1 and _connect == 1:
            _body["Code"] = "Err"
        elif set_type == 0 and _connect == 0:
            _body["Code"] = "Err"
        else:
            self.application.Connect = set_type
            print(" = ",self.application.Connect,set_type)
        self.write(_body)


class IotDeviceListHandler(BaseHandler):

    def get(self):

        _body = {}

        _id = 0
        _arr = ["Gate","env","light","infrared","intelligentSwitch","intellingentSocket","infraredController","curtainMotor","intelligentCurtain"]

        for _dtype in _arr:
            for i in range(0,3):
                _id += 1
                _ddata = {}
                _ddata["deviceSubType"] = _dtype
                _ddata["ieeeAddress"] = str(_id)
                #_body.append(_ddata)
                _body[str(_id)] = _ddata
        print(_body)
        self.write(_body)