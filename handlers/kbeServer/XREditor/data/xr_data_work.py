import hashlib
import json
import time

import requests

import Global
from handlers.kbeServer.Editor.Interface import interface_global
import application
import logging


def NewPID(DB,UID):
    sql = "select max(PID) from tb_xr_worklocal where uid = "+str(UID)+";"
    data = DB.fetchone(sql, None)
    if data:
        if data[0] is None:
            return 1
        return int(data[0]) + 1
    return 1

#PUID,PPID,MARKET,ISDET 制作者/来源数据数据
#from 101 - 自由创作 102-模板新建 103-转移 104-购买
def CreateWork(DB,UID,WNAME,SID,FROM,PUID,PPID,ISDET):
    # 获取一个新的PID
    PID = NewPID(DB,UID)

    cdate = int(time.time())

    target_table = Global.GetXRObjTableName(UID,PID)
    #参数
    sourse_table = ""
    MARKET = 0
    if FROM == 102 or FROM == 103:
        sourse_table = Global.GetXRObjTableName(PUID,PPID)
    elif FROM == 104:
        MARKET = 1
        sourse_table = Global.GetMXRObjTableName(PUID,PPID)

    #判断下是否存在源数据
    if len(sourse_table) > 0:
        if not interface_global.Global_TableExist(sourse_table,DB):
            return 0    #源表不存在

    #创建本地作品
    #作品
    if FROM == 101:
        sql = "insert into tb_xr_worklocal (UID,PID,WNAME,CDATE,`FROM`,SID,VERSION,STATE) VALUE("+str(UID)+","+str(PID)+",'"+str(WNAME)+"','"+str(cdate)+"',"+str(FROM)+","+str(SID)+",1,0);"
    elif FROM == 102:
        sql = "insert into tb_xr_worklocal (UID,PID,WNAME,CDATE,`FROM`,SID,VERSION,STATE) select " + str(UID) + "," + str(PID) + ",'" + str(WNAME) + "','" + str(cdate) + "'," + str(FROM) + ",SID,1,0 FROM tb_xr_worklocal WHERE UID = " \
                                                                                                                                                                                           "'"+str(PUID)+"' AND PID = '"+str(PPID)+"' limit 0,1;"
    elif FROM == 103:
        sql = "insert into tb_xr_worklocal (UID,PID,WNAME,CDATE,`FROM`,SID,VERSION,STATE,PUID,PPID) select " + str(UID) + "," + str(PID) + ",'" + str(WNAME) + "','" + str(cdate) + "'," + str(FROM) + ",SID,1,0,"+str(PUID)+","+str(PPID)+" FROM tb_xr_worklocal WHERE UID = " \
                    "'" + str(PUID) + "' AND PID = '" + str(PPID) + "' limit 0,1;"
    elif FROM == 104:
        sql = "insert into tb_xr_worklocal (UID,PID,WNAME,CDATE,`FROM`,SID,VERSION,STATE,PUID,PPID) select " + str(UID) + "," + str(PID) + ",WNAME,'" + str(cdate) + "'," + str(FROM) + ",SID,1,1," + str(PUID) + "," + str(PPID) + " FROM tb_xr_workmarket WHERE UID = " \
                                      "'" + str(PUID) + "' AND PID = '" + str(PPID) + "' limit 0,1;"
    data = DB.edit(sql,None)
    if not data:
        logging.info("[CreateWork] workdata insert error")
        return -1

    #资源
    sql = "create table " + target_table + " like tb_xr_obj;"
    DB.edit(sql, None)
    if FROM == 101:
        sql = "insert into "+target_table+" (ObjID,objName,CreateDate,ResType,ComID,Version) values (20,'场景编辑区','"+str(cdate)+"',1,1,1),(20,'3D相机','"+str(cdate)+"',2,2,1);"
        data = DB.edit(sql, None)
        if not data:
            logging.info("[CreateWork] obj insert error")
            return -2

    else:
        sql = "insert into " + target_table + " (ObjID,objName,CreateDate,ResType,ComID,Version,state,posx,posy,posz,rotex,rotey,rotez,scalex,scaley,scalez,fullview,Commonts,sizeDeltax,sizeDeltay,Content,Collider,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10) select ObjID,objName,'"+str(cdate)+"',ResType,ComID,1,state,posx,posy,posz,rotex,rotey,rotez,scalex,scaley,scalez,fullview,Commonts,sizeDeltax,sizeDeltay,Content,Collider,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 from "+sourse_table+";"
        data = DB.edit(sql, None)
        if not data:
            logging.info("[CreateWork] obj insert error")
            return -2

    #删除
    if ISDET:
        code = DeleteWork(DB,PUID,PPID,MARKET)
        if code != 1:
            logging.info("[CreateWork] delete work error")
            return -3

    # 保存PID
    #application.App.Redis_Config.SavePID(UID, PID)
    return PID

#删除作品
def DeleteWork(DB,UID,PID,MARKET):



    if MARKET == 0:
        work_table = "tb_xr_worklocal"
        sourse_table = Global.GetXRObjTableName(UID,PID)
    else:
        sourse_table = Global.GetMXRObjTableName(UID,PID)
        work_table = "tb_xr_workmarket"

    sql = "delete from "+work_table+" where UID = "+str(UID) + " and PID = "+str(PID)
    data = DB.edit(sql,None)
    if not data:
        logging.info("[DeleteWork] work delete error")
        return 0
    else:
        sql = "drop table "+sourse_table
        DB.edit(sql,None)
        # if not data:
        #     logging.info("[DeleteWork] obj delete error")
        #     return -1

    return 1

#FLAG 0-获取精简数据
#type 数据结果类型 0-json
def GetData(DB,FLAG,type,uid,pid,market):

    if market == 0:
        work_table = "tb_xr_worklocal"
    else:
        work_table = "tb_xr_workmarket"

    sql = "select * from " + work_table + " where UID = "+ str(uid) + " and pid = "+str(pid) + " limit 0,1;"
    data = DB.fetchone(sql,None)
    if data:
        if FLAG == 0:
            return {
                "wname":data[1],
                "uid": data[2],
                "version": data[8],
                "pid": data[9],
                "template": data[10],
                "state": data[12],
                "from": data[13],
            }

    return None


def Publish(DB,uid,pid,wname,classiy,platform,price,tab,desc):

    sql = "update tb_xr_worklocal set workname = '"+wname+"',classify = "+str(classiy)+",platforms = '"+platform+"',price = "+str(price)+",tabs = '"+tab+"',wdesc = '"+desc+"' where uid = " + str(uid) + " and pid = " + str(pid)
    data = DB.edit(sql,None)
    if data:
        return True
    return False



def AlterName(DB,self_uid,pid,wname):

    sql = "update tb_xr_worklocal set wname = '" + wname + "' where uid = " + str(self_uid) + " and pid = " + str(pid)
    data = DB.edit(sql, None)
    if data:
        return True
    return False


#待审核数量
def MaxSHPage(DB):

    sql = "select count(id) from tb_xr_worklocal where state = 1"
    data = DB.fetchone(sql, None)
    if data:
        return int(data[0])
    return 0


#获取作品列表
#type = 0-审核列表 1-普通市场 2-精品市场 3-自建作品集
def GetDatas(DB,type,page,line,uid = 0):

    sql = ""
    dition = ""
    callback = {

    }

    if type == 3:
        callback = {
            "publish":{},       #发布的数据
            "self": {},         #自由创作
            "template": {},     #模板工程
            "buy": {},          #购买的
        }

    if page > 0:
        dition = " limit " + str((page-1)*line) + ","+str(line)
    if type == 0:
        sql = "select t1.WNAME,t1.UID,t1.WDESC,t1.platforms,t1.tabs,t1.price,t1.classify,t1.PID,t1.template,t1.cdate,t1.state,t1.SID,t2.UserName from tb_xr_worklocal t1 inner join tb_userdata t2 on t1.uid = t2.uid and t1.state = 1 order by t1.cdate "
    elif type == 1:
        sql = "select t3.* from (select t1.WNAME,t1.UID,t1.WDESC,t1.platforms,t1.tabs,t1.price,t1.classify,t1.PID,t1.template,t1.cdate,t1.state,t1.SID,t2.UserName from tb_xr_workmarket t1 inner join tb_userdata t2 on t1.uid = t2.uid and t1.state = 0 order by t1.cdate) t3 inner join tb_xr_workmarketsort t4 on t3.uid = t4.uid and t3.pid = t4.wid order by t4.sort;"
    elif type == 2:
        sql = "select t3.* from (select t1.WNAME,t1.UID,t1.WDESC,t1.platforms,t1.tabs,t1.price,t1.classify,t1.PID,t1.template,t1.cdate,t1.state,t1.SID,t2.UserName from tb_xr_workmarket t1 inner join tb_userdata t2 on t1.uid = t2.uid and t1.state = 1 order by t1.cdate) t3 inner join tb_xr_workmarketsort t4 on t3.uid = t4.uid and t3.pid = t4.wid order by t4.sort;"
    elif type == 3:
        sql = "select * from (select t1.WNAME,t1.UID,t1.WDESC,t1.platforms,t1.tabs,t1.price,t1.classify,t1.PID,t1.template,t1.cdate,t1.state,t1.SID,t2.UserName,t1.`from` from tb_xr_worklocal t1 left join tb_userdata t2 on t1.puid = t2.uid ) t3 where uid = "+str(uid)+" order by cdate desc;"

    if len(dition) > 0:
        sql = sql + dition

    data = DB.fetchall(sql,None)
    if data:
        list_data = list(data)
        for minfo in list_data:

            username = ""
            if minfo[12]:
                username = minfo[12]

            info = {
                "wname": minfo[0],  # 作品名称
                "uid": int(minfo[1]),  # 用户ID
                "wdesc": minfo[2],  # 作品描述
                "platforms": minfo[3],  # 发布平添
                "tabs": minfo[4],  # 标签
                "price": int(minfo[5]),  # 价格
                "classify": minfo[6],  # 分类
                "pid": int(minfo[7]),  #
                "template": int(minfo[8]),  # 模板状态
                "cdate": int(minfo[9]),  # 创建时间
                "state": int(minfo[10]),  # 状态
                "SID": int(minfo[11]),  # 场景ID
                "username": username  # 作者名称
            }
            unionID = str(minfo[1]) + "_" + str(minfo[7])
            if type != 3:
                callback[unionID] = info
            else:
                ifrom = int(minfo[13])
                platforms = minfo[3]
                if len(platforms) > 0:
                    callback["publish"][unionID] = info
                elif ifrom == 101: #自由创建
                    itemplate = int(minfo[8])
                    if itemplate == 0:
                        callback["self"][unionID] = info
                    else:
                        callback["template"][unionID] = info
                elif ifrom == 102:  #模板新建
                    callback["self"][unionID] = info
                elif ifrom == 103:  #转移的作品
                    callback["self"][unionID] = info
                elif ifrom == 104:  #购买的作品
                    callback["buy"][unionID] = info
        return callback

    return None


#审核作品
def SHWork(DB, uid, pid, state):

    if state == 0:
        state = 3
    else:
        state = 2

    sql = "update tb_xr_worklocal set state = "+str(state) + " where uid = " + str(uid) + " and pid = " + str(pid)
    data = DB.edit(sql,None)
    if data:
        return True
    return False


def PushInMarket(DB,uid,pid):

    #data = GetData(DB, 0, 0, uid, pid, 0)
    workVersion = 1
    state = 0
    mdata = GetData(DB, 0, 0, uid, pid, 1)
    if mdata:
        workVersion = mdata["version"] + 1
        state = mdata["state"]
        sql = "delete from tb_xr_workmarket where uid = " + str(uid) + " and pid = " + str(pid)
        DB.edit(sql,None)
    #市场中插入这个作品
    sql = "insert into tb_xr_workmarket (UID,PID,WNAME,CDATE,`FROM`,SID,VERSION,STATE,PUID,PPID,platforms,tabs,price,classify) select " + str(uid) + "," + str(pid) + ",workname,'" + str(int(time.time())) + "',0,SID,"+str(workVersion)+","+str(state)+",0,0,platforms,tabs,price,classify FROM tb_xr_worklocal WHERE UID = " \
                "'" + str(uid) + "' AND PID = '" + str(pid) + "' limit 0,1;"
    code = DB.edit(sql,None)
    if not code:
        return 0

    #资源数据
    tablename = Global.GetMXRObjTableName(uid,pid)
    sourse_table =  Global.GetXRObjTableName(uid,pid)
    if mdata:
        sql = "delete from "+tablename
        DB.edit(sql,None)
    else:
        sql = "create table " + tablename + " like tb_xr_obj"
        DB.edit(sql, None)
    sql = "insert into " + tablename + " (ObjID,objName,CreateDate,ResType,ComID,Version,state,posx,posy,posz,rotex,rotey,rotez,scalex,scaley,scalez,fullview,Commonts,sizeDeltax,sizeDeltay,Content,Collider,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10) select ObjID,objName,'" + str(
        int(time.time())) + "',ResType,ComID,1,state,posx,posy,posz,rotex,rotey,rotez,scalex,scaley,scalez,fullview,Commonts,sizeDeltax,sizeDeltay,Content,Collider,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 from " + sourse_table + ";"
    code = DB.edit(sql, None)
    if not code:
        return -1

    if not mdata:
        #这里把数据插入到排序表中
        sql = "insert into tb_xr_workmarketsort (uid,wid,wname,sort) select uid,pid,workname,0 from tb_xr_worklocal where uid = " + str(uid) + " and pid = " + str(pid) + " limit 0,1"
        DB.edit(sql, None)
    return 1