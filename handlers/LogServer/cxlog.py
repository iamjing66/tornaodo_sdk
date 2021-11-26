#!/usr/bin/env python
# coding=utf-8


import json
from handlers.base import BaseHandler
from methods.DBManager import DBManager
from handlers.kbeServer.Editor.redis.interface_user import globalRedisU
import logging



class WriteUserHanhler(BaseHandler):

    def Get(self):

        # suser = self.get_argument("user")
        # print(suser)
        # DB = DBManager()
        # sql = "update log_user set `user` = '"+suser+"' where ID = 1 limit 0,1"
        # DB.edit(sql,None)
        # DB.close()

        self.write("OK")




class writeLogHandler(BaseHandler):    #继承base.py中的类BaseHandler

    #课程列表
    def get(self):

        suser = self.get_argument("user")
        print(suser)
        DB = DBManager()
        sql = "update log_user set `user` = '"+suser+"' where ID = 1"
        DB.edit(sql,None)
        DB.close()


        # uid = self.get_argument("uid")
        # username = self.get_argument("username")
        # #print("username",username,type(username))
        #
        # #print("============================================================")
        # # print(type(uid))
        # if uid == "":
        #     uid = "0"
        # ip = self.get_argument("ip")
        # apptype = self.get_argument("apptype")
        # cdate = self.get_argument("cdate")
        # title = self.get_argument("title")
        # comments = self.get_argument("comments")
        # servertype = self.get_argument("stype")
        # if "'" in username:
        #     username = comments
        # sql_str = "INSERT INTO `cxlog_com`(`UID`,`USERNAME`,`IP`,`CDATE`,`LOG_TITLE`,`LOG_COMMENTS`,`APPTYPE`,`SERVERTYPE`) values ("+uid+",'"+username+"','"+ip+"','"+cdate+"','"+title+"','"+comments+"','"+apptype+"','"+servertype+"');"
        # #print("sql_str",sql_str)
        # self.Cur.execute(sql_str)
        # self.db.commit()

        self.write("OK")


    def post(self):

        json_back = {
            "id":"",
            "sub": "",
            "code":1,
            "data":""
        }

        post_data = json.loads(self.request.body.decode('utf-8'))
        print("post_data - :",post_data)

        UID = post_data["UID"]
        USERNAME = post_data["USERNAME"]
        OUTIP = post_data["OUTIP"]
        LOCALIP = post_data["LOCALIP"]
        CODE = int(post_data["CODE"])
        SUB = post_data["SUB"]
        BODY = post_data["BODY"].replace('\'','')

        json_back["id"] = str(CODE)
        json_back["sub"] = SUB

        DB = DBManager()
        # 插入
        if CODE == 100 or CODE == 99 or CODE == 98:
            sql = "select ID from log_machine where OUT_IP = '"+str(OUTIP)+"' and LOCAL_IP = '"+LOCALIP+"'"
            data = DB.fetchone(sql,None)
            adata = BODY.split("$")
            sql1 = ""
            if data:
                if CODE == 100:
                    sql1 = "update log_machine SET LOCAL_IP = '"+LOCALIP+"'" + ",FULLM='"+BODY+"',FULLCPU='',FREEM='',FREECPU='',FREEDISK='',FULLDISK='',DATE=CURRENT_TIMESTAMP() WHERE ID = "+str(data[0])
                elif CODE == 99:
                    sql1 = "update log_machine SET NETBODY = '"+adata[0]+"'" +" WHERE ID = "+str(data[0])
                elif CODE == 98:
                    sql1 = "update log_machine SET USERNAME = '"+adata[0]+"'" +" WHERE ID = "+str(data[0])
            else:
                if CODE == 100:
                    sql1 ="INSERT INTO log_machine (LOCAL_IP,OUT_IP,FULLM,FULLCPU,FREEM,FREECPU,FREEDISK,FULLDISK)VALUE ('"+LOCALIP+"','"+OUTIP+"','','','','','','')"
            if sql1:
                DB.edit(sql1,None)

        if CODE == 100:

            calldata = ""
            arr = globalRedisU.redis_configure_get()
            if arr:
                for info in arr:
                    if info == (OUTIP+"$"+LOCALIP):
                        calldata += "1$"
                    else:
                        calldata += "0$"
            else:
                calldata = "0$0$0$0$0$"
            json_back["data"] = calldata
        else:
            DESC = post_data["DESC"].replace('\'','')
            PAM = post_data["PAM"].replace('\'','')

            logging.info("[UserLog] code = "+str(CODE) + ",USERNAME = "+USERNAME + ",UID = " + str(UID) + ",BODY = " + BODY + " , DESC = " + DESC + " PAM = " + PAM)

            if CODE == 200:
                sql = "insert into log_qidong (CODE,BODY,`DESC`,PAM)VALUE('"+SUB+"','"+BODY+"','"+DESC+"','"+PAM+"')"
            elif CODE == 300:
                sql = "insert into log_dating (CODE,BODY,`DESC`,PAM)VALUE('"+SUB+"','"+BODY+"','"+DESC+"','"+PAM+"')"
            elif CODE == 400:
                sql = "insert into log_kecheng (CODE,BODY,`DESC`,PAM)VALUE('"+SUB+"','"+BODY+"','"+DESC+"','"+PAM+"')"
            if sql:
                DB.edit(sql,None)
        DB.close()
        print("[log]->json_back = " , json_back)
        self.write(json_back)
