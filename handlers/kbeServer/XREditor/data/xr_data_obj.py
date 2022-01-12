import json
import time

import requests

import Global
from handlers.kbeServer.Editor.Interface import interface_global
import application
import logging



def Update(DB,UID,PID,MARKET,obj):

    if MARKET == 0:
        sourse_table = Global.GetXRObjTableName(UID,PID)
    else:
        sourse_table = Global.GetMXRObjTableName(UID,PID)


    #解析obj
    spdata = ""
    spfirst = obj.split('|')
    for str in spfirst:
        spcen = str.split('`')
        print("spcen = " , spcen)
        print("spcen[13] = ",spcen[13])
        print("spcen[14] = ", spcen[14])
        #`ObjID`,`objName`,`CreateDate`,`Posx`,`Posy`,`Posz`,`Rotex`,`Rotey`,`Rotez`,`Scalex`,`Scaley`,
        # `Scalez`,`state`,`fullview`,`Commonts`,`ResType`,`ComID`,`sizeDeltax`,`sizeDeltay`,`Content`,`Collider`,`Version`,
        # `p1`,`p2`,`p3`,`p4`,`p5`,`p6`,`p7`,`p8`,`p9`,`p10`

        #需要更新的数据
        #20`3D1`1641376196`0`0`0`0`0`0`1`1`1`0```1`1`9`9``0`1``````````|5`3D2`1641376196`0`0`0`0`0`0`2`2`2`1```1`2`8`8``1`2``````````

        msg = "("+spcen[0]+",'"+spcen[1]+"','"+spcen[2]+"',"+spcen[3]+","+spcen[4]+","+spcen[5]+","+spcen[6]+","+spcen[7]+","+spcen[8]+","+spcen[9]+","+spcen[10]+"," \
        ""+spcen[11]+","+spcen[12]+",'"+spcen[13]+"','"+spcen[14]+"',"+spcen[15]+","+spcen[16]+","+spcen[17]+","+spcen[18]+",'"+spcen[19]+"',"+spcen[20]+",'"+spcen[21]+"'" \
        ",'"+spcen[22]+"','"+spcen[23]+"','"+spcen[24]+"','"+spcen[25]+"','"+spcen[26]+"','"+spcen[27]+"','"+spcen[28]+"','"+spcen[29]+"','"+spcen[30]+"','"+spcen[31]+"')"

        #sql = "insert into " + sourse_table + "(`ObjID`,`objName`,`CreateDate`,`Posx`,`Posy`,`Posz`,`Rotex`,`Rotey`,`Rotez`,`Scalex`,`Scaley`,`Scalez`,`state`,`fullview`,`Commonts`,`ResType`,`ComID`,`sizeDeltax`,`sizeDeltay`,`Content`,`Collider`,`Version`,`p1`,`p2`,`p3`,`p4`,`p5`,`p6`,`p7`,`p8`,`p9`,`p10`) values " + spdata

        if spdata == "":
            spdata = msg
        else:
            spdata = spdata + "," + msg


    sql = "replace into "+sourse_table + "(`ObjID`,`objName`,`CreateDate`,`Posx`,`Posy`,`Posz`,`Rotex`,`Rotey`,`Rotez`,`Scalex`,`Scaley`,`Scalez`,`state`,`fullview`,`Commonts`,`ResType`,`ComID`,`sizeDeltax`,`sizeDeltay`,`Content`,`Collider`,`Version`,`p1`,`p2`,`p3`,`p4`,`p5`,`p6`,`p7`,`p8`,`p9`,`p10`) values "+spdata
    data = DB.edit(sql,None)
    if data:
        return 1
    return 0



def GetVersion(DB,UID,PID,MARKET):

    callback = ""

    if MARKET == 0:
        sourse_table = Global.GetXRObjTableName(UID,PID)
    else:
        sourse_table = Global.GetMXRObjTableName(UID,PID)


    sql = "select COMID,VERSION from " + sourse_table
    data = DB.fetchall(sql,None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            if callback == "":
                callback = str(minfo[0])+"`"+str(minfo[1])
            else:
                callback = callback + "|" + str(minfo[0]) + "`" + str(minfo[1])

    return callback