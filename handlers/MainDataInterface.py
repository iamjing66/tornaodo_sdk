#!/usr/bin/env python
# coding=utf-8

import logging
import copy
import Global
import json
from handlers.base import BaseHandler
from handlers.kbeServer.Editor.Interface import interface_course,interface_project,interface_work,interface_obj
from handlers.kbeServer.Editor.response import response_upload,response_global,response_project

class post_plistINIHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #工程列表
    def post(self):
        UID = self.POST_VERIFY_MAIN
        p_back = ""
        if UID > 0:
            JSON_Bck = copy.deepcopy(Global.JSON_Bck)
            JSON_Data = {}
            # BODY=====================================
            #获取 工程列表
            #print("self.JData:",self.JData)
            pdata = json.loads(self.JData)
            #print("pdata : ",pdata)
            read_type = int(pdata["rtype"])
            #read_page = int(pdata["page"])
            upload = int(pdata["upload"])
            #uploadover = int(pdata["uploadover"])
            post_data = ""
            print("PostInterfaceRequest read_type[%i] upload[%i] UID[%i]  " % (read_type, upload, UID))
            logging.info("PostInterfaceRequest -> UID[%i],read_type[%i],upload[%i]" % (UID, read_type,upload))
            #logging.info("read_type:"+str(read_type))
            if upload == 1:

                # if read_page == 1:
                #     self.post_upload_temp_init(UID)
                # self.post_upload_temp_set(UID, pdata["data"])
                # if uploadover == 1:
                #     if read_type == 9:  # 上传的数据
                #         self.post_data_temp_set(UID, PCInst.SavePDataEnd(self.post_upload_temp_get(UID), UID))
                if read_type == 9:  # 上传的数据

                    #print("pdata",pdata)

                    post_data = response_upload.UpLoad(pdata["data"], UID)
                    #post_data = Data_Inst.SavePDataEnd(pdata["data"], UID)

            else:
                #if read_page == 1:
                    #self.post_data_temp_init()
                if read_type == 1:  #自由工程数据
                    post_data = interface_project.Get(pdata["data"],UID, 0)
                elif read_type == 2:  #本地作品数据
                    post_data = interface_work.Get(pdata["data"],UID, 0)
                elif read_type == 3:  #本地课程数据
                    post_data = interface_course.Get(pdata["data"],UID, 0)#Data_LessonInst.GetLessonDataWithVersion(pdata["data"],UID, 0,0)
                elif read_type == 4:  #课程购买数据
                    post_data = interface_course.Get(pdata["data"],UID, 1)
                elif read_type == 5:  #课程市场
                    post_data = interface_course.Get(pdata["data"],UID, 2)
                elif read_type == 6:  #作品市场数据
                    post_data = interface_work.Get(pdata["data"],UID, 1)
                elif read_type == 7:  #下架的课程数据
                    post_data = response_global.GetCourseXJ()#Data_CourseInst.DosGetsCourse()
                elif read_type == 8:  #上传的数据版本号
                    post_data = response_upload.GetVersion(pdata["data"],UID)
                elif read_type == 10:  #检测工程是否需要更新
                    post_data = response_project.GetPVersion(pdata["data"])#Data_PInst.GetPUploadFlag(pdata["data"])
                elif read_type == 11:  #PC端进入工程
                    post_data = interface_obj.Get(pdata["data"])    #GetPCPData
                elif read_type == 12:  #GM审核列表
                    post_data = interface_course.Get(pdata["data"],UID, 3)  #GetShCourse(int(pdata["data"]),UID)
                elif read_type == 13:  #GM作品审核列表
                    post_data = interface_work.Get(pdata["data"],UID, 2)
                    #post_data = Data_Inst.GetShWork(int(pdata["data"]),"",UID)
                elif read_type == 14:  #市场中的工程数据
                    post_data = interface_project.Get(pdata["data"],UID, 1)
                elif read_type == 15:  #VR买看数据
                    post_data = response_global.SDK_MK(UID)
                elif read_type == 16:  #频道包月数据
                    post_data = response_global.SDK_CHANNEL(UID)
                elif read_type == 17:  #IP记录
                    post_data = response_global.SetLoginIP(UID,pdata["data"],self.SoftType)
                elif read_type == 18:  # 精品作品市场数据
                    post_data = interface_work.GetNew(pdata["data"], UID, 1, course_level=1)
                elif read_type == 106:  #作品市场数据 2021-11-24
                    post_data = interface_work.GetNew(pdata["data"],UID, 1, course_level=2)
                # elif read_type == 1001:  #APP端登录数据
                #     post_data = VrInst.GetLoginData(UID, pdata["data"])
                # elif read_type == 1002:  #APP端进入工程
                #     post_data = VrInst.App_EnterProject(pdata["data"])


            JSON_Bck["Code"] = 1
            JSON_Bck["Data"] = post_data
            JSON_Bck["Msg"] = "0"
            # BODY=====================================
            #print("JSON_Bck : " , JSON_Bck)
            self.write(JSON_Bck)

    def set_default_headers(self):
        self.allowMyOrigin()
