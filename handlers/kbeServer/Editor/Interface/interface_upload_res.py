# coding=utf-8
'''
上传资源相关方法
'''
import re
import time
from typing import Tuple


def update_user_save(db, uid) -> int:
    '''
    description:
        用户开通云存储功能
    Args:
        db:数据库连接
        uid:用户id
    return:
        0:失败
        1:成功
    '''
    sql = "update tb_userdata set save_status = 1 where UID = %s"
    data = db.edit(sql, uid)
    if data:
        return 1
    else:
        return 0


def resource_upload_judge(db, uid, res_name) -> Tuple[int, str]:
    '''
    description:
        验证用户能否上传资源
    args:
        db:数据库连接
        uid:用户id
        res_name:资源名称
    return:
        0:失败
        1:成功
    '''
    sql = "select ID from tb_p_res where Name = %s and uid = %s union all select ID from tb_config_res where name = %s;"
    data = db.fetchone(sql, (res_name, uid, res_name))
    if data:
        return 0, "模型名称重复请修改"
    else:
        return 1, "可以上传"


def resource_upload(db, uid, res_id, res_name, pic_path, res_path, res_type) -> Tuple[int, str]:
    '''
    description:
        用户上传资源成功（obs调用成功以后）
    args:
        db:数据库连接
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
    data = db.edit(sql, (res_id, uid, res_name, pic_path, res_path, now, res_type))
    if data:
        return 1, "上传成功"
    else:
        return 0, "上传失败"


def del_resource(db, uid, res_id) -> Tuple[int, str]:
    '''
    description:
        删除当前资源数据
    args:
        db: 数据库连接
        uid: 用户id
        res_id: 资源id
    return:
        0: 失败
        1: 成功
    '''
    sql = "update tb_p_res set isdel = 1 where uid = %s and rid = %s;"
    data = db.edit(sql, (uid, res_id))
    if data:
        return 1, "删除成功"
    else:
        return 0, "删除失败"


def transfer_resource(db, uid, res_id, res_type):
    '''
    description:
        转移资源类型
    args:
        db: 数据库连接
        uid: 用户id
        res_id: 资源id
        res_type: 要转移到的资源类型id
    '''
    sql = "update tb_p_res set TID = %s where uid = %s and rid = %s;"
    data = db.edit(sql, (res_id, uid, res_type))
    if data:
        return 1, "转移资源成功"
    else:
        return 0, "转移资源失败"


def user_upload_data(db, uid, page) -> Tuple[int, str]:
    '''
    description:
        用户上传数据
    args:
        db: 数据库连接
        uid: 用户id
        page: 页码
    return:
        0: 失败
        1: 成功
    '''
    user_data = {
        "rid": "",
    }
    sql = "select * from tb_p_res where uid = %s " + sql_limit(page)+";"
    data = db.fetchall(sql, uid)
    if data:
        for i in data:
            # TODO: 数据循环给值
            rid = i[0]
        return 1, "数据获取成功",user_data
    return 0, "数据获取失败",user_data


def create_new_type(db, uid, type_name, tid,desc) -> Tuple[int, str]:
    '''
    description:
        新建资源类型
    args:
        db: 数据库连接
        uid: 用户id
        type_name: 资源类型名称
        tid: 资源类型id
        desc: 资源类型描述
    return:
        0: 失败
        1: 成功
    '''
    sql = "insert into tb_p_resType(Tid, name, createUserId, Desc) values (%s, %s, %s, %s);"
    data = db.edit(sql, (uid, type_name, tid, desc))
    if data:
        return 1, "新建资源类型成功"
    else:
        return 0, "新建资源类型失败"


def del_res_type(db, uid, tid) -> Tuple[int, str]:
    '''
    description:
        删除资源类型
    args:
        db: 数据库连接
        uid: 用户id
        tid: 资源类型id
    return:
        0: 失败
        1: 成功
    '''
    sql = "update tb_p_resType set isdel = 1 where uid = %s and tid = %s;"
    data = db.edit(sql, (uid, tid))
    if data:
        return 1, "删除资源类型成功"
    else:
        return 0, "删除资源类型失败"


def get_user_res_type(db, uid) -> Tuple[int, str]:
    '''
    description:
        获取用户资源类型
    args:
        db: 数据库连接
        uid: 用户id
    return:
        0: 失败
        1: 成功
    '''
    user_data = {
        "tid": "",
        "name": "",
        "desc": "",
    }
    sql = "select * from tb_p_resType where createUserId = %s;"
    data = db.fetchall(sql, uid)
    if data:
        for i in data:
            user_data["tid"] = i[1]
            user_data["name"] = i[2]
            user_data["desc"] = i[4]
        return 1, "获取用户资源类型成功",user_data
    return 0, "获取用户资源类型失败",user_data


def sql_limit(page):
    ipage = int(page)
    _limit = "limit " + str((ipage - 1) * 500) + ",500"
    return _limit
