import logging
from handlers.kbeServer.Editor.response import response_course
from handlers.kbeServer.Editor.response import response_lesson, response_project, response_account, response_zy, \
    response_coursebag, response_work, response_gm, response_res


class Avatar_Editor:  # 继承base.py中的类BaseHandler

    def __init__(self):
        pass

    def Transactions_Code(self, sub_code, self_uid, self_username, json_data):

        json_back = {}
        logging.info(
            "sub code[%i] self_uid[%i] self_username[%s] json_data[%s]" % (
            sub_code, self_uid, self_username, json_data))
        if sub_code == 1001:  # 购买课程
            json_back = response_course.Transactions_Code_1001(self_uid, self_username, json_data)
        elif sub_code == 1002:  # 删除课程
            json_back = response_course.Transactions_Code_1002(self_uid, self_username, json_data)
        elif sub_code == 1003:  # 删除课时
            json_back = response_lesson.Transactions_Code_1003(self_uid, self_username, json_data)
        elif sub_code == 1004:  # 审核课程
            json_back = response_course.Transactions_Code_1004(self_uid, self_username, json_data)
        elif sub_code == 1005:  # 审核作品
            json_back = response_work.Transactions_Code_1005(self_uid, self_username, json_data)
        elif sub_code == 1006:  # 移出工程(从制作市场)
            json_back = response_project.Transactions_Code_1006(self_uid, self_username, json_data)
        elif sub_code == 1007:  # 删除工程
            json_back = response_project.Transactions_Code_1007(self_uid, self_username, json_data)
        elif sub_code == 1008:  # 购买作品
            json_back = response_work.Transactions_Code_1008(self_uid, self_username, json_data)
        elif sub_code == 1009:  # 发布到背包
            json_back = response_project.Transactions_Code_1009(self_uid, self_username, json_data)
        elif sub_code == 1010:  # 设置为模板
            json_back = response_project.Transactions_Code_1010(self_uid, self_username, json_data)
        elif sub_code == 1011:  # 转移/复制工程
            json_back = response_project.Transactions_Code_1011(self_uid, self_username, json_data)
        elif sub_code == 1012:  # PC端登录数据
            json_back = response_account.Transactions_Code_1012(self_uid, self_username, json_data)
        elif sub_code == 1013:  # 验证身份信息
            json_back = response_account.Transactions_Code_1013(self_uid, self_username, json_data)
        elif sub_code == 1014:  # 验证账号信息
            json_back = response_account.Transactions_Code_1014(self_uid, self_username, json_data)
        elif sub_code == 1015:  # 提交作业
            json_back = response_zy.Transactions_Code_1015(self_uid, self_username, json_data)
        elif sub_code == 1016:  # 作业打分
            json_back = response_zy.Transactions_Code_1016(self_uid, self_username, json_data)
        elif sub_code == 1017:  # 班级分享
            json_back = response_zy.Transactions_Code_1017(self_uid, self_username, json_data)
        elif sub_code == 1018:  # 登录课程包赠送
            json_back = response_coursebag.Transactions_Code_1018(self_uid, self_username, json_data)
        elif sub_code == 1019:  # PC端登录
            json_back = response_account.Transactions_Code_1019(self_uid, self_username, json_data)
        elif sub_code == 1021:  # 工程数据获取
            json_back = response_project.Transactions_Code_1021(self_uid, self_username, json_data)
        elif sub_code == 1022:  # 撤销课程
            json_back = response_course.Transactions_Code_1022(self_uid, self_username, json_data)
        elif sub_code == 1023:  # 撤销作品
            json_back = response_work.Transactions_Code_1023(self_uid, self_username, json_data)
        elif sub_code == 1024:  # GM增加智慧豆
            json_back = response_gm.Transactions_Code_1024(self_uid, self_username, json_data)
        elif sub_code == 1025:  # GM获取账号信息
            json_back = response_gm.Transactions_Code_1025(self_uid, self_username, json_data)
        elif sub_code == 1026:  # GM修改账号信息
            json_back = response_gm.Transactions_Code_1026(self_uid, self_username, json_data)
        elif sub_code == 1027:  # GM获取权限跟补偿包裹
            json_back = response_gm.Transactions_Code_1027(self_uid, self_username, json_data)
        elif sub_code == 1028:  # GM设置权限跟补偿包裹
            json_back = response_gm.Transactions_Code_1028(self_uid, self_username, json_data)
        elif sub_code == 1029:  # 课程上架下架
            json_back = response_gm.Transactions_Code_1029(self_uid, self_username, json_data)
        elif sub_code == 1030:  # 发送邮件
            json_back = response_gm.Transactions_Code_1030(self_uid, self_username, json_data)
        elif sub_code == 1031:  # 智慧豆同步
            json_back = response_account.Transactions_Code_1031(self_uid, self_username, json_data)
        elif sub_code == 1032:  # 购买资源
            json_back = response_account.Transactions_Code_1032(self_uid, self_username, json_data)
        elif sub_code == 1033:  # 购买存储位
            json_back = response_account.Transactions_Code_1033(self_uid, self_username, json_data)
        elif sub_code == 1034:  # 存储位绑定工程
            json_back = response_account.Transactions_Code_1034(self_uid, self_username, json_data)
        elif sub_code == 1035:  # GM赠送存储位
            json_back = response_gm.Transactions_Code_1035(self_uid, self_username, json_data)
        elif sub_code == 1036:  # GM导出工程
            json_back = response_gm.Transactions_Code_1036(self_uid, self_username, json_data)
        elif sub_code == 1037:  # GM导入工程
            json_back = response_gm.Transactions_Code_1037(self_uid, self_username, json_data)
        elif sub_code == 1038:  # 个人信息修改
            json_back = response_account.Transactions_Code_1038(self_uid, self_username, json_data)
        elif sub_code == 1039:  # 设置GM
            json_back = response_account.Transactions_Code_1039(self_uid, self_username, json_data)
        elif sub_code == 1040:  # PC端登出
            json_back = response_account.Transactions_Code_1040(self_uid, self_username, json_data)
        elif sub_code == 1041:  # 导出视频
            json_back = response_account.Transactions_Code_1041(self_uid, self_username, json_data)
        elif sub_code == 1042:  # 获取导出的视频定价
            json_back = response_account.Transactions_Code_1042()
        elif sub_code == 1043:  # 获取账号导出视频的次数
            json_back = response_account.Transactions_Code_1043(self_uid)
        elif sub_code == 1044:  # 获取工程配置数据
            json_back = response_account.Transactions_Code_1044(self_uid, self_username, json_data)
        elif sub_code == 1045:  # 获取工程配置数据
            json_back = response_account.Transactions_Code_1045(self_uid, self_username, json_data)
        elif sub_code == 1046:  # 用户开通云储存
            json_back["code"], json_back["msg"] = response_res.update_user_save(json_data["uid"])
        elif sub_code == 1047:  # 判断资源名是否重复
            json_back["code"], json_back["msg"], json_back["pam"] = response_res.resource_upload_judge(
                json_data["uid"], json_data["resName"])
        elif sub_code == 1048:  # 上传资源
            json_back["code"], json_back["msg"], json_back["pam"] = response_res.resource_upload(
                json_data["uid"], json_data["resName"], json_data["iconPath"],
                json_data["filePath"], json_data["resTypeID"])
        elif sub_code == 1049:  # 删除资源
            json_back["code"], json_back["msg"] = response_res.del_resource(json_data["uid"], json_data["resID"])
        elif sub_code == 1050:  # 转移资源分类
            json_back["code"], json_back["msg"] = response_res.transfer_resource(json_data["uid"], json_data["resID"],
                                                                                 json_data["resTypeID"])
        elif sub_code == 1051:  # 获取用户资源
            json_back["code"], json_back["msg"], json_back["pam"] = response_res.user_upload_data(json_data["uid"],
                                                                                                  json_data["page"])
        elif sub_code == 1052:  # 创建新分类
            json_back["code"], json_back["msg"] = response_res.create_new_type(json_data["uid"],
                                                                               json_data["resTypeName"],
                                                                               json_data["resTypeID"],
                                                                               json_data["desc"])
        elif sub_code == 1053:  # 删除资源分类
            json_back["code"], json_back["msg"] = response_res.del_res_type(json_data["uid"], json_data["resTypeID"])
        elif sub_code == 1054:  # 获取资源分类
            json_back["code"], json_back["msg"], json_back["pam"] = response_res.get_user_res_type(json_data["uid"])
        elif sub_code == 1055:  # 更新资源分类信息
            json_back["code"], json_back["msg"] = response_res.update_type_name(json_data["uid"],
                                                                                json_data["resTypeID"],
                                                                                json_data["resTypeName"],
                                                                                json_data["desc"])
        elif sub_code == 1056:  # 发送课程排序 tb_course_sort
            json_back = response_work.Transactions_Code_1056()
        elif sub_code == 1057:  # 发送作品排序 tb_work_sort
            json_back = response_work.Transactions_Code_1057()
        elif sub_code == 1058:  # 发送D类作品 tb_eservices_workmarket
            json_back = response_work.Transactions_Code_1058()
        elif sub_code == 1059:  # 获取用户当前最大PID+10002
            json_back = response_work.Transactions_Code_1059(json_data["uid"])
        elif sub_code == 1060:  # 更新用户pid
            json_back = response_work.Transactions_Code_1060(json_data["uid"])
        return json_back


AvatarEditorInst = Avatar_Editor()
