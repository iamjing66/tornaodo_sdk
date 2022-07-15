# coding=utf-8
"""
上传资源相关方法
"""
import hashlib
import time
import logging
from typing import Tuple
from methods.DBManager import DB


def update_user_save(uid) -> Tuple[int, str]:
    """
    description:
        用户开通云存储功能
    args:
        uid:用户id
    return:
        0:失败
        1:成功
    """
    sql = "update tb_userdata set save_status = 1 where UID = %s"
    data = DB.edit(sql, uid)
    if data:
        logging.info("用户: %s 开通云存储功能成功" % uid)
        return 1, "开通成功"
    logging.info("用户: %s 开通云存储功能失败" % uid)
    return 0, "开通失败"


def resource_upload_judge(uid, res_name) -> Tuple[int, str, str]:
    """
    description:
        验证用户能否上传资源
    args:
        uid:用户id
        res_name:资源名称
    return:
        0:失败
        1:成功
    """
    sql = "select ID from tb_p_res where Name = %s and uid = %s and isDel = 0 union all select ID from tb_config_res where name = %s;"
    data = DB.fetchone(sql, (res_name, uid, res_name))
    r_data = ""
    res_name = "@".join([str(uid), res_name])
    if data:
        return 0, "模型名称重复请修改", r_data
    r_data = hashlib.md5(res_name.encode(encoding='UTF-8')).hexdigest()
    return 1, "可以上传", r_data


def resource_upload(uid, res_name, pic_path, res_path,
                    res_type) -> Tuple[int, str, int]:
    """
    description:
        用户上传资源成功（obs调用成功以后）
    args:
        uid:用户id
        res_name:资源名称
        pic_path:资源图片路径
        res_path:资源路径
        res_type:资源类型
    return:
        0:失败
        1:成功
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    rid_sql = "select rid from tb_config_res where ID = (select max(id) from tb_config_res);"
    data_rid = DB.fetchone(rid_sql)
    insert_status = 1
    res_id = int(data_rid[0]) + 1
    res_sql = "insert into tb_config_res(rid, p2, name, abpath, picpath, MPos, MRot, MSca) values(%s, %s, %s, %s, %s, %s, %s, %s);"
    res_data = DB.edit(res_sql, (res_id, uid, res_name, res_path, pic_path, '0,0,0', '0,0,0', '1,1,1'))
    if not res_data:
        insert_status = 0
    sql = "insert into tb_p_res(rid, uid, Name, uploadtime, auditTime, TID) values(%s, %s, %s, %s, %s, %s);"
    data = DB.edit(sql, (res_id, uid, res_name, now, now, res_type))
    if not data:
        insert_status = 0
    if insert_status:
        logging.info("用户: %s 上传资源 %s 成功" % (uid, res_name))
        return 1, "上传成功", res_id
    logging.info("用户: %s 上传资源 %s 失败" % (uid, res_name))
    return 0, "上传失败", 0


def del_resource(uid, res_id) -> Tuple[int, str]:
    """
    description:
        删除当前资源数据
    args:
        uid: 用户id
        res_id: 资源id
    return:
        0: 失败
        1: 成功
    """
    sql = "update tb_p_res set isdel = 1 where uid = %s and rid = %s;"
    data = DB.edit(sql, (uid, res_id))
    if data:
        return 1, "删除成功"
    return 0, "删除失败"


def transfer_resource(uid, res_id, res_type) -> Tuple[int, str]:
    """
    description:
        转移资源类型
    args:
        uid: 用户id
        res_id: 资源id
        res_type: 要转移到的资源类型id
    return:
        0: 失败
        1: 成功
        -1: 资源类型不存在
        -2: 资源不存在
    """
    sql_type = "select id from tb_p_resType where createUserId = %s and tid = %s;"
    data_type = DB.fetchone(sql_type, (uid, res_type))
    if not data_type:
        logging.info("资源类型不存在")
        return -1, "资源分类不存在"
    sql_res = "select id from tb_p_res where uid = %s and rid = %s;"
    data_res = DB.fetchone(sql_res, (uid, res_id))
    if not data_res:
        logging.info("资源不存在")
        return -2, "资源不存在"
    sql = "update tb_p_res set TID = %s where uid = %s and rid = %s;"
    data = DB.edit(sql, (res_type, uid, res_id))
    if data:
        logging.info("用户: %s 转移资源 %s 成功" % (uid, res_id))
        return 1, "转移资源成功"
    logging.info("用户: %s 转移资源 %s 失败" % (uid, res_id))
    return 0, "转移资源失败"


def user_upload_data(uid, page) -> Tuple[int, int, str]:
    """
    description:
        获取用户上传资源数据
    args:
        uid: 用户id
        page: 页码
    return:
        0: 失败
        1: 成功
        msg:
            1: 还有数据
            -1: 没有数据
    """
    user_list = []
    user_data = ""
    msg = -1
    sql = "select s.*, m.msgDesc, c.ABPATH, c.PICPATH from tb_p_res as s inner join tb_rebut_msg as m inner join tb_config_res as c on s.rebutId = m.id and s.rid = c.rid and uid = %s " + sql_limit(page) + ";"
    data = DB.fetchall(sql, uid)
    if data:
        if len(data) == 500:
            msg = int(page) + 1
        for i in data:
            user_list.append("`".join(str(j) for j in i))
        user_data = "*".join(user_list)
        return 1, msg, user_data
    return 0, msg, user_data


def create_new_type(uid, type_name, tid, desc) -> Tuple[int, str]:
    """
    description:
        新建资源类型
    args:
        uid: 用户id
        type_name: 资源类型名称
        tid: 资源类型id
        desc: 资源类型描述
    return:
        0: 失败
        1: 成功
        -1: 资源类型数量超过五个
        -2: 资源类型已存在
    """
    sql_user_type = "select count(id) from tb_p_resType where createUserId = %s and isDel = 0;"
    data_type = DB.fetchone(sql_user_type, uid)
    if data_type:
        if data_type[0] >= 5:
            return -1, "资源类型数量超过5个"
    sql_type = "select id from tb_p_resType where createUserId = %s and tid = %s and isDel = 0;"
    data_type2 = DB.fetchone(sql_type, (uid, tid))
    if data_type2:
        return -2, "资源类型已存在"
    sql = "insert into tb_p_resType(Tid, name, createUserId, `Desc`) values (%s, %s, %s, %s);"
    data = DB.edit(sql, (tid, type_name, uid, desc))
    if data:
        return 1, "新建资源类型成功"
    return 0, "新建资源类型失败"


def del_res_type(uid, tid) -> Tuple[int, str]:
    """
    description:
        删除资源类型
    args:
        uid: 用户id
        tid: 资源类型id
    return:
        0: 失败
        1: 成功
        -1: 该资源类型下有资源，不能删除
    """
    sql_res = "select id from tb_p_res where uid = %s and TID = %s and isDel = 0;"
    data_res = DB.fetchone(sql_res, (uid, tid))
    if data_res:
        return -1, "该资源类型下有资源，不能删除"
    sql = "update tb_p_resType set isdel = 1 where createUserId = %s and tid = %s;"
    data = DB.edit(sql, (uid, tid))
    if data:
        return 1, "删除资源类型成功"
    return 0, "删除资源类型失败"


def get_user_res_type(uid) -> Tuple[int, str, str]:
    """
    description:
        获取用户资源类型
    args:
        uid: 用户id
    return:
        0: 失败
        1: 成功
    """
    user_list = []
    user_data = ""
    sql = "select TID, name, `desc`, isDel from tb_p_resType where createUserId = %s;"
    data = DB.fetchall(sql, uid)
    if data:
        for i in data:
            user_list.append("`".join(str(j) for j in i))
        user_data = "*".join(user_list)
        return 1, "获取用户资源类型成功", user_data
    return 0, "获取用户资源类型失败", user_data


def update_type_name(uid, tid, name, desc) -> Tuple[int, str]:
    """
    description:
        修改资源类型名称
    args:
        uid: 用户id
        tid: 资源类型id 使用@分隔
        name: 资源类型名称 使用@分隔
        desc: 资源类型描述 使用@分隔
    return:
        1: 成功
    """
    tid_list = tid.split("@")
    name_list = name.split("@")
    desc_list = desc.split("@")
    for i, j in enumerate(tid_list):
        sql = "update tb_p_resType set name = %s, `desc` = %s where createUserId = %s and tid = %s and isDel = 0;"
        DB.edit(sql, (name_list[i], desc_list[i], uid, j))
    return 1, "修改资源类型名称成功"


def sql_limit(page):
    """
    sql 语句分页
    """
    page = int(page)
    _limit = "limit " + str((page - 1) * 500) + ",500"
    return _limit
