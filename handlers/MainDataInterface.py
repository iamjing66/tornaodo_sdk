#!/usr/bin/env python
# coding=utf-8

import logging
import copy
import Global
import json
from handlers.base import BaseHandler
from handlers.kbeServer.Editor.Interface import interface_course, interface_project, interface_work, interface_obj
from handlers.kbeServer.Editor.response import response_upload, response_global, response_project


class post_plistINIHandler(BaseHandler):  # 继承base.py中的类BaseHandler

    # 工程列表
    def post(self):
        uid = self.POST_VERIFY_MAIN
        p_back = ""
        if uid > 0:
            json_bck = copy.deepcopy(Global.JSON_Bck)
            # BODY=====================================
            # 获取 工程列表
            pdata = json.loads(self.JData)
            # print("pdata : ",pdata)
            read_type = int(pdata["rtype"])
            # read_page = int(pdata["page"])
            upload = int(pdata["upload"])
            post_data = ""
            logging.info("PostInterfaceRequest -> uid[%i],read_type[%i],upload[%i]" % (uid, read_type, upload))
            # logging.info("read_type:"+str(read_type))
            if upload == 1:
                if read_type == 9:  # 上传的数据
                    post_data = response_upload.UpLoad(pdata["data"], uid)
            else:
                if read_type == 1:  # 自由工程数据
                    post_data = interface_project.Get(pdata["data"], uid, 0)
                elif read_type == 2:  # 本地作品数据
                    post_data = interface_work.Get(pdata["data"], uid, 0)
                elif read_type == 3:  # 本地课程数据
                    post_data = interface_course.Get(pdata["data"], uid, 0)
                elif read_type == 4:  # 课程购买数据
                    post_data = interface_course.Get(pdata["data"], uid, 1, 1)
                elif read_type == 5:  # 课程市场
                    post_data = interface_course.Get(pdata["data"], uid, 2)
                elif read_type == 6:  # 作品市场数据
                    post_data = interface_work.Get(pdata["data"], uid, 1)
                elif read_type == 7:  # 下架的课程数据
                    post_data = response_global.GetCourseXJ()  # Data_CourseInst.DosGetsCourse()
                elif read_type == 8:  # 上传的数据版本号
                    post_data = response_upload.GetVersion(pdata["data"], uid)
                elif read_type == 10:  # 检测工程是否需要更新
                    post_data = response_project.GetPVersion(pdata["data"])  # Data_PInst.GetPUploadFlag(pdata["data"])
                elif read_type == 11:  # PC端进入工程
                    post_data = interface_obj.Get(pdata["data"])  # GetPCPData
                elif read_type == 12:  # GM审核列表
                    post_data = interface_course.Get(pdata["data"], uid, 3)  # GetShCourse(int(pdata["data"]),uid)
                elif read_type == 13:  # GM作品审核列表
                    post_data = interface_work.Get(pdata["data"], uid, 2)
                    # post_data = Data_Inst.GetShWork(int(pdata["data"]),"",uid)
                elif read_type == 14:  # 市场中的工程数据
                    post_data = interface_project.Get(pdata["data"], uid, 1)
                elif read_type == 15:  # VR买看数据
                    post_data = response_global.SDK_MK(uid)
                elif read_type == 16:  # 频道包月数据
                    post_data = response_global.SDK_CHANNEL(uid)
                elif read_type == 17:  # IP记录
                    post_data = response_global.SetLoginIP(uid, pdata["data"], self.SoftType)
                elif read_type == 18:  # 精品作品市场数据
                    post_data = interface_work.GetNew(pdata["data"], uid, 1, course_level=1)
                elif read_type == 106:  # 作品市场数据 2021-11-24
                    post_data = interface_work.GetNew(pdata["data"], uid, 1, course_level=2)

            json_bck["Code"] = 1
            json_bck["Data"] = post_data
            json_bck["Msg"] = "0"
            self.write(json_bck)

    def set_default_headers(self):
        self.allowMyOrigin()
