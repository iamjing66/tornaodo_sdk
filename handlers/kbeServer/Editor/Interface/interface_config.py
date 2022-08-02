#!/usr/bin/env python
# coding=utf-8
import json
import logging
from handlers.kbeServer.Editor.Interface import interface_res
from methods.DBManager import DBManager


class IConfig:

    def __init__(self):
        self.ReadConfig_Timer = 0
        self.Config_Index = 0
        self.AllCount = 0
        self.LimitCount = 500
        # self.ReadComData()
        self.Content = ""
        self.Config_List = ["203", "204", "207", "208", "xrvipconfig", "xrworkconfig"]  # "202",
        self.DB = DBManager()
        # 配表数据
        # = 课程包
        # self.CBagConfig = {}
        # self.VipConfig = {}
        self.ObjConfig = {}
        self.SceneConfig = {}
        # self.CourseConfig = {}
        # self.LeftBagConfig = {}
        self.ChannelConfig = {}
        self.ChannelZKConfig = {}
        self.XrVipConfig = {}
        self.XrWorkConfig = {}
        self.DataConfig = {"bagprice": 0}
        # self.ReadConfig()

    # ====================配置配表数据读取==============
    def ReadConfig(self):
        logging.info("Config Loading")
        # print("ReadConfig")
        # 全局数据
        sql = "SELECT WorksAPrice from tb_new_config;"
        data = self.DB.fetchone(sql, None)
        # DEBUG_MSG("data : " , data)
        if data != None and len(data) > 0:
            self.DataConfig["bagprice"] = int(data[0]) / 10
        self.Config_Index = 1
        self.Content = ""
        self.AllCount = 0
        pam = " limit " + str(self.AllCount) + "," + str(self.LimitCount)
        self.ReadDataConfig(self.Config_List[0], pam)

    def ReadDataConfig(self, OpenCode, Pam):

        json_Data = {
                "OpenCode": OpenCode,
                "Pam": Pam
        }
        TheData = interface_res.Server_ConfigGet(self.DB, json_Data)
        # TheData = res.json()#json.loads(res.text)
        # DEBUG_MSG("TheData:", TheData)
        self.AnlyzeConfig(TheData, "")

    def AnlyzeConfig(self, json_Data, HasRow):

        code = json_Data["OpenCode"]
        data = json_Data["Data"]
        # print(str(code) + ":" + data)
        if self.Content == "":
            self.Content = data
        else:
            if data != "":
                self.Content = self.Content + "^" + data
        if data == "":
            # 下载完成了
            # if code == "201":
            #     self.ConfigSure_CBag(self.Content)
            if code == "202":
                self.ConfigSure_Vip(self.Content)
            elif code == "203":
                self.ConfigSure_Obj(self.Content)
            elif code == "204":
                self.ConfigSure_Scene(self.Content)
            elif code == "205":
                self.ConfigSure_CourseIds(self.Content)
            elif code == "206":
                self.ConfigSure_LeftBag(self.Content)
            elif code == "207":
                self.ConfigSure_Channel(self.Content)
            elif code == "208":
                self.ConfigSure_ChannelZK(self.Content)
            elif code == "xrvipconfig":
                self.ConfigXrVipConfig(self.Content)
            elif code == "xrworkconfig":
                self.ConfigXrWorkConfig(self.Content)

            if self.Config_Index >= len(self.Config_List):
                logging.info("Config Loaded")
                self.DB.destroy()
                return
            code = self.Config_List[self.Config_Index]
            self.Config_Index += 1
            self.AllCount = 0
            pam = " limit " + str(self.AllCount) + "," + str(self.LimitCount)
            self.Content = ""
            self.ReadDataConfig(code, pam)  # 赠送包裹
        else:
            self.AllCount += 1
            pam = " limit " + str(self.AllCount * self.LimitCount) + "," + str(self.LimitCount)
            self.ReadDataConfig(code, pam)  # 赠送包裹

    def ConfigSure_CBag(self, data):

        # CDBID`LID&LID`一年还是永久,CDBID`LID&LID`一年还是永久

        self.CBagConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.CBagConfig[int(_arr1[0])] = _arr1[1]

                # DEBUG_MSG("ConfigSure_CBag : " , self.CBagConfig)

    def ConfigSure_Vip(self, data):

        # ID`价格^ID`价格

        self.VipConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.VipConfig[int(_arr1[0])] = int(_arr1[1])

                # DEBUG_MSG("ConfigSure_Vip : " , self.VipConfig)

    def ConfigSure_Obj(self, data):

        # ID`价格^ID`价格

        self.ObjConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.ObjConfig[int(_arr1[0])] = [int(_arr1[1]), int(_arr1[2]), _arr1[3]]

                # DEBUG_MSG("ConfigSure_Obj : " , self.ObjConfig)

    def ConfigSure_Scene(self, data):

        # ID`价格^ID`价格

        self.SceneConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.SceneConfig[int(_arr1[0])] = [int(_arr1[1]), int(_arr1[2]), _arr1[3]]

                # DEBUG_MSG("ConfigSure_Scene : " , self.SceneConfig)

    def ConfigSure_CourseIds(self, data):

        # ID`价格^ID`价格

        self.CourseConfig = {}
        # DEBUG_MSG("ConfigSure_CourseIds data : ", data)
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        # DEBUG_MSG("_arr1 : ", _arr1)
                        if _arr1[3] == "":
                            _arr1[3] = "0"
                        if _arr1[2] == "":
                            _arr1[2] = "0"
                        if _arr1[1] == "":
                            _arr1[1] = "0"
                        _uid = int(_arr1[3])
                        _lid = int(_arr1[2])
                        _cid = int(_arr1[1])
                        _active = int(_arr1[4])
                        _id = _arr1[0]
                        if _uid == 0 or _lid == 0 or _cid == 0:
                            continue
                        if _uid not in self.CourseConfig.keys():
                            self.CourseConfig[_uid] = {}
                        if _cid not in self.CourseConfig[_uid].keys():
                            self.CourseConfig[_uid][_cid] = {}
                        if _lid not in self.CourseConfig[_uid][_cid].keys():
                            self.CourseConfig[_uid][_cid][_lid] = ""
                        self.CourseConfig[_uid][_cid][_lid] = [_id, _active]

                # DEBUG_MSG("ConfigSure_CourseIds : " , self.CourseConfig)

    def GetCConfigData(self, _cid, _uid, _lid):
        if _uid not in self.CourseConfig.keys():
            return ""
        if _cid not in self.CourseConfig[_uid].keys():
            return ""
        if _lid not in self.CourseConfig[_uid][_cid].keys():
            return ""
        return self.CourseConfig[_uid][_cid][_lid][0]

    def ConfigSure_LeftBag(self, data):

        # ID`资源购买列表

        self.LeftBagConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        if _arr1[2] == "":
                            _arr1[2] = "0"
                        self.LeftBagConfig[_arr1[0]] = [_arr1[1], int(_arr1[2])]

                # DEBUG_MSG("ConfigSure_LeftBag : ", self.LeftBagConfig)

    def ConfigSure_Channel(self, data):
        self.ChannelConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.ChannelConfig[int(_arr1[0])] = [int(_arr1[1]), int(_arr1[2]), int(_arr1[3])]

                # DEBUG_MSG("ConfigSure_Channel : ", self.ChannelConfig)

    def ConfigSure_ChannelZK(self, data):
        self.ChannelZKConfig = {}
        if data != "" and len(data) > 0:
            _arr = data.split('^')
            if len(_arr) > 0:
                for _arr_str in _arr:
                    if len(_arr_str) > 0:
                        _arr1 = _arr_str.split('*')
                        self.ChannelZKConfig[int(_arr1[0])] = [int(_arr1[1]), _arr1[2]]

    def ConfigXrVipConfig(self, data):
        # print("data" , data)
        self.XrVipConfig = json.loads(data)
        print("self.XrVipConfig = ", self.XrVipConfig)

    def ConfigXrWorkConfig(self, data):
        self.XrWorkConfig = json.loads(data)
        print("self.XrVipConfig = ", self.XrWorkConfig)


IC = IConfig()
