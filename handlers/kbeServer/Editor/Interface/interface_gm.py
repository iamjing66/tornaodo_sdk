#!/usr/bin/env python
# coding=utf-8

import time
from datetime import datetime

import sys

import os

from handlers.kbeServer.Editor.Data import data_ppackage
from handlers.kbeServer.Editor.Interface import interface_global, interface_course, interface_mail
from xml.dom.minidom import Document, parse


# GM增加智慧豆
def AddWit(DB, uid, username, num):
    if not interface_global.Global_IsGM(uid, DB):
        return 0  # 不是GM
    if len(username) < 0:
        return -1  # 用户名异常
    if num <= 0:
        return -2  # 数量异常

    sql = "update tb_userdata set Wit_Score = Wit_Score + " + str(num) + " where username = '" + username + "'"
    if DB.edit(sql, None):
        return 1
    return -3  # 增加失败


"""
账号信息查询
"""


def GM_AccountData(DB, uid, username):
    if not interface_global.Global_IsGM(uid, DB):
        return 0  # 不是GM
    sql = "SELECT EndDate,AccountDesc FROM tb_userdata WHERE UserName = '" + username + "';"
    result = DB.fetchone(sql, None)
    _back = "0$"
    if result:
        _back = str(result[0]) + "$" + str(result[1])
    return _back


# 修改账号信息
def GM_Alter_AccountData(DB, uid, username, passdate, companyname):
    if not interface_global.Global_IsGM(uid, DB):
        return 0  # 不是GM
    sql = "update tb_userdata set EndDate = '" + str(passdate) + "',AccountDesc = '" + str(companyname) + "' where UserName =  '" + username + "';"
    DB.edit(sql, None)
    return 1


"""
    =========================账号权限，以及课程基础背包相关====
"""


def GetPowerAndBag(DB, uid, username):
    if not interface_global.Global_IsGM(uid, DB):
        return 0  # 不是GM
    sql = "select Power,BCBag from tb_userdata where UserName = '" + username + "';"
    result = DB.fetchone(sql, None)
    _back = "0$"
    if result:
        _back = str(result[0]) + "$" + str(result[1])
    return _back


"""
    =========================账号权限，以及课程基础背包相关====
"""


def SetPowerAndBag(DB, uid, username, power, bcbag):
    if not interface_global.Global_IsGM(uid, DB):
        return 0  # 不是GM
    sql = "update tb_userdata set Power = " + str(power) + ",BCBag = '" + bcbag + "' where UserName = '" + username + "';"
    result = DB.edit(sql, None)
    return 1


# GM上架/下架  课程
def GM_LessonUD(DB, self_uid, cid, uid, lid, status):
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM
    return interface_course.LessonUD(DB, cid, uid, lid, status)


# ===================GM发送邮件==================
# type 0-指定用户 1-系统通知 2-竞赛通知
# pam 指定用户 传"用户名 用户名"  群组系统消息 传 "用户类型,用户等级" 群组竞赛消息 传 "所属竞赛,所属阶段"  参数逗号隔开
# title 标题
# tbody 内容
def GM_SendMails(DB, self_uid, type, pam, title, tbody):
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM

    _channel = 0
    if type == 0:
        # 个人
        sql = "select uid from tb_userdata where username = '" + pam + "'"
        result = DB.fetchone(sql, None)
        if result:
            _channel = int(result[0])
        else:
            return -1
    interface_mail.WriteMail(DB, _channel, title, tbody)
    return 1


# 赠送存储包裹
def GM_AddPBag(DB, self_uid, username, num):
    if num < 1:
        return -1
    if len(username) < 1:
        return -2
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM

    _date = int(time.time()) + 31536000

    for i in range(num):
        data_ppackage.InsertToDBOfUserName(DB, username, _date)

    return 1


"""
    导出工程
"""


def GM_ExportProject(DB, self_uid, pid, UID, desc):
    # DEBUG_MSG("GM_ExportProject:" ,pid)
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM
    # DEBUG_MSG("GM_ExportProject:---2")
    doc = Document()  # 创建DOM文档对象
    # 创建根元素
    rootElement = doc.createElement('project')

    # 创建子元素
    childElement = doc.createElement('common')
    # 为子元素添加id属性
    childElement.setAttribute('pid', str(pid))
    childElement.setAttribute('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    childElement.setAttribute('desc', desc)
    # 将子元素追加到根元素中
    rootElement.appendChild(childElement)
    # DEBUG_MSG("GM_ExportProject:---2")
    doc.appendChild(rootElement)
    path = sys.path[0] + "/projects/" + str(UID) + "_" + str(pid) + ".xml"
    # DEBUG_MSG("path:",path)
    str_sql = "SELECT * FROM tb_project where PID = " + str(pid) + " and UID = " + str(UID) + ";"
    data = DB.fetchone(str_sql, None)
    if data:
        childElement = doc.createElement('project_private')
        childElement.setAttribute('sm_TheData_PID', str(data[1]))
        childElement.setAttribute('sm_TheData_PName', desc)
        childElement.setAttribute('sm_TheData_CreateDate', str(data[3]))
        childElement.setAttribute('sm_TheData_EditDate', str(data[4]))
        childElement.setAttribute('sm_TheData_SID', str(data[5]))
        childElement.setAttribute('sm_TheData_BDelete', str(data[6]))
        childElement.setAttribute('sm_0_TheData_C_Pos', str(data[7]))
        childElement.setAttribute('sm_1_TheData_C_Pos', str(data[8]))
        childElement.setAttribute('sm_2_TheData_C_Pos', str(data[9]))
        childElement.setAttribute('sm_0_TheData_C_Rot', str(data[10]))
        childElement.setAttribute('sm_1_TheData_C_Rot', str(data[11]))
        childElement.setAttribute('sm_2_TheData_C_Rot', str(data[12]))
        childElement.setAttribute('sm_TheData_Template', "0")  # str(data[14])
        childElement.setAttribute('sm_TheData_LightIntensity', str(data[14]))
        childElement.setAttribute('sm_TheData_LightColor', str(data[15]))
        childElement.setAttribute('sm_TheData_LightAngle', str(data[16]))
        childElement.setAttribute('sm_TheData_Power', str(data[17]))
        childElement.setAttribute('sm_TheData_Sort', str(data[18]))
        childElement.setAttribute('sm_TheData_FullViewPath', str(data[19]))
        childElement.setAttribute('sm_TheData_ParentPid', str(data[20]))
        childElement.setAttribute('sm_TheData_Publish', str(data[21]))
        childElement.setAttribute('sm_TheData_Skybox', str(data[22]))
        childElement.setAttribute('sm_TheData_HType', str(data[23]))
        # 将子元素追加到根元素中
        rootElement.appendChild(childElement)

        table_name = "tb_obj_" + str(UID) + "_" + str(data[1])
        str_sql = "select * from " + table_name
        result = DB.fetchall(str_sql, None)
        if result:
            # 创建子元素
            parentElement = doc.createElement('project_objs')
            rootElement.appendChild(parentElement)
            for data in result:
                # 创建子元素
                # DEBUG_MSG("data", data)
                childElement = doc.createElement('project_obj')
                parentElement.appendChild(childElement)
                aa = data[2]
                childElement.setAttribute('sm_TheData_ObjID', str(data[1]))
                childElement.setAttribute('sm_TheData_objName', str(aa))
                childElement.setAttribute('sm_TheData_CreateDate', str(data[3]))
                childElement.setAttribute('sm_0_TheData_Obj_Pos', str(data[4]))
                childElement.setAttribute('sm_1_TheData_Obj_Pos', str(data[5]))
                childElement.setAttribute('sm_2_TheData_Obj_Pos', str(data[6]))
                childElement.setAttribute('sm_0_TheData_Obj_Rote', str(data[7]))
                childElement.setAttribute('sm_1_TheData_Obj_Rote', str(data[8]))
                childElement.setAttribute('sm_2_TheData_Obj_Rote', str(data[9]))
                childElement.setAttribute('sm_0_TheData_Obj_Scale', str(data[10]))
                childElement.setAttribute('sm_1_TheData_Obj_Scale', str(data[11]))
                childElement.setAttribute('sm_2_TheData_Obj_Scale', str(data[12]))
                childElement.setAttribute('sm_TheData_Active', str(data[13]))
                childElement.setAttribute('sm_TheData_ResPath_User', str(data[14]))
                childElement.setAttribute('sm_TheData_Commonts', str(data[15].decode('utf-8')))
                childElement.setAttribute('sm_TheData_AdsortDetection', str(data[16]))
                childElement.setAttribute('sm_TheData_AdsortBeDetection', str(data[17]))
                childElement.setAttribute('sm_TheData_ParentID', str(data[18]))
                childElement.setAttribute('sm_TheData_ResType', str(data[19]))
                childElement.setAttribute('sm_TheData_ComID', str(data[20]))
                childElement.setAttribute('sm_TheData_View_FullPath', str(data[21]))
                childElement.setAttribute('sm_TheData_View_FullAbPath', str(data[22]))
                childElement.setAttribute('sm_0_TheData_sizeDelta', str(data[23]))
                childElement.setAttribute('sm_1_TheData_sizeDelta', str(data[24]))
                childElement.setAttribute('sm_TheData_Content', str(data[25]))
                childElement.setAttribute('sm_TheData_Collider', str(data[26]))
                childElement.setAttribute('BDelete', str(data[28]))
            if os.path.exists(path):
                # 删除文件，可使用以下两种方法。
                os.remove(path)
            # print("path",path)
            f = open(path, 'a', encoding='utf-8')
            # 写入文件
            doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
            # 关闭
            f.close()

            return 1
        return 0
    return 0


"""
    导入工程挂载到某个文件
"""


def GM_ImportProject(DB, self_uid, tuid, pid, UID, pname):
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM
    # 读取下本地文件
    path = sys.path[0] + "/projects/" + str(UID) + "_" + str(pid) + ".xml"
    if not os.path.exists(path):
        return -1
    if tuid == 0:
        tuid = self_uid
    xmldoc = parse(path)
    elementobj = xmldoc.documentElement
    # 重新获取一个PID
    newpid = interface_global.NewPID(DB, tuid)
    # 先导入工程
    subElementObj1 = elementobj.getElementsByTagName("project_private")

    if not pname or len(pname) < 1:
        pname = str(subElementObj1[0].getAttribute("sm_TheData_PName"))

    data = DB.callprocAll('GM_CreateProject', (newpid, pname, int(str(subElementObj1[0].getAttribute("sm_TheData_CreateDate"))), int(str(subElementObj1[0].getAttribute("sm_TheData_EditDate"))),
                                               int(str(subElementObj1[0].getAttribute("sm_TheData_SID"))), int(str(subElementObj1[0].getAttribute("sm_TheData_BDelete")))
                                               , float(str(subElementObj1[0].getAttribute("sm_0_TheData_C_Pos"))), float(str(subElementObj1[0].getAttribute("sm_1_TheData_C_Pos"))),
                                               float(str(subElementObj1[0].getAttribute("sm_2_TheData_C_Pos")))
                                               , float(str(subElementObj1[0].getAttribute("sm_0_TheData_C_Rot"))), float(str(subElementObj1[0].getAttribute("sm_1_TheData_C_Rot"))),
                                               float(str(subElementObj1[0].getAttribute("sm_2_TheData_C_Rot")))
                                               , 0, float(str(subElementObj1[0].getAttribute("sm_TheData_LightIntensity"))), str(subElementObj1[0].getAttribute("sm_TheData_LightColor")),
                                               str(subElementObj1[0].getAttribute("sm_TheData_LightAngle"))
                                               , int(str(subElementObj1[0].getAttribute("sm_TheData_Power"))), int(str(subElementObj1[0].getAttribute("sm_TheData_Sort"))),
                                               str(subElementObj1[0].getAttribute("sm_TheData_FullViewPath")), int(str(subElementObj1[0].getAttribute("sm_TheData_Publish")))
                                               , int(str(subElementObj1[0].getAttribute("sm_TheData_Skybox"))), int(str(subElementObj1[0].getAttribute("sm_TheData_HType"))), tuid)
                          )

    if data:
        # DEBUG_MSG("data:",data)
        table_name = "tb_obj_" + str(tuid) + "_" + str(newpid)
        sql = "CREATE TABLE " + table_name + " like tb_object;"
        DB.edit(sql, None)

        subElementObj2 = elementobj.getElementsByTagName("project_obj")
        for i in range(len(subElementObj2)):
            _sql = "INSERT INTO " + table_name + " (`ObjID`,`objName`,`CreateDate`,`Obj_Posx`,`Obj_Posy`,`Obj_Posz`,`Obj_Rotex`,`Obj_Rotey`,`Obj_Rotez`,`Obj_Scalex`,`Obj_Scaley`,`Obj_Scalez`,`Active`,`Commonts`,`AdsortDetection`,`AdsortBeDetection`,`ParentID`,`ResType`,`ComID`,`View_FullPath`,`View_FullAbPath`,`sizeDeltax`,`sizeDeltay`,`Content`,`Collider`,`BDelete`) VALUES(" + str(
                subElementObj2[i].getAttribute("sm_TheData_ObjID")) + ",'" + subElementObj2[i].getAttribute("sm_TheData_objName") + "'," + str(
                subElementObj2[i].getAttribute("sm_TheData_CreateDate")) + "," + str(subElementObj2[i].getAttribute("sm_0_TheData_Obj_Pos")) + "," + str(
                subElementObj2[i].getAttribute("sm_1_TheData_Obj_Pos")) + "," + str(subElementObj2[i].getAttribute("sm_2_TheData_Obj_Pos")) + "," + str(
                subElementObj2[i].getAttribute("sm_0_TheData_Obj_Rote")) + "," + str(subElementObj2[i].getAttribute("sm_1_TheData_Obj_Rote")) + "," + str(
                subElementObj2[i].getAttribute("sm_2_TheData_Obj_Rote")) + "," + str(subElementObj2[i].getAttribute("sm_0_TheData_Obj_Scale")) + "," + str(
                subElementObj2[i].getAttribute("sm_1_TheData_Obj_Scale")) + "," + str(subElementObj2[i].getAttribute("sm_2_TheData_Obj_Scale")) + "," + str(
                subElementObj2[i].getAttribute("sm_TheData_Active")) + ",'" + str(subElementObj2[i].getAttribute("sm_TheData_Commonts")) + "','" + str(
                subElementObj2[i].getAttribute("sm_TheData_AdsortDetection")) + "','" + str(subElementObj2[i].getAttribute("sm_TheData_AdsortBeDetection")) + "'," + str(
                subElementObj2[i].getAttribute("sm_TheData_ParentID")) + "," + str(subElementObj2[i].getAttribute("sm_TheData_ResType")) + "," + str(
                subElementObj2[i].getAttribute("sm_TheData_ComID")) + ",'" + str(subElementObj2[i].getAttribute("sm_TheData_View_FullPath")) + "','" + str(
                subElementObj2[i].getAttribute("sm_TheData_View_FullAbPath")) + "'," + str(subElementObj2[i].getAttribute("sm_0_TheData_sizeDelta")) + "," + str(
                subElementObj2[i].getAttribute("sm_1_TheData_sizeDelta")) + ",'" + str(subElementObj2[i].getAttribute("sm_TheData_Content")) + "'," + str(
                subElementObj2[i].getAttribute("sm_TheData_Collider")) + "," + str(subElementObj2[i].getAttribute("BDelete")) + ");"
            DB.edit(_sql, None)

    return 1


"""
设置GM权限
"""


def GM_SetGM(self, username):
    if not interface_global.Global_IsGM(self_uid, DB):
        return 0  # 不是GM
    if self.GM_UserFlag(0, username) == 1:
        avatar = KBEngine.baseAppData["users"][username][0]
        if avatar != None:
            avatar.SetGM()
        if self.client:
            self.client.GM_Rsut(4)
    else:
        str_sql = "update tbl_avatar_editor set sm_GM_STATE = 5 where id = (SELECT sm_Avatar_DbID FROM tbl_account where id = (SELECT entityDBID FROM kbe_accountinfos where accountName = '" + username + "') and sm_AvatarType = 0);"
        KBEngine.executeRawDatabaseCommand(str_sql, self.GM_SetGMCallback)


def GM_SetGMCallback(self, result, rows, insertid, error):
    if error == None:
        if self.client:
            self.client.GM_Rsut(4)  # 获取数据失败
    else:
        if self.client:
            self.client.GM_Rsut(-4)  # 获取数据失败
