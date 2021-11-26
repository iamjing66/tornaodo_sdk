#!/usr/bin/env python
# coding=utf-8
import logging


def GetUpdateVersion(DB,UID,pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    operateType = ""
    SqlID = ""
    if pam == "":
        #0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        json_data["code"] = "0"
        json_data["msg"] = "false"
        return json_data
    versions = pam["pam"].split(',')
    table_project = "tb_res_version"
    # TODO
    # sql_str = "select VERSION,OPENCODE from tb_res_version where OPENCODE in %s" % (pam["pam"])
    if len(versions) == 4:
        sql_str = "select VERSION,OPENCODE  from " + table_project + " where OPENCODE in (105,106,107,125)"
    elif len(versions) == 5:
        sql_str = "select VERSION,OPENCODE  from " + table_project + " where OPENCODE in (105,106,107,112,125)"
    elif len(versions) == 8:
        sql_str = "select VERSION,OPENCODE  from " + table_project + " where OPENCODE in (105,106,107,111,112,116,117,125)"
    else:
        sql_str = "select VERSION,OPENCODE  from " + table_project
    data = DB.fetchall(sql_str,None)
    _cback = ""
    _cback2 = ""
    index = 0
    _Minfo = ""
    _Minfo2 =""
    ##print("data:",data)
    if data:
        list_data = list(data)
        for minfo in list_data:

            if versions[index] != str(minfo[0]):
                _Minfo = str(minfo[1])
                _Minfo2 = versions[index]
            else:
                _Minfo = "-"
                _Minfo2 = "-"
            if _cback2 != "":
                _cback2 = _cback2+"," + _Minfo2
            else:
                _cback2 = _Minfo2

            if _cback != "":
                _cback = _cback + "," + _Minfo
            else:
                _cback = _Minfo
            index = index+1

        _cback = _cback+"*"+ _cback2
    json_data["code"] = "1"
    json_data["msg"] = _cback
    #print("json_data:", json_data)
    return json_data


def new_get_update_version(DB, pam):
    json_data = {"code": 0, "msg": ""}
    if pam == "":
        # 101,102,103,104,....
        json_data["msg"] = "false"
        return json_data
    sql_else = ";"
    if pam["pam"]:
        sql_else = " where OPENCODE in (" + pam["pam"] + ");"
    sql_str = "select VERSION from tb_res_version" + sql_else
    logging.info("version sql = %s" % sql_str)
    data = DB.fetchall(sql_str, None)
    _cback = ""
    _backlist = []
    if data:
        for i in data:
            _backlist.append(str(i[0]))
        _cback = ",".join(_backlist)
    json_data["code"] = 1
    json_data["msg"] = _cback
    logging.info("json_data = %s" % json_data)
    return json_data


def AnlyzeCode(DB,UID,Pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if Pam == "":
        json_data["code"] = "0"
        json_data["msg"] = "false"
        return json_data
    json_data =DoCode(DB,Pam["code"],Pam["page"],Pam["version"])
    return json_data


def new_anlyze_code(DB, Pam):
    json_data = {
        "code": 0,
        "msg": ""
    }
    if Pam == "":
        json_data["msg"] = "false"
        return json_data
    json_data = new_do_code(DB, Pam["code"], Pam["page"], Pam["version"])
    return json_data


def DoCode(DB,OpenCode,page,version):
    json_data = {
        "code": 0,
        "msg": ""
    }

    table_project = ""
    sql_str = ""
    _cback = ""
    _getresAll = "1"
    if OpenCode == "101":
        table_project = "tb_ft_res"
        sql_str = "select FID,FNAME,KSClass from " + table_project + GetLimit(page)
    elif OpenCode == "102":
        table_project = "tb_st_res"
        sql_str = "select SID,SNAME,PID from " + table_project + GetLimit(page)
    elif OpenCode == "103":
        table_project = "tb_ft_scene"
        sql_str = "select FID,FNAME from " + table_project + GetLimit(page)
    elif OpenCode == "104":
        table_project = "tb_ft_audio"
        sql_str = "select FID,FNAME from " + table_project + GetLimit(page)
    elif OpenCode == "105" or OpenCode == "205":
        minVersion = GetUpdateResMinVersion(DB,"105", version)
        table_project = "tb_config_res"
        if minVersion != "0":
            if int(version) < int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            elif int(version) > int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            else:
                _getresAll = "0"
                ResID = GetUpdateResData(DB,"105", version)
                sql_str = "select * from " + table_project + "  where  RID in (" + ResID + ")" + GetLimit(page)
        else:
            sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "106" or OpenCode == "206":
        minVersion = GetUpdateResMinVersion(DB,"106", version)
        table_project = "tb_config_scene"
        if minVersion != "0":
            if int(version) < int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            elif int(version) > int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            else:
                _getresAll = "0"
                ResID = GetUpdateResData(DB,"106", version)
                sql_str = "select * from " + table_project + "  where  RID in (" + ResID + ")" + GetLimit(page)
        else:
            sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "107"  or OpenCode == "207" :
        minVersion = GetUpdateResMinVersion(DB,"107", version)
        table_project = "tb_config_audio"
        if minVersion != "0":
            if int(version) < int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            if int(version) > int(minVersion):
                _getresAll = "1"
                sql_str = "select * from " + table_project + GetLimit(page)
            else:
                _getresAll = "0"
                ResID = GetUpdateResData(DB,"107", version)
                sql_str = "select * from " + table_project + "  where  RID in (" + ResID + ")" + GetLimit(page)
        else:
            sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "108":
        table_project = "tb_config_vip"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "109":
        table_project = "tb_config_coursedata"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "110":
        table_project = "tb_config_left_res"
        sql_str = "select * from " + table_project + GetLimit(page)
    # elif OpenCode == "111":
    #     table_project = "tb_course_type"
    #     sql_str = "select t2.ct, t1.TypeName, t1.cIconPath,t2.UID, t2.CID from tb_course_type t1 inner join tb_course_sort t2 on t1.CID = t2.ct and t2.visible = 0 group by t2.UID, t1.Sort, t2.sort order by t1.Sort, t2.sort"
    elif OpenCode == "111":
        table_project = "tb_course_type"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "112":
        table_project = "tb_work_type"
        sql_str = "select * from " + table_project + " order by Sort"
    elif OpenCode == "113":
        table_project = "tb_crclass_res"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "114":
        table_project = "tb_star_level"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "115":
        table_project = "tb_framer_level"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "116":
        table_project = "tb_channel"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "117":
        table_project = "tb_discount"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "118":
        table_project = "tb_new_vip"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "119":
        table_project = "tb_new_vipdiscount"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "120":
        table_project = "tb_new_suffix"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "121":
        table_project = "tb_new_config"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "122":
        table_project = "tb_config_subject"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "123":
        table_project = "tb_config_class"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "124":
        table_project = "tb_config_section"
        sql_str = "select * from " + table_project + GetLimit(page)
    elif OpenCode == "125":
        table_project = "tb_config_skybox"
        sql_str = "select * from " + table_project + GetLimit(page)

    data = DB.fetchall(sql_str,None)
    _cback = GetSqlData(OpenCode,data)
    version = GetCodeVersion(DB,str(OpenCode))
    _cback =str(OpenCode)+ "*" + str(_cback) + "*" + str(version) + "*" + str(page)+  "*" + str(_getresAll)
    json_data["code"] = 1
    json_data["msg"] = _cback
    return  json_data


def new_do_code(DB, OpenCode, page, version):
    json_data = {
        "code": 0,
        "msg": ""
    }

    table_project = ""
    sql_str = ""
    _cback = ""
    _getresAll = "1"
    if OpenCode == "101":
        table_project = "tb_ft_res"
        sql_str = "select FID,FNAME,KSClass from " + table_project
    elif OpenCode == "102":
        table_project = "tb_st_res"
        sql_str = "select SID,SNAME,PID from " + table_project
    elif OpenCode == "103":
        table_project = "tb_ft_scene"
        sql_str = "select FID,FNAME from " + table_project
    elif OpenCode == "104":
        table_project = "tb_ft_audio"
        sql_str = "select FID,FNAME from " + table_project
    elif OpenCode == "105" or OpenCode == "205":
        minVersion = GetUpdateResMinVersion(DB, "105", version)
        table_project = "tb_config_res"
        sql_str = "select * from " + table_project + GetLimit(page)
        if minVersion != "0" and int(version) == int(minVersion):
            _getresAll = "0"
            ResID = GetUpdateResData(DB, "105", version)
            sql_str = "select * from " + table_project + " where RID in (" + ResID + ")" + GetLimit(page)
    elif OpenCode == "106" or OpenCode == "206":
        minVersion = GetUpdateResMinVersion(DB, "106", version)
        table_project = "tb_config_scene"
        sql_str = "select * from " + table_project + GetLimit(page)
        if minVersion != "0" and int(version) == int(minVersion):
            _getresAll = "0"
            ResID = GetUpdateResData(DB, "106", version)
            sql_str = "select * from " + table_project + " where RID in (" + ResID + ")" + GetLimit(page)
    elif OpenCode == "107" or OpenCode == "207":
        minVersion = GetUpdateResMinVersion(DB, "107", version)
        table_project = "tb_config_audio"
        sql_str = "select * from " + table_project + GetLimit(page)
        if minVersion != "0" and int(version) == int(minVersion):
            _getresAll = "0"
            ResID = GetUpdateResData(DB, "107", version)
            sql_str = "select * from " + table_project + " where RID in (" + ResID + ")" + GetLimit(page)
    elif OpenCode == "108":
        table_project = "tb_config_vip"
        sql_str = "select * from " + table_project
    elif OpenCode == "109":
        table_project = "tb_config_coursedata"
        sql_str = "select * from " + table_project
    elif OpenCode == "110":
        table_project = "tb_config_left_res"
        sql_str = "select * from " + table_project
    elif OpenCode == "111":
        sql_str = "select t2.ct, t1.TypeName, t1.cIconPath,t2.UID, t2.CID from tb_course_type t1 inner join tb_course_sort t2 on t1.CID = t2.ct and t2.visible = 0 group by t2.UID, t1.Sort, t2.sort order by t1.Sort, t2.sort"
    elif OpenCode == "112":
        table_project = "tb_work_type"
        sql_str = "select * from " + table_project + " order by Sort"
    elif OpenCode == "113":
        table_project = "tb_crclass_res"
        sql_str = "select * from " + table_project
    elif OpenCode == "114":
        table_project = "tb_star_level"
        sql_str = "select * from " + table_project
    elif OpenCode == "115":
        table_project = "tb_framer_level"
        sql_str = "select * from " + table_project
    elif OpenCode == "116":
        table_project = "tb_channel"
        sql_str = "select * from " + table_project
    elif OpenCode == "117":
        table_project = "tb_discount"
        sql_str = "select * from " + table_project
    elif OpenCode == "118":
        table_project = "tb_new_vip"
        sql_str = "select * from " + table_project
    elif OpenCode == "119":
        table_project = "tb_new_vipdiscount"
        sql_str = "select * from " + table_project
    elif OpenCode == "120":
        table_project = "tb_new_suffix"
        sql_str = "select * from " + table_project
    elif OpenCode == "121":
        table_project = "tb_new_config"
        sql_str = "select * from " + table_project
    elif OpenCode == "122":
        table_project = "tb_config_subject"
        sql_str = "select * from " + table_project
    elif OpenCode == "123":
        table_project = "tb_config_class"
        sql_str = "select * from " + table_project
    elif OpenCode == "124":
        table_project = "tb_config_section"
        sql_str = "select * from " + table_project
    elif OpenCode == "125":
        table_project = "tb_config_skybox"
        sql_str = "select * from " + table_project

    data = DB.fetchall(sql_str, None)
    _cback = new_get_sql_data(OpenCode, data)
    version = GetCodeVersion(DB, str(OpenCode))
    _cback = "*".join([str(OpenCode), str(_cback), str(version), str(page), _getresAll])
    json_data["code"] = 1
    json_data["msg"] = _cback
    return json_data


def new_get_sql_data(OpenCode, data):
    _cback = ""
    _count = 0
    _backlist = []
    if data:
        for minfo in data:
            if _count < 500:
                if OpenCode == "101":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "102":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "103":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "104":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "105":
                    _backlist.append("`".join(
                        list(map(str, list(minfo[2:30]) + [minfo[1]] + list(minfo[30:])))))
                elif OpenCode == "106":
                    _backlist.append("`".join(
                        list(map(str, list(minfo[2:30]) + [minfo[1]] + list(minfo[30:])))))
                elif OpenCode == "107":
                    _backlist.append("`".join(
                        list(map(str, list(minfo[2:15]) + [minfo[1], minfo[15]]))))
                elif OpenCode == "108":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "109":
                    _backlist.append("`".join([str(i) for i in minfo[1:8]]))
                elif OpenCode == "110":
                    _backlist.append("`".join([str(i) for i in minfo[1:]]))
                elif OpenCode == "111":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "112":
                    _backlist.append("`".join([str(i) for i in minfo[1:5]]))
                elif OpenCode == "113":
                    _backlist.append("`".join([str(i) for i in minfo[1:]]))
                elif OpenCode == "114":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "115":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "116":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "117":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "118":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "119":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "120":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "121":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "122":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "123":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "124":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "125":
                    _backlist.append("`".join([str(i) for i in minfo]))
                elif OpenCode == "205":
                    _backlist.append("`".join([
                        str(minfo[2]),
                        str(minfo[14]),
                        str(minfo[15]),
                        str(minfo[32]),
                        str(minfo[33]),
                        str(minfo[34]),
                        str(minfo[30])
                    ]))
                elif OpenCode == "206":
                    _backlist.append("`".join([
                        str(minfo[2]),
                        str(minfo[15]),
                        str(minfo[14]),
                        str(minfo[31]),
                        str(minfo[32]),
                        str(minfo[33]),
                        str(minfo[13])
                    ]))
                elif OpenCode == "207":
                    _backlist.append("`".join(
                        [str(minfo[2]),
                         str(minfo[14]),
                         str(minfo[15])]))
            _count = _count + 1
        _cback = "^".join(_backlist)
    if _count < 500:
        _cback += "*1"
    else:
        _cback += "*0"
    return _cback


def GetSqlData(OpenCode,data):
    _cback = ""
    _count = 0
    if data:
        list_data = list(data)
        for minfo in list_data:
            if _count < 500:
                if OpenCode == "101":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                elif OpenCode == "102":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                elif OpenCode == "103":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1])
                elif OpenCode == "104":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1])
                elif OpenCode == "105":

                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4]) + "`" + str(
                            minfo[5]) + "`" + str(minfo[6]) + "`" + str(minfo[7]) + "`" + str(minfo[8]) + "`" + str(
                            minfo[9]) + "`" + str(minfo[10]) + "`" + str(minfo[11]) + "`" + str(minfo[12]) + "`" + str(
                            minfo[13]) + "`" + str(minfo[14]) + "`" + str(minfo[15]) + "`" + str(minfo[16]) + "`" + str(
                            minfo[17]) + "`" + str(minfo[18]) + "`" + str(minfo[19]) + "`" + str(minfo[20]) + "`" + str(
                            minfo[21]) + "`" + str(minfo[22]) + "`" + str(minfo[23]) + "`" + str(minfo[24]) + "`" + str(
                            minfo[25]) + "`" + str(minfo[26]) + "`" + str(minfo[27]) + "`" + str(minfo[28]) + "`" + str(
                            minfo[29]) + "`" + str(minfo[1]) + "`" + str(minfo[30]) + "`" + str(minfo[31]) + "`" + str(
                            minfo[32]) + "`" + str(minfo[33]) + "`" + str(minfo[34]) + "`" + str(minfo[35]) + "`" + str(
                            minfo[36])
                    else:
                        _cback = str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4]) + "`" + str(
                            minfo[5]) + "`" + str(minfo[6]) + "`" + str(minfo[7]) + "`" + str(minfo[8]) + "`" + str(
                            minfo[9]) + "`" + str(minfo[10]) + "`" + str(minfo[11]) + "`" + str(
                            minfo[12]) + "`" + str(
                            minfo[13]) + "`" + str(minfo[14]) + "`" + str(minfo[15]) + "`" + str(
                            minfo[16]) + "`" + str(
                            minfo[17]) + "`" + str(minfo[18]) + "`" + str(minfo[19]) + "`" + str(
                            minfo[20]) + "`" + str(
                            minfo[21]) + "`" + str(minfo[22]) + "`" + str(minfo[23]) + "`" + str(
                            minfo[24]) + "`" + str(
                            minfo[25]) + "`" + str(minfo[26]) + "`" + str(minfo[27]) + "`" + str(
                            minfo[28]) + "`" + str(
                            minfo[29]) + "`" + str(minfo[1]) + "`" + str(minfo[30]) + "`" + str(
                            minfo[31]) + "`" + str(
                            minfo[32]) + "`" + str(minfo[33]) + "`" + str(minfo[34]) + "`" + str(
                            minfo[35]) + "`" + str(
                            minfo[36])
                elif OpenCode == "106":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(
                            minfo[15]) + "`" + str(minfo[16]) + "`" + str(minfo[17]) + "`" + str(
                            minfo[18]) + "`" + str(
                            minfo[19]) + "`" + str(minfo[20]) + "`" + str(minfo[21]) + "`" + str(
                            minfo[22]) + "`" + str(
                            minfo[23]) + "`" + str(minfo[24]) + "`" + str(minfo[25]) + "`" + str(
                            minfo[26]) + "`" + str(
                            minfo[27]) + "`" + str(minfo[28]) + "`" + str(minfo[29]) + "`" + str(
                            minfo[1]) + "`" + str(
                            minfo[30]) + "`" + str(
                            minfo[31]) + "`" + str(minfo[32]) + "`" + str(minfo[33])
                    else:
                        _cback = str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(
                            minfo[15]) + "`" + str(minfo[16]) + "`" + str(minfo[17]) + "`" + str(
                            minfo[18]) + "`" + str(
                            minfo[19]) + "`" + str(minfo[20]) + "`" + str(minfo[21]) + "`" + str(
                            minfo[22]) + "`" + str(
                            minfo[23]) + "`" + str(minfo[24]) + "`" + str(minfo[25]) + "`" + str(
                            minfo[26]) + "`" + str(
                            minfo[27]) + "`" + str(minfo[28]) + "`" + str(minfo[29]) + "`" + str(
                            minfo[1]) + "`" + str(
                            minfo[30]) + "`" + str(
                            minfo[31]) + "`" + str(minfo[32]) + "`" + str(minfo[33])
                elif OpenCode == "107":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[15])
                    else:
                        _cback = str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[15])
                elif OpenCode == "108":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(
                            minfo[15])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13]) + "`" + str(
                            minfo[14]) + "`" + str(
                            minfo[15])
                elif OpenCode == "109":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(
                            minfo[6]) + "`" + str(minfo[7])
                    else:
                        _cback = str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(
                            minfo[6]) + "`" + str(minfo[7])
                elif OpenCode == "110":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4])
                    else:
                        _cback = str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4])
                elif OpenCode == "111":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4])
                    else:
                        _cback = str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4])
                        # _cback = str(minfo[0])+"`"+str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4])
                elif OpenCode == "112":
                    if _cback != "":
                        _cback += "^" + "`".join([str(i) for i in minfo[1:5]])
                    else:
                        _cback = "`".join([str(i) for i in minfo[1:5]])
                    # if _cback != "":
                    #     _cback = _cback + "^" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                    #         minfo[3]) + "`" + str(
                    #         minfo[4])
                    # else:
                    #     _cback = str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3]) + "`" + str(minfo[4])
                elif OpenCode == "113":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[1]) + "`" + str(minfo[2])
                    else:
                        _cback = str(minfo[1]) + "`" + str(minfo[2])
                elif OpenCode == "114":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "115":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "116":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5])

                elif OpenCode == "117":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4])
                elif OpenCode == "118":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7]) + "`" + str(minfo[8]) + "`" + str(minfo[9]) + "`" + str(
                            minfo[10]) + "`" + str(
                            minfo[11]) + "`" + str(minfo[12]) + "`" + str(minfo[13])
                elif OpenCode == "119":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "120":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5])
                elif OpenCode == "121":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(
                            minfo[3]) + "`" + str(minfo[4]) + "`" + str(minfo[5]) + "`" + str(minfo[6]) + "`" + str(
                            minfo[7])

                elif OpenCode == "122":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2])
                elif OpenCode == "123":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "124":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(
                            minfo[2]) + "`" + str(
                            minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "125":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                    else:
                        _cback = str(minfo[0]) + "`" + str(minfo[1]) + "`" + str(minfo[2]) + "`" + str(minfo[3])
                elif OpenCode == "205":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(minfo[14]) + "`" + str(minfo[15]) + "`" + str(minfo[32])+ "`" + str(minfo[33])+ "`" + str(minfo[34])+ "`" + str(minfo[30])
                    else:
                        _cback = str(minfo[2]) + "`" + str(minfo[14]) + "`" + str(minfo[15]) + "`" + str(minfo[32])+ "`" + str(minfo[33])+ "`" + str(minfo[34])+ "`" + str(minfo[30])
                elif OpenCode == "206":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(minfo[15]) + "`" + str(minfo[14]) + "`" + str(minfo[31])+ "`" + str(minfo[32])+ "`" + str(minfo[33])+ "`" + str(minfo[13])
                    else:
                        _cback = str(minfo[2]) + "`" + str(minfo[15]) + "`" + str(minfo[14]) + "`" + str(minfo[31])+ "`" + str(minfo[32])+ "`" + str(minfo[33])+ "`" + str(minfo[13])
                elif OpenCode == "207":
                    if _cback != "":
                        _cback = _cback + "^" + str(minfo[2]) + "`" + str(minfo[14]) + "`" + str(minfo[15])
                    else:
                        _cback = str(minfo[2]) + "`" + str(minfo[14]) + "`" + str(minfo[15])
            _count = _count + 1
    if _count < 500:
        _cback = _cback + "*1"
    else:
        _cback = _cback + "*0"
    return _cback


def GetLimit(page):
    ipage = int(page)
    _limit = " limit " + str((ipage - 1) * 500) + ",500"
    return _limit


def GetCodeVersion(DB, code):
    d1 = {
        "205": "105",
        "206": "106",
        "207": "107"
    }
    code = d1.get(code, code)
    data = ""
    table_project = "tb_res_version"
    sql_str = "select VERSION from " + table_project +" where OPENCODE = " + str(code)
    data = DB.fetchone(sql_str, None)
    version = ""
    if data:
        version= data[0]
    return version


def GetUpdateResData(DB,code,version):

    table_project = ""
    sql_str = ""
    _cback = "0"
    table_project = "tb_config_vdetails"
    sql_str = "select resids from " + table_project + " where OPENCODE = "+str(code) +" and version > " +str(version)
    # &ID, &Res_Id, &Res, &BuyRes, &SceneID
    sqlinfo = []
    data = DB.fetchall(sql_str, None)
    if data:
        list_data = list(data)
        for minfo in list_data:
            sqlinfo.append(minfo[0])
        sqlinfo= list(set(sqlinfo))
        sqlinfo.sort()
        for back in sqlinfo:
            if  _cback != "":
                _cback =_cback+ ","+back
            else:
                _cback = back
    return _cback


#获取最小版本号
def GetUpdateResMinVersion(DB, code, version):

    table_project = "tb_config_vdetails"
    sql_str = "select * from " + table_project + " where OPENCODE = " + str(code) + " ORDER  BY version limit 1"
    # &ID, &Res_Id, &Res, &BuyRes, &SceneID

    data = DB.fetchone(sql_str,None)
    if data:
        _cback = data[2]
    else:
        _cback = "0"
    return _cback


def Server_ConfigGet(DB,params):
    json_data = {
        "code": 0,
        "Data": "",
        "OpenCode": ""
    }
    if params == "":
        json_data["code"] = "0"
        json_data["Data"] = ""
        return json_data
    OpenCode= params["OpenCode"]
    limit =params["Pam"]
    json_data["OpenCode"] = OpenCode
    if OpenCode == "202":
        _table_name = "tb_config_vip"
        _sql = "select Rank,PrivilegePrice from " + _table_name + limit
    elif OpenCode == "203":
        _table_name = "tb_config_res"
        _sql = "select RID,PriceYear,PriceForever from " + _table_name + " where IsNeedBuy = 1" + limit
    elif OpenCode == "204":
        _table_name = "tb_config_scene"
        _sql = "select RID,PriceYear,PriceForever from " + _table_name + " where IsNeedBuy = 1" + limit
    elif OpenCode == "205":
        _table_name = "tb_config_coursedata"
        _sql = "select CourseId,CID,LID,UID,Active from " + _table_name + limit
    elif OpenCode == "206":
        _table_name = "tb_config_left_res"
        _sql = "select Res_Id,BuyRes,SceneID from " + _table_name + limit
    elif OpenCode == "207":
        _table_name = "tb_channel"
        _sql = "select CID,WTYPE,WID,PRICE from " + _table_name + limit
    elif OpenCode == "208":
        _table_name = "tb_discount"
        _sql = "select CID,DAYS,Discount from " + _table_name + limit

    ##print(_sql)

    ##print(_sql)
    data = DB.fetchall(_sql,None)
    _cback = ""
    if data:
        minfo = list(data)
        if OpenCode == "202":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0])+"*"+str(info[1])
                else:
                    _cback = _cback +"^"+str(info[0])+"*"+str(info[1])
        elif OpenCode == "203":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
        elif OpenCode == "204":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
        elif OpenCode == "205":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])+ "*" + str(info[3]) + "*" + str(info[4])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])+ "*" + str(info[3]) + "*" + str(info[4])
        elif OpenCode == "206":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
        elif OpenCode == "207":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])+ "*" + str(info[3])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])+ "*" + str(info[3])
        elif OpenCode == "208":
            for info in minfo:
                if _cback == "":
                    _cback = str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])
                else:
                    _cback = _cback + "^" + str(info[0]) + "*" + str(info[1]) + "*" + str(info[2])

    json_data["code"] = "1"
    json_data["Data"] = _cback
    return json_data

