import Global
import logging
from handlers.kbeServer.Editor.Interface import interface_global

#点赞
def DoMsg_Dianzan(DB ,self_uid,uid ,wid ,lid ,siscid ,tid ,dian ,ctype):
    # DEBUG_MSG("Msg_Dianzan : %d - %d - %d - %d - %d - %s" % (uid, wid, tid, dian,lid,siscid))
    #logging.info("Dianzan - uid[%i],wid[%i],lid[%i],siscid[%s],tid[%i],dian[%i],ctype[%i]",(uid ,wid ,lid ,siscid ,tid ,dian ,ctype))
    #print("dianzan,",uid ,wid ,lid ,siscid ,tid ,dian ,ctype)
    if ctype == 0:
        table_name = Global.GetWorkZanTableName(uid ,wid)
    elif ctype == 1:
        table_name = Global.GetCourseZanTableName(uid ,wid ,lid)
    else:
        table_name = Global.GetSisZanTableName(siscid)

    # table_name = "tb_work_zan_" + str(uid) + "_" + str(wid)

    sql = "select zan from " + table_name + " where UID = " + str(self_uid) + " and TID = " + str(tid) + ";"
    data = DB.fetchone(sql,None)
    _zan = -1
    if data:
        _zan = int(data[0])
        # DEBUG_MSG("Msg_Dianzan : %d - %d " % (dian, _zan))
    if dian == 0:
        # 取消点赞
        if _zan != 1:
            return 0
    else:
        if _zan == 1:
            return -1
            # DEBUG_MSG("Msg_Dianzan 1 : %d - %d " % (dian, _zan))
    sql = ""
    if _zan == -1:
        sql = "Insert into " + table_name + " (UID,TID,ZAN) values (" + str(self_uid) + "," + str(tid) + ",1);"
    elif dian == 0:
        sql = "update " + table_name + " set zan = 0 where uid = " + str(self_uid) + " and TID = " + str(tid) + ";"
    else:
        sql = "update " + table_name + " set zan = 1 where uid = " + str(self_uid) + " and TID = " + str(tid) + ";"
    DB.edit(sql,None)

    return tid
    #self.client.App_MsgToClient(101, str(tid))


#作品评分/评论
#wid 作品ID
#uid 作者ID
#score 评分 >0 的整形
# log 如果无内容表示评分 有内容表示评论
#P_UID 不为0 表示回复消息
#s_lid 课时ID
#ctype 评论分类 0-作品 1-市场的课程 2-SIS课程

def DoWorkMark(DB,self_uid,s_wid,s_lid,uid,score,log,P_UID,ctype):

    wid = 0
    lid = 0
    sis_cid = ""
    if ctype == 0:
        wid = int(s_wid)
    elif ctype == 1:
        wid = int(s_wid)
        lid = s_lid
    else:
        sis_cid = s_wid

    if score < 0:
        return 0

    if ctype == 0:
        table_name = Global.GetWorkLogTableName(uid,wid)
    elif ctype == 1:
        table_name = Global.GetCourseLogTableName(uid,wid,lid)
    else:
        table_name = Global.GetSisLogTableName(sis_cid)

    _exist = interface_global.Global_TableExist(table_name,DB)
    if not _exist:
        data = DB.callprocAll('CreateWorkLogTable', (uid,wid,lid,ctype,sis_cid))
        if data:
            code = int(data[0])
            if code == 0:
                return -1  #作品不存在

        DB.callprocAll('CreateWorkZanTable', (uid, wid,lid,ctype,sis_cid))

    _succ = 0
    if score > 0:

        if ctype == 0 or ctype == 1:
            if uid == self_uid:
                return -3  #作品不存在

        _succ = 1
        sql = "select ID,score from "+table_name+" where UID = "+str(self_uid) + " and log = '';"

        data = DB.fetchone(sql,None)

        _score = 0
        _id = 0
        if data:
            _id = int(data[0])
            _score = int(data[1])
            if _id > 0 and _score > 0:
                return -2  # 已经评过分


        if _id == 0:
            sql = "Insert into "+table_name+" (UID,score,log) values ("+str(self_uid)+","+str(score)+",'');"
        else:
            sql = "update " + table_name + " set score = "+str(score) + " where ID = "+str(_id)
        DB.edit(sql,None)
        # 转发消息
        # self.SendMsgOnLine(0, 1, _author_name, _work_name)
        # self.SendMsgOnLine(1, 1, _author_name, _work_name)

    if len(log) > 0:
        _succ = 2
        sql = "Insert into " + table_name + " (UID,score,log,PID) values (" + str(self_uid) + ",0,'"+log+"',"+str(P_UID)+");"
        DB.edit(sql,None)

        # 转发消息
        # self.SendMsgOnLine(0,2,_author_name,_work_name)
        # self.SendMsgOnLine(1, 2, _author_name, _work_name)

    return _succ


#获取 作品评分数据
def DoWorkScoreData(DB,self_uid,wid,lid,uid,sis_cid,ctype):

    _base_string = ""


    #table_name = "tb_work_log_" + str(uid) + "_" + str(wid)
    if ctype == 0:
        table_name = Global.GetWorkLogTableName(uid,wid)
    elif ctype == 1:
        table_name = Global.GetCourseLogTableName(uid,wid,lid)
    else:
        table_name = Global.GetSisLogTableName(sis_cid)

    _exist = interface_global.Global_TableExist(table_name,DB)

    _pf = 0
    if _exist:
        sql = "select score from  " + table_name + " where LOG = '' and uid = " + str(self_uid) + ";"

        data = DB.fetchone(sql,None)
        if data:
            _pf = int(data[0])
    else:
        _pf = 0

    if ctype == 0 or ctype == 1:
        sql = "select UserName,NickName,NickUrl from tb_userdata where uid = " + str(uid)

        data = DB.fetchone(sql,None)
        if data:
            _base_string = data[0] + "$" + data[1] + "$" + data[2] + "$" + str(_pf)
    else:
        _base_string = "Feidie$飞蝶VR$$" + str(_pf)

        #DEBUG_MSG(_base_string)

    _score_data = ""
    if _exist:
        sql = "select count(ID),1 from " + table_name + " where log = '' AND SCORE = 1 union ALL select count(ID),2 from " + table_name + " where log = '' AND SCORE = 2 union ALL select count(ID),3 from " + table_name + " where log = '' AND SCORE = 3 union ALL select count(ID),4 from " + table_name + " where log = '' AND SCORE = 4 union ALL select count(ID),5 from " + table_name + " where log = '' AND SCORE = 5;"
        data = DB.fetchall(sql,None)
        if data:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)

                if _score_data == "":
                    _score_data = str(minfo_list[1]) + "," + str(minfo_list[0])
                else:
                    _score_data = _score_data + "&" + str(minfo_list[1]) + "," + str(minfo_list[0])

    _send_data = _base_string + "@" + _score_data

    return _send_data



#获取评论数据
def DoWorkLogData(DB,self_uid,wid,lid, uid, sis_cid, PID , ipage , ilenght,ctype):

    _base_string = ""
    _url_string = ""

    if ctype == 0:
        table_name = Global.GetWorkLogTableName(uid,wid)
    elif ctype == 1:
        table_name = Global.GetCourseLogTableName(uid,wid,lid)
    else:
        table_name = Global.GetSisLogTableName(sis_cid)

    #table_name1 = "tb_work_zan_" + str(uid) + "_" + str(wid)
    if ctype == 0:
        table_name1 = Global.GetWorkZanTableName(uid,wid)
    elif ctype == 1:
        table_name1 = Global.GetCourseZanTableName(uid,wid,lid)
    else:
        table_name1 = Global.GetSisZanTableName(sis_cid)

    _exist = interface_global.Global_TableExist(table_name,DB)

    sql1 = ""

    if _exist:
        if ipage == 0:
            if PID == 0:
                sql = "select t1.log,t1.`Date`,t2.UserName,t2.NickName,t2.UID,t1.ID,(SELECT COUNT(ID) FROM " + table_name + " WHERE PID = t1.ID) AS HF,(SELECT COUNT(ID) FROM " + table_name1 + " WHERE TID = t1.ID AND ZAN = 1) AS ZAN,(select zan from " + table_name1 + " where UID = " + str(self_uid) + " and TID  = t1.ID) as IsZan from " + table_name + " as t1 inner join tb_userdata as t2 on t1.uid = t2.uid and t1.log != '' AND T1.PID = 0 order by t1.`Date` desc;"
                sql1 = "select UID,NickUrl from tb_userdata where uid in ( select UID from " + table_name + " WHERE LOG != '' AND PID = 0 GROUP BY UID );"
            else:
                sql = "select t1.log,t1.`Date`,t2.UserName,t2.NickName,t2.UID,t1.ID,(SELECT COUNT(ID) FROM " + table_name + " WHERE PID = t1.ID) AS HF,(SELECT COUNT(ID) FROM " + table_name1 + " WHERE TID = t1.ID AND ZAN = 1) AS ZAN,(select zan from " + table_name1 + " where UID = " + str(self_uid) + " and TID  = t1.ID) as IsZan from " + table_name + " as t1 inner join tb_userdata as t2 on t1.uid = t2.uid and t1.log != '' AND T1.PID = " + str(PID) + " order by t1.`Date` desc;"
                sql1 = "select UID,NickUrl from tb_userdata where uid in ( select UID from " + table_name + " WHERE LOG != '' AND PID = " + str(PID) + " GROUP BY UID );"
        else:
            if PID == 0:
                sql = "select t1.log,t1.`Date`,t2.UserName,t2.NickName,t2.UID,t1.ID,(SELECT COUNT(ID) FROM " + table_name + " WHERE PID = t1.ID) AS HF,(SELECT COUNT(ID) FROM " + table_name1 + " WHERE TID = t1.ID AND ZAN = 1) AS ZAN,(select zan from " + table_name1 + " where UID = " + str(self_uid) + " and TID  = t1.ID) as IsZan from " + table_name + " as t1 inner join tb_userdata as t2 on t1.uid = t2.uid and t1.log != '' AND T1.PID = 0 order by t1.`Date` desc limit " + str((ipage - 1) * ilenght) + "," + str(ilenght) + ";"
                sql1 = "select UID,NickUrl from tb_userdata where uid in ( select UID from " + table_name + " WHERE LOG != '' AND PID = 0 GROUP BY UID );"
            else:
                sql = "select t1.log,t1.`Date`,t2.UserName,t2.NickName,t2.UID,t1.ID,(SELECT COUNT(ID) FROM " + table_name + " WHERE PID = t1.ID) AS HF,(SELECT COUNT(ID) FROM " + table_name1 + " WHERE TID = t1.ID AND ZAN = 1) AS ZAN,(select zan from " + table_name1 + " where UID = " + str(self_uid) + " and TID  = t1.ID) as IsZan from " + table_name + " as t1 inner join tb_userdata as t2 on t1.uid = t2.uid and t1.log != '' AND T1.PID = " + str(PID) + " order by t1.`Date` desc limit " + str((ipage - 1) * ilenght) + "," + str(ilenght) + ";"
                sql1 = "select UID,NickUrl from tb_userdata where uid in ( select UID from " + table_name + " WHERE LOG != '' AND PID = " + str(PID) + " GROUP BY UID );"
            # sql = "select t1.log,t1.`Date`,t2.UserName,t2.TheName,t2.UID from " + table_name + " as t1 inner join tb_userdata as t2 on t1.uid = t2.uid and t1.log != '' order by t1.`Date` desc limit "+str((ipage-1)*ilenght)+","+str(ilenght)+";"
            # sql1 = "select UID,NickUrl from tb_userdata where uid in ( select UID from " + table_name + " WHERE LOG != '' GROUP BY UID ) limit "+str((ipage-1)*ilenght)+","+str(ilenght)+";"

        data = DB.fetchall(sql,None)
        if data:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)

                _ZAN_NUM = 0
                if minfo_list[7] != None:
                    _ZAN_NUM = minfo_list[7]
                _ZAN = 0
                if minfo_list[8] != None:
                    _ZAN = minfo_list[8]

                if _base_string == "":
                    _base_string = minfo_list[0] + "@lyyym@" + str(minfo_list[1]) + "@lyyym@" + minfo_list[2] + "@lyyym@" + minfo_list[3] + "@lyyym@" + str(minfo_list[4]) + "@lyyym@" + str(minfo_list[5]) + "@lyyym@" + str(minfo_list[6]) + "@lyyym@" + str(_ZAN_NUM) + "@lyyym@" + str(_ZAN)
                else:
                    _base_string = _base_string + "@lyyyym@" + minfo_list[0] + "@lyyym@" + str(minfo_list[1]) + "@lyyym@" + minfo_list[2] + "@lyyym@" + minfo_list[3] + "@lyyym@" + str(minfo_list[4]) + "@lyyym@" + str(minfo_list[5]) + "@lyyym@" + str(minfo_list[6]) + "@lyyym@" + str(_ZAN_NUM) + "@lyyym@" + str(_ZAN)


        data = DB.fetchall(sql1,None)
        if data:
            list_data = list(data)
            for minfo in list_data:
                minfo_list = list(minfo)

                if _url_string == "":
                    _url_string = str(minfo_list[0]) + "@lyyym@" + minfo_list[1]
                else:
                    _url_string = _url_string + "@lyyyym@" + str(minfo_list[0]) + "@lyyym@" + minfo_list[1]


    _send_string = _url_string + "@lyyyyym@" + _base_string

    return _send_string