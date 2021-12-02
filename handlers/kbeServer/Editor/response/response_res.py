# coding=utf-8
'''
上传资源相关方法
'''
import re
import time
from typing import Tuple
import uuid
from methods.DBManager import DB


def update_user_save(uid) -> int:
    '''
    description:
        用户开通云存储功能
    Args:
        DB:数据库连接
        uid:用户id
    return:
        0:失败
        1:成功
    '''
    sql = "update tb_userdata set save_status = 1 where UID = %s"
    data = DB.edit(sql, uid)
    if data:
        return 1, "开通成功"
    return 0, "开通失败"


def resource_upload_judge(uid, res_name) -> Tuple[int, str, str]:
    '''
    description:
        验证用户能否上传资源
    args:
        DB:数据库连接
        uid:用户id
        res_name:资源名称
    return:
        0:失败
        1:成功
    '''
    sql = "select ID from tb_p_res where Name = %s and uid = %s and isDel = 0 union all select ID from tb_config_res where name = %s;"
    data = DB.fetchone(sql, (res_name, uid, res_name))
    r_data = ""
    if data:
        return 0, "模型名称重复请修改", r_data
    r_data = uuid.uuid3(uuid.NAMESPACE_X500, str(uid) + "_" + res_name)
    return 1, "可以上传", r_data


def resource_upload(uid, res_id, res_name, pic_path, res_path,
                    res_type) -> Tuple[int, str]:
    '''
    description:
        用户上传资源成功（obs调用成功以后）
    args:
        DB:数据库连接
        uid:用户id
        res_id:资源id
        res_name:资源名称
        pic_path:资源图片路径
        res_path:资源路径
        res_type:资源类型
    return:
        0:失败
        1:成功
    '''
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "insert into tb_p_res(rid, uid, Name, picPath, resPath, uploadtime, TID) values(%s, %s, %s, %s, %s, %s, %s);"
    data = DB.edit(sql,
                   (res_id, uid, res_name, pic_path, res_path, now, res_type))
    if data:
        return 1, "上传成功"
    return 0, "上传失败"


def del_resource(uid, res_id) -> Tuple[int, str]:
    '''
    description:
        删除当前资源数据
    args:
        DB: 数据库连接
        uid: 用户id
        res_id: 资源id
    return:
        0: 失败
        1: 成功
    '''
    sql = "update tb_p_res set isdel = 1 where uid = %s and rid = %s;"
    data = DB.edit(sql, (uid, res_id))
    if data:
        return 1, "删除成功"
    return 0, "删除失败"


def transfer_resource(uid, res_id, res_type) -> Tuple[int, str]:
    '''
    description:
        转移资源类型
    args:
        DB: 数据库连接
        uid: 用户id
        res_id: 资源id
        res_type: 要转移到的资源类型id
    return:
        0: 失败
        1: 成功
        -1: 资源类型不存在
        -2: 资源不存在
    '''
    sql_type = "selece id from tb_p_resType where uid = %s and tid = %s;"
    data_type = DB.fetchone(sql_type, (uid, res_type))
    if not data_type:
        return -1, "资源分类不存在"
    sql_res = "select id from tb_p_res where uid = %s and rid = %s;"
    data_res = DB.fetchone(sql_res, (uid, res_id))
    if not data_res:
        return -2, "资源不存在"
    sql = "update tb_p_res set TID = %s where uid = %s and rid = %s;"
    data = DB.edit(sql, (res_id, uid, res_type))
    if data:
        return 1, "转移资源成功"
    return 0, "转移资源失败"


def user_upload_data(uid, page) -> Tuple[int, int, str]:
    '''
    description:
        获取用户上传资源数据
    args:
        DB: 数据库连接
        uid: 用户id
        page: 页码
    return:
        0: 失败
        1: 成功
        msg:
            1: 还有数据
            -1: 没有数据
    '''
    user_list = []
    user_data = ""
    msg = -1
    sql = "select s.*, m.msgDesc from tb_p_res as s left join tb_rebut_msg as m on s.rebutId = m.id and uid = %s " + sql_limit(page) + ";"
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
    '''
    description:
        新建资源类型
    args:
        DB: 数据库连接
        uid: 用户id
        type_name: 资源类型名称
        tid: 资源类型id
        desc: 资源类型描述
    return:
        0: 失败
        1: 成功
        -1: 资源类型数量超过五个
    '''
    sql_user_type = "select count(id) from tb_p_resType where uid = %s and tid = %s and isDel = 0;"
    data_type = DB.fetchone(sql_user_type, (uid, tid))
    if data_type:
        if data_type[0] >= 5:
            return -1, "资源类型数量超过5个"
    sql = "insert into tb_p_resType(Tid, name, createUserId, Desc, isDel) values (%s, %s, %s, %s, %s);"
    data = DB.edit(sql, (uid, type_name, tid, desc,0))
    if data:
        return 1, "新建资源类型成功"
    return 0, "新建资源类型失败"


def del_res_type(uid, tid) -> Tuple[int, str]:
    '''
    description:
        删除资源类型
    args:
        DB: 数据库连接
        uid: 用户id
        tid: 资源类型id
    return:
        0: 失败
        1: 成功
        -1: 该资源类型下有资源，不能删除
    '''
    sql_res = "select id from tb_p_res where uid = %s and TID = %s and isDel = 0;"
    data_res = DB.fetchone(sql_res, (uid, tid))
    if data_res:
        return -1, "该资源类型下有资源，不能删除"
    sql = "update tb_p_resType set isdel = 1 where uid = %s and tid = %s;"
    data = DB.edit(sql, (uid, tid))
    if data:
        return 1, "删除资源类型成功"
    return 0, "删除资源类型失败"


def get_user_res_type(uid) -> Tuple[int, str, str]:
    '''
    description:
        获取用户资源类型
    args:
        DB: 数据库连接
        uid: 用户id
    return:
        0: 失败
        1: 成功
    '''
    user_list = []
    user_data = ""
    sql = "select TID, name, `desc` from tb_p_resType where createUserId = %s;"
    data = DB.fetchall(sql, uid)
    if data:
        for i in data:
            user_list.append("`".join(str(j) for j in i))
        user_data = "*".join(user_list)
        return 1, "获取用户资源类型成功", user_data
    return 0, "获取用户资源类型失败", user_data


def sql_limit(page):
    ipage = int(page)
    _limit = "limit " + str((ipage - 1) * 500) + ",500"
    return _limit
