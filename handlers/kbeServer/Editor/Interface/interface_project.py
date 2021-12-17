#!/usr/bin/env python
# coding=utf-8

import logging
import time,Global
from handlers.kbeServer.Editor.Data import data_work
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.Interface import interface_obj,interface_global,interface_project
from handlers.kbeServer.Editor.Interface import interface_account
from handlers.kbeServer.Editor.Data import data_course
from handlers.kbeServer.Editor.Data import data_project,data_obj



#客户端列表(带版本号)转json，用来比对
def clientVersionDataToJson(pdata):
    p_server = {}
    if pdata != None and len(pdata) > 0:
        l_pdata = pdata.split('*')
        for info in l_pdata:
            sdata = info.split('^')
            uid = int(sdata[0])
            pid = int(sdata[1])
            version = int(sdata[2])
            if uid not in p_server.keys():
                p_server[uid] = {}
            p_server[uid][pid] = version

    return p_server


#同步数据
def Get(pdata, self_uid, itype):

    #版本验证
    p_server = clientVersionDataToJson(pdata)
    # 业务执行
    DB = DBManager()
    sql = data_project.GetProjectSQLFromType(itype,self_uid)
    result = data_project.Data_Projects_Base(sql,DB,p_server,0)
    DB.destroy()
    return result[1] + "！"


#是否需要更新
def GetPVersion(DB,UID,PID,target):

    return data_project.GetPVersion(DB,UID,PID,target)


#获取版本号
def GetVersion(data,uid,DB):
    pid = int(data)
    pversion = data_project.GetVersion(pid,uid,DB,0)
    _back = str(pid) + "^" + str(pversion) + "^" + data_obj.GetVersion(pid, uid, DB, 0) + "^"
    return _back

#上传数据
def UpLoad(l_pdata, uid,DB):
    code = 1
    ##print("l_pdata",l_pdata)
    #['1',
    # '10087',
    #  '10087`qffg`1621908973`1621914045`1002`0`1.691426`5.963621`-7.707121`8.500001`357`-2.104186E-06`0`0`1,1,1`45,180`0`0``0`0`0`0`5`1277`0`0`1`1`',
    #  '20`场景编程区`1621908973`0`0`0`0`0`0`1`1`1`0``&0,0&```0`0`1```0`0``0`7`0!5`3D相机`1621908973`5`6`5`20.75002`345.5`6.847463E-07`1`1`1`0``&0,0&```0`0`2```0`0``0`11`0!13`跳点`1621909005`-4.99883`0`-0.004079991`0`180`0`1`1`1`0``1@5@-236.3524,135.8373,0@D:2@@~2@111@@@1$1|1$0@&0,0&```0`0`3```0`0``0`13`0!23370`女人二`1621909037`-0.0004117982`0`-1.28284`0`184.5`0`1`1`1`0``1@7@-209.9685,56.3863,0@D:2@1$1@~2@103@@@1$1|1$<2d>5|1$0|1$0|2$0@&0,0&```0`0`4```0`0``0`11`0']
    pid = int(l_pdata[1])
    if l_pdata[2] != "":
        project_data = l_pdata[2].split('`')
        ProjectToDB(DB,pid, uid,0,project_data)
    if l_pdata[3] != "":
        object_data = l_pdata[3]
        #object_del = l_pdata[5]
        interface_obj.UpdateToDB(0,DB,uid, pid , object_data)

#发布到背包
def FB(DB,self_uid,uid,pid,template):

    sql = "update tb_project set Template = "+str(template)+" where UID = " + str(uid) + " and PID = " + str(pid)
    if DB.edit(sql,None):
        return 1
    return 0

#发布到背包
def SetPublish(DB,self_uid,uid,pid,publish):

    sql = "update tb_project set Publish = "+str(publish)+" where UID = " + str(uid) + " and PID = " + str(pid)
    if DB.edit(sql,None):
        return 1
    return 0


#是否空闲状态
def PFlag(DB,uid,pid,dtype):
    list_work_base = data_work.Data_Work_Base(uid, pid, 0, DB, 2)
    if list_work_base:
        # #print("xxxxxxxxxxxxxxxxxx : ", list_work_base)
        if int(list_work_base[7]) == 1 and int(list_work_base[4]) == pid:
            return 0  # 作品审核中不能移出
    if data_course.ProjectInCourses(DB, uid, pid,dtype):
        return -1  # 课程审核中不能移出

    return 1

#移出
def RemoveP(DB,self_uid,uid,pid):

    code = PFlag(DB,uid,pid,0)
    if code == 1:
        sql = "update tb_project set Template = 0 where UID = " + str(uid) + " and PID = " + str(pid)
        result = DB.edit(sql,None)
        if result:
            sql = "delete from tb_workbag where uid = " + str(uid) + " and WID = " + str(pid)
            DB.edit(sql, None)
        return 1
    return code

#删除
def DeleteP(DB,self_uid,uid,pid,nocheck):
    if nocheck == 1:
        code = 1
    else:
        code = PFlag(DB, uid, pid,1)
    if code == 1:
        if data_project.Delete(DB,uid,pid,0):
            if data_obj.Delete(DB,uid,pid,0):
                interface_account.DelPPackage(DB, uid, pid)
                return 1
            else:
                return -99
        else:
            return -99
    return code



#存库
def ProjectToDB(DB,pid, uid,target,data):

    table_name = ""
    if target == 0:
        table_name = "tb_project"
    else:
        table_name = "tb_mproject"

    sql = "select id from "+table_name+" where uid = " + str(uid) + " and PID = " + str(pid)
    result = DB.fetchone(sql,None)
    # TODO
    if result:
        sql = "Update "+table_name+" set PID=" + str(data[0]) + ", PName='" + str(data[1]) + "', CreateDate=" + str(data[2]) + ", EditDate=" + str(data[3]) + ", SID=" + str(data[4]) + ",BDelete = "+str(data[5])+", C_Posx=" + str(data[6]) + ", C_Posy=" + str(data[7]) + ", C_Posz=" + str(data[8]) + ", C_Rotx=" + str(data[9]) +", C_Roty=" + str(data[10]) + ", C_Rotz=" + str(data[11]) + ", Template=" + str(data[12]) + ", LightIntensity=" + str(data[13]) + ", LightColor='" + str(data[14]) + "', LightAngle='" + str(data[15]) + "', Power=" + str(data[16]) + ", Sort=" + str(data[17]) + ",FullViewPath='" + str(data[18]) + "', ParentPid=" + str(data[19]) + ", Publish=" + str(data[20]) + ", Skybox=" + str(data[21]) + ", HType=" + str(data[22]) + ",Version=" + str(data[23]) + ",p_uid = "+str(data[25])+",P_TYPE= "+str(data[26])+",PDate= "+str(data[27])+",`From` = "+str(data[28])+",FromPam = '"+str(data[29])+"' where PID = " + str(pid) + " and uid =" + str(uid)
    else:
        sql = "Insert into "+table_name+" (PID, PName, CreateDate, EditDate, SID,BDelete, C_Posx, C_Posy, C_Posz, C_Rotx, C_Roty, C_Rotz, Template, LightIntensity, LightColor, LightAngle, Power, Sort, FullViewPath, ParentPid, Publish, Skybox, HType,Version,UID,p_uid,P_TYPE,PDate,`From`,FromPam) values (" + str(data[0]) + ",'" + str(data[1]) + "'," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + "," + str(data[6]) + "," + str(data[7]) + "," + str(data[8]) + "," + str(data[9]) + "," + str(data[10]) + "," + str(data[11]) + "," + str(data[12])+ "," + str(data[13]) + ",'" + str(data[14]) + "','" + str(data[15]) + "'," + str(data[16]) + "," + str(data[17]) + ",'" + str(data[18]) + "'," + str(data[19]) + "," + str(data[20]) + "," + str(data[21]) + "," + str(data[22]) + "," + str(data[23]) + "," + str(uid) + "," + str(data[25])+ "," + str(data[26])+ "," + str(data[27])+ "," + str(data[28])+ ",'" + str(data[29]) + "')"
    #print("insert Into P : " , sql)
    DB.edit(sql,None)


def SetFrom(DB,uid,pid,From,FromPam):
    sql = "Update tb_project set `From`="+str(From) + ",FromPam = '"+str(FromPam)+"' where uid = " + str(uid) + " and pid = "+str(pid)
    DB.edit(sql,None)
    return 1

#复制或者转移工程到别的账号
#pid 我的工程ID
#cmode 0-复制 1-转移
#username 转移到的账号
def CopyMyProjectToAccount(DB,self_uid,pid,pname,username,cmode):

    if len(pname) < 1:
        return 0 #工程名称长度不足

    if cmode == 1:
        #转移
        code = PFlag(DB, self_uid, pid, 1)
        if code != 1:
            return -1

    ARRID = interface_global.NewPIDFromUserName(DB,username)
    NPID = ARRID[0]
    P_UID = ARRID[1]
    
    b_type = False
    user_power = interface_account.get_user_power(DB,username)
    # 判断是否是B类用户
    if user_power in (2, 3, 4):
        b_type = True
    
    # B类用户不需要判断，直接转移
    target_bag = 0
    if not b_type:
        target_bag = interface_account.get_user_bag(DB,username)
        if not target_bag:
            # 用户无空余包裹位
            return -2

    #复制工程数据
    data__p = data_project.Data_Project_Base(self_uid, pid, 0, DB, 2)
    if data__p:
        data__p[0] = NPID
        data__p[1] = pname
        data__p[2] = int(time.time())
        data__p[3] = int(time.time())
        data__p[12] = 0
        data__p[19] = 0
        data__p[20] = 0
        data__p[24] = P_UID
        data__p[25] = 0
        data__p[27] = 0
        data__p[28] = 104
        data__p[29] = str(self_uid)
        interface_project.ProjectToDB(DB, NPID , P_UID , 0, data__p)

    #复制资源
    data_o = data_obj.Data_Objs_Base(0, DB, pid, self_uid, {}, 0)
    if data_o:
        #print("data_o:", data_o)
        #interface_obj.UpdateToDB(0, DB, P_UID, NPID, data_o)

        interface_obj.CopyToDB(0, DB, P_UID, NPID, Global.GetObjTableName(self_uid, pid))

        # NPID 转移的工程PID
        # target_bag 目标账号的一个空余包裹位
        if not b_type:
            interface_account.update_user_bag(DB, NPID, target_bag)

    if cmode == 1:
        # 工程转移时调用，清除工程并清除本账号当前的存储位
        del_pro = DeleteP(DB, self_uid, self_uid, pid,1)
        logging.info("转移工程: %s" % del_pro)
        # data_project.Delete(DB,self_uid,pid,0)

    return 1