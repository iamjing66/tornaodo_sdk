# -*- coding: utf-8 -*-
"""
  create-x source code grading and score.
  parse all script of one game.

  Xi'an Feidie VR technology co. LTD
  2019/10/08
"""
import logging
import re

import ScoreBase as sb
from ComputingThink import (BlockDistribution, ComputingThinkIndex,
                            ScoreGradeObjectivity1, ScoreGradeObjectivity2)
from EvaluateReport import EvaluateingResult
from get_sql import get_course_list, str_replace
from ScoreReport import ScoreReporter


class GameInfo:
    def __init__(self):
        self.gamename = ''
        # 0.job, 1.skill no model answer, 2.skill has model answer,3.others
        self.createtype = 1

        # 小学阶段(1,2,3,4,5,6),中学阶段(7,8,9,10,11,12),其他(13)
        self.grade = 3
        self.gameobject = []

        self.variables_sets_global = []  # 全局变量列表(变量类型,变量ID,变量名称,默认值)
        self.variables_list_global = []  # (variables name,count) # 2012/12/11

        # broadcast
        self.broadcast_net = []
        # [message-type,messageid,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        # clone
        self.clone_net = []  
        # [message-type,clone target-objectgameid,target-objectgamename,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        # variables
        self.variables_net = [] 
        # [message-type,var-type,var-hostobjectid,var-hostobjectname,var-id,var-name,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid,target-value]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        # other event
        self.others_event_net = []  
        # [message-type,message-value,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        # 跨 sprite 循环检测
        self.loop_index_number_cross_sprite_by_broadcast = 0  # 基于消息(广播)的跨sprite大循环数目[暂不处理]
        self.loop_index_number_cross_sprite_by_variables = 0  # 基于消息(变量)的跨sprite大循环数目[暂不处理]


class GameObjectInfo:
    def __init__(self):
        # 1. base info
        self.gameobject_name = ''  # 对象名称
        self.gameobject_id = -1  # 对象id
        self.gameobject_type = -1  # 对象类型 0:root,1:player,2:others
        self.gameobject_attributes = []  # [属性名称,属性类型,属性值]
        self.has_music = 0  # 是否播放音乐

        # 2. variables list
        self.variables_sets_local = []  # 局部变量列表(变量类型,变量ID,变量名称,默认值)
        self.variables_list_local = []  # (variables name,count) # 2012/12/11

        # 3. script info
        self.scripts_sets = []  # 脚本列表

        # 4. coordinate
        self.coordinatea = []

        # 5. 跨 script 循环
        self.loop_index_number_cross_script_by_broadcast = 0  # 基于消息(广播)的跨script大循环数目[暂不处理]
        self.loop_index_number_cross_script_by_variables = 0  # 基于消息(变量)的跨script大循环数目[暂不处理]


class ScriptInfo:
    def __init__(self):
        # 0. 字典
        self.block_dict_seqid_index = {}  # 块序号 ---> block_set[]中的索引

        # 1. 基本信息
        self.scriptid = -1  # scriptID

        # 2. block info
        self.block_set = []  # 块数据集合

        # 3. 属性信息
        self.has_trigger = 0  # 是否有触点
        self.be_trigger_atworking = 0  # 工程运行时触发
        self.block_nest_depth = 0  # 语句块嵌套深度
        self.paramblock_nest_depth = 0  # 参数块嵌套深度
        self.stateparamblock_nest_depth = 0  # 语句块参数块混合嵌套深度
        self.nest_useless = 0  # 无效的嵌套数目
        self.running_time = 0  # script可能运行时间

        # 4. 条件属性
        self.condition_index_number_ifelse = 0  # ifelse数目
        self.condition_index_number_if = 0  # if数目
        self.condition_index_nest_depth = 0  # 条件嵌套最大深度(跳过loop)
        self.condition_index_nest_depth_total = 0  # 累计
        self.condition_index_number_no_statement = 0  # if,if else下面没有block的数目
        self.condition_index_number_param_imcompleted = 0  # if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
        self.condition_index_number_param_variables_nochanged = 0  # 条件表达式中的变量外部不变数目(基于嵌套顶层)
        self.condition_index_number_true_forever = 0  # 条件永假数目(基于嵌套顶层)
        self.condition_index_number_false_forever = 0  # 条件永真数目(基于嵌套顶层)

        # 5. loop属性
        self.loop_index_number_totals = 0  # 循环数目
        self.loop_index_nest_depth = 0  # 循环嵌套深度
        self.loop_index_nest_depth_total = 0  # 累计
        self.loop_index_endlessloop_nobreak = 0  # 死循环数目(不能跳出,或者break条件永不为真)
        self.loop_index_endlessloop_nowait = 0  # 死循环数目(循环体中没有阻塞)
        self.loop_index_number_no_statement = 0

        # 6. 顺序块
        self.sequenceblock_index_number_top_max = 0  # 一级顺序块最大数目
        self.sequenceblock_index_number_if_max = 0  # if中的一级顺序块最大数目
        self.sequenceblock_index_number_loop_max = 0  # loop中的一级顺序块最大数目

        # 7. wait
        self.wait_index_number = 0  # wait数目
        self.wait_index_max_waittime = 0  # wait最大等待时间

        # 8. logicalexpr
        self.logicalexpr_index_number_totals = 0  # 逻辑表达式数目
        self.logicalexpr_index_number_type = [0, 0, 0, 0, 0]  # 逻辑表达式种类数目
        self.logicalexpr_index_number_nest_depth_max = 0  # 逻辑表达式参数嵌套最大深度
        self.logicalexpr_index_number_nest_depth_avg = 0  # 逻辑表达式参数嵌套平均深度
        self.logicalexpr_index_number_param_imcompleted = 0  # 逻辑表达式缺参数数目(向上传递)


class BlockInfo:
    def __init__(self):
        # 1. block 自有属性
        # 1.1 block 自有基本信息
        self.sequenceid = -1  # 在script中的序号(script中的次序),base = 1
        self.refid = -1  # 参考序号(每个block类型的编号)
        self.blocktype = 0  # 类型
        self.blocksubtype = 0  # 子类型
        self.blockname = ''  # 名称
        self.coordinate = [-1, -1, -1]  # 坐标
        self.controltype = ()  # 控件类型

        # 2 自有参数属性
        # 2.1 参数基本信息及子关系
        self.is_parameter_block = 0  # 是否是参数 block
        self.parameter_nest_depth = 0  # 参数嵌入层级s"
        self.parameter_count_need = 0  # 参数数目(本层,不考虑嵌套参数影响)
        self.parameter_count = 0  # 参数数目(本层,不考虑嵌套参数影响)
        self.parameter_argtype = ()  # 参数可以使用的类型
        self.parameter_info = []  # (参数序号/从左到右次序/,参数类型1(1-8,条件表达式不标),参数值(缺省值),可有参数类型2(1-25),实际参数类型2(1-25),参数块编号,参数参考序号,是否合法)
        self.parameter_info0 = []  # 只记录块序号,次序
        # 2.2 参数块父关系
        self.parameter_parent_block_sequenceid = -1  # 只有参数块
        self.parameter_ancestor_block_seqenceid = -1  # 非参数块祖宗
        # 2.3 参数块兄弟关系
        self.parameter_brother_left = -1  # 上一个兄弟
        self.parameter_brother_right = -1  # 下一个兄弟

        # 3. 兄弟父子关系
        # 3.1 兄弟关系
        self.brother_up = -1  # 上一个兄弟
        self.brother_down = -1  # 下一个兄弟
        # 3.2 父关系
        self.indent_depth = 0  # 缩进层级,2级以后才有父
        self.father_block_seqeneceid = -1  # 所属父 block 序号
        # 3.3 子关系
        self.is_container = 0  # 是否container,容器才有子关系
        self.childblock_list1 = []  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目
        self.childblock_list2 = [
        ]  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目,目前只应用到else

        # 4. 执行时间
        self.is_asyn = 0  # 是否异步执行
        self.time_used = 0  # 执行用时
        self.time_used_accumulated = 0  # 累计执行用时
        self.time_ralatedvariable = []  # 涉及的变量,这些变量决定了用时

        # 5. check entity
        self.can_be_excuted = 0  # 是否会被执行
        self.has_child1 = 0  # 如果是container
        self.has_child2 = 0  # 如果是container,2 for else
        self.condition_value_iscontant = 0  # 条件值是常量


"""
  object     = {<对象名称,对象序号>[<对象属性>]}:<script>#<script>&<blocks坐标>&<变量表>
  对象名称   = 实际对象名称,序号
  对象属性   = [影藏(1/0)|落地(1/0)|<坐标>(x,y,z)|...]
  坐标       = [世界坐标系|自身坐标系]
  script    = <block>[~block][...]
  block     = <序号>@BLKREFID@[x,y,z]@<位置信息>@<初始值>@
  序号       = 对象内序号 ; 注:对象内统一排序,base1
  位置信息   = [D:n][|][M:n[|][I1:n[|I2:m[|...]]]
  初始值     = [[1|2][$值或者序号]][[1|2][$值或者序号]][...] 
               1-->数字或者文本;                     ==>inputField
               2-->下拉选项,base0;                   ==>dropdown
               3(67,9,60,108,105),                   ==>dropdown2
               4(18,101,102,40,88,3,46,85,9,105,63), ==>objectdoropdown
               5(94,93),                             ==>UIdropdown
               6(85,63),                             ==>objectdoropdown2
               7(41,39)0则表示没有选择音乐,            ==>text
               8(105)                                ==>dropdown3
               注:条件框不标 
  blocks坐标 = x,y
  变量表     = [[[1|2]|variables_id|变量名称][[1|2]|variables_id|变量名称],...]
  -----------------------------------------------------------------------
  注:
    变量下拉框显示变量的序号base0,可以重复编号,删除变量序号重排;
    对象序号base1,增加对象不考虑之前删除留下的空号,序号一直增加;
"""


class Parser:
    def __init__(self):
        self.gameinfo = GameInfo()
        self.blockdist = BlockDistribution()
        self.ct_index = ComputingThinkIndex()
        self.standard = ScoreGradeObjectivity2(course_id="63_318_1")
        self.report = ScoreReporter()

    """
    [in]:
        游戏例子1
        ^
        C:2|G:5
        ^
        Root      & 1 & 0 & &  &0,0&0|55545|gA
        *
        Player    & 2 & 1 & &  &0,1600&
        *
        爆竹三     & 3 & 2 & &  1@4@-552.2653,1832.809,0@D:2@@~2@40@@D:3@4$1@~3@62@@@2$0|1$0@#4@7@-424.7472,1658.2,0@D:5@1$1@~5@103@@@1$1|1$0|1$0|1$0|2$0@&400,3200&1|55545|lA%1|55545|lB
        *
        魔法圈     & 4 & 2 & &  1@6@-395.4414,1216.576,0@D:2|I1:14@@~2@98@@I1:3|I2:10|I4:13@1$1|1$0|1$0|1$0|2$0@~3@54@@I1:4@1$4|1$3@~4@47@@I1:5@1$0@~5@47@@I1:6@1$0@~6@47@@I1:7@1$0@~7@49@@I1:8|I2:9@1$0|1$1@~8@48@@@1$0|2$0|1$0@~9@59@@@2$0@~10@54@@I1:11|I2:12@1$4|1$3@~11@55@@@2$0|1$0@~12@63@@@4$1|6$1@~13@48@@@1$0|2$0|1$0@~14@52@@I1:15|I2:16@2$0@~15@45@@@2$0|3$0@~16@57@@I1:17@@~17@52@@I2:18@2$0@~18@50@@@1$0|2$0@&0,2000&1|55546|aaa
        *
        蓝色文本框  & 5 & 2 & & &0,0&
        *
        矩形输入框  & 6 & 2 & & &0,0&1|56222|bbb%1|56222|ccc
        *
        女孩       & 7 & 2 & &  1@4@-375,2050,0@D:2@@~2@23@@M:5|D:15|I1:3@@~3@56@@I1:4@1$0|2$0|1$0@~4@59@@@2$1@~5@99@@D:6@@~6@17@@M:7|D:14@@~7@2@@D:8@1$2@~8@22@@D:9@1$5@~9@60@@D:10@2$1|3$0|1$1@~10@23@@M:13|I1:11@@~11@56@@I1:12@1$0|2$5|1$10@~12@59@@@2$1@~13@66@@@@~14@102@@@4$4@~15@41@@D:16@7$1033@~16@43@@@@&0,3600&1|56923|bb
        *
        海盗三    & 8 & 2 & &  1@98@-612.1673,1216.47,0@I1:2|I2:9|I4:12@1$1|1$0|1$0|1$0|2$0@~2@54@@I1:3@1$4|1$3@~3@47@@I1:4@1$0@~4@47@@I1:5@1$0@~5@47@@I1:6@1$0@~6@49@@I1:7|I2:8@1$0|1$1@~7@48@@@1$0|2$0|1$0@~8@59@@@2$0@~9@54@@I1:10|I2:11@1$4|1$3@~10@55@@@2$0|1$0@~11@63@@@4$1|6$1@~12@48@@@1$0|2$0|1$0@#13@6@-634.2041,1278.462,0@I1:14@@~14@52@@I1:15|I2:16@2$0@~15@45@@@2$0|3$0@~16@57@@I1:17@@~17@52@@I2:18@2$0@~18@50@@@1$0|2$0@&400,2800&1|58466|aaa
        *
    [out]:
        none
    """

    def ParseGame(self, strgame, course_id):
        # 1. 解析项目所有块信息,构建语法树
        _blocklist = strgame.split(sb.SPLIT_INGAME1)
        if len(_blocklist) != 3:
            logging.critical('format invalidated!')
            return ""
        self.gameinfo.gamename = _blocklist[0]  # 1. game name
        _blocklist1 = re.split(
            "[" + sb.SPLIT_INGAME1_ATTR1 + sb.SPLIT_INGAME1_ATTR2 + "]",
            _blocklist[1])
        if len(_blocklist1) % 2 != 0:
            logging.critical('format invalidated!')
            return ""

        for i in range(0, len(_blocklist1), 2):
            if _blocklist1[i] == "C":
                self.gameinfo.createtype = int(_blocklist1[i + 1])  # 2. create type
            elif _blocklist1[i] == "G":
                self.gameinfo.grade = int(_blocklist1[i + 1])  # 3. grade
            else:
                logging.warning('no support type: ' + _blocklist1[i])

        _gameobject_str_list = _blocklist[2].split(sb.SPLIT_INGAME2)
        for i in range(len(_gameobject_str_list)):
            if len(_gameobject_str_list[i]) > 0:
                self.gameinfo.gameobject.append(
                    self.ParseGameObject(
                        _gameobject_str_list[i]))  #4. gameobject

        # 2. 构建广播,克隆,变量等网状关系
        self.create_event_relation(self.gameinfo)

        # 3. 收集基本评价指标
        self.collect_index()
        self.ct_index.create_map()

        # 4. 构建基于统计分布的评价指标,并计算基于统计的得分,进行均衡
        try:
            rule1 = ScoreGradeObjectivity1(course_id)
            score1 = rule1.calculate_score_with_balance(self.blockdist.dict_block_dist)
        except Exception as e:
            logging.error(e)
            return "", "块评分标准出错"

        # 5. 构建基于语法分析的评价指标,并计算基于语法的得分,进行均衡
        try:
            rule2 = ScoreGradeObjectivity2(course_id)
            score2 = rule2.calculate_score_with_balance_and_deduction(self.ct_index)
        except Exception as e:
            logging.error(e)
            return "", "语法评价标准出错"

        # 6. 重大扣分项
        self.report.score_calculator.set_originalscore(score1, rule1.rule,
                                                       score2, rule2.rule)
        score_adjust = self.report.score_calculator.calculating()

        # 7. 最终客观得分,CT权重重调
        score1.clear()
        score2.clear()
        score1 = score_adjust[0]
        score2 = score_adjust[1]

        if 0.0 == score1[8]:
            score2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        objectivity_score = []
        last_weight_base = []

        weight = 0.4  # weight of rule1 and rule2
        for i in range(9):
            objectivity_score.append(score1[i] * weight + score2[i] *
                                     (1 - weight))
        for i in range(8):
            last_weight_base.append(score1[i] * weight * rule1.rule[i][1] +
                                    score2[i] *
                                    (1 - weight) * rule2.rule[i][0])

        self.report.objectivity_score[1] = 0.0

        for i in range(8):
            if 0.0 != objectivity_score[8]:
                self.report.objectivity_score[2 + i][1] = last_weight_base[i] / objectivity_score[8]  # 两个规则的权数不同,不能简单用其中一个,或者两者用weight加权来计算
            self.report.objectivity_score[2 + i][2] = objectivity_score[i]
            self.report.objectivity_score[1] += self.report.objectivity_score[
                2 + i][2] * self.report.objectivity_score[2 + i][1]

        for i in range(8):
            self.report.objectivity_score[2 + i][1] = round(
                self.report.objectivity_score[2 + i][1], 2)
            self.report.objectivity_score[2 + i][2] = round(
                self.report.objectivity_score[2 + i][2], 2)
        self.report.objectivity_score[1] = round(
            self.report.objectivity_score[1], 2)

        # 8. 生成评述报告
        evaluatingReport = EvaluateingResult()
        #        # 8.1. 主观 set
        #        evaluatingReport.set_subjective_total_score(20)                # 主观满分20
        #        evaluatingReport.set_subjective_fullscore([6,4,4,4,2])         # 主观分项满分
        #        evaluatingReport.set_subjective_realscore([5,3,4,3,2])         # 主观分项得分
        #        evaluatingReport.cal_subjective_score()
        #        # 8.2. 客观 set
        #        evaluatingReport.set_objective_total_score(80)                 # 客观满分80
        #        object_score_dist = []
        #        for i in range(8):
        #            object_score_dist.append([self.report.objectivity_score[i+2][2],self.report.objectivity_score[i+2][1]])
        #        evaluatingReport.set_objective_score(object_score_dist)
        #        out_string = self.report.tostr()
        #        split_item = out_string.split(sb.SPLIT_SCORE_GRAMMAR)
        #        evaluatingReport.set_objective_checkresult_blockdist(split_item[1],self.blockdist.tostr())
        #        evaluatingReport.cal_objective_score(self.report.objectivity_score[1])
        #        # 8.3. 获取分项值
        #        # 8.3.1. 获取评分方式的主客观百分比
        #        outvalue1 = evaluatingReport.get_scale_of_marks() # [主(20),客(80)]
        #        print(outvalue1)
        #        # 8.3.2. 获取评测总分
        #        outvalue2 = evaluatingReport.get_total_score() # 总分
        #        print(outvalue2)
        #        # 8.3.3. 获取主观分数sum
        #        outvalue3 = evaluatingReport.get_subjective_total_score() # [主观总分,主观实际得分]
        #        print(outvalue3)
        #        # 8.3.4. 获取主观得分分项分数
        #        outvalue4 = evaluatingReport.get_subjective_score_detail() # [[1项满分,1项得分],,,,[5项满分,5项得分]]
        #        print(outvalue4)
        #        # 8.3.5. 获取客观分数sum
        #        outvalue5 = evaluatingReport.get_objective_total_score() # [客观满分, 客观得分, 客观百分制分数, 客观分数占比]
        #        print(outvalue5)
        #        # 8.3.6. 获取客观分数分项分值
        #        outvalue6 = evaluatingReport.get_objective_score_detail() # [百分制分数1,百分制分数2,...,百分制分数8]
        #        print(outvalue6)
        #        # 8.3.7. 获取主观评价评述
        #        outvalue7 = evaluatingReport.get_subject_statement() # 主观评述
        #        print(outvalue7)
        #        # 8.3.8. 获取客观评述评述
        #        outvalue8 = evaluatingReport.get_object_statement() # 客观评述
        #        print(outvalue8)
        #        # 8.3.9. 评价结果: 优|良|中|差，通过/不通过
        #        outvalue9 = evaluatingReport.get_last_test_result() # [优|良|中|差，通过/不通过]
        #        print(outvalue9)

        # 8.1. 主观 set
        evaluatingReport.set_subjective_total_score(0)  # 主观满分20
        evaluatingReport.set_subjective_fullscore([0, 0, 0, 0, 0])  # 主观分项满分
        evaluatingReport.set_subjective_realscore([0, 0, 0, 0, 0])  # 主观分项得分
        evaluatingReport.cal_subjective_score()
        # # 8.2. 客观 set
        evaluatingReport.set_objective_total_score(100)  # 客观满分80
        object_score_dist = []
        for i in range(8):
            object_score_dist.append([
                self.report.objectivity_score[i + 2][2],
                self.report.objectivity_score[i + 2][1]
            ])
        evaluatingReport.set_objective_score(object_score_dist)
        out_string = self.report.tostr()
        split_item = out_string.split(sb.SPLIT_SCORE_GRAMMAR)
        evaluatingReport.set_objective_checkresult_blockdist(
            split_item[1], self.blockdist.tostr())
        evaluatingReport.cal_objective_score(self.report.objectivity_score[1])
        # 8.3. 获取分项值
        #        # 8.3.1. 获取评分方式的主客观百分比
        # outvalue1 = evaluatingReport.get_scale_of_marks() # [主(20),客(80)]
        # print(outvalue1)
        #        # 8.3.2. 获取评测总分
        # outvalue2 = evaluatingReport.get_total_score() # 总分
        # print("all: ", outvalue2)
        #        # 8.3.3. 获取主观分数sum
        #        outvalue3 = evaluatingReport.get_subjective_total_score() # [主观总分,主观实际得分]
        #        print(outvalue3)
        #        # 8.3.4. 获取主观得分分项分数
        #        outvalue4 = evaluatingReport.get_subjective_score_detail() # [[1项满分,1项得分],,,,[5项满分,5项得分]]
        #        print(outvalue4)
        #        # 8.3.5. 获取客观分数sum
        #        outvalue5 = evaluatingReport.get_objective_total_score() # [客观满分, 客观得分, 客观百分制分数, 客观分数占比]
        #        print(outvalue5)
        #        # 8.3.6. 获取客观分数分项分值
        #        outvalue6 = evaluatingReport.get_objective_score_detail() # [百分制分数1,百分制分数2,...,百分制分数8]
        #        print(outvalue6)
        # # 8.3.7. 获取主观评价评述
        # outvalue7 = evaluatingReport.get_subject_statement()
        # # 主观评述
        # print(outvalue7)
        # 8.3.8. 获取客观评述评述
        outvalue8 = evaluatingReport.get_object_statement()  # 客观评述
        # print(outvalue8)
        #        # 8.3.9. 评价结果: 优|良|中|差，通过/不通过
        outvalue9 = evaluatingReport.get_last_test_result()  # [优|良|中|差，通过/不通过]
        # print(outvalue9)

        # 9. 输出结果
        return self.report.tostr() + outvalue8, ""

    """
    [in]:
        爆竹三
            &
        3
            &
        2
            &

            &
        1@4@-552.2653,1832.809,0@D:2@@~2@40@@D:3@4$1@~3@62@@@2$0|1$0@#4@7@-424.7472,1658.2,0@D:5@1$1@~5@103@@@1$1|1$0|1$0|1$0|2$0@
            &
        400,3200
            &
        1|55545|lA%1|55545|lB
    [out]:
        GameObjectInfo
    """

    def ParseGameObject(self, strgameobject):
        _blocklist = strgameobject.split(sb.SPLIT_INGAMEOBJECT1)
        #        if len(_blocklist) != 7:
        #            logging.critical('format invalidated!')
        #            return

        gobject = GameObjectInfo()

        gobject.gameobject_name = _blocklist[0]  # 1. 对象名称
        gobject.gameobject_id = int(_blocklist[1])  # 2. 对象id
        gobject.gameobject_type = int(
            _blocklist[2])  # 3. 对象类型 0:root,1:player,2:others
        if len(_blocklist[3]) != 0:  # 4. (属性名称,属性类型,属性值) _blocklist[3].
            _object_attr_list = re.split(
                "[" + sb.SPLIT_INGAMEOBJECT2_ATTR1 +
                sb.SPLIT_INGAMEOBJECT2_ATTR2 + "]", _blocklist[3])
            for i in range(0, len(_object_attr_list), 3):
                gobject.gameobject_attributes.append([
                    _object_attr_list[i],
                    int(_object_attr_list[i + 1]),
                    int(_object_attr_list[i + 2])
                ])

        gobject.variables_sets_local = [
        ]  # 7. 局部变量列表(变量类型,变量ID,变量名称,默认值),提前,后面分析脚本的时候需要知道本地变量
        if len(_blocklist) >= 7:
            if len(_blocklist[6]) != 0:
                if gobject.gameobject_type == 0:  # root,global variables
                    _variables_list = re.split(
                        "[" + sb.SPLIT_INGAMEOBJECT2_VARIABLES1 +
                        sb.SPLIT_INGAMEOBJECT2_VARIABLES2 + "]",
                        _blocklist[6])  # 暂时不做缺省值的类型转换
                    for i in range(0, len(_variables_list), 3):
                        if 0 == int(_variables_list[i]):  # global
                            self.gameinfo.variables_sets_global.append(
                                (int(_variables_list[i]),
                                 _variables_list[i + 1],
                                 _variables_list[i + 2], 0))
                        elif 1 == int(_variables_list[i]):  # local
                            gobject.variables_sets_local.append(
                                (int(_variables_list[i]),
                                 _variables_list[i + 1],
                                 _variables_list[i + 2], 0))
                        else:
                            pass
                else:  # local variable
                    _variables_list = re.split(
                        "[" + sb.SPLIT_INGAMEOBJECT2_VARIABLES1 +
                        sb.SPLIT_INGAMEOBJECT2_VARIABLES2 + "]",
                        _blocklist[6])  # 暂时不做缺省值的类型转换
                    for i in range(0, len(_variables_list), 3):
                        gobject.variables_sets_local.append(
                            (int(_variables_list[i]), _variables_list[i + 1],
                             _variables_list[i + 2], 0))

        _block_script_list = []
        if len(_blocklist) >= 5:
            if len(_blocklist[4]) != 0:
                _block_script_list = _blocklist[4].split(
                    sb.SPLIT_INGAMEOBJECT2_SCRIPT)
            for i in range(len(_block_script_list)):
                gobject.scripts_sets.append(
                    self.ParseScript(
                        gobject.gameobject_id, gobject.gameobject_name,
                        _block_script_list[i], i + 1,
                        len(gobject.variables_sets_local)))  # 5. 脚本列表

        if len(_blocklist) >= 6:
            if len(_blocklist[5]) != 0:
                _coordinate_list = _blocklist[5].split(
                    sb.SPLIT_INGAMEOBJECT2_COORDINATE)
                gobject.coordinatea = [
                    float(_coordinate_list[0]),
                    float(_coordinate_list[1])
                ]  # 6. 坐标
        else:
            gobject.coordinatea = [0.0, 0.0]

        return gobject

    '''
        解析 script 属性;
        [in]:  block # block # ... # block
        [out]: BlockInfo
    '''

    def ParseScript(self, gameobject_id, gameobject_name, strscript,
                    index_in_gameobject, local_var_count):
        scriptinfo = ScriptInfo()
        scriptinfo.scriptid = index_in_gameobject
        _blocklist = strscript.split(sb.SPLIT_INSCRIPT_BLOCK)
        for i in range(len(_blocklist)):
            scriptinfo.block_set.append(self.ParseBlock(_blocklist[i]))
            scriptinfo.block_dict_seqid_index[
                scriptinfo.block_set[-1].sequenceid] = len(
                    scriptinfo.block_set) - 1

        self.analyze_script(gameobject_id, gameobject_name, scriptinfo,
                            local_var_count)

        return scriptinfo

    def analyze_script(self, gameobject_id, gameobject_name, sc_info,
                       local_var_count):
        # 注意: 由于block的编号没有按照,直观语句次序进行编号,所以不能逐句分析,如: a, b(if . else d),c, c 在 d 的后面;
        for i in range(len(sc_info.block_set)):
            for j in range(len(sc_info.block_set)):
                if i == j:
                    continue
                # 1. check D
                if sc_info.block_set[j].sequenceid == sc_info.block_set[
                        i].brother_down:  # j 是 i 的兄弟
                    sc_info.block_set[j].brother_up = sc_info.block_set[
                        i].sequenceid
                # 2. check Mn
                elif sc_info.block_set[j].sequenceid in sc_info.block_set[
                        i].childblock_list1:
                    sc_info.block_set[
                        j].father_block_seqeneceid = sc_info.block_set[
                            i].sequenceid
                    # 通知所有兄弟
                    brother = sc_info.block_set[j].brother_down
                    while True:
                        if -1 != brother:
                            sc_info.block_set[sc_info.block_dict_seqid_index[
                                brother]].father_block_seqeneceid = sc_info.block_set[
                                    i].sequenceid  # 记住父
                            if sc_info.block_set[sc_info.block_dict_seqid_index[
                                    brother]].sequenceid not in sc_info.block_set[
                                        i].childblock_list1:  # 父记住子
                                sc_info.block_set[i].childblock_list1.append(
                                    brother)
                            brother = sc_info.block_set[
                                sc_info.
                                block_dict_seqid_index[brother]].brother_down
                            continue
                        else:
                            break
                elif sc_info.block_set[j].sequenceid in sc_info.block_set[
                        i].childblock_list2:  # j 是 i 的儿子,j的兄弟都是i的儿子
                    sc_info.block_set[
                        j].father_block_seqeneceid = sc_info.block_set[
                            i].sequenceid
                    # 通知所有兄弟
                    brother = sc_info.block_set[j].brother_down
                    while True:
                        if -1 != brother:
                            sc_info.block_set[sc_info.block_dict_seqid_index[
                                brother]].father_block_seqeneceid = sc_info.block_set[
                                    i].sequenceid  # 记住父
                            if sc_info.block_set[sc_info.block_dict_seqid_index[
                                    brother]].sequenceid not in sc_info.block_set[
                                        i].childblock_list2:  # 父记住子
                                sc_info.block_set[i].childblock_list2.append(
                                    brother)
                            brother = sc_info.block_set[
                                sc_info.
                                block_dict_seqid_index[brother]].brother_down
                            continue
                        else:
                            break
                # 3. check In
                elif sc_info.block_set[
                        j].is_parameter_block and sc_info.block_set[
                            j].sequenceid in sc_info.block_set[
                                i].parameter_info0:
                    # 记录父
                    if 1 == sc_info.block_set[i].is_parameter_block:  # i 是参数块
                        sc_info.block_set[
                            j].parameter_parent_block_sequenceid = sc_info.block_set[
                                i].sequenceid  # 记录父参数块
                        # 追踪非参数块父
                        ff = sc_info.block_set[i].sequenceid
                        while -1 != ff:
                            if -1 != sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        ff]].parameter_ancestor_block_seqenceid:
                                sc_info.block_set[
                                    j].parameter_ancestor_block_seqenceid = sc_info.block_set[
                                        sc_info.block_dict_seqid_index[
                                            ff]].parameter_ancestor_block_seqenceid  # 记录非参数块父
                                break
                            else:
                                ff = sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        ff]].parameter_parent_block_sequenceid
                    else:  # i 不是参数块,即为容器快
                        sc_info.block_set[
                            j].parameter_parent_block_sequenceid = -1  # 没有父参数块
                        sc_info.block_set[
                            j].parameter_ancestor_block_seqenceid = sc_info.block_set[
                                i].sequenceid  # 记录非参数块父
                    # 记录兄弟关系
                    index = sc_info.block_set[i].parameter_info0.index(
                        sc_info.block_set[j].sequenceid
                    )  # (2,-1,-1,3,5) seqenceid,不是block_set索引
                    info0_len = len(sc_info.block_set[i].parameter_info0)
                    for m in range(index - 1, -1, -1):
                        if sc_info.block_set[i].parameter_info0[m] != -1:
                            sc_info.block_set[
                                j].parameter_brother_left = sc_info.block_set[
                                    i].parameter_info0[m]
                            break
                    for m in range(index + 1, info0_len, 1):
                        if sc_info.block_set[i].parameter_info0[m] != -1:
                            sc_info.block_set[
                                j].parameter_brother_right = sc_info.block_set[
                                    i].parameter_info0[m]
                            break
                else:
                    pass

        for i in range(len(sc_info.block_set)):
            indent_depth = 1
            parameter_nest_depth = 1
            seqn = i
            if 1 == sc_info.block_set[i].is_parameter_block:  # 参数块
                # 1. parameter_nest_depth
                while True:
                    if -1 != sc_info.block_set[
                            seqn].parameter_parent_block_sequenceid:
                        parameter_nest_depth += 1
                        seqn = sc_info.block_dict_seqid_index[
                            sc_info.block_set[seqn].
                            parameter_parent_block_sequenceid]
                        continue
                    else:
                        break
                sc_info.block_set[
                    i].parameter_nest_depth = parameter_nest_depth
                # 2. param7_paramtype_blockrefid
                for param_count in range(
                        sc_info.block_set[i].parameter_count_need):
                    if sc_info.block_set[i].parameter_info[param_count][
                            5] > 0:  # 嵌套
                        if sc_info.block_set[i].parameter_info[param_count][4] & sb.PARAMTYPE_SC_BLKTYPE_CONDITION:
                            sc_info.block_set[i].parameter_info[param_count][6] = sc_info.block_set[sc_info.block_dict_seqid_index[
                                        sc_info.block_set[i].
                                        parameter_info[param_count][5]]].refid
                        elif sc_info.block_set[i].parameter_info[param_count][4] == sb.PARAMTYPE_SC_BLK_VARIABLES | sb.PARAMTYPE_SC_BLKTYPE_DATACAL:
                            sc_info.block_set[i].parameter_info[param_count][6] = sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        sc_info.block_set[i].
                                        parameter_info[param_count][5]]].refid
                            if sc_info.block_set[i].parameter_info[
                                    param_count][
                                        6] == sb.BLKREFID_VAR_VARIABLES:
                                sc_info.block_set[i].parameter_info[
                                    param_count][
                                        4] = sb.PARAMTYPE_SC_BLK_VARIABLES
                            else:
                                sc_info.block_set[i].parameter_info[
                                    param_count][
                                        4] = sb.PARAMTYPE_SC_BLKTYPE_DATACAL
            else:  # 非参数块
                # 1. indent_depth
                while True:
                    if -1 != sc_info.block_set[seqn].father_block_seqeneceid:
                        indent_depth += 1
                        #seqn = sc_info.block_set[seqn].father_block_seqeneceid - 1
                        seqn = sc_info.block_dict_seqid_index[
                            sc_info.block_set[seqn].father_block_seqeneceid]
                        continue
                    else:
                        break
                sc_info.block_set[i].indent_depth = indent_depth

                # 2. param7_paramtype_blockrefid
                for param_count in range(
                        sc_info.block_set[i].parameter_count_need):
                    if sc_info.block_set[i].parameter_info[param_count][
                            5] > 0:  # 嵌套
                        if sc_info.block_set[i].parameter_info[param_count][
                                4] & sb.PARAMTYPE_SC_BLKTYPE_CONDITION:
                            sc_info.block_set[i].parameter_info[param_count][
                                6] = sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        sc_info.block_set[i].
                                        parameter_info[param_count][5]]].refid
                        elif sc_info.block_set[i].parameter_info[param_count][
                                4] == sb.PARAMTYPE_SC_BLK_VARIABLES | sb.PARAMTYPE_SC_BLKTYPE_DATACAL:
                            sc_info.block_set[i].parameter_info[param_count][
                                6] = sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        sc_info.block_set[i].
                                        parameter_info[param_count][5]]].refid
                            if sc_info.block_set[i].parameter_info[
                                    param_count][
                                        6] == sb.BLKREFID_VAR_VARIABLES:
                                sc_info.block_set[i].parameter_info[
                                    param_count][
                                        4] = sb.PARAMTYPE_SC_BLK_VARIABLES
                            else:
                                sc_info.block_set[i].parameter_info[
                                    param_count][
                                        4] = sb.PARAMTYPE_SC_BLKTYPE_DATACAL
                        if sc_info.block_set[
                                i].refid == sb.BLKREFID_VAR_VARIABLESASSIGNMENT:  # 2019/12/11 add
                            sc_info.block_set[i].parameter_info[param_count][
                                6] = sc_info.block_set[
                                    sc_info.block_dict_seqid_index[
                                        sc_info.block_set[i].
                                        parameter_info[param_count][5]]].refid

        # 计算block用时
        first_block_seqeunceid = sc_info.block_set[0].sequenceid
        self.calucate_runtime(sc_info, first_block_seqeunceid)
        next_brother_block_sequenceid = sc_info.block_set[
            sc_info.
            block_dict_seqid_index[first_block_seqeunceid]].brother_down
        while next_brother_block_sequenceid != -1:
            self.calucate_runtime(sc_info, next_brother_block_sequenceid)
            next_brother_block_sequenceid = sc_info.block_set[
                sc_info.block_dict_seqid_index[
                    next_brother_block_sequenceid]].brother_down

        # 属性分析
        if sc_info.block_set[0].blocktype == sb.BLKTYPE_TRIGGER:  # 是否有触点
            sc_info.has_trigger = 1
            if sc_info.block_set[0].refid == sb.BLKREFID_TRG_WHENPROJECTSTART:
                sc_info.be_trigger_atworking = 1  # 工程运行时触发

        block_nest_depth = 0  # 语句块嵌套深度
        paramblock_nest_depth = 0  # 参数块嵌套深度
        stateparamblock_nest_depth = 0  # 语句块参数块混合嵌套深度
        nest_useless = 0  # 无效的嵌套数目
        running_time = 0  # script可能运行时间
        for i in range(len(sc_info.block_set)):
            # 语句块嵌套深度
            # 参数块嵌套深度
            # 语句块参数块混合嵌套深度
            if 1 == sc_info.block_set[i].is_parameter_block:  # 参数块
                if paramblock_nest_depth < sc_info.block_set[
                        i].parameter_nest_depth:
                    paramblock_nest_depth = sc_info.block_set[
                        i].parameter_nest_depth
                # report script 3
                if sc_info.block_set[i].parameter_nest_depth > self.standard.rule_abstraction[1][14][5][2]:
                    self.report.add_script_param_nest(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid,
                        sc_info.block_set[i].parameter_nest_depth)

                ancestor_block_seqenceid = sc_info.block_set[
                    i].parameter_ancestor_block_seqenceid
                if -1 != ancestor_block_seqenceid:  # 有
                    ancestor_block_index = sc_info.block_dict_seqid_index[
                        ancestor_block_seqenceid]
                    if stateparamblock_nest_depth < sc_info.block_set[
                            i].parameter_nest_depth + sc_info.block_set[
                                ancestor_block_index].indent_depth:
                        stateparamblock_nest_depth = sc_info.block_set[
                            i].parameter_nest_depth + sc_info.block_set[
                                ancestor_block_index].indent_depth
                        # report script 4
                        if sc_info.block_set[
                                i].parameter_nest_depth + sc_info.block_set[
                                    ancestor_block_index].indent_depth > self.standard.rule_abstraction[1][16][5][2]:
                            self.report.add_script_stateparam_nest(
                                gameobject_id, gameobject_name,
                                sc_info.scriptid,
                                sc_info.block_set[i].sequenceid,
                                sc_info.block_set[i].parameter_nest_depth +
                                sc_info.block_set[ancestor_block_index].
                                indent_depth)
                else:  # 没有
                    if stateparamblock_nest_depth < sc_info.block_set[
                            i].parameter_nest_depth:
                        sc_info.block_set[
                            i].stateparamblock_nest_depth = sc_info.block_set[
                                i].parameter_nest_depth

            else:  # 非参数块
                if block_nest_depth < sc_info.block_set[i].indent_depth:
                    block_nest_depth = sc_info.block_set[i].indent_depth
                if stateparamblock_nest_depth < sc_info.block_set[
                        i].indent_depth:
                    stateparamblock_nest_depth = sc_info.block_set[
                        i].indent_depth
                # report script 2
                if sc_info.block_set[i].indent_depth > self.standard.rule_abstraction[1][3][5][2]:
                    self.report.add_script_state_nest(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid,
                        sc_info.block_set[i].indent_depth)

            # 无效的嵌套数目
            if sb.BLKREFID_DC_VARIABLECELL == sc_info.block_set[i].refid:
                param_block_seqenceid = sc_info.block_set[
                    i].parameter_parent_block_sequenceid
                if -1 != param_block_seqenceid:
                    param_block_index = sc_info.block_dict_seqid_index[
                        param_block_seqenceid]
                    if sb.BLKREFID_DC_VARIABLECELL == sc_info.block_set[
                            param_block_index].refid:
                        nest_useless += 1
                        # report script 5
                        self.report.add_script_useless_nest(
                            gameobject_id, gameobject_name, sc_info.scriptid,
                            sc_info.block_set[i].sequenceid)

        # script可能运行时间
        first_block_seqeunceid = sc_info.block_set[0].sequenceid
        first_block_index = sc_info.block_dict_seqid_index[
            first_block_seqeunceid]
        running_time += sc_info.block_set[first_block_index].time_used
        next_brother_block_sequenceid = sc_info.block_set[
            first_block_index].brother_down
        while next_brother_block_sequenceid != -1:
            if running_time >= sb.MAX_TIME:
                break
            block_index = sc_info.block_dict_seqid_index[
                next_brother_block_sequenceid]
            running_time += sc_info.block_set[block_index].time_used
            if running_time >= sb.MAX_TIME:
                break
            next_brother_block_sequenceid = sc_info.block_set[
                block_index].brother_down

        sc_info.block_nest_depth = block_nest_depth  # 语句块嵌套深度
        sc_info.paramblock_nest_depth = paramblock_nest_depth  # 参数块嵌套深度
        sc_info.stateparamblock_nest_depth = stateparamblock_nest_depth  # 语句块参数块混合嵌套深度
        sc_info.nest_useless = nest_useless  # 无效的嵌套数目
        sc_info.running_time = running_time  # script可能运行时间

        # 处理循环和条件数据
        for i in range(len(sc_info.block_set)):
            if sc_info.block_set[
                    i].refid == sb.BLKREFID_CND_BOOLANDOR or sc_info.block_set[
                        i].refid == sb.BLKREFID_CND_BOOLNOT:  # 条件块,检查它的非参数块祖先是否为条件块,如果是,自己缺参数,则条件块也缺参数
                ancestor_sequenceid = sc_info.block_set[
                    i].parameter_ancestor_block_seqenceid
                if -1 != ancestor_sequenceid:
                    ancestor_index = sc_info.block_dict_seqid_index[
                        ancestor_sequenceid]
                    if sc_info.block_set[
                            ancestor_index].refid == sb.BLKREFID_LF_IF or sc_info.block_set[
                                ancestor_index].refid == sb.BLKREFID_LF_IFELSE:
                        if sc_info.block_set[
                                i].refid == sb.BLKREFID_CND_BOOLANDOR:
                            if 0 == sc_info.block_set[i].parameter_info[0][
                                    7] or 0 == sc_info.block_set[
                                        i].parameter_info[2][7]:
                                sc_info.block_set[
                                    ancestor_index].parameter_info[0][7] = 0
                        elif sc_info.block_set[
                                i].refid == sb.BLKREFID_CND_BOOLNOT:
                            if 0 == sc_info.block_set[i].parameter_info[0][7]:
                                sc_info.block_set[
                                    ancestor_index].parameter_info[0][7] = 0
                        else:
                            pass
                    else:
                        pass
            if sc_info.block_set[
                    i].refid == sb.BLKREFID_VAR_VARIABLES:  # 变量块,检查它的非参数块祖先是否为条件块,如果是,自己缺参数,则条件块也缺参数
                ancestor_sequenceid = sc_info.block_set[
                    i].parameter_ancestor_block_seqenceid
                if -1 != ancestor_sequenceid:
                    ancestor_index = sc_info.block_dict_seqid_index[
                        ancestor_sequenceid]
                    if sc_info.block_set[
                            ancestor_index].refid == sb.BLKREFID_LF_IF or sc_info.block_set[
                                ancestor_index].refid == sb.BLKREFID_LF_IFELSE:
                        if 0 == sc_info.block_set[i].parameter_info[0][
                                2] and 0 == len(
                                    self.gameinfo.variables_sets_global
                                ) and 0 == local_var_count:
                            sc_info.block_set[ancestor_index].parameter_info[
                                0][7] = 0
                            sc_info.block_set[i].parameter_info[0][
                                7] = 0  # 变量块此时才能判断合法性
                # report vairiables 4
                if 0 == sc_info.block_set[i].parameter_info[0][2] and 0 == len(
                        self.gameinfo.variables_sets_global
                ) and 0 == local_var_count:
                    self.report.add_variables_varblock_noselected(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)

        for i in range(len(sc_info.block_set)):
            if (sc_info.block_set[i].refid == sb.BLKREFID_LF_LOOPUNLIMITED
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_LOOPNUMBER
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_LOOP_WHILE_WHILENOT
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_LOOP_STEP
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_LOOP_TRAVERSELIST
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_IFELSE_PLUS
                or sc_info.block_set[i].refid == sb.BLKREFID_LF_IF):
                sc_info.loop_index_number_totals += 1  # 5.1. contain循环: (+)循环数目
                if sc_info.block_set[i].has_child1 < 1:
                    sc_info.loop_index_number_no_statement += 1  # 4.4 if,if else下面没有block的数目
                    # report loop 2
                    self.report.add_loop_noblock(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
                # 向上追溯
                nest_depth = 1
                father_sequenceid = sc_info.block_set[
                    i].father_block_seqeneceid
                while -1 != father_sequenceid:
                    father_index = sc_info.block_dict_seqid_index[
                        father_sequenceid]
                    if (
                        sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOPUNLIMITED
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOPNUMBER
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_WHILE_WHILENOT
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_STEP
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_TRAVERSELIST
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_IFELSE_PLUS
                        or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_IF
                        ):
                        nest_depth += 1
                    else:
                        pass
                    father_sequenceid = sc_info.block_set[
                        father_index].father_block_seqeneceid

                # report loop 1
                if nest_depth > self.standard.rule_flowcontrol[0][3][5][2]:
                    self.report.add_loop_nest(gameobject_id, gameobject_name,
                                              sc_info.scriptid,
                                              sc_info.block_set[i].sequenceid,
                                              nest_depth)
                if nest_depth > sc_info.loop_index_nest_depth:
                    sc_info.loop_index_nest_depth = nest_depth  # 5.2 循环嵌套深度
                sc_info.loop_index_endlessloop_nobreak = 0  # 5.3 死循环数目(不能跳出,或者break条件永不为真)[暂不处理]
                sc_info.loop_index_endlessloop_nowait = 0  # 5.4 死循环数目(循环体中没有阻塞)[暂不处理]
                sc_info.loop_index_nest_depth_total += nest_depth  # 累计脚本中的条件语句嵌套深度
            elif sc_info.block_set[i].refid == sb.BLKREFID_LF_IF:
                sc_info.condition_index_number_if += 1  # 4.2. contain条件: (+)if数目
                if sc_info.block_set[i].has_child1 < 1:
                    sc_info.condition_index_number_no_statement += 1  # 4.4 if,if else下面没有block的数目
                    # report condition 3
                    self.report.add_condition_noblock(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
                if 0 == sc_info.block_set[i].parameter_info[0][7]:
                    sc_info.condition_index_number_param_imcompleted += 1  # 4.5 if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
                    # report condition 2
                    self.report.add_condition_noparam(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
                sc_info.condition_index_number_param_variables_nochanged = 0  # 4.6 条件表达式中的变量外部不变数目(基于嵌套顶层)[暂不处理]
                sc_info.condition_index_number_true_forever = 0  # 4.7 条件永假数目(基于嵌套顶层)[暂不处理]
                sc_info.condition_index_number_false_forever = 0  # 4.8 条件永真数目(基于嵌套顶层)[暂不处理]
                # 向上追溯
                nest_depth = 1
                father_sequenceid = sc_info.block_set[
                    i].father_block_seqeneceid
                while -1 != father_sequenceid:
                    father_index = sc_info.block_dict_seqid_index[
                        father_sequenceid]
                    if (sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOPUNLIMITED
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOPNUMBER
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_WHILE_WHILENOT
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_STEP
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_LOOP_TRAVERSELIST
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_IFELSE_PLUS
                            or sc_info.block_set[father_index].refid == sb.BLKREFID_LF_IF):
                        nest_depth += 1
                    else:
                        pass
                    father_sequenceid = sc_info.block_set[
                        father_index].father_block_seqeneceid
                # report condition 1
                if nest_depth > self.standard.rule_logical[1][4][5][3]:
                    self.report.add_condition_nest(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid, nest_depth)
                if nest_depth > sc_info.condition_index_nest_depth:
                    sc_info.condition_index_nest_depth = nest_depth  # 4.3 条件嵌套最大深度(跳过loop)
                sc_info.condition_index_nest_depth_total += nest_depth  # 累计脚本中的条件语句嵌套深度
            elif (sc_info.block_set[i].refid == sb.BLKREFID_LF_IFELSE
                    or sc_info.block_set[i].refid == sb.BLKREFID_LF_IFELSE_PLUS):
                sc_info.condition_index_number_ifelse += 1  # 4.1. contain条件: (+)ifelse数目
                if sc_info.block_set[i].has_child1 < 1 or sc_info.block_set[
                        i].has_child2 < 1:
                    sc_info.condition_index_number_no_statement += 1  # 4.4 if,if else下面没有block的数目
                    # report condition 3
                    self.report.add_condition_noblock(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
                if 0 == sc_info.block_set[i].parameter_info[0][7]:
                    sc_info.condition_index_number_param_imcompleted += 1  # 4.5 if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
                    # report condition 2
                    self.report.add_condition_noparam(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
                sc_info.condition_index_number_param_variables_nochanged = 0  # 4.6 条件表达式中的变量外部不变数目(基于嵌套顶层)[暂不处理]
                sc_info.condition_index_number_true_forever = 0  # 4.7 条件永假数目(基于嵌套顶层)[暂不处理]
                sc_info.condition_index_number_false_forever = 0  # 4.8 条件永真数目(基于嵌套顶层)[暂不处理]
                # 向上追溯
                nest_depth = 1
                father_sequenceid = sc_info.block_set[
                    i].father_block_seqeneceid
                while -1 != father_sequenceid:
                    father_index = sc_info.block_dict_seqid_index[
                        father_sequenceid]
                    if sc_info.block_set[
                            father_index].refid == sb.BLKREFID_LF_IF or sc_info.block_set[
                                father_index].refid == sb.BLKREFID_LF_IFELSE:
                        nest_depth += 1
                    else:
                        pass
                    father_sequenceid = sc_info.block_set[
                        father_index].father_block_seqeneceid
                # report condition 1
                if nest_depth > self.standard.rule_logical[1][4][5][2]:
                    self.report.add_condition_nest(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid, nest_depth)
                if nest_depth > sc_info.condition_index_nest_depth:
                    sc_info.condition_index_nest_depth = nest_depth  # 4.3 条件嵌套最大深度(跳过loop)   
                sc_info.condition_index_nest_depth_total += nest_depth  # 累计脚本中的条件语句嵌套深度
            else:
                pass
        # 顺序块
        block_sequenceid = sc_info.block_set[0].sequenceid
        while block_sequenceid > 0:
            sc_info.sequenceblock_index_number_top_max += 1  # 6.1 一级顺序块最大数目
            block_sequenceindex = sc_info.block_dict_seqid_index[
                block_sequenceid]
            block_sequenceid = sc_info.block_set[
                block_sequenceindex].brother_down
        for i in range(len(sc_info.block_set)):
            if sc_info.block_set[
                    i].refid == sb.BLKREFID_LF_IFELSE or sc_info.block_set[
                        i].refid == sb.BLKREFID_LF_IF:
                if len(sc_info.block_set[i].childblock_list1
                       ) > sc_info.sequenceblock_index_number_if_max:
                    sc_info.sequenceblock_index_number_if_max = len(
                        sc_info.block_set[i].childblock_list1
                    )  # 6.2 if中的一级顺序块最大数目
            elif sc_info.block_set[
                    i].refid == sb.BLKREFID_LF_LOOPUNLIMITED or sc_info.block_set[
                        i].refid == sb.BLKREFID_LF_LOOPNUMBER:
                if len(sc_info.block_set[i].childblock_list1
                       ) > sc_info.sequenceblock_index_number_loop_max:
                    sc_info.sequenceblock_index_number_loop_max = len(
                        sc_info.block_set[i].childblock_list1
                    )  # 6.3 loop中的一级顺序块最大数目
                if len(sc_info.block_set[i].childblock_list2
                       ) > sc_info.sequenceblock_index_number_loop_max:
                    sc_info.sequenceblock_index_number_loop_max = len(
                        sc_info.block_set[i].childblock_list2
                    )  # 6.3 loop中的一级顺序块最大数目
            else:
                pass

        # wait
        for i in range(len(sc_info.block_set)):
            if sc_info.block_set[i].refid == sb.BLKREFID_LF_WAITNUMBERSECONDS:
                sc_info.wait_index_number += 1  # 7.1 wait数目
                if sc_info.block_set[i].parameter_info[0][
                        2] > sc_info.wait_index_max_waittime:
                    sc_info.wait_index_max_waittime = sc_info.block_set[
                        i].parameter_info[0][2]  # 7.2 wait最大等待时间
                # report wait
                if sc_info.block_set[i].parameter_info[0][
                        2] > self.standard.rule_sync[1][3][4][1]:
                    self.report.add_wait_longtime(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid,
                        sc_info.block_set[i].parameter_info[0][2])

        # 8. logicalexpr
        for i in range(len(sc_info.block_set)):
            if sc_info.block_set[i].refid == sb.BLKREFID_CND_NUMBERISOJZZZF or \
               sc_info.block_set[i].refid == sb.BLKREFID_CND_EXACTDIVISION or \
               sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLANDOR or \
               sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLCOMPARE or \
               sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLNOT:
                sc_info.logicalexpr_index_number_totals += 1  # 8.1 逻辑表达式数目
                if sc_info.block_set[
                        i].parameter_nest_depth > sc_info.logicalexpr_index_number_nest_depth_max:
                    sc_info.logicalexpr_index_number_nest_depth_max = sc_info.block_set[
                        i].parameter_nest_depth  # 8.3 逻辑表达式参数嵌套最大深度
                # report logical expression 1
                if sc_info.block_set[
                        i].parameter_nest_depth > self.standard.rule_logical[
                            2][4][5][2]:
                    self.report.add_expression_nest(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid,
                        sc_info.block_set[i].parameter_nest_depth)
                sc_info.logicalexpr_index_number_nest_depth_avg += sc_info.block_set[
                    i].parameter_nest_depth  # 8.4 逻辑表达式参数嵌套平均深度
            if sc_info.block_set[i].refid == sb.BLKREFID_CND_NUMBERISOJZZZF:
                sc_info.logicalexpr_index_number_type[0] += 1  # 8.2 逻辑表达式种类数目
            elif sc_info.block_set[i].refid == sb.BLKREFID_CND_EXACTDIVISION:
                sc_info.logicalexpr_index_number_type[1] += 1  # 8.2 逻辑表达式种类数目
            elif sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLANDOR:
                sc_info.logicalexpr_index_number_type[2] += 1  # 8.2 逻辑表达式种类数目
                if 0 == sc_info.block_set[i].parameter_info[0][
                        7] or 0 == sc_info.block_set[i].parameter_info[2][7]:
                    sc_info.logicalexpr_index_number_param_imcompleted += 1  # 8.5 逻辑表达式缺参数数目(向上传递)
                    # report logical expression 2
                    self.report.add_expression_noparam(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
            elif sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLCOMPARE:
                sc_info.logicalexpr_index_number_type[3] += 1  # 8.2 逻辑表达式种类数目
            elif sc_info.block_set[i].refid == sb.BLKREFID_CND_BOOLNOT:
                sc_info.logicalexpr_index_number_type[4] += 1  # 8.2 逻辑表达式种类数目
                if 0 == sc_info.block_set[i].parameter_info[0][7]:
                    sc_info.logicalexpr_index_number_param_imcompleted += 1  # 8.5 逻辑表达式缺参数数目(向上传递)
                    # report logical expression 2
                    self.report.add_expression_noparam(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)
            else:
                pass
        if sc_info.logicalexpr_index_number_totals > 0:
            sc_info.logicalexpr_index_number_nest_depth_avg = sc_info.logicalexpr_index_number_nest_depth_avg / sc_info.logicalexpr_index_number_totals  # 8.4 逻辑表达式参数嵌套平均深度

        # 9. check block 1 2019/12/11
        for i in range(len(sc_info.block_set)):
            if sc_info.block_set[i].refid == sb.BLKREFID_VAR_LIST:
                if 0 == sc_info.block_set[i].parameter_count:
                    # report block 1
                    self.report.add_list_noitem(
                        gameobject_id, gameobject_name, sc_info.scriptid,
                        sc_info.block_set[i].sequenceid)

    '''
        解析 block 属性;
        [in]:  1@4@-930.4897,431.9926,0@D:2@@
        [out]: BlockInfo
    '''

    def ParseBlock(self, strblock):
        _subentitylist = strblock.split(sb.SPLIT_INBLOCK_ATTRIBUTION5)
        if len(_subentitylist) != 6:
            logging.critical('format invalidated!')
            return -1
        location = re.split(
            "[" + sb.SPLIT_INBLOCK_LOCATION_VALUE_TYPE +
            sb.SPLIT_INBLOCK_LOCATION_VALUE_DMI + "]",
            _subentitylist[3])  # ['M', '5', 'D', '15', 'I1', '3']
        parameter_default_value = re.split(
            "[" + sb.SPLIT_INBLOCK_DEFAULT_VALUE_DEF +
            sb.SPLIT_INBLOCK_DEFAULT_VALUE_ARGTYPE9 + "]",
            _subentitylist[4])  # ['1', '0', '2', '5', '3', '8']
        # 将块中的默认值转义时符号的变化转为正确符号
        parameter_default_value = [str_replace(i) for i in parameter_default_value]

        block = BlockInfo()

        # 1. block 自有属性
        # 1.1 block 自有基本信息 7
        block.sequenceid = int(
            _subentitylist[0])  #1.1.1t 在script中的序号(script中的次序),base = 1
        block.refid = int(_subentitylist[1])  #1.1.2t 参考序号(每个block类型的编号)
        """
        统计块的分布
        """
        self.blockdist.add_block(block.refid)

        if block.refid in sb.DictBlockAttribute.keys():
            block.blocktype = sb.DictBlockAttribute[block.refid][sb.BLKATTR_CATEGORY]  #1.1.3t 类型
            block.controltype = sb.DictBlockAttribute[block.refid][sb.BLKATTR_CONTROLTYPE]  #1.1.7t # 控件类型
        else:
            logging.warn("not support block: %s" % block.refid)
            block.blocktype = sb.BLKTYPE_OBJECTACTION  #1.1.3t 类型
            block.controltype = sb.CT_NONE  #1.1.7t # 控件类型

        coor = _subentitylist[2].split(sb.SPLIT_INBLOCK_COORDINATE)  #1.1.6t 坐标
        if len(coor) == 3:
            block.coordinate[0] = float(coor[0])
            block.coordinate[1] = float(coor[1])
            block.coordinate[2] = float(coor[2])

        # 2 自有参数属性
        # 2.1 参数基本信息及子关系 7
        block.is_parameter_block = self.isparameterblock(
            block.blocktype, block.refid)  #2.1.1* 是否是参数 block
        if 1 == block.is_parameter_block:
            block.parameter_nest_depth = 1  #2.1.2*- 参数嵌入层级s"
        else:
            block.parameter_nest_depth = 0
        if block.refid in sb.DictBlockAttribute.keys():
            block.parameter_count_need = sb.DictBlockAttribute[block.refid][
                sb.BLKATTR_PARAMETERCOUNT]  #2.1.4* 参数数目(本层,不考虑嵌套参数影响)
            block.parameter_count = block.parameter_count_need  #2.1.5* 参数数目(本层,不考虑嵌套参数影响)
            block.parameter_argtype = sb.DictBlockAttribute[block.refid][
                sb.BLKATTR_ARGTYPE]  #2.1.6* 参数可以使用的类型(25)
        else:
            block.parameter_count_need = 0  #2.1.4* 参数数目(本层,不考虑嵌套参数影响)
            block.parameter_count = 0  #2.1.5* 参数数目(本层,不考虑嵌套参数影响)
            block.parameter_argtype = 0  #2.1.6* 参数可以使用的类型(25)

        # 参数个数可变, 2019/12/12 add,根据"I"动态计算参数数目;
        if -1 == block.parameter_count:
            if len(parameter_default_value) % 2 != 0:
                block.parameter_count_need = 0
                block.parameter_count = 0
            else:
                block.parameter_count_need = int(
                    len(parameter_default_value) / 2)
                block.parameter_count = int(len(parameter_default_value) / 2)

            j = 0  # for 处理缺省值
            k = 1  # for 处理嵌入参数,注意list从 2 开始
            for i in range(block.parameter_count_need
                           ):  # check 每个参数项,处理缺省值,以及嵌入子参数block
                # ['1', '0', '2', '5', '3', '8']
                # 非condition,condition,非condition,非condition
                param1_index = i + 1  #2.1.7.1* 参数序号/从左到右次序/ base 1 #
                param2_argtype = int(parameter_default_value[j]
                                     )  #2.1.7.2* 参数类型1(1-8,条件表达式不标),条件框没有缺省值 #
                j += 1
                param3_default_value = parameter_default_value[
                    j]  #2.1.7.3* 参数值(缺省值) #
                j += 1
                param4_paramtype_sets = block.parameter_argtype[
                    0]  #2.1.7.4* 可有参数类型2(1-25),不能提前预知 #

                k += 1
                instr = 'I' + str(
                    k)  # In编号规则,只对CT_NUMBERBOX,CT_CONDITIONBOX,CT_TEXTBOX
                if instr in location:
                    nblockindex = location[location.index(instr) + 1]
                    param5_paramtype_instantce = sb.PARAMTYPE_SC_BLK_VARIABLES | sb.PARAMTYPE_SC_BLKTYPE_DATACAL  #2.1.7.5 实际参数类型2(1-25) #
                    param6_paramtype_blockid = int(
                        nblockindex)  #2.1.7.6* 参数块编号 #
                    param7_paramtype_blockrefid = -1  #2.1.7.7 参数参考序号 #
                    param8_is_validated = 1  #2.1.7.8* 是否合法 #
                else:
                    param5_paramtype_instantce = sb.PARAMTYPE_SD_TEXT  #2.1.7.5* 实际参数类型2(1-25) #
                    param6_paramtype_blockid = -1  #2.1.7.6* 参数块编号 #
                    param7_paramtype_blockrefid = -1  #2.1.7.7* 参数参考序号 #
                    param8_is_validated = 1  #2.1.7.8* 是否合法 #

                paraminfo = []
                paraminfo.append(param1_index)  #2.1.7.1 参数序号/从左到右次序/ base 1 #
                paraminfo.append(
                    param2_argtype)  #2.1.7.2 参数类型1(1-8,条件表达式不标),条件框没有缺省值
                paraminfo.append(param3_default_value)  #2.1.7.3 参数值(缺省值)
                paraminfo.append(param4_paramtype_sets)  #2.1.7.4 可有参数类型2(1-25)
                paraminfo.append(
                    param5_paramtype_instantce)  #2.1.7.5 实际参数类型2(1-25)
                paraminfo.append(param6_paramtype_blockid)  #2.1.7.6 参数块编号
                paraminfo.append(param7_paramtype_blockrefid)  #2.1.7.7 参数参考序号
                paraminfo.append(param8_is_validated)  #2.1.7.8 是否合法

                block.parameter_info.append(paraminfo)  #2.1.7 参数信息
                block.parameter_info0.append(param6_paramtype_blockid)  # 2.1.8
        else:
            j = 0  # for 处理缺省值
            k = 0  # for 处理嵌入参数
            for i in range(block.parameter_count_need):  # check 每个参数项,处理缺省值,以及嵌入子参数block
                # ['1', '0', '2', '5', '3', '8']
                # 非condition,condition,非condition,非condition
                param1_index = i + 1  #2.1.7.1* 参数序号/从左到右次序/ base 1 #
                if block.parameter_argtype[i] & sb.PARAMTYPE_SC_BLKTYPE_CONDITION:  #处理缺省值
                    param2_argtype = sb.ARGTYPE_CONDITION  #2.1.7.2* 参数类型1(1-8,条件表达式不标),条件框没有缺省值 #
                    param3_default_value = -1  #2.1.7.3* 参数值(缺省值) #
                else:
                    param2_argtype = int(
                        parameter_default_value[j]
                    )  #2.1.7.2* 参数类型1(1-8,条件表达式不标),条件框没有缺省值 #
                    j += 1
                    if block.controltype[i] == sb.CT_TEXTBOX:
                        param3_default_value = parameter_default_value[
                            j]  #2.1.7.3* 参数值(缺省值) #
                    else:
                        if 0 != len(parameter_default_value[j]):
                            param3_default_value = round(
                                float(parameter_default_value[j]))
                        else:
                            param3_default_value = -1
                    j += 1
                param4_paramtype_sets = block.parameter_argtype[
                    i]  #2.1.7.4* 可有参数类型2(1-25) #

                if block.controltype[i] == sb.CT_NUMBERBOX or block.controltype[i] == sb.CT_CONDITIONBOX or block.controltype[i] == sb.CT_TEXTBOX:  # 注意:只对这些可嵌入参数block的参数编号,1,2,...
                    k += 1
                    instr = 'I' + str(k)  # In编号规则,只对CT_NUMBERBOX,CT_CONDITIONBOX,CT_TEXTBOX
                    if instr in location:
                        nblockindex = location[location.index(instr) + 1]
                        if block.controltype[i] == sb.CT_CONDITIONBOX:
                            param5_paramtype_instantce = sb.PARAMTYPE_SC_BLKTYPE_CONDITION  #2.1.7.5* 实际参数类型2(1-25) #
                            param6_paramtype_blockid = int(
                                nblockindex)  #2.1.7.6* 参数块编号 #
                            param7_paramtype_blockrefid = -1  #2.1.7.7 参数参考序号
                            param8_is_validated = 1  #2.1.7.8* 是否合法 #
                        else:
                            param5_paramtype_instantce = sb.PARAMTYPE_SC_BLK_VARIABLES | sb.PARAMTYPE_SC_BLKTYPE_DATACAL  #2.1.7.5 实际参数类型2(1-25) #
                            param6_paramtype_blockid = int(
                                nblockindex)  #2.1.7.6* 参数块编号 #
                            param7_paramtype_blockrefid = -1  #2.1.7.7 参数参考序号 #
                            param8_is_validated = 1  #2.1.7.8* 是否合法 #
                    else:
                        if block.controltype[i] == sb.CT_CONDITIONBOX:  ### error,缺少条件表达式
                            param5_paramtype_instantce = 0  #2.1.7.5* 实际参数类型2(1-25) #
                            param6_paramtype_blockid = -1  #2.1.7.6* 参数块编号 #
                            param7_paramtype_blockrefid = -1  #2.1.7.7* 参数参考序号 #
                            param8_is_validated = 0  #2.1.7.8* 是否合法 #
                            block.parameter_count -= 1
                        elif block.controltype[i] == sb.CT_NUMBERBOX:
                            param5_paramtype_instantce = sb.PARAMTYPE_SD_NUMBER  #2.1.7.5* 实际参数类型2(1-25) #
                            param6_paramtype_blockid = -1  #2.1.7.6* 参数块编号 #
                            param7_paramtype_blockrefid = -1  #2.1.7.7* 参数参考序号 #
                            param8_is_validated = 1  #2.1.7.8* 是否合法 #
                        else:
                            param5_paramtype_instantce = sb.PARAMTYPE_SD_TEXT  #2.1.7.5* 实际参数类型2(1-25) #
                            param6_paramtype_blockid = -1  #2.1.7.6* 参数块编号 #
                            param7_paramtype_blockrefid = -1  #2.1.7.7* 参数参考序号 #
                            param8_is_validated = 1  #2.1.7.8* 是否合法 #
                else:
                    param5_paramtype_instantce = block.parameter_argtype[
                        i]  #2.1.7.5* 实际参数类型2(1-25) #
                    param6_paramtype_blockid = -1  #2.1.7.6* 参数块编号 #
                    param7_paramtype_blockrefid = -1  #2.1.7.7* 参数参考序号 #
                    param8_is_validated = 1  #2.1.7.8* 是否合法 #
                if (block.parameter_argtype[i] & sb.PARAMTYPE_SD_SOUND
                    ) and param3_default_value == 0:  # source没有赋值
                    param8_is_validated = 0
                    block.parameter_count -= 1

                paraminfo = []
                paraminfo.append(param1_index)  #2.1.7.1 参数序号/从左到右次序/ base 1 #
                paraminfo.append(
                    param2_argtype)  #2.1.7.2 参数类型1(1-8,条件表达式不标),条件框没有缺省值
                paraminfo.append(param3_default_value)  #2.1.7.3 参数值(缺省值)
                paraminfo.append(param4_paramtype_sets)  #2.1.7.4 可有参数类型2(1-25)
                paraminfo.append(
                    param5_paramtype_instantce)  #2.1.7.5 实际参数类型2(1-25)
                paraminfo.append(param6_paramtype_blockid)  #2.1.7.6 参数块编号
                paraminfo.append(param7_paramtype_blockrefid)  #2.1.7.7 参数参考序号
                paraminfo.append(param8_is_validated)  #2.1.7.8 是否合法

                block.parameter_info.append(paraminfo)  #2.1.7 参数信息
                block.parameter_info0.append(param6_paramtype_blockid)  # 2.1.8

        # 2.2 参数块父关系,[for参数块only]
        block.parameter_parent_block_sequenceid = -1  #
        block.parameter_ancestor_block_seqenceid = -1  # 非参数块祖宗
        # 2.3 参数块兄弟关系,[for参数块only]
        block.parameter_brother_left = -1  # 上一个兄弟
        block.parameter_brother_right = -1  # 下一个兄弟

        # 3. 兄弟父子关系
        # 3.1 兄弟关系
        block.brother_up = -1  # 上一个兄弟
        if "D" in location:
            block.brother_down = int(location[location.index("D") + 1])
        else:
            block.brother_down = -1  # 下一个兄弟

        # 3.2 父关系
        block.indent_depth = 0  # 缩进层级,2级以后才有父
        block.father_block_seqeneceid = -1  # 所属父 block 序号
        # 3.3 子关系
        block.is_container = self.iscontainer(
            block.refid)  #* 是否container,容器才有子关系
        if 1 == block.is_container:
            if block.refid == sb.BLKREFID_LF_IFELSE:
                if "M" in location:
                    block.childblock_list1.append(
                        int(location[location.index("M") + 1]))  #
                if "M2" in location:
                    block.childblock_list2.append(
                        int(location[location.index("M2") + 1]))  #
            else:
                if "M" in location:
                    block.childblock_list1.append(
                        int(location[location.index("M") + 1]))  #
        else:
            block.childblock_list1 = []  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目
            block.childblock_list2 = [
            ]  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目,目前只应用到else

        # 4. 执行时间,暂时不考虑: BLKREFID_LF_LOOPSTOP,BLKREFID_OS_GAMEOVER 考虑循环次数
        if 1 == block.is_parameter_block:  # 参数块不计算执行时间
            block.is_asyn = 0  # 4.1 是否异步执行
            block.time_used = 0  # 4.2 执行用时
            block.time_used_accumulated = 0  # 4.3 累计执行用时
            block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
        else:
            # 考虑到参数块嵌套,累计用时和涉及变量暂时不能决定
            if sb.BLKREFID_LF_WAITNUMBERSECONDS == block.refid:
                block.is_asyn = 0  # 4.1 是否异步执行
                block.time_used = block.parameter_info[0][2]  # 4.2 执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
            elif sb.BLKREFID_LF_IF == block.refid:
                block.is_asyn = 1  # 4.1 是否异步执行
                block.time_used = 0  # 4.2 *执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
            elif sb.BLKREFID_LF_IFELSE == block.refid:
                block.is_asyn = 2  # 4.1 是否异步执行
                block.time_used = 0  # 4.2 *执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
            elif sb.BLKREFID_LF_LOOPUNLIMITED == block.refid:
                block.is_asyn = 3  # 4.1 是否异步执行
                block.time_used = 0  # 4.2 *执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
            elif sb.BLKREFID_LF_LOOPNUMBER == block.refid:
                block.is_asyn = 4  # 4.1 是否异步执行
                block.time_used = 0  # 4.2 *执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时
            else:
                block.is_asyn = 0  # 4.1 是否异步执行
                block.time_used = 0  # 4.2 执行用时
                block.time_used_accumulated = 0  # 4.3 *累计执行用时
                block.time_ralatedvariable.clear()  # 4.4 涉及的变量,这些变量决定了用时

        # 5. check entity
        block.can_be_excuted = 0  # 5.1* 是否会被执行
        block.has_child1 = block.has_child2 = 0  # 5.2 是否有子块
        if 1 == block.is_container:
            if 0 != len(block.childblock_list1):
                block.has_child1 = 1  # 5.2 是否有子块
            if 0 != len(block.childblock_list2):
                block.has_child2 = 1  # 5.2 是否有子块
        else:
            block.has_child1 = 0  # 5.3 是否有子块
            block.has_child2 = 0  # 5.3 是否有子块

        block.condition_value_iscontant = 0  # 5.4* 条件值是常量

        return block

    """
        构建事件网络
    """

    def create_event_relation(self, gameinfo):
        cur_gameobjectid = -1
        cur_gameobjectname = ""
        cur_scriptid = -1

        for goindex in range(len(gameinfo.gameobject)):
            cur_gameobjectid = gameinfo.gameobject[goindex].gameobject_id
            cur_gameobjectname = gameinfo.gameobject[goindex].gameobject_name
            for scindex in range(len(
                    gameinfo.gameobject[goindex].scripts_sets)):
                cur_scriptid = gameinfo.gameobject[goindex].scripts_sets[
                    scindex].scriptid
                for bkindex in range(
                        len(gameinfo.gameobject[goindex].scripts_sets[scindex].
                            block_set)):
                    # fanout
                    # 2012/12/12 add EST_PROGRAM_BROADCASTMSG_ALL
                    #                    if sb.BLKREFID_OS_BROADCASTMESSAGE == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                    #                       sb.BLKREFID_OS_BROADCASTMESSAGE_P2P == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 广播[注意变量问题], 2019/12/12 合并两种发送点在一起
                    #                        # [message-type,messageid,[sendlist],[recvlist]]
                    #                        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
                    #                        found = -1
                    #                        for i in range(len(gameinfo.broadcast_net)):
                    #                            if(gameinfo.broadcast_net[i][0] == sb.EST_PROGRAM_BROADCASTMSG_ALL and \
                    #                               gameinfo.broadcast_net[i][1] == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2]):
                    #                                found = i
                    #                                break
                    #                        if -1 == found: # 没有找到
                    #                            item = []
                    #                            item.append(sb.EST_PROGRAM_BROADCASTMSG_ALL)
                    #                            item.append(gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2])
                    #                            item.append([])
                    #                            item.append([])
                    #                            subitem = []
                    #                            subitem.append(cur_gameobjectid)
                    #                            subitem.append(cur_scriptid)
                    #                            subitem.append(gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    #                            subitem.append(gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    #
                    #                            item[2].append(subitem)
                    #                            gameinfo.broadcast_net.append(item)
                    #                            pass
                    #                        else: # 找到
                    #                            subitem = []
                    #                            subitem.append(cur_gameobjectid)
                    #                            subitem.append(cur_scriptid)
                    #                            subitem.append(gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    #                            subitem.append(gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    #
                    #                            gameinfo.broadcast_net[found][2].append(subitem)
                    #                            pass

                    if sb.BLKREFID_OS_BROADCASTMESSAGE == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 广播[注意变量问题], 2019/12/12 合并两种发送点在一起
                        # [message-type,messageid,[sendlist],[recvlist]]
                        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
                        found = -1
                        for i in range(len(gameinfo.broadcast_net)):
                            if(gameinfo.broadcast_net[i][0] == sb.EST_PROGRAM_BROADCASTMSG and \
                               gameinfo.broadcast_net[i][1] == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2]):
                                found = i
                                break
                        if -1 == found:  # 没有找到
                            item = []
                            item.append(sb.EST_PROGRAM_BROADCASTMSG)
                            item.append(
                                gameinfo.gameobject[goindex].
                                scripts_sets[scindex].block_set[bkindex].
                                parameter_info[0][2])
                            item.append([])
                            item.append([])
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            item[2].append(subitem)
                            gameinfo.broadcast_net.append(item)
                            pass
                        else:  # 找到
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            gameinfo.broadcast_net[found][2].append(subitem)
                            pass

                    # 2012/12/12 add BLKREFID_OS_BROADCASTMESSAGE_P2P
                    elif sb.BLKREFID_OS_BROADCASTMESSAGE_P2P == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 广播[注意变量问题],点对点
                        # 记录发送信息
                        # [message-type,messageid,[sendlist],[recvlist]]
                        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
                        found = -1
                        send_target_id = -1
                        if len(gameinfo.gameobject[goindex].
                               scripts_sets[scindex].block_set[bkindex].
                               parameter_info) >= 2:
                            if sb.BLKREFID_VAR_OBJECT == gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[1][6]:
                                block_seqid = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[1][5]
                                block_index = gameinfo.gameobject[
                                    goindex].scripts_sets[
                                        scindex].block_dict_seqid_index[
                                            block_seqid]
                                send_target_id = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        block_index].parameter_info[0][2]
                            else:
                                send_target_id = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[1][2]
                        else:
                            send_target_id = -1  # gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid

                        typeid = sb.EST_PROGRAM_BROADCASTMSG_P2P
                        if 0 == send_target_id:
                            typeid = sb.EST_PROGRAM_BROADCASTMSG
                        for i in range(len(gameinfo.broadcast_net)):
                            if(gameinfo.broadcast_net[i][0] == typeid and \
                               gameinfo.broadcast_net[i][1] == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2]):
                                found = i
                                break
                        if -1 == found:  # 没有找到
                            item = []
                            item.append(typeid)
                            item.append(
                                gameinfo.gameobject[goindex].
                                scripts_sets[scindex].block_set[bkindex].
                                parameter_info[0][2])
                            item.append([])
                            item.append([])
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            if typeid == sb.EST_PROGRAM_BROADCASTMSG_P2P:
                                subitem.append(send_target_id)
                            else:
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                            item[2].append(subitem)
                            gameinfo.broadcast_net.append(item)
                            pass
                        else:  # 找到
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            if typeid == sb.EST_PROGRAM_BROADCASTMSG_P2P:
                                subitem.append(send_target_id)
                            else:
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)

                            gameinfo.broadcast_net[found][2].append(subitem)
                            pass

                    elif sb.BLKREFID_OS_CLONERESOURCE == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 克隆[注意下拉列表序号,与传入的objectid的一致性]
                        # [message-type,clone target-objectgameid,target-objectgamename,[sendlist],[recvlist]]
                        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
                        found = -1
                        object_name = self.get_objectname_by_objectid(
                            gameinfo.gameobject[goindex].scripts_sets[scindex].
                            block_set[bkindex].parameter_info[0][2])
                        for i in range(len(gameinfo.clone_net)):
                            if(gameinfo.clone_net[i][0] == sb.EST_PROGRAM_CLONE and \
                               gameinfo.clone_net[i][1] == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2] and \
                               gameinfo.clone_net[i][2] == object_name):
                                found = i
                                break
                        if -1 == found:  # 没有找到
                            item = []
                            item.append(sb.EST_PROGRAM_CLONE)
                            item.append(
                                gameinfo.gameobject[goindex].
                                scripts_sets[scindex].block_set[bkindex].
                                parameter_info[0][2])
                            item.append(object_name)
                            item.append([])
                            item.append([])
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            item[3].append(subitem)
                            gameinfo.clone_net.append(item)
                        else:  # 找到
                            subitem = []
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            gameinfo.clone_net[found][3].append(subitem)
                    elif sb.BLKREFID_VAR_VARIABLESINCDEC == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                         sb.BLKREFID_VAR_LIST_SET == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                         sb.BLKREFID_VAR_VARIABLESASSIGNMENT == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 变量
                        # [message-type,var-type,var-hostobjectid,var-hostobjectname,var-id,var-name,[sendlist],[recvlist]]
                        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid,target-value]
                        found = -1
                        var_info = self.get_variables_info(
                            goindex,
                            gameinfo.gameobject[goindex].scripts_sets[scindex].
                            block_set[bkindex].parameter_info[0][2])
                        if 0 == len(var_info):
                            pass
                        else:
                            # [var-type,var-hostobjectid,var-hostobjectname,var-id,var-name]
                            for i in range(len(gameinfo.variables_net)):
                                if(gameinfo.variables_net[i][0] == sb.EST_PROGRAM_WRITEVARIABLES and \
                                   gameinfo.variables_net[i][1] == var_info[0] and \
                                   gameinfo.variables_net[i][2] == var_info[1] and \
                                   gameinfo.variables_net[i][3] == var_info[2] and \
                                   gameinfo.variables_net[i][4] == var_info[3] and \
                                   gameinfo.variables_net[i][5] == var_info[4]):
                                    found = i
                                    break
                            if -1 == found:  # 没有找到
                                item = []
                                item.append(sb.EST_PROGRAM_WRITEVARIABLES)
                                item.append(var_info[0])
                                item.append(var_info[1])
                                item.append(var_info[2])
                                item.append(var_info[3])
                                item.append(var_info[4])
                                item.append([])
                                item.append([])

                                subitem = []
                                subitem.append(cur_gameobjectid)
                                subitem.append(cur_scriptid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(0)

                                item[6].append(subitem)
                                gameinfo.variables_net.append(item)
                            else:  # 找到
                                subitem = []
                                subitem.append(cur_gameobjectid)
                                subitem.append(cur_scriptid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(0)

                                gameinfo.variables_net[found][6].append(
                                    subitem)
                    else:
                        pass

                    # fanin
                    if sb.BLKREFID_TRG_WHENRECIEVEBROADCASTMESSAGE == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 广播
                        # [message-type,messageid,[sendlist],[recvlist]]
                        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
                        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
                        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
                        found = -1
                        for i in range(len(gameinfo.broadcast_net)):
                            if(gameinfo.broadcast_net[i][0] == sb.EST_PROGRAM_BROADCASTMSG and \
                               gameinfo.broadcast_net[i][1] == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].parameter_info[0][2]):
                                found = i
                                break
                        if -1 == found:  # 没有找到
                            item = []
                            item.append(sb.EST_PROGRAM_BROADCASTMSG)
                            item.append(
                                gameinfo.gameobject[goindex].
                                scripts_sets[scindex].block_set[bkindex].
                                parameter_info[0][2])
                            item.append([])
                            item.append([])
                            subitem = []
                            subitem.append(1)
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            item[3].append(subitem)
                            gameinfo.broadcast_net.append(item)
                            pass
                        else:  # 找到
                            subitem = []
                            subitem.append(1)
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            gameinfo.broadcast_net[found][3].append(subitem)
                            pass
                    elif sb.BLKREFID_TRG_WHENRUNNINGASCLONE == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 克隆
                        # [message-type,clone target-objectgameid,target-objectgamename,[sendlist],[recvlist]]
                        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
                        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
                        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
                        found = -1
                        for i in range(len(gameinfo.clone_net)):
                            if(gameinfo.clone_net[i][0] == sb.EST_PROGRAM_CLONE and \
                               gameinfo.clone_net[i][1] == cur_gameobjectid and \
                               gameinfo.clone_net[i][2] == cur_gameobjectname):
                                found = i
                                break
                        if -1 == found:  # 没有找到
                            item = []
                            item.append(sb.EST_PROGRAM_CLONE)
                            item.append(cur_gameobjectid)
                            item.append(cur_gameobjectname)
                            item.append([])
                            item.append([])
                            subitem = []
                            subitem.append(1)
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            item[4].append(subitem)
                            gameinfo.clone_net.append(item)
                        else:  # 找到
                            subitem = []
                            subitem.append(1)
                            subitem.append(cur_gameobjectid)
                            subitem.append(cur_scriptid)
                            subitem.append(
                                gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)

                            gameinfo.clone_net[found][4].append(subitem)
                    elif sb.BLKREFID_VAR_LIST_GET == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                         sb.BLKREFID_VAR_VARIABLES == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 变量,需要检测它的非参数父
                        # [message-type,var-type,var-hostobjectid,var-hostobjectname,var-id,var-name,[sendlist],[recvlist]]
                        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
                        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
                        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
                        # BLKREFID_TRG_WHENCONDITION
                        # BLKREFID_LF_IF
                        # BLKREFID_LF_IFELSE
                        found = -1
                        var_info = self.get_variables_info(
                            goindex,
                            gameinfo.gameobject[goindex].scripts_sets[scindex].
                            block_set[bkindex].parameter_info[0][2])
                        if 0 == len(var_info):
                            pass
                        else:
                            # [var-type,var-hostobjectid,var-hostobjectname,var-id,var-name]
                            for i in range(len(gameinfo.variables_net)):
                                if(gameinfo.variables_net[i][0] == sb.EST_PROGRAM_WRITEVARIABLES and \
                                   gameinfo.variables_net[i][1] == var_info[0] and \
                                   gameinfo.variables_net[i][2] == var_info[1] and \
                                   gameinfo.variables_net[i][3] == var_info[2] and \
                                   gameinfo.variables_net[i][4] == var_info[3] and \
                                   gameinfo.variables_net[i][5] == var_info[4]):
                                    found = i
                                    break
                            if -1 == found:  # 没有找到
                                item = []
                                item.append(sb.EST_PROGRAM_WRITEVARIABLES)
                                item.append(var_info[0])
                                item.append(var_info[1])
                                item.append(var_info[2])
                                item.append(var_info[3])
                                item.append(var_info[4])
                                item.append([])
                                item.append([])

                                subitem = []
                                ancestor_sequenceid = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_ancestor_block_seqenceid
                                if -1 != ancestor_sequenceid:
                                    ancestor_index = gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_dict_seqid_index[
                                                ancestor_sequenceid]
                                    ancestor_refid = gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_set[
                                                ancestor_index].refid
                                else:
                                    ancestor_refid = -1
                                if ancestor_refid == sb.BLKREFID_TRG_WHENCONDITION:
                                    subitem.append(1)
                                elif ancestor_refid == sb.BLKREFID_LF_IF or ancestor_refid == sb.BLKREFID_LF_IFELSE:
                                    subitem.append(2)
                                else:
                                    subitem.append(-1)
                                subitem.append(cur_gameobjectid)
                                subitem.append(cur_scriptid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(ancestor_sequenceid)

                                item[7].append(subitem)
                                gameinfo.variables_net.append(item)
                            else:  # 找到
                                subitem = []
                                ancestor_sequenceid = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_ancestor_block_seqenceid
                                if -1 != ancestor_sequenceid:
                                    ancestor_index = gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_dict_seqid_index[
                                                ancestor_sequenceid]
                                    ancestor_refid = gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_set[
                                                ancestor_index].refid
                                else:
                                    ancestor_refid = -1
                                if ancestor_refid == sb.BLKREFID_TRG_WHENCONDITION:
                                    subitem.append(1)
                                elif ancestor_refid == sb.BLKREFID_LF_IF or ancestor_refid == sb.BLKREFID_LF_IFELSE:
                                    subitem.append(2)
                                else:
                                    subitem.append(-1)
                                subitem.append(cur_gameobjectid)
                                subitem.append(cur_scriptid)
                                subitem.append(
                                    gameinfo.gameobject[goindex].scripts_sets[
                                        scindex].block_set[bkindex].sequenceid)
                                subitem.append(ancestor_sequenceid)

                                gameinfo.variables_net[found][7].append(
                                    subitem)
                    else:
                        pass

                    # 上面建立 broadcast,clone,variables 网络结束,下面增加附加数据分析

                    # check 显示影藏,偏重正面,所有只检查显示,不检查影藏BLKREFID_OS_HIDERESOURCE
                    if sb.BLKREFID_OS_DISPLAYRESOURCE == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        target_source_objectid = gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        target_source_index = self.get_objectindex_by_objectid(
                            target_source_objectid)
                        if -1 != target_source_index:
                            if gameinfo.gameobject[
                                target_source_index].gameobject_attributes:
                                gameinfo.gameobject[
                                    target_source_index].gameobject_attributes[0][
                                        1] = 1
                        else:
                            pass

                    # 支持21,支持32,支持33
                    if sb.BLKREFID_OS_DISPLAY == gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        fatherblock_sequenceid = gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].father_block_seqeneceid
                        if -1 != fatherblock_sequenceid:  # 所属父 block 序号
                            fatherblock_index = gameinfo.gameobject[
                                goindex].scripts_sets[
                                    scindex].block_dict_seqid_index[
                                        fatherblock_sequenceid]
                            if sb.BLKREFID_LF_TELLOBJECT2EXCUTING == gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        fatherblock_index].refid:
                                target_source_objectid = gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        fatherblock_index].parameter_info[0][2]
                                target_source_index = self.get_objectindex_by_objectid(
                                    target_source_objectid)
                                if -1 != target_source_index:
                                    gameinfo.gameobject[
                                        target_source_index].gameobject_attributes[
                                            0][1] = 1
                                else:
                                    pass

                    # check gameobject中是否有音乐播放
                    if sb.BLKREFID_SD_PLAYSOUNDREPEAT == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_SD_PLAYSOUNDONCE == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:
                        if gameinfo.gameobject[goindex].has_music == 0:
                            gameinfo.gameobject[
                                goindex].has_music = 1  # 有,则为 1
                        if gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[bkindex].parameter_info[0][
                                    7] == 1:  # 参数合法
                            if gameinfo.gameobject[goindex].has_music == 1:
                                gameinfo.gameobject[
                                    goindex].has_music = 2  # 合法,则为2

                    # 调整组 父子组,计算最大,不计算脱离,sb.BLKREFID_OS_BREADAWAYFROWPARENTRESOURCE
                    if sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINOVERLAPPING == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINORIGINALSTATE == gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:
                        target_source_objectid = gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        target_source_index = self.get_objectindex_by_objectid(
                            target_source_objectid)
                        if -1 != target_source_index:  # H:1:0|G:1:1
                            if len(gameinfo.gameobject[target_source_index].
                                   gameobject_attributes) > 1:  # 目标父在一个组中
                                father_gourdid = gameinfo.gameobject[
                                    target_source_index].gameobject_attributes[
                                        1][1]
                                if len(gameinfo.gameobject[goindex].
                                       gameobject_attributes
                                       ) > 1:  # 自己在一个组中,该组其他成员在原组
                                    gameinfo.gameobject[
                                        goindex].gameobject_attributes[1][
                                            1] = father_gourdid
                                else:  # 自己不在一个组中
                                    gameinfo.gameobject[
                                        goindex].gameobject_attributes.append(
                                            ["G", father_gourdid, 0])
                            else:  # 目标父不在组中
                                father_gourdid = 1 + self.get_max_gourpid()
                                gameinfo.gameobject[
                                    target_source_index].gameobject_attributes.append(
                                        ["G", father_gourdid, 1])  # 父建新组
                                if len(gameinfo.gameobject[goindex].
                                       gameobject_attributes) > 1:  # 自己在一个组中
                                    gameinfo.gameobject[
                                        goindex].gameobject_attributes[1][
                                            1] = father_gourdid
                                else:  # 自己不在一个组中
                                    gameinfo.gameobject[
                                        goindex].gameobject_attributes.append(
                                            ["G", father_gourdid, 0])
                        else:  # 找不到目标父对象
                            pass

        # check 从未在block中出现过得变量,加入变量网络中
        # 1. check gloabl variables
        for i in range(len(gameinfo.variables_sets_global)):
            found = 0
            for j in range(len(gameinfo.variables_net)):
                if gameinfo.variables_sets_global[i][
                        0] == gameinfo.variables_net[j][
                            1] and gameinfo.variables_sets_global[i][
                                2] == gameinfo.variables_net[j][5]:
                    found = 1
                    break
            if 0 == found:
                gameinfo.variables_net.append([
                    16, 0, 1, "Root", gameinfo.variables_sets_global[i][1],
                    gameinfo.variables_sets_global[i][2], [], []
                ])
        # 2. check local variables
        for i in range(len(gameinfo.gameobject)):
            for j in range(len(gameinfo.gameobject[i].variables_sets_local)):
                found = 0
                for k in range(len(gameinfo.variables_net)):
                    if gameinfo.gameobject[i].variables_sets_local[j][0] == gameinfo.variables_net[k][1] \
                       and gameinfo.gameobject[i].variables_sets_local[j][2] == gameinfo.variables_net[k][5] \
                       and gameinfo.gameobject[i].gameobject_id == gameinfo.variables_net[k][2]:
                        found = 1
                        break
                if 0 == found:
                    gameinfo.variables_net.append([
                        16, 1, gameinfo.gameobject[i].gameobject_id,
                        gameinfo.gameobject[i].gameobject_name,
                        gameinfo.gameobject[i].variables_sets_local[j][1],
                        gameinfo.gameobject[i].variables_sets_local[j][2], [],
                        []
                    ])

        # check list 2019/12/11
        for goindex in range(len(self.gameinfo.gameobject)):
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_VAR_VARIABLESASSIGNMENT == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[bkindex].parameter_info[1][
                                    6] == sb.BLKREFID_VAR_LIST:
                            list_seqid = self.gameinfo.gameobject[
                                goindex].scripts_sets[scindex].block_set[
                                    bkindex].parameter_info[1][5]
                            list_index = gameinfo.gameobject[
                                goindex].scripts_sets[
                                    scindex].block_dict_seqid_index[list_seqid]
                            list_len = self.gameinfo.gameobject[
                                goindex].scripts_sets[scindex].block_set[
                                    list_index].parameter_count
                            var_index = self.gameinfo.gameobject[
                                goindex].scripts_sets[scindex].block_set[
                                    bkindex].parameter_info[0][2]  # 1-->2
                            var_info = self.get_variables_info(
                                goindex, var_index)
                            if len(var_info) > 0:
                                if 0 == var_info[0]:  # global
                                    self.gameinfo.variables_list_global.append(
                                        (var_info[4], list_len))
                                else:
                                    self.gameinfo.gameobject[
                                        goindex].variables_list_local.append(
                                            (var_info[4], list_len))
        for goindex in range(len(self.gameinfo.gameobject)):
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_VAR_VARIABLES == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        var_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        var_info = self.get_variables_info(goindex, var_index)
                        if len(var_info) > 0:
                            list_info = self.get_list_info(var_info, goindex)
                            if (1 == list_info[0]):
                                # report block 2
                                # 非法,list变量不能单独参与计算;
                                self.report.add_list_invalidated_cal(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)
                    elif sb.BLKREFID_VAR_VARIABLESINCDEC == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        var_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        var_info = self.get_variables_info(goindex, var_index)
                        if len(var_info) > 0:
                            list_info = self.get_list_info(var_info, goindex)
                            if (1 == list_info[0]):
                                # report block 2
                                # 非法,list变量不能单独参与计算;
                                self.report.add_list_invalidated_cal(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)
                    elif sb.BLKREFID_VAR_LIST_SET == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        var_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        write_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[1][2]
                        var_info = self.get_variables_info(goindex, var_index)
                        if len(var_info) > 0:
                            list_info = self.get_list_info(var_info, goindex)
                            if (1 != list_info[0]):
                                # report block 3
                                # 非法,非list变量不能不能在此处set值;
                                self.report.add_list_invalidated_set(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)
                            else:
                                if write_index.isdigit():
                                    index = int(write_index)
                                    if index >= list_info[1]:
                                        # report block 5
                                        # 非法,list变量下标越界
                                        self.report.add_list_invalidated_subscript_overflow(
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_id,
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_name,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].scriptid,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].
                                            block_set[bkindex].sequenceid)
                                    elif index < 0:
                                        # report block 5
                                        # 非法,list变量下标越界
                                        self.report.add_list_invalidated_subscript_overflow(
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_id,
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_name,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].scriptid,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].
                                            block_set[bkindex].sequenceid)
                                    else:
                                        pass
                                else:
                                    # report block 6
                                    # 非法,list变量下标必须是数字
                                    self.report.add_list_invalidated_subscript_nonum(
                                        self.gameinfo.gameobject[goindex].
                                        gameobject_id, self.gameinfo.
                                        gameobject[goindex].gameobject_name,
                                        self.gameinfo.gameobject[goindex].
                                        scripts_sets[scindex].scriptid,
                                        self.gameinfo.gameobject[goindex].
                                        scripts_sets[scindex].
                                        block_set[bkindex].sequenceid)
                    elif sb.BLKREFID_VAR_LIST_GET == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        var_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        write_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[1][2]
                        var_info = self.get_variables_info(goindex, var_index)
                        if len(var_info) > 0:
                            list_info = self.get_list_info(var_info, goindex)
                            if (1 != list_info[0]):
                                # report block 4
                                # 非法,非list变量不能不能在此处get值;
                                self.report.add_list_invalidated_get(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)
                            else:
                                if write_index.isdigit():
                                    index = int(write_index)
                                    if index >= list_info[1]:
                                        # report block 5
                                        # 非法,list变量下标越界
                                        self.report.add_list_invalidated_subscript_overflow(
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_id,
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_name,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].scriptid,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].
                                            block_set[bkindex].sequenceid)
                                    elif index < 0:
                                        # report block 5
                                        # 非法,list变量下标越界
                                        self.report.add_list_invalidated_subscript_overflow(
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_id,
                                            self.gameinfo.gameobject[goindex].
                                            gameobject_name,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].scriptid,
                                            self.gameinfo.gameobject[goindex].
                                            scripts_sets[scindex].
                                            block_set[bkindex].sequenceid)
                                    else:
                                        pass
                                else:
                                    # report block 6
                                    # 非法,list变量下标必须是数字
                                    self.report.add_list_invalidated_subscript_nonum(
                                        self.gameinfo.gameobject[goindex].
                                        gameobject_id, self.gameinfo.
                                        gameobject[goindex].gameobject_name,
                                        self.gameinfo.gameobject[goindex].
                                        scripts_sets[scindex].scriptid,
                                        self.gameinfo.gameobject[goindex].
                                        scripts_sets[scindex].
                                        block_set[bkindex].sequenceid)
                    else:
                        pass

        # 2019/12/17 added,check 没有选择变量,没有选择UI资源,播放动作,list塞到非法变量框
        for goindex in range(len(self.gameinfo.gameobject)):
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_VAR_VARIABLESINCDEC == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_VAR_VARIABLESASSIGNMENT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_VAR_LIST_SET == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_VAR_LIST_GET == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:
                        var_index = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        var_info = self.get_variables_info(goindex, var_index)
                        if len(var_info) <= 0:
                            # report vairiables 4
                            self.report.add_variables_varblock_noselected(
                                self.gameinfo.gameobject[goindex].
                                gameobject_id, self.gameinfo.
                                gameobject[goindex].gameobject_name,
                                self.gameinfo.gameobject[goindex].
                                scripts_sets[scindex].scriptid,
                                self.gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                    elif sb.BLKREFID_DC_TEXTOFRESOUREUI == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                         sb.BLKREFID_OA_DISPLAYTEXTINUIRESOURCE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:
                        default_value = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        if -1 == default_value:
                            # report vairiables 5
                            self.report.add_uiresource_noselected(
                                self.gameinfo.gameobject[goindex].
                                gameobject_id, self.gameinfo.
                                gameobject[goindex].gameobject_name,
                                self.gameinfo.gameobject[goindex].
                                scripts_sets[scindex].scriptid,
                                self.gameinfo.gameobject[goindex].scripts_sets[
                                    scindex].block_set[bkindex].sequenceid)
                    elif sb.BLKREFID_OA_PLAYRESOURCEACTION == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        default_value = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_info[0][2]
                        if 0 == default_value:
                            # report vairiables 6,此处选不选都是0,分不清楚,暂时不报
                            pass
#                             self.report.add_action_noselected(self.gameinfo.gameobject[goindex].gameobject_id,
#                                                               self.gameinfo.gameobject[goindex].gameobject_name,
#                                                               self.gameinfo.gameobject[goindex].scripts_sets[scindex].scriptid,
#                                                               self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    elif sb.BLKREFID_VAR_LIST == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        fatherblock_sequenceid = self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].parameter_ancestor_block_seqenceid
                        if -1 != fatherblock_sequenceid:
                            fatherblock_index = gameinfo.gameobject[
                                goindex].scripts_sets[
                                    scindex].block_dict_seqid_index[
                                        fatherblock_sequenceid]
                            if sb.BLKREFID_TRG_WHENRECIEVEBROADCASTMESSAGE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_LF_LOOPNUMBER == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_LF_WAITNUMBERSECONDS == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_MOVINGRXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_MOVINGRXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_MOVINGAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_ROTATERXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_ROTATERXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_ROTATEAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_RESIZEPERSENT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_DISPLAYTEXTONTOP == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_BREAKRESOURCE2XYZ == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OA_DISPLAYTEXTINUIRESOURCE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OS_BROADCASTMESSAGE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_OS_BROADCASTMESSAGE_P2P == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_CND_NUMBERISOJZZZF == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_CND_EXACTDIVISION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_CND_BOOLCOMPARE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_VAR_VARIABLESINCDEC == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_VAR_LIST_SET == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_PF_SETTINGMASS == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_PF_FORCEFROMXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_SD_PLAYSOUNDREPEAT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_SD_PLAYSOUNDONCE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_SD_STOPSOUND == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_VARIABLECELL == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_ARITHMETIC == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_FUNCTION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_RANDOMNUMBER == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_REMAINDER == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid or \
                                sb.BLKREFID_DC_TRIFUNCTION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[fatherblock_index].refid:
                                # report list 7
                                self.report.add_list_invalidated_location(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)

    def collect_index(self):
        # 1. sprite(3)
        self.ct_index.sprite_index_totals = len(
            self.gameinfo.gameobject) - 2  # 1.1. sprite指标: (+)sprite总数
        for i in range(len(self.gameinfo.gameobject)):
            if "Root" == self.gameinfo.gameobject[
                    i].gameobject_name or "Player" == self.gameinfo.gameobject[
                        i].gameobject_name:
                #                self.ct_index.sprite_index_useful += 1                 # 1.2. sprite指标: (+)sprite有效数目
                continue
            if len(self.gameinfo.gameobject[i].gameobject_attributes) > 0:
                if self.gameinfo.gameobject[i].gameobject_attributes[0][
                        1] >= 1:  # 可显示则有效
                    self.ct_index.sprite_index_useful += 1  # 1.2. sprite指标: (+)sprite有效数目
                else:  # 不可显示
                    if self.gameinfo.gameobject[i].has_music >= 2:  # 能有效播放音乐
                        self.ct_index.sprite_index_useful += 1  # 1.2. sprite指标: (+)sprite有效数目
                    else:
                        self.ct_index.sprite_index_useless += 1  # 1.3. sprite指标: (-)sprite无效数目

                        # report sprite
                        self.report.add_sprite_unused_sprite(
                            self.gameinfo.gameobject[i].gameobject_id,
                            self.gameinfo.gameobject[i].gameobject_name)
            else:
                self.ct_index.sprite_index_useful += 1  # 1.2. sprite指标: (+)sprite有效数目

        # 2. script(18)
        script_index_tatals = 0  # 2.1. script指标: (+)script总数
        script_index_has_detonator = 0  # 2.2. script指标: (+)script有触点数目
        script_index_hasnot_detonator = 0  # 2.3. script指标: (-)script无触点数目
        script_index_trigger_atworking = 0  # 2.4. script指标: (+)script工程运行时可触发数目
        script_index_trigger_cannot_be_fired = 0  # 2.5. script指标: (-)script实际不可触发数目
        script_index_blocknum_max = 0  # 2.6. script指标: (+)script中最大block数目
        script_index_blocknum_min = sb.MAX_BLOCKCOUNT  # 2.7. script指标: (+)script中最小block数目
        script_index_blocknum_avg = 0.0  # 2.8. script指标: (+)script中平均block数目
        script_index_statementblock_nest_depth_max = 0  # 2.9. script指标: (+-)script中语句块嵌套最大深度
        script_index_statementblock_nest_depth_avg = 0.0  # 2.10. script指标: (+-)script中语句块嵌套平均深度
        script_index_paramblock_nest_depth_max = 0  # 2.11. script指标: (+-)script中参数块嵌套最大深度
        script_index_paramblock_nest_depth_avg = 0.0  # 2.12. script指标: (+-)script中参数块嵌套平均深度
        script_index_stateparamblock_nest_depth_max = 0  # 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度
        script_index_stateparamblock_nest_depth_avg = 0.0  # 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度
        script_index_nest_useless = 0  # 2.15. script指标: (-)script中无效的嵌套
        script_index_runtime_max = 0.0  # 2.16. script指标: (+)script最大运行时间
        script_index_runtime_min = sb.MAX_TIME  # 2.17. script指标: (+)script最小运行时间
        script_index_runtime_avg = 0.0  # 2.18. script指标: (+)script平均运行时间
        for iobj in range(len(self.gameinfo.gameobject)):
            script_index_tatals += len(
                self.gameinfo.gameobject[iobj].scripts_sets
            )  # 2.1. script指标: (+)script总数
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                if 0 != self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].has_trigger:
                    script_index_has_detonator += 1  # 2.2. script指标: (+)script有触点数目
                else:
                    script_index_hasnot_detonator += 1  # 2.3. script指标: (-)script无触点数目
                if 0 != self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].be_trigger_atworking:
                    script_index_trigger_atworking += 1  # 2.4. script指标: (+)script工程运行时可触发数目
                elif 0 == self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].has_trigger:
                    script_index_trigger_cannot_be_fired += 1  # 2.5. script指标: (-)script实际不可触发数目
                    # report script 1
                    self.report.add_script_useless_script(
                        self.gameinfo.gameobject[iobj].gameobject_id,
                        self.gameinfo.gameobject[iobj].gameobject_name, self.
                        gameinfo.gameobject[iobj].scripts_sets[jsc].scriptid,
                        self.gameinfo.gameobject[iobj].scripts_sets[jsc].
                        block_set[0].sequenceid)
                else:
                    can_trigger = self.check_trigger(
                        iobj, jsc, 0)  # broadcast,clone,variables
                    if 0 == can_trigger:
                        script_index_trigger_cannot_be_fired += 1  # 2.5. script指标: (-)script实际不可触发数目
                        # report script 1
                        self.report.add_script_useless_script(
                            self.gameinfo.gameobject[iobj].gameobject_id,
                            self.gameinfo.gameobject[iobj].gameobject_name,
                            self.gameinfo.gameobject[iobj].scripts_sets[jsc].
                            scriptid, self.gameinfo.gameobject[iobj].
                            scripts_sets[jsc].block_set[0].sequenceid)
                    else:
                        pass

                block_count = len(
                    self.gameinfo.gameobject[iobj].scripts_sets[jsc].block_set)
                if 1 == self.get_noparam_block_count(
                        iobj, jsc):  # 2019/12/04 added,只有一个块的script判断为无效;
                    # report script 1
                    self.report.add_script_useless_script(
                        self.gameinfo.gameobject[iobj].gameobject_id,
                        self.gameinfo.gameobject[iobj].gameobject_name, self.
                        gameinfo.gameobject[iobj].scripts_sets[jsc].scriptid,
                        self.gameinfo.gameobject[iobj].scripts_sets[jsc].
                        block_set[0].sequenceid)

                if block_count > script_index_blocknum_max:
                    script_index_blocknum_max = block_count  # 2.6. script指标: (+)script中最大block数目
                if block_count < script_index_blocknum_min:
                    script_index_blocknum_min = block_count  # 2.7. script指标: (+)script中最小block数目
                script_index_blocknum_avg += block_count  # 2.8. script指标: (+)script中平均block数目
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].block_nest_depth > script_index_statementblock_nest_depth_max:
                    script_index_statementblock_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].block_nest_depth  # 2.9. script指标: (+-)script中语句块嵌套最大深度
                script_index_statementblock_nest_depth_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].block_nest_depth  # 2.10. script指标: (+-)script中语句块嵌套平均深度

                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].paramblock_nest_depth > script_index_paramblock_nest_depth_max:
                    script_index_paramblock_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].paramblock_nest_depth  # 2.11. script指标: (+-)script中参数块嵌套最大深度
                script_index_paramblock_nest_depth_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].paramblock_nest_depth  # 2.12. script指标: (+-)script中参数块嵌套平均深度

                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].stateparamblock_nest_depth > script_index_stateparamblock_nest_depth_max:
                    script_index_stateparamblock_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].stateparamblock_nest_depth  # 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度
                script_index_stateparamblock_nest_depth_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].stateparamblock_nest_depth  # 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度

                script_index_nest_useless += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].nest_useless  # 2.15. script指标: (-)script中无效的嵌套

                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].running_time > script_index_runtime_max:
                    script_index_runtime_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].running_time  # 2.16. script指标: (+)script最大运行时间
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].running_time < script_index_runtime_min:
                    script_index_runtime_min = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].running_time  # 2.17. script指标: (+)script最小运行时间
                script_index_runtime_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].running_time  # 2.18. script指标: (+)script平均运行时间

        self.ct_index.script_index_tatals = script_index_tatals  # 2.1. script指标: (+)script总数
        self.ct_index.script_index_has_detonator = script_index_has_detonator  # 2.2. script指标: (+)script有触点数目
        self.ct_index.script_index_hasnot_detonator = script_index_hasnot_detonator  # 2.3. script指标: (-)script无触点数目

        self.ct_index.script_index_trigger_atworking = script_index_trigger_atworking  # 2.4. script指标: (+)script工程运行时可触发数目
        self.ct_index.script_index_trigger_cannot_be_fired = script_index_trigger_cannot_be_fired  # 2.5. script指标: (-)script实际不可触发数目

        self.ct_index.script_index_blocknum_max = script_index_blocknum_max  # 2.6. script指标: (+)script中最大block数目
        self.ct_index.script_index_blocknum_min = script_index_blocknum_min  # 2.7. script指标: (+)script中最小block数目
        if script_index_tatals > 0:
            self.ct_index.script_index_blocknum_avg = script_index_blocknum_avg / script_index_tatals  # 2.8. script指标: (+)script中平均block数目

        self.ct_index.script_index_statementblock_nest_depth_max = script_index_statementblock_nest_depth_max  # 2.9. script指标: (+-)script中语句块嵌套最大深度
        if script_index_tatals > 0:
            self.ct_index.script_index_statementblock_nest_depth_avg = script_index_statementblock_nest_depth_avg / script_index_tatals  # 2.10. script指标: (+-)script中语句块嵌套平均深度
        self.ct_index.script_index_paramblock_nest_depth_max = script_index_paramblock_nest_depth_max  # 2.11. script指标: (+-)script中参数块嵌套最大深度
        if script_index_tatals > 0:
            self.ct_index.script_index_paramblock_nest_depth_avg = script_index_paramblock_nest_depth_avg / script_index_tatals  # 2.12. script指标: (+-)script中参数块嵌套平均深度
        self.ct_index.script_index_stateparamblock_nest_depth_max = script_index_stateparamblock_nest_depth_max  # 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度
        if script_index_tatals > 0:
            self.ct_index.script_index_stateparamblock_nest_depth_avg = script_index_stateparamblock_nest_depth_avg / script_index_tatals  # 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度
        self.ct_index.script_index_nest_useless = script_index_nest_useless  # 2.15. script指标: (-)script中无效的嵌套

        self.ct_index.script_index_runtime_max = script_index_runtime_max  # 2.16. script指标: (+)script最大运行时间
        self.ct_index.script_index_runtime_min = script_index_runtime_min  # 2.17. script指标: (+)script最小运行时间
        if script_index_tatals > 0:
            self.ct_index.script_index_runtime_avg = script_index_runtime_avg / script_index_tatals  # 2.18. script指标: (+)script平均运行时间

        if self.ct_index.script_index_blocknum_min == sb.MAX_BLOCKCOUNT:
            self.ct_index.script_index_blocknum_min = 0
        if self.ct_index.script_index_runtime_min == sb.MAX_TIME:
            self.ct_index.script_index_runtime_min = 0

        # 3. block(2)
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                self.ct_index.block_index_totals += len(
                    self.gameinfo.gameobject[iobj].scripts_sets[jsc].block_set
                )  # 3.1. block数目: (+)block总数
        self.ct_index.block_index_nowork = 0  # 3.2. block数目: (-)block不能被执行的总数 [暂不支持]

        # 4. trigger(4)
        self.ct_index.trigger_index_trigger_script_number_atworking = self.ct_index.script_index_trigger_atworking  # 4.1. trigger: (+)工程运行时触发的script数目
        self.ct_index.trigger_index_trigger_script_number_meanwhile = self.ct_index.script_index_trigger_atworking  # 4.2. trigger: (+)同时触发的script数目
        # check broadcast,clone,no check variables and human action
        for i in range(len(self.gameinfo.broadcast_net)):
            if len(
                    self.gameinfo.broadcast_net[i][3]
            ) > self.ct_index.trigger_index_trigger_script_number_meanwhile:
                self.ct_index.trigger_index_trigger_script_number_meanwhile = len(
                    self.gameinfo.broadcast_net[i]
                    [3])  # 4.2. trigger: (+)同时触发的script数目
        for i in range(len(self.gameinfo.clone_net)):
            if len(
                    self.gameinfo.clone_net[i][4]
            ) > self.ct_index.trigger_index_trigger_script_number_meanwhile:  # 4.2. trigger: (+)同时触发的script数目
                self.ct_index.trigger_index_trigger_script_number_meanwhile = len(
                    self.gameinfo.clone_net[i][4])
        self.ct_index.trigger_index_script_running_number_meanwhile = 0  # 4.3. trigger: (+)并发执行的最大script数目 [暂不支持]
        self.ct_index.trigger_index_script_running_overlap_maxtime = 0  # 4.4. trigger: (+)并发执行的script最大重叠时间 [暂不支持]

        # 5. condition(9)
        # 6. loop(9)
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                # condition
                self.ct_index.condition_index_number_ifelse += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].condition_index_number_ifelse  # 5.1. contain条件: (+)ifelse数目
                self.ct_index.condition_index_number_if += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].condition_index_number_if  # 5.2. contain条件: (+)if数目
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].condition_index_nest_depth > self.ct_index.condition_index_nest_depth_max:
                    self.ct_index.condition_index_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].condition_index_nest_depth  # 5.3. contain条件: (+-)条件嵌套最大深度(跳过loop)
                self.ct_index.condition_index_nest_depth_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].condition_index_nest_depth_total  # 5.4. contain条件: (+-)条件平均嵌套深度(跳过loop)
                self.ct_index.condition_index_number_no_statement += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].condition_index_number_no_statement  # 5.5. contain条件: (-)if,if else下面没有block的数目
                self.ct_index.condition_index_number_param_imcompleted += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].condition_index_number_param_imcompleted  # 5.6. contain条件: (-)if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
                # loop
                self.ct_index.loop_index_number_totals += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].loop_index_number_totals  # 6.1. contain循环: (+)循环数目
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].loop_index_nest_depth > self.ct_index.loop_index_nest_depth_max:
                    self.ct_index.loop_index_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].loop_index_nest_depth  # 6.2. contain循环: (+-)循环嵌套最大深度
                self.ct_index.loop_index_nest_depth_avg += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].loop_index_nest_depth_total  # 6.3. contain循环: (+-)循环嵌套平均深度
        if self.ct_index.condition_index_number_ifelse + self.ct_index.condition_index_number_if > 0:
            self.ct_index.condition_index_nest_depth_avg = self.ct_index.condition_index_nest_depth_avg / (
                self.ct_index.condition_index_number_ifelse +
                self.ct_index.condition_index_number_if
            )  # 5.4. contain条件: (+-)条件平均嵌套深度(跳过loop)
        if self.ct_index.loop_index_number_totals > 0:
            self.ct_index.loop_index_nest_depth_avg = self.ct_index.loop_index_nest_depth_avg / self.ct_index.loop_index_number_totals  # 6.3. contain循环: (+-)循环嵌套平均深度
        # condition
        self.ct_index.condition_index_number_param_variables_nochanged = 0  # 5.7. contain条件: (-)条件表达式中的变量外部不变数目(基于嵌套顶层)[暂不处理]
        self.ct_index.condition_index_number_true_forever = 0  # 5.8. contain条件: (-)条件永假数目(基于嵌套顶层)[暂不处理]
        self.ct_index.condition_index_number_false_forever = 0  # 5.9. contain条件: (-)条件永真数目(基于嵌套顶层)[暂不处理]
        # loop
        self.ct_index.loop_index_number_cross_sprite_by_broadcast = 0  # 6.4. contain循环: (+)基于消息(广播)的跨sprite大循环数目[暂不处理]
        self.ct_index.loop_index_number_cross_sprite_by_variables = 0  # 6.5. contain循环: (+)基于消息(变量)的跨sprite大循环数目[暂不处理]
        self.ct_index.loop_index_number_cross_script_by_broadcast = 0  # 6.6. contain循环: (+)基于消息(广播)的跨script大循环数目[暂不处理]
        self.ct_index.loop_index_number_cross_script_by_variables = 0  # 6.7. contain循环: (+)基于消息(变量)的跨script大循环数目[暂不处理]
        self.ct_index.loop_index_endlessloop_nobreak = 0  # 6.8. contain循环: (*)死循环数目(不能跳出,或者break条件永不为真)[暂不处理]
        self.ct_index.loop_index_endlessloop_nowait = 0  # 6.9. contain循环: (-)死循环数目(循环体中没有阻塞)[暂不处理]

        # 7. sequenceblock(3)
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].sequenceblock_index_number_top_max > self.ct_index.sequenceblock_index_number_top_max:
                    self.ct_index.sequenceblock_index_number_top_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].sequenceblock_index_number_top_max
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].sequenceblock_index_number_if_max > self.ct_index.sequenceblock_index_number_if_max:
                    self.ct_index.sequenceblock_index_number_if_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].sequenceblock_index_number_if_max
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].sequenceblock_index_number_loop_max > self.ct_index.sequenceblock_index_number_loop_max:
                    self.ct_index.sequenceblock_index_number_loop_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].sequenceblock_index_number_loop_max

        # 8. clone(5)
        #   self.clone_net = [] # [message-type,clone target-objectgameid,target-objectgamename,[sendlist],[recvlist]]
        #                       # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        #                       # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        #                       # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        #                       # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        for i in range(len(self.gameinfo.clone_net)):
            self.ct_index.clone_index_number_blocks += len(
                self.gameinfo.clone_net[i][3])  # 8.1. 克隆: (+)克隆点数目
            self.ct_index.clone_index_number_trigger_script += len(
                self.gameinfo.clone_net[i]
                [4])  # 8.4. 克隆: (+)克隆sprite触发script数目
        self.ct_index.clone_index_number_sprites = len(
            self.gameinfo.clone_net)  # 8.2. 克隆: (+)克隆sprite数量
        self.ct_index.clone_index_number_sprites_type = len(
            self.gameinfo.clone_net)  # 8.3. 克隆: (+)克隆sprite类型数量,目前不分对象类型
        self.ct_index.clone_index_recursion_or_unlimited = 0  # 8.5. 克隆: (-)是否存在递归克隆 [暂时不处理]

        # 9. wait(2)
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                self.ct_index.wait_index_number += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].wait_index_number  # 9.1. wait数目: (+)wait数目
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].wait_index_max_waittime > self.ct_index.wait_index_max_waittime:
                    self.ct_index.wait_index_max_waittime = self.gameinfo.gameobject[
                        iobj].scripts_sets[jsc].wait_index_max_waittime

        # 10. broadcast(6)
        # broadcast
        #   self.broadcast_net = []  # [message-type,messageid,[sendlist],[recvlist]]
        #                            # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        #                            # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        #                            # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        #                            # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        #    [
        #       [4,      1, [[3, 2, 4, 4]], [[1, 3, 1, 1]]],
        #       [4,      3, [],             [[1, 3, 3, 5]]],
        #       [524288, 5, [[3, 3, 7, 3]], []],
        #       [4,      2, [],             [[1, 3, 4, 9], [1, 4, 1, 1]]],
        #       [4,      5, [],             [[1, 3, 6, 12]]],
        #       [524288, 3, [[4, 2, 4, 3]], []],
        #       [4,      4, [[4, 2, 6, 6]], []]
        #    ]
        #    补充标记位, send: flag广播0/点播1, flag有收1/无0/-1不定; recv: flag收广播0/点播1/待定-1, flag有发送1/无0/待定-1
        for i in range(len(self.gameinfo.broadcast_net)):
            fanout_count = len(self.gameinfo.broadcast_net[i][2])
            fanin_count = len(self.gameinfo.broadcast_net[i][3])
            if 0 == fanout_count and 0 != fanin_count:  # [4,      2, [],             [[1, 3, 4, 9], [1, 4, 1, 1]]],
                for j in range(fanin_count):
                    self.gameinfo.broadcast_net[i][3][j].append(-1)
                    self.gameinfo.broadcast_net[i][3][j].append(-1)
            if 0 != fanout_count and 0 == fanin_count:  # [4,      4, [[4, 2, 6, 6]], []]]  | [524288, 3, [[4, 2, 4, 3]], []],
                for j in range(fanout_count):
                    if sb.EST_PROGRAM_BROADCASTMSG_P2P == self.gameinfo.broadcast_net[
                            i][0]:
                        self.gameinfo.broadcast_net[i][2][j].append(1)
                        self.gameinfo.broadcast_net[i][2][j].append(-1)
                    else:
                        self.gameinfo.broadcast_net[i][2][j].append(0)
                        self.gameinfo.broadcast_net[i][2][j].append(0)
            if 0 != fanout_count and 0 != fanin_count:  # [4,      1, [[3, 2, 4, 4]], [[1, 3, 1, 1]]],
                for j in range(fanout_count):
                    self.gameinfo.broadcast_net[i][2][j].append(0)
                    self.gameinfo.broadcast_net[i][2][j].append(1)
                for j in range(fanin_count):
                    self.gameinfo.broadcast_net[i][3][j].append(0)
                    self.gameinfo.broadcast_net[i][3][j].append(1)
            if 0 == fanout_count and 0 == fanin_count:
                pass  # 永远不会发生

        #    [
        #       [4,         1, [[3, 2, 4, 4, 0, 1]],    [[1, 3, 1, 1, 0, 1]]],                          ==>pass,需要用来消点播消息 c
        #       [4,         3, [],                      [[1, 3, 3, 5, -1, -1]]],                               --> 待决
        #       [524288,    5, [[3, 3, 7, 3, 1, -1]],   []],                                                   --> 待决 A
        #       [4,         2, [],                      [[1, 3, 4, 9, -1, -1], [1, 4, 1, 1, -1, -1]]],         --> 待决 b
        #       [4,         5, [],                      [[1, 3, 6, 12, -1, -1]]],                              --> 待决 b
        #       [524288,    3, [[4, 2, 4, 3, 1, -1]],   []],                                                   --> 待决 A
        #       [4,         4, [[4, 2, 6, 6, 0, 0]],    []]                                             ==>pass,warning d
        #    ]

        #    核查 recviever,sender
        for i in range(len(self.gameinfo.broadcast_net)):
            if sb.EST_PROGRAM_BROADCASTMSG_P2P == self.gameinfo.broadcast_net[
                    i][0]:
                send_msgid = self.gameinfo.broadcast_net[i][1]  # 发送msgid
                send_target_resourceid = set()  # 发送目标资源集合 --->
                for u in range(len(self.gameinfo.broadcast_net[i][2])):
                    send_target_resourceid.add(
                        self.gameinfo.broadcast_net[i][2][u][3])
                for j in range(len(self.gameinfo.broadcast_net)):
                    if sb.EST_PROGRAM_BROADCASTMSG == self.gameinfo.broadcast_net[
                            j][0] and 0 != len(
                                self.gameinfo.broadcast_net[j][3]):
                        recv_msgid = self.gameinfo.broadcast_net[j][
                            1]  # 接收msgid
                        recv_resourceid = set()  # 接收点资源集合 <---
                        for v in range(len(self.gameinfo.broadcast_net[j][3])):
                            recv_resourceid.add(
                                self.gameinfo.broadcast_net[j][3][v][1])
                        if send_msgid == recv_msgid:
                            # check recv
                            for m in range(
                                    len(self.gameinfo.broadcast_net[j][3])):
                                if self.gameinfo.broadcast_net[j][3][m][
                                        1] in send_target_resourceid:
                                    if -1 == self.gameinfo.broadcast_net[j][3][
                                            m][4] and -1 == self.gameinfo.broadcast_net[
                                                j][3][m][5]:  # 待决
                                        self.gameinfo.broadcast_net[j][3][m][
                                            4] = 1
                                        self.gameinfo.broadcast_net[j][3][m][
                                            5] = 1
                            # check send
                            for n in range(
                                    len(self.gameinfo.broadcast_net[i][2])):
                                if self.gameinfo.broadcast_net[i][2][n][
                                        3] in recv_resourceid:
                                    if 1 == self.gameinfo.broadcast_net[i][2][n][
                                            4] and -1 == self.gameinfo.broadcast_net[
                                                i][2][n][5]:  # 待决
                                        self.gameinfo.broadcast_net[i][2][n][
                                            5] = 1

        #    [
        #        [4,        1, [[3, 2, 4, 4, 0, 1]],    [[1, 3, 1, 1, 0, 1]]],
        #        [4,        3, [],                      [[1, 3, 3, 5, 1, 1]]],
        #        [524288,   5, [[3, 3, 7, 3, 1, 1]],    []],
        #        [4,        2, [],                      [[1, 3, 4, 9, -1, -1], [1, 4, 1, 1, -1, -1]]],
        #        [4,        5, [],                      [[1, 3, 6, 12, 1, 1]]],
        #        [524288,   3, [[4, 2, 4, 3, 1, 1]],    []],
        #        [4,        4, [[4, 2, 6, 6, 0, 0]],    []]
        #    ]
        # 消息合并
        for i in range(len(self.gameinfo.broadcast_net)):
            if -1 == self.gameinfo.broadcast_net[i][0]:
                continue
            self.gameinfo.broadcast_net[i][0] = sb.EST_PROGRAM_BROADCASTMSG_ALL
            msgid1 = self.gameinfo.broadcast_net[i][1]
            for j in range(len(self.gameinfo.broadcast_net)):
                msgid2 = self.gameinfo.broadcast_net[j][1]
                if i == j:
                    continue
                if msgid1 == msgid2:
                    fanout_count = len(self.gameinfo.broadcast_net[j][2])
                    fanin_count = len(self.gameinfo.broadcast_net[j][3])
                    for m in range(fanout_count):
                        self.gameinfo.broadcast_net[i][2].append(
                            self.gameinfo.broadcast_net[j][2][m])
                    for m in range(fanin_count):
                        self.gameinfo.broadcast_net[i][3].append(
                            self.gameinfo.broadcast_net[j][3][m])
                    self.gameinfo.broadcast_net[j][0] = -1

        #    [
        #       [1048576, 1, [[3, 2, 4, 4, 0, 1]],  [[1, 3, 1, 1, 0, 1]]],
        #       [1048576, 3, [[4, 2, 4, 3, 1, 1]],  [[1, 3, 3, 5, 1, 1]]],
        #       [1048576, 5, [[3, 3, 7, 3, 1, 1]],  [[1, 3, 6, 12, 1, 1]]],
        #       [1048576, 2, [],                    [[1, 3, 4, 9, -1, -1], [1, 4, 1, 1, -1, -1]]],
        #       [-1,      5, [],                    [[1, 3, 6, 12, 1, 1]]],
        #       [-1,      3, [[4, 2, 4, 3, 1, 1]],  []],
        #       [1048576, 4, [[4, 2, 6, 6, 0, 0]],  []]
        #    ]
        # 删除被合并的消息
        del_net = []
        for i in range(len(self.gameinfo.broadcast_net)):
            if -1 == self.gameinfo.broadcast_net[i][0]:
                del_net.append(self.gameinfo.broadcast_net[i])
        for data in del_net:
            self.gameinfo.broadcast_net.remove(data)

        #    [
        #       [1048576, 1, [[3, 2, 4, 4, 0, 1]], [[1, 3, 1, 1, 0, 1]]],
        #       [1048576, 3, [[4, 2, 4, 3, 1, 1]], [[1, 3, 3, 5, 1, 1]]],
        #       [1048576, 5, [[3, 3, 7, 3, 1, 1]], [[1, 3, 6, 12, 1, 1]]],
        #       [1048576, 2, [],                   [[1, 3, 4, 9, -1, -1], [1, 4, 1, 1, -1, -1]]],
        #       [1048576, 4, [[4, 2, 6, 6, 0, 0]], []]
        #    ]
        #    标记位, send: flag广播0/点播1, flag有收1/无0/-1不定; recv: flag收广播0/点播1/待定-1, flag有发送1/无0/待定-1
        #    report:
        #        sender:   x,  !=1
        #        reciver:  -1, !=1
        self.ct_index.broadcast_index_number_messageid = len(
            self.gameinfo.broadcast_net)  # 10.1. broadcast: (+)广播消息ID数目
        for i in range(len(self.gameinfo.broadcast_net)):
            if sb.EST_PROGRAM_BROADCASTMSG_ALL == self.gameinfo.broadcast_net[
                    i][0]:  # 2019/12/12, 只 check 合并后的两种广播
                fanout_count = len(self.gameinfo.broadcast_net[i][2])
                fanin_count = len(self.gameinfo.broadcast_net[i][3])
                self.ct_index.broadcast_index_number_sendpointer += fanout_count  # 10.2. broadcast: (+)广播点数目
                self.ct_index.broadcast_index_number_recvpointer += fanin_count  # 10.4. broadcast: (+)广播接收点数目
                for j in range(fanout_count):
                    if 1 != self.gameinfo.broadcast_net[i][2][j][5]:  # 没有接收者
                        self.ct_index.broadcast_index_number_recvpointer_noreach += 1  # 10.5. broadcast: (-)广播接收点(不可执行到的)数目
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.broadcast_net[i][2][j][0])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_broadcast_noreceiver(self.gameinfo.broadcast_net[i][1], \
                                                                self.gameinfo.broadcast_net[i][2][j][0], \
                                                                sprite_name, \
                                                                self.gameinfo.broadcast_net[i][2][j][1], \
                                                                self.gameinfo.broadcast_net[i][2][j][2])
                for j in range(fanin_count):
                    if -1 == self.gameinfo.broadcast_net[i][3][j][
                            4] or 1 != self.gameinfo.broadcast_net[i][3][j][
                                5]:  # 没有发送者
                        self.ct_index.broadcast_index_number_sendpointer_noreach += 1  # 10.3. broadcast: (-)广播点(不可执行到的)数目
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.broadcast_net[i][3][j][1])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_broadcast_nosender(self.gameinfo.broadcast_net[i][1], \
                                                              self.gameinfo.broadcast_net[i][3][j][1], \
                                                              sprite_name, \
                                                              self.gameinfo.broadcast_net[i][3][j][2], \
                                                              self.gameinfo.broadcast_net[i][3][j][3])

        self.ct_index.broadcast_index_number_rise_endless_loop = 0  # 10.6. broadcast: (-)广播形成无效死循环(循环体中没有阻塞)数目 [暂时不处理]

        # check broadcast trigger
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                if 1 == self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].has_trigger:
                    can_trigger = self.check_trigger(iobj, jsc,
                                                     1)  # broadcast only
                    if 0 == can_trigger:
                        # report script 1
                        self.report.add_script_useless_script(
                            self.gameinfo.gameobject[iobj].gameobject_id,
                            self.gameinfo.gameobject[iobj].gameobject_name,
                            self.gameinfo.gameobject[iobj].scripts_sets[jsc].
                            scriptid, self.gameinfo.gameobject[iobj].
                            scripts_sets[jsc].block_set[0].sequenceid)
                    else:
                        pass

        # 11. logicalexpr(8)
        for iobj in range(len(self.gameinfo.gameobject)):
            for jsc in range(len(self.gameinfo.gameobject[iobj].scripts_sets)):
                self.ct_index.logicalexpr_index_number_totals += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].logicalexpr_index_number_totals  # 11.1. 逻辑表达式: (+)逻辑表达式数目
                for expk in range(
                        len(self.ct_index.logicalexpr_index_number_type)):
                    self.ct_index.logicalexpr_index_number_type[
                        expk] += self.gameinfo.gameobject[iobj].scripts_sets[
                            jsc].logicalexpr_index_number_type[
                                expk]  # 11.2. 逻辑表达式: (+)逻辑表达式种类数目
                if self.gameinfo.gameobject[iobj].scripts_sets[
                        jsc].logicalexpr_index_number_nest_depth_max > self.ct_index.logicalexpr_index_number_nest_depth_max:  # 11.3. 逻辑表达式: (+-)逻辑表达式参数嵌套最大深度
                    self.ct_index.logicalexpr_index_number_nest_depth_max = self.gameinfo.gameobject[
                        iobj].scripts_sets[
                            jsc].logicalexpr_index_number_nest_depth_max
                self.ct_index.logicalexpr_index_number_nest_depth_avg += \
                     (self.gameinfo.gameobject[iobj].scripts_sets[jsc].logicalexpr_index_number_totals * \
                      self.gameinfo.gameobject[iobj].scripts_sets[jsc].logicalexpr_index_number_nest_depth_avg) # 11.4. 逻辑表达式: (+-)逻辑表达式参数嵌套平均深度
                self.ct_index.logicalexpr_index_number_param_imcompleted += self.gameinfo.gameobject[
                    iobj].scripts_sets[
                        jsc].logicalexpr_index_number_param_imcompleted  # 11.7. 逻辑表达式: (-)逻辑表达式缺参数数目(向上传递)
        if self.ct_index.logicalexpr_index_number_totals > 0:
            self.ct_index.logicalexpr_index_number_nest_depth_avg = self.ct_index.logicalexpr_index_number_nest_depth_avg / self.ct_index.logicalexpr_index_number_totals  # 11.4. 逻辑表达式: (+-)逻辑表达式参数嵌套平均深度
        self.ct_index.logicalexpr_index_number_true_forever = 0  # 11.5. 逻辑表达式: (-)逻辑表达式永真数目(向上传递) [暂时不处理]
        self.ct_index.logicalexpr_index_number_false_forever = 0  # 11.6. 逻辑表达式: (-)逻辑表达式永假数目(向上传递) [暂时不处理]
        self.ct_index.logicalexpr_index_number_variables_nochanged = 0  # 11.8. 逻辑表达式: (-)逻辑表达式变量外部不变数目(向上传递) [暂时不处理]

        # 12. globalvar(11)
        # 13. localvar(10)
        #   self.variables_net = [] # [message-type,var-type,var-hostobjectid,var-hostobjectname,var-id,var-name,[sendlist],[recvlist]]
        #                           # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid,target-value]
        #                           # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        #                           # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        #                           # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        for i in range(len(self.gameinfo.variables_net)):
            if 0 == self.gameinfo.variables_net[i][1]:  # global
                self.ct_index.globalvar_index_number_totals += 1  # 12.1. 全局变量: (+)使用数目
                if len(self.gameinfo.variables_net[i][6]) > 0:
                    self.ct_index.globalvar_index_number_modified += 1  # 12.2. 全局变量: (+)更改数目
                self.ct_index.globalvar_index_number_check_pointer += len(
                    self.gameinfo.variables_net[i]
                    [7])  # 12.9. 全局变量: (+)变量检测点数目(script头)
                self.ct_index.globalvar_index_number_changed_pointer += len(
                    self.gameinfo.variables_net[i]
                    [6])  # 12.7. 全局变量: (+)变量修改点数目
                sprite_set = set()
                for k in range(len(self.gameinfo.variables_net[i][6])):
                    sprite_set.add(self.gameinfo.variables_net[i][6][k][0])
                for k in range(len(self.gameinfo.variables_net[i][7])):
                    sprite_set.add(self.gameinfo.variables_net[i][7][k][1])
                if len(sprite_set) > 1:
                    self.ct_index.globalvar_index_number_cross_sprite += 1  # 12.3. 全局变量: (+)跨sprite使用数目

                if 0 == len(self.gameinfo.variables_net[i][6]) and 0 == len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 1
                    self.report.add_variables_free("global", \
                                                      self.gameinfo.variables_net[i][5], \
                                                      self.gameinfo.variables_net[i][2], \
                                                      self.gameinfo.variables_net[i][3])
                if 0 == len(self.gameinfo.variables_net[i][6]) and 0 != len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 2
                    for m in range(len(self.gameinfo.variables_net[i][7])):
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.variables_net[i][7][m][1])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_variables_nomodified("global", \
                                                                self.gameinfo.variables_net[i][5], \
                                                                self.gameinfo.variables_net[i][7][m][1], \
                                                                sprite_name, \
                                                                self.gameinfo.variables_net[i][7][m][2], \
                                                                self.gameinfo.variables_net[i][7][m][3])
                if 0 != len(self.gameinfo.variables_net[i][6]) and 0 == len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 3
                    for m in range(len(self.gameinfo.variables_net[i][6])):
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.variables_net[i][6][m][0])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_variables_noused("global", \
                                                                self.gameinfo.variables_net[i][5], \
                                                                self.gameinfo.variables_net[i][6][m][0], \
                                                                sprite_name, \
                                                                self.gameinfo.variables_net[i][6][m][1], \
                                                                self.gameinfo.variables_net[i][6][m][2])
            else:  # local
                self.ct_index.localvar_index_number_totals += 1  # 13.1. 局部变量: (+)使用数目
                if len(self.gameinfo.variables_net[i][6]) > 0:
                    self.ct_index.localvar_index_number_modified += 1  # 13.2. 局部变量: (+)更改数目
                self.ct_index.localvar_index_number_check_pointer += len(
                    self.gameinfo.variables_net[i]
                    [7])  # 13.8. 局部变量: (+)变量检测点数目(script头)
                self.ct_index.localvar_index_number_changed_pointer += len(
                    self.gameinfo.variables_net[i]
                    [6])  # 13.6. 局部变量: (+)变量修改点数目

                if 0 == len(self.gameinfo.variables_net[i][6]) and 0 == len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 1
                    self.report.add_variables_free("local", \
                                                      self.gameinfo.variables_net[i][5], \
                                                      self.gameinfo.variables_net[i][2], \
                                                      self.gameinfo.variables_net[i][3])
                if 0 == len(self.gameinfo.variables_net[i][6]) and 0 != len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 2
                    for m in range(len(self.gameinfo.variables_net[i][7])):
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.variables_net[i][7][m][1])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_variables_nomodified("local", \
                                                                self.gameinfo.variables_net[i][5], \
                                                                self.gameinfo.variables_net[i][7][m][1], \
                                                                sprite_name, \
                                                                self.gameinfo.variables_net[i][7][m][2], \
                                                                self.gameinfo.variables_net[i][7][m][3])
                if 0 != len(self.gameinfo.variables_net[i][6]) and 0 == len(
                        self.gameinfo.variables_net[i][7]):
                    # report vairiables 3
                    for m in range(len(self.gameinfo.variables_net[i][6])):
                        sprite_name = ""
                        object_index = self.get_objectindex_by_objectid(
                            self.gameinfo.variables_net[i][6][m][0])
                        if -1 != object_index:
                            sprite_name = self.gameinfo.gameobject[
                                object_index].gameobject_name
                        self.report.add_variables_noused("local", \
                                                                self.gameinfo.variables_net[i][5], \
                                                                self.gameinfo.variables_net[i][6][m][0], \
                                                                sprite_name, \
                                                                self.gameinfo.variables_net[i][6][m][1], \
                                                                self.gameinfo.variables_net[i][6][m][2])

        # global
        self.ct_index.globalvar_index_number_trigger_script = 0  # 12.4. 全局变量: (+)触发script数目 [暂时不处理]
        self.ct_index.globalvar_index_number_control_loop = 0  # 12.5. 全局变量: (+)变量控制的循环数目 [暂时不处理]
        self.ct_index.globalvar_index_number_control_condition = 0  # 12.6. 全局变量: (+)变量控制的条件数目 [暂时不处理]
        self.ct_index.globalvar_index_number_changed_pointer_noreach = 0  # 12.8. 全局变量: (-)变量修改点(不可执行到的)数目 [暂时不处理]
        self.ct_index.globalvar_index_number_check_pointer_noreach = 0  # 12.10. 全局变量: (-)变量检测点(不可执行到的)数目(script头) [暂时不处理]
        self.ct_index.globalvar_index_number_rise_endless_loop = 0  # 12.11. 全局变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目
        # local
        self.ct_index.localvar_index_number_trigger_script = 0  # 13.3. 局部变量: (+)触发script数目 [暂时不处理]
        self.ct_index.localvar_index_number_control_loop = 0  # 13.4. 局部变量: (+)变量控制的循环数目 [暂时不处理]
        self.ct_index.localvar_index_number_control_condition = 0  # 13.5. 局部变量: (+)变量控制的条件数目 [暂时不处理]
        self.ct_index.localvar_index_number_changed_pointer_noreach = 0  # 13.7. 局部变量: (-)变量修改点(不可执行到的)数目 [暂时不处理]
        self.ct_index.localvar_index_number_check_pointer_noreach = 0  # 13.9. 局部变量: (-)变量检测点(不可执行到的)数目(script头) [暂时不处理]
        self.ct_index.localvar_index_number_rise_endless_loop = 0  # 13.10. 局部变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目 [暂时不处理]

        # 14. interaction(11)
        # 15. phycharacteristics(4)
        # 16. phyaction(12)
        # interaction
        cur_gameobjectid = -1
        mouse_sprite_set = set()
        keyboard_sprite_set = set()
        joystick_sprite_set = set()
        # phycharacteristics
        sripte_open_engine_set = set()
        # phyaction
        moving_sprite_set = set()
        rotate_sprite_set = set()
        play_animation_sprite_set = set()
        for goindex in range(len(self.gameinfo.gameobject)):
            cur_gameobjectid = self.gameinfo.gameobject[goindex].gameobject_id
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    # interaction
                    if sb.BLKREFID_TRG_WHENMOUSEMOVING == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_TRG_WHENMOUSELEFTKEYACTION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 鼠标
                        mouse_sprite_set.add(
                            cur_gameobjectid)  # 14.7. 交互: (+)鼠标:处理sprite数目
                        self.ct_index.interaction_index_number_mouse_checkpointer += 1  # 14.8. 交互: (+)鼠标:处理点数目
                    if sb.BLKREFID_TRG_WHENSELFBEENCLICK == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_TRG_WHENKEYBOARDACTION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 键盘
                        keyboard_sprite_set.add(
                            cur_gameobjectid)  # 14.1. 交互: (+)键盘:处理sprite数目
                        self.ct_index.interaction_index_number_keyboard_checkpointer += 1  # 14.2. 交互: (+)键盘:处理点数目
                    # BLKREFID_TRG_WHENSELFBEENCLICK 有重复计入;
                    if sb.BLKREFID_TRG_WHENSELFBEENCLICK == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_TRG_WHENPICOHANDLECURSOR == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_TRG_WHENPICOHANDLEACTION == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_CND_POCIKEYDOWNRELEASE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 手柄
                        joystick_sprite_set.add(
                            cur_gameobjectid)  # 14.4. 交互: (+)手柄:处理sprite数目
                        self.ct_index.interaction_index_number_joystick_checkpointer += 1  # 14.5. 交互: (+)手柄:处理点数目
                    if sb.BLKREFID_OA_DISPLAYTEXTONTOP == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 提示
                        self.ct_index.interaction_index_number_user_inputprompt += 1  # 14.11. 交互: (+)用户输入提示频率
                    if sb.BLKREFID_OA_DISPLAYTEXTINUIRESOURCE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 提示,输入
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:
                                self.ct_index.interaction_index_number_user_inputpointer += 1  # 14.10. 交互: (+)用户输入点数目
                        self.ct_index.interaction_index_number_user_inputprompt += 1  # 14.11. 交互: (+)用户输入提示频率
                    if sb.BLKREFID_DC_TEXTOFRESOUREUI == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 输入
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:
                                self.ct_index.interaction_index_number_user_inputpointer += 1  # 14.10. 交互: (+)用户输入点数目
                    # phycharacteristics
                    if sb.BLKREFID_PF_STARTPHYSICSENGINE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 开启物理引擎
                        sripte_open_engine_set.add(cur_gameobjectid)
                    # phyaction
                    if sb.BLKREFID_OA_MOVINGRXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_MOVINGRXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_MOVINGAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 移动
                        moving_sprite_set.add(cur_gameobjectid)
                        self.ct_index.phyaction_index_moving_sprite_blocks += 1  # 16.2. 物理行为: (+)移动的sprite指令块数目
                        self.ct_index.phyaction_index_moving_sprite_times += 1  # 16.4. 物理行为: (+)移动的sprite次数 [暂不考虑运行期间的循环次数等]
                    if sb.BLKREFID_OA_ROTATERXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_ROTATERXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_ROTATEAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_RESIZEPERSENT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 旋转(含缩放)
                        rotate_sprite_set.add(cur_gameobjectid)
                        self.ct_index.phyaction_index_rotate_sprite_blocks += 1  # 16.6. 旋转行为: (+)移动的sprite指令块数目
                        self.ct_index.phyaction_index_rotate_sprite_times += 1  # 16.8. 物理行为: (+)旋转的sprite次数 [暂不考虑运行期间的循环次数等]
                    if sb.BLKREFID_OA_PLAYRESOURCEACTION == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 播放动作
                        play_animation_sprite_set.add(cur_gameobjectid)
                        self.ct_index.phyaction_index_play_animation_sprite_blocks += 1  # 16.10. 物理行为: (+)播放动画效果的sprite指令块数目
                        self.ct_index.phyaction_index_play_animation_sprite_times += 1  # 16.12. 物理行为: (+)播放动画效果的sprite次数 [暂不考虑运行期间的循环次数等]

        # interaction
        self.ct_index.interaction_index_number_mouse_sprite = len(
            mouse_sprite_set)  # 14.7. 交互: (+)鼠标:处理sprite数目
        self.ct_index.interaction_index_number_mouse_checkpointer_useless = 0  # 14.9. 交互: (-)鼠标:无效处理点数目 [暂时不处理]
        self.ct_index.interaction_index_number_keyboard_sprite = len(
            keyboard_sprite_set)  # 14.1. 交互: (+)键盘:处理sprite数目
        self.ct_index.interaction_index_number_keyboard_checkpointer_useless = 0  # 14.3. 交互: (-)键盘:无效处理点数目 [暂时不处理]
        self.ct_index.interaction_index_number_joystick_sprite = len(
            joystick_sprite_set)  # 14.4. 交互: (+)手柄:处理sprite数目
        self.ct_index.interaction_index_number_joystick_checkpointer_useless = 0  # 14.6. 交互: (-)手柄:无效处理点数目 [暂时不处理]
        # phycharacteristics
        self.ct_index.phycharacteristics_index_number_sripte_open_engine = len(
            sripte_open_engine_set)  # 15.1. 物理特性: (+)开启物理引擎的sprite数目
        self.ct_index.phycharacteristics_index_number_sripte_open_engine_useless = 0  # 15.2. 物理特性: (-)开启物理特性动作能否执行到 [暂时不处理]
        self.ct_index.phycharacteristics_index_number_blocks_in_engine_windows = 0  # 15.3. 物理特性: (+)物理引擎窗口内受制block数目 [暂时不处理]
        self.ct_index.phycharacteristics_index_number_blocks_out_engine_wondows = 0  # 15.4. 物理特性: (-)物理引擎窗口外受制block数目 [暂时不处理]
        # 2019/12/04 added, check phycharacteristics(4) begin
        #  注意: 物理引擎的打开,关闭可能不在同一个script中,需要通过script执行时序,条件循环的控制(变量),消息间通知等实现,此处只检查一个脚本中的情况,可能有误报,考虑到script中块的执行受序号,条件等影响,可能更会有误;
        #        BLKREFID_PF_STARTPHYSICSENGINE
        #        BLKREFID_PF_STOPPHYSICSENGINE
        #        BLKREFID_PF_SETTINGMASS
        #        BLKREFID_PF_OPENGRAVITY
        #        BLKREFID_PF_CLOSEGRAVITY
        #        BLKREFID_PF_FORCEFROMXYZBYCOORDINATE
        #        BLKREFID_PF_TOBETRIGGER
        #        BLKREFID_PF_TOBECOLLIDER
        for goindex in range(len(self.gameinfo.gameobject)):
            open_engine_set = set()
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_PF_STARTPHYSICSENGINE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        open_engine_set.add(scindex)
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                engine_open = False
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_PF_STARTPHYSICSENGINE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        engine_open = True
                    if sb.BLKREFID_PF_STOPPHYSICSENGINE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:
                        engine_open = False
                    if sb.BLKREFID_PF_SETTINGMASS == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_PF_OPENGRAVITY == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_PF_CLOSEGRAVITY == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_PF_FORCEFROMXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_PF_TOBETRIGGER == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_PF_TOBECOLLIDER == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:
                        if not engine_open:
                            if not ((len(open_engine_set) >= 1
                                     and scindex not in open_engine_set) or
                                    (len(open_engine_set) >= 2
                                     and scindex in open_engine_set)):
                                # report phycharacteristics 1
                                self.report.add_phycharacteristics_block_noopenengine(
                                    self.gameinfo.gameobject[goindex].
                                    gameobject_id, self.gameinfo.
                                    gameobject[goindex].gameobject_name,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].scriptid,
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    sequenceid)
        # 2019/12/04 added, check phycharacteristics(4) end
        # phyaction
        self.ct_index.phyaction_index_moving_sprite_type_number = len(
            moving_sprite_set)  # 16.1. 物理行为: (+)移动的sprite数目
        self.ct_index.phyaction_index_rotate_sprite_type_number = len(
            rotate_sprite_set)  # 16.5. 旋转行为: (+)移动的sprite数目
        self.ct_index.phyaction_index_play_animation_sprite_type_number = len(
            play_animation_sprite_set)  # 16.9. 物理行为: (+)播放动画效果的sprite数目
        self.ct_index.phyaction_index_moving_sprite_blocks_useless = 0  # 16.3. 物理行为: (-)移动的sprite指令块数目(不能执行到) [暂时不处理]
        self.ct_index.phyaction_index_rotate_sprite_blocks_useless = 0  # 16.7. 旋转行为: (-)移动的sprite指令块数目(不能执行到) [暂时不处理]
        self.ct_index.phyaction_index_play_animation_sprite_blocks_useless = 0  # 16.11. 物理行为: (-)播放动画效果的sprite指令块数目(不能执行到) [暂时不处理]

        # 17. objsetting(22)
        # 18. music(5)
        # objsetting
        sprite_in_group = set()
        del_sprite_set = set()
        display_sprite_set = set()
        hide_sprite_set = set()
        group_moving_sprite_set = set()
        group_rotate_sprite_set = set()
        # music
        music_set = set()

        cur_gameobjectid = -1
        group_info_dict = self.calculate_static_group_info(
        )  # {groupid:{objectid set},...}
        # objsetting
        self.ct_index.objsetting_index_number_group = len(
            group_info_dict)  # 17.10. 物体设置: (+)父子关系团数目
        for key in group_info_dict:
            sprite_in_group = sprite_in_group | group_info_dict[key]
            if len(group_info_dict[key]
                   ) > self.ct_index.objsetting_index_number_group_max_unit:
                self.ct_index.objsetting_index_number_group_max_unit = len(
                    group_info_dict[key])  # 17.11. 物体设置: (+)父子团最大sprite数目
            self.ct_index.objsetting_index_number_group_avg_unit += len(
                group_info_dict[key])
        if self.ct_index.objsetting_index_number_group > 0:
            self.ct_index.objsetting_index_number_group_avg_unit = self.ct_index.objsetting_index_number_group_avg_unit / self.ct_index.objsetting_index_number_group  # 17.12. 物体设置: (+)父子团平均sprite数目

        for goindex in range(len(self.gameinfo.gameobject)):
            cur_gameobjectid = self.gameinfo.gameobject[goindex].gameobject_id
            # objsetting
            for scindex in range(
                    len(self.gameinfo.gameobject[goindex].scripts_sets)):
                for bkindex in range(
                        len(self.gameinfo.gameobject[goindex].
                            scripts_sets[scindex].block_set)):
                    if sb.BLKREFID_OS_DELETESELF == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 删除
                        del_sprite_set.add(
                            cur_gameobjectid)  # 17.1. 物体设置: (+)删除sprite数目
                        self.ct_index.objsetting_index_number_del_sprite_blocks += 1  # 17.2. 物体设置: (+)删除sprite指令块数目
                    if sb.BLKREFID_OS_DISPLAYRESOURCE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 显示
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:
                                display_sprite_set.add(
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    parameter_info[0][2])
                                if self.gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_set[
                                                bkindex].parameter_info[0][
                                                    2] in sprite_in_group:  # 在组中
                                    self.ct_index.objsetting_index_number_group_show += 1  # 17.19. 物体设置: (+)父子团子sprite显示数目
                        self.ct_index.objsetting_index_number_show_sprite_blocks += 1  # 17.5. 物体设置: (+)显示sprite指令块数目
                    if sb.BLKREFID_OS_HIDERESOURCE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 隐藏
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:
                                hide_sprite_set.add(
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    parameter_info[0][2])
                                if self.gameinfo.gameobject[
                                        goindex].scripts_sets[
                                            scindex].block_set[
                                                bkindex].parameter_info[0][
                                                    2] in sprite_in_group:  # 在组中
                                    self.ct_index.objsetting_index_number_group_hide += 1  # 17.20. 物体设置: (+)父子团子sprite影藏数目
                        self.ct_index.objsetting_index_number_hide_sprite_blocks += 1  # 17.8. 物体设置: (+)影藏sprite指令块数目
                    if sb.BLKREFID_OA_MOVINGRXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_MOVINGRXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_MOVINGAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 移动
                        group_moving_sprite_set.add(cur_gameobjectid)
                    if sb.BLKREFID_OA_ROTATERXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_ROTATERXYZBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_ROTATEAXYZINTIMEBYCOORDINATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OA_RESIZEPERSENT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 旋转(含缩放)
                        group_rotate_sprite_set.add(cur_gameobjectid)
                    if sb.BLKREFID_OA_PLAYRESOURCEACTION == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 播放动作
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:  # 合法
                                self.ct_index.objsetting_index_number_group_play_animation += 1  # 17.17. 物体设置: (+)父子团播放动作数目
                            else:
                                self.ct_index.objsetting_index_number_group_not_play_animation += 1  # 17.18. 物体设置: (-)父子团不播放动作数目
                    if sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINOVERLAPPING == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINORIGINALSTATE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 组合并
                        self.ct_index.objsetting_index_number_group_packaged_dynamically += 1  # 17.21. 物体设置: (+)父子团子sprite动态组团数目
                    if sb.BLKREFID_OS_BREADAWAYFROWPARENTRESOURCE == self.gameinfo.gameobject[
                            goindex].scripts_sets[scindex].block_set[
                                bkindex].refid:  # 组拆分
                        self.ct_index.objsetting_index_number_group_unpackaged_dynamically += 1  # 17.22. 物体设置: (+)父子团子sprite动态拆分数目
                    # music
                    if sb.BLKREFID_SD_PLAYSOUNDREPEAT == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid or \
                       sb.BLKREFID_SD_PLAYSOUNDONCE == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid: # 播放音乐
                        if self.gameinfo.gameobject[goindex].scripts_sets[
                                scindex].block_set[
                                    bkindex].parameter_count_need > 0:
                            if 1 == self.gameinfo.gameobject[
                                    goindex].scripts_sets[scindex].block_set[
                                        bkindex].parameter_info[0][7]:  # 合法
                                self.ct_index.music_index_number_play_pointer += 1  # 18.1. 音乐: (+)音乐播放数目
                                music_set.add(
                                    self.gameinfo.gameobject[goindex].
                                    scripts_sets[scindex].block_set[bkindex].
                                    parameter_info[0][2])
                            else:
                                self.ct_index.music_index_number_play_pointer_noreach += 1  # 18.2. 音乐: (-)不能被播放数目
                                self.ct_index.music_index_number_play_pointer_param_incompleted += 1  # 18.4. 音乐: (-)缺少参数数目
                                # report music
                                self.report.add_music_noparam(self.gameinfo.gameobject[goindex].gameobject_id, self.gameinfo.gameobject[goindex].gameobject_name, self.gameinfo.gameobject[goindex].scripts_sets[scindex].scriptid, self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].sequenceid)
                    if sb.BLKREFID_SD_STOPSOUND == self.gameinfo.gameobject[goindex].scripts_sets[scindex].block_set[bkindex].refid:  # 停止播放音乐
                        self.ct_index.music_index_number_stop_pointer += 1  # 18.5. 音乐: (+)主动停止数目

        # objsetting
        self.ct_index.objsetting_index_number_del_sprite = len(
            del_sprite_set)  # 17.1. 物体设置: (+)删除sprite数目
        self.ct_index.objsetting_index_number_del_sprite_blocks_noreach = 0  # 17.3. 物体设置: (-)删除sprite指令块数目(不能执行到)  [暂时不处理]
        self.ct_index.objsetting_index_number_show_sprite = len(
            display_sprite_set)  # 17.4. 物体设置: (+)显示sprite数目
        self.ct_index.objsetting_index_number_show_sprite_blocks_noreach = 0  # 17.6. 物体设置: (-)显示sprite指令块数目(不能执行到)
        self.ct_index.objsetting_index_number_hide_sprite = len(
            hide_sprite_set)  # 17.7. 物体设置: (+)影藏sprite数目
        self.ct_index.objsetting_index_number_hide_sprite_blocks_noreach = 0  # 17.9. 物体设置: (-)影藏sprite指令块数目(不能执行到)
        for key in group_info_dict:
            if 0 == len(group_info_dict[key] & group_moving_sprite_set):
                self.ct_index.objsetting_index_number_group_not_moving += 1  # 17.14. 物体设置: (-)父子团不移动数目
            else:
                self.ct_index.objsetting_index_number_group_moving += 1  # 17.13. 物体设置: (+)父子团移动数目

            if 0 == len(group_info_dict[key] & group_rotate_sprite_set):
                self.ct_index.objsetting_index_number_group_not_rotate += 1  # 17.16. 物体设置: (-)父子团不旋转数目
            else:
                self.ct_index.objsetting_index_number_group_rotate += 1  # 17.15. 物体设置: (+)父子团旋转数目

        # 18. music(5)
        self.ct_index.music_index_number_play_songs = len(
            music_set)  # 18.3. 音乐: (+)音乐播放曲目数目

    # 递归计算block用时
    def calucate_runtime(self, sc_info, block_sequenceid):
        block_index = sc_info.block_dict_seqid_index[block_sequenceid]
        if 1 == sc_info.block_set[
                block_index].is_parameter_block:  # 参数块不计算执行时间
            sc_info.block_set[block_index].time_used = 0
            return 0
        else:
            # 考虑到参数块嵌套,累计用时和涉及变量暂时不能决定
            if sb.BLKREFID_LF_WAITNUMBERSECONDS == sc_info.block_set[
                    block_index].refid:
                return sc_info.block_set[block_index].time_used
            elif sb.BLKREFID_LF_IF == sc_info.block_set[block_index].refid:
                if 0 == sc_info.block_set[block_index].has_child1:
                    sc_info.block_set[block_index].time_used = 0
                    return 0
                else:
                    used_time = 0
                    for i in range(
                            len(sc_info.block_set[block_index].childblock_list1
                                )):
                        temp = self.calucate_runtime(
                            sc_info,
                            sc_info.block_set[block_index].childblock_list1[i])
                        if sb.MAX_TIME == temp:
                            sc_info.block_set[
                                block_index].time_used = sb.MAX_TIME
                            return sb.MAX_TIME  # 其他的块用时不用在计算
                        else:
                            used_time += temp
                    sc_info.block_set[block_index].time_used = used_time
                    return used_time
            elif sb.BLKREFID_LF_IFELSE == sc_info.block_set[block_index].refid:
                if 0 == sc_info.block_set[
                        block_index].has_child1 and 0 == sc_info.block_set[
                            block_index].has_child2:
                    sc_info.block_set[block_index].time_used = 0
                    return 0
                else:
                    used_time1 = 0
                    for i in range(
                            len(sc_info.block_set[block_index].childblock_list1
                                )):
                        temp = self.calucate_runtime(
                            sc_info,
                            sc_info.block_set[block_index].childblock_list1[i])
                        if sb.MAX_TIME == temp:
                            sc_info.block_set[
                                block_index].time_used = sb.MAX_TIME
                            return sb.MAX_TIME  # 其他的块用时不用在计算
                        else:
                            used_time1 += temp
                    used_time2 = 0
                    for i in range(
                            len(sc_info.block_set[block_index].childblock_list2
                                )):
                        temp = self.calucate_runtime(
                            sc_info,
                            sc_info.block_set[block_index].childblock_list2[i])
                        if sb.MAX_TIME == temp:
                            sc_info.block_set[
                                block_index].time_used = sb.MAX_TIME
                            return sb.MAX_TIME  # 其他的块用时不用在计算
                        else:
                            used_time2 += temp
                    if used_time1 > used_time2:
                        sc_info.block_set[block_index].time_used = used_time1
                        return used_time1
                    else:
                        sc_info.block_set[block_index].time_used = used_time2
                        return used_time2
            elif sb.BLKREFID_LF_LOOPUNLIMITED == sc_info.block_set[
                    block_index].refid:  # 暂时不判断BLKREFID_LF_LOOPSTOP,BLKREFID_OS_GAMEOVER
                sc_info.block_set[block_index].time_used = sb.MAX_TIME
                return sb.MAX_TIME
            elif sb.BLKREFID_LF_LOOPNUMBER == sc_info.block_set[
                    block_index].refid:
                if 0 == sc_info.block_set[block_index].has_child1:
                    sc_info.block_set[block_index].time_used = 0
                    return 0
                else:
                    used_time = 0
                    for i in range(
                            len(sc_info.block_set[block_index].childblock_list1
                                )):
                        temp = self.calucate_runtime(
                            sc_info,
                            sc_info.block_set[block_index].childblock_list1[i])
                        if sb.MAX_TIME == temp:
                            sc_info.block_set[
                                block_index].time_used = sb.MAX_TIME
                            return sb.MAX_TIME  # 其他的块用时不用在计算
                        else:
                            used_time += temp
                    if sc_info.block_set[block_index].parameter_info[0][2] > 1:
                        used_time *= sc_info.block_set[
                            block_index].parameter_info[0][2]
                    sc_info.block_set[block_index].time_used = used_time
                    return used_time
            else:
                return 0

    def iscontainer(self, block_ref_id):
        if (block_ref_id == sb.BLKREFID_LF_LOOPUNLIMITED
                or block_ref_id == sb.BLKREFID_LF_LOOPNUMBER
                or block_ref_id == sb.BLKREFID_LF_LOOP_WHILE_WHILENOT
                or block_ref_id == sb.BLKREFID_LF_IF
                or block_ref_id == sb.BLKREFID_LF_LOOP_STEP
                or block_ref_id == sb.BLKREFID_LF_LOOP_TRAVERSELIST
                or block_ref_id == sb.BLKREFID_LF_IFELSE_PLUS
                or block_ref_id == sb.BLKREFID_LF_IFELSE or block_ref_id
                == sb.BLKREFID_LF_TELLOBJECT2EXCUTING):  # 支持 21
            return 1
        else:
            return 0

    # 2019/12/11 modified
    def isparameterblock(self, blocktype, block_ref_id):
        if (
            (
                block_ref_id == sb.BLKREFID_VAR_VARIABLES
                or block_ref_id == sb.BLKREFID_VAR_STRING
                or block_ref_id == sb.BLKREFID_VAR_LIST
                or block_ref_id == sb.BLKREFID_VAR_OBJECT
                or block_ref_id == sb.BLKREFID_VAR_LIST_GET
                or block_ref_id == sb.BLKREFID_VAR_STRING_JOINT
                or block_ref_id == sb.BLKREFID_VAR_STRING_GETLENGTH
                or block_ref_id == sb.BLKREFID_VAR_STRING_SUBCOUNT
                or block_ref_id == sb.BLKREFID_VAR_STRING_FUNCTION
                or block_ref_id == sb.BLKREFID_VAR_STRINGCHAR
                or block_ref_id == sb.BLKREFID_VAR_STRINGLASTCHAR
                or block_ref_id == sb.BLKREFID_VAR_STRINGSUBSTRPICK
                or block_ref_id == sb.BLKREFID_VAR_STRINGJOINTBYTOKEN
                or block_ref_id == sb.BLKREFID_VAR_STRINGSPLITLIMITCOUNT
                or block_ref_id == sb.BLKREFID_VAR_STRINGSUB
                or block_ref_id == sb.BLKREFID_VAR_STRINGSUBCOUNT
                or block_ref_id == sb.BLKREFID_VAR_STRINGREPLACE
                or block_ref_id == sb.BLKREFID_VAR_VARIABLESINCDEC
                or block_ref_id == sb.BLKREFID_VAR_VARIABLESASSIGNMENT
                or block_ref_id == sb.BLKREFID_VAR_LIST_SET
                or block_ref_id == sb.BLKREFID_VAR_LOG
                or block_ref_id == sb.BLKREFID_VAR_LIST_APPEND
                or block_ref_id == sb.BLKREFID_VAR_LIST_INSERT
                or block_ref_id == sb.BLKREFID_VAR_LIST_REMOVE
                or block_ref_id == sb.BLKREFID_VAR_LISTSORT
                or block_ref_id == sb.BLKREFID_VAR_PLUSEQUEAL
                or block_ref_id == sb.BLKREFID_VAR_REMOVETAIL
             )
            and blocktype == sb.BLKTYPE_VARIABLES  #
            or blocktype == sb.BLKTYPE_CONDITION
            or blocktype == sb.BLKTYPE_DATACAL):
            return 1
        else:
            return 0

    def isdetonator(self, blocktype):
        if blocktype == sb.BLKTYPE_TRIGGER:
            return 1
        else:
            return 0

    def get_objectname_by_objectid(self, objectid):
        for i in range(len(self.gameinfo.gameobject)):
            if self.gameinfo.gameobject[i].gameobject_id == objectid:
                return self.gameinfo.gameobject[i].gameobject_name
        return ""

    def get_variables_info(self, goindex, var_order):
        # [var-type,var-hostobjectid,var-hostobjectname,var-id,var-name]
        # 注意: 变量控件中没有变量的时候,缺省值显示的也是0,有一个变量的时候显示的也是0
        var_info = []
        global_var_count = len(self.gameinfo.variables_sets_global)
        if var_order + 1 > global_var_count:
            # local variables
            if 0 == len(
                    self.gameinfo.gameobject[goindex].variables_sets_local):
                return var_info
            var_info.append(1)
            var_info.append(self.gameinfo.gameobject[goindex].gameobject_id)
            var_info.append(self.gameinfo.gameobject[goindex].gameobject_name)
            var_info.append(
                self.gameinfo.gameobject[goindex].variables_sets_local[
                    var_order - global_var_count][1])
            var_info.append(
                self.gameinfo.gameobject[goindex].variables_sets_local[
                    var_order - global_var_count][2])
        else:
            # global variables
            if 0 == len(self.gameinfo.variables_sets_global):
                return var_info
            var_info.append(0)
            var_info.append(1)
            var_info.append("Root")
            var_info.append(self.gameinfo.variables_sets_global[var_order][1])
            var_info.append(self.gameinfo.variables_sets_global[var_order][2])
        return var_info

    # 2019/12/11 add
    def get_list_info(self, var_info, goindex):
        list_info = [0, 0]
        if 0 == var_info[0]:  # global
            # search in global list
            for i in range(len(self.gameinfo.variables_list_global)):
                if var_info[4] == self.gameinfo.variables_list_global[i][0]:
                    list_info[0] = 1
                    list_info[1] = self.gameinfo.variables_list_global[i][1]
                    break
        else:  # local
            # search in local list
            for i in range(
                    len(self.gameinfo.gameobject[goindex].variables_list_local)
            ):
                if var_info[4] == self.gameinfo.gameobject[
                        goindex].variables_list_local[i][0]:
                    list_info[0] = 1
                    list_info[1] = self.gameinfo.gameobject[
                        goindex].variables_list_local[i][1]
                    break

        return list_info

    def get_objectindex_by_objectid(self, target_source_objectid):
        for i in range(len(self.gameinfo.gameobject)):
            if self.gameinfo.gameobject[
                    i].gameobject_id == target_source_objectid:
                return i
        return -1

    def get_max_gourpid(self):
        maxid = 0
        for i in range(len(self.gameinfo.gameobject)):
            if len(self.gameinfo.gameobject[i].gameobject_attributes) > 1:
                if maxid < self.gameinfo.gameobject[i].gameobject_attributes[
                        1][1]:
                    maxid = self.gameinfo.gameobject[i].gameobject_attributes[
                        1][1]
                else:
                    pass
            else:
                pass
        return maxid

    # check script,whether can be triggered  # broadcast,clone,variables
    def check_trigger(self, gameobject_index, script_index, broadcast_flag):
        if 0 == self.gameinfo.gameobject[gameobject_index].scripts_sets[
                script_index].has_trigger:
            return 0
        else:
            if sb.BLKREFID_TRG_WHENRECIEVEBROADCASTMESSAGE == self.gameinfo.gameobject[
                    gameobject_index].scripts_sets[script_index].block_set[
                        0].refid and 1 == broadcast_flag:
                return self.check_broadcast(gameobject_index, script_index, 0)
            elif sb.BLKREFID_TRG_WHENCONDITION == self.gameinfo.gameobject[
                    gameobject_index].scripts_sets[script_index].block_set[
                        0].refid and 0 == broadcast_flag:
                return self.check_variables(gameobject_index, script_index, 0)
            elif sb.BLKREFID_TRG_WHENRUNNINGASCLONE == self.gameinfo.gameobject[
                    gameobject_index].scripts_sets[script_index].block_set[
                        0].refid and 0 == broadcast_flag:
                return self.check_clone(gameobject_index, script_index, 0)
            else:
                return 1  # 其他类型认为都可以 trigger

    def check_broadcast(self, gameobject_index, script_index, block_index):
        # broadcast
        # self.broadcast_net = []    # [message-type,messageid,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        #  标记位, send: flag广播0/点播1, flag有收1/无0/-1不定; recv: flag收广播0/点播1/待定-1, flag有发送1/无0/待定-1
        if sb.BLKREFID_TRG_WHENRECIEVEBROADCASTMESSAGE != self.gameinfo.gameobject[
                gameobject_index].scripts_sets[script_index].block_set[
                    block_index].refid:
            return 0
        messageid = self.gameinfo.gameobject[gameobject_index].scripts_sets[
            script_index].block_set[block_index].parameter_info[0][2]
        if messageid < 0:
            return 0
        for i in range(len(self.gameinfo.broadcast_net)):
            if messageid == self.gameinfo.broadcast_net[i][1]:  # found
                if len(self.gameinfo.broadcast_net[i][2]) <= 0:  # 不发消息
                    return 0
                else:
                    objid = self.gameinfo.gameobject[
                        gameobject_index].gameobject_id
                    scripteid = self.gameinfo.gameobject[
                        gameobject_index].scripts_sets[script_index].scriptid
                    blockid = self.gameinfo.gameobject[
                        gameobject_index].scripts_sets[script_index].block_set[
                            block_index].sequenceid
                    for j in range(len(self.gameinfo.broadcast_net[i]
                                       [3])):  # 在reciver中找自己的状态
                        if objid == self.gameinfo.broadcast_net[i][3][j][1] and \
                           scripteid == self.gameinfo.broadcast_net[i][3][j][2] and \
                           blockid == self.gameinfo.broadcast_net[i][3][j][3]:
                            if not (-1
                                    == self.gameinfo.broadcast_net[i][3][j][4]
                                    or 1 !=
                                    self.gameinfo.broadcast_net[i][3][j][5]):
                                return 1
            else:
                pass
        #        for i in range(len(self.gameinfo.broadcast_net)):
        #            if messageid == self.gameinfo.broadcast_net[i][1]: # found
        #                if len(self.gameinfo.broadcast_net[i][2]) <= 0: # 没有触发点
        #                    return 0
        #                else:
        #                    for j in range(len(self.gameinfo.broadcast_net[i][2])):
        #                        if self.gameinfo.gameobject[gameobject_index].gameobject_id != self.gameinfo.broadcast_net[i][2][j][0] or \
        #                           self.gameinfo.gameobject[gameobject_index].scripts_sets[script_index].scriptid != self.gameinfo.broadcast_net[i][2][j][1]: # 触发点不在自己内部
        #                           return 1
        #            else:
        #                pass
        return 0

    def check_clone(self, gameobject_index, script_index, block_index):
        # clone
        # self.clone_net = []        # [message-type,clone target-objectgameid,target-objectgamename,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        if sb.BLKREFID_TRG_WHENCONDITION != self.gameinfo.gameobject[
                gameobject_index].scripts_sets[script_index].block_set[
                    block_index].refid:
            return 0
        objectid = self.gameinfo.gameobject[gameobject_index].gameobject_id
        objectname = self.gameinfo.gameobject[gameobject_index].gameobject_name
        for i in range(len(self.gameinfo.clone_net)):
            if objectid == self.gameinfo.clone_net[i][
                    1] and objectname == self.gameinfo.clone_net[i][2]:  # found
                if len(self.gameinfo.clone_net[i][3]) <= 0:  # 没有触发点
                    return 0
                else:
                    for j in range(len(self.gameinfo.clone_net[i][3])):
                        if self.gameinfo.gameobject[gameobject_index].gameobject_id != self.gameinfo.clone_net[i][3][j][0] or \
                           self.gameinfo.gameobject[gameobject_index].scripts_sets[script_index].scriptid != self.gameinfo.clone_net[i][3][j][1]: # 触发点不在自己内部
                            return 1
            else:
                pass
        return 0

    def check_variables(self, gameobject_index, script_index, block_index):
        # variables
        # self.variables_net = []    # # [message-type,var-type,var-hostobjectid,var-hostobjectname,var-id,var-name,[sendlist],[recvlist]]
        # [sendlist] = [gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid,target-value]
        # [recvlist] = [recv-type,gameobjectid,scriptid,block-sequenceid,hostblock-sequenceid]
        # 第一类触发点指script的首块,块类型是BLKTYPE_TRIGGER,一直等待直到某个事件触发;
        # 第二类触发点指条件判断中的条件表达式,可能一闪而过或者循环检测;
        # self.variables_sets_global = [] # 全局变量列表(变量类型,变量ID,变量名称,默认值)
        # self.variables_sets_local = []  # 局部变量列表(变量类型,变量ID,变量名称,默认值)
        if sb.BLKREFID_TRG_WHENCONDITION != self.gameinfo.gameobject[
                gameobject_index].scripts_sets[script_index].block_set[
                    block_index].refid:
            return 0
        return 1  # 暂时不check

    def calculate_static_group_info(self):
        # [属性名称,属性类型,属性值] [['H', 1, 0], ['G', 1, 0]]
        dict_group_info = {}  # {groupid:{objectid set},...}
        for i in range(len(self.gameinfo.gameobject)):
            if "Root" == self.gameinfo.gameobject[
                    i].gameobject_name or "Player" == self.gameinfo.gameobject[
                        i].gameobject_name:
                continue
            objectid = self.gameinfo.gameobject[i].gameobject_id
            if len(self.gameinfo.gameobject[i].gameobject_attributes
                   ) > 1:  # 在组中
                dict_value = dict_group_info.get(
                    self.gameinfo.gameobject[i].gameobject_attributes[1][1])
                if None == dict_value:  # no key
                    dict_group_info[self.gameinfo.gameobject[i].
                                    gameobject_attributes[1][1]] = {objectid}
                else:
                    dict_value.add(objectid)
                    dict_group_info[self.gameinfo.gameobject[i].
                                    gameobject_attributes[1][1]] = dict_value
            else:
                pass

        #print(dict_group_info)
        return dict_group_info

    def get_noparam_block_count(self, gameobject_index, script_index):
        no_param_block_count = 0
        block_count = len(self.gameinfo.gameobject[gameobject_index].
                          scripts_sets[script_index].block_set)
        for i in range(block_count):
            if 1 != self.isparameterblock(
                    self.gameinfo.gameobject[gameobject_index].
                    scripts_sets[script_index].block_set[i].blocktype,
                    self.gameinfo.gameobject[gameobject_index].
                    scripts_sets[script_index].block_set[i].refid):
                no_param_block_count += 1
        return no_param_block_count

    def debug_print_game(self, game):
        print("+++++++++++++++++ game info base +++++++++++++++++")
        print("             game.gamename = ", game.gamename)
        print("           game.createtype = ", game.createtype)
        print("                game.grade = ", game.grade)
        print("game.variables_sets_global = ", game.variables_sets_global)
        print("    game.gameobject number = ", len(game.gameobject))

        print("        game.broadcast_net = ", game.broadcast_net)
        print("            game.clone_net = ", game.clone_net)
        print("        game.variables_net = ", game.variables_net)
        print("     game.others_event_net = ", game.others_event_net)

        print("     game.loop_index_number_cross_sprite_by_broadcast = ",
              game.loop_index_number_cross_sprite_by_broadcast)
        print("     game.loop_index_number_cross_sprite_by_variables = ",
              game.loop_index_number_cross_sprite_by_variables)

        print("----------------- game info base ----------------")
        print("")
        for i in range(len(game.gameobject)):
            self.debug_print_gameobject(game.gameobject[i])

    def debug_print_gameobject(self, gameobject):
        print("+++++++++++++++++ game object +++++++++++++++++")
        print("      gameobjec.gameobject_name = ", gameobject.gameobject_name)
        print("        gameobjec.gameobject_id = ", gameobject.gameobject_id)
        print("      gameobjec.gameobject_type = ", gameobject.gameobject_type)
        print("gameobjec.gameobject_attributes = ",
              gameobject.gameobject_attributes)
        print("            gameobjec.has_music = ", gameobject.has_music)
        print(" gameobjec.variables_sets_local = ",
              gameobject.variables_sets_local)
        print("          gameobjec.coordinatea = ", gameobject.coordinatea)
        print("gameobjec.loop_index_number_cross_script_by_broadcast = ",
              gameobject.loop_index_number_cross_script_by_broadcast)
        print("gameobjec.loop_index_number_cross_script_by_variables = ",
              gameobject.loop_index_number_cross_script_by_variables)
        print("  gameobjec.scripts_sets number = ",
              len(gameobject.scripts_sets))
        print("----------------- game object ----------------")
        print("")
        for i in range(len(gameobject.scripts_sets)):
            self.debug_print_script(gameobject.scripts_sets[i])

    def debug_print_script(self, script):
        print("    +++++++++++++++++ script +++++++++++++++++")
        print("             script.block_dict_seqid_index = ",
              script.block_dict_seqid_index)
        print("                           script.scriptid = ", script.scriptid)
        print("                   script.block_set number = ",
              len(script.block_set))
        print("                         script.has_trigge = ",
              script.has_trigger)
        print("               script.be_trigger_atworking = ",
              script.be_trigger_atworking)
        print("                   script.block_nest_depth = ",
              script.block_nest_depth)
        print("              script.paramblock_nest_depth = ",
              script.paramblock_nest_depth)
        print("         script.stateparamblock_nest_depth = ",
              script.stateparamblock_nest_depth)
        print("                       script.nest_useless = ",
              script.nest_useless)
        print("                       script.running_time = ",
              script.running_time)
        print("script.condition_index_number_ifelse = ",
              script.condition_index_number_ifelse)
        print("script.condition_index_number_if = ",
              script.condition_index_number_if)
        print("script.condition_index_nest_depth = ",
              script.condition_index_nest_depth)
        print("script.condition_index_number_no_statement = ",
              script.condition_index_number_no_statement)
        print("script.condition_index_number_param_imcompleted = ",
              script.condition_index_number_param_imcompleted)
        print("script.condition_index_number_param_variables_nochanged = ",
              script.condition_index_number_param_variables_nochanged)
        print("script.condition_index_number_true_forever = ",
              script.condition_index_number_true_forever)
        print("script.condition_index_number_false_forever = ",
              script.condition_index_number_false_forever)
        print("script.loop_index_number_totals = ",
              script.loop_index_number_totals)
        print("script.loop_index_nest_depth = 0 = ",
              script.loop_index_nest_depth)
        print("script.loop_index_endlessloop_nobreak = ",
              script.loop_index_endlessloop_nobreak)
        print("script.loop_index_endlessloop_nowait = ",
              script.loop_index_endlessloop_nowait)
        print("    ----------------- script ----------------")
        print("")
        for i in range(len(script.block_set)):
            self.debug_print_block(script.block_set[i])

    def debug_print_block(self, block):
        print("        +++++++++++++++++ block +++++++++++++++++")
        # 1. block 自有属性
        # 1.1 block 自有基本信息
        print("                                block.sequenceid = ",
              block.sequenceid)  # 在script中的序号(script中的次序),base = 1
        print("                                     block.refid = ",
              block.refid)  # 参考序号(每个block类型的编号)
        print("                                 block.blocktype = ",
              block.blocktype)  # 类型
        print("                              block.blocksubtype = ",
              block.blocksubtype)  # 子类型
        print("                                 block.blockname = ",
              block.blockname)  # 名称
        print("                                block.coordinate = ",
              block.coordinate)  # 坐标
        print("                               block.controltype = ",
              block.controltype)  # 控件类型
        # 2 自有参数属性
        # 2.1 参数基本信息及子关系
        print("                        block.is_parameter_block = ",
              block.is_parameter_block)  # 是否是参数 block
        print("                      block.parameter_nest_depth = ",
              block.parameter_nest_depth)  # 参数嵌入层级s"
        print("                      block.parameter_count_need = ",
              block.parameter_count_need)  # 参数数目(本层,不考虑嵌套参数影响)
        print("                           block.parameter_count = ",
              block.parameter_count)  # 参数数目(本层,不考虑嵌套参数影响)
        print("                         block.parameter_argtype = ",
              block.parameter_argtype)  # 参数可以使用的类型
        print(
            "                            block.parameter_info = ",
            block.parameter_info
        )  # (参数序号/从左到右次序/,参数类型1(1-8,条件表达式不标),参数值(缺省值),可有参数类型2(1-25),实际参数类型2(1-25),参数块编号,参数参考序号,是否合法)
        print("                           block.parameter_info0 = ",
              block.parameter_info0)
        # 2.2 参数块父关系
        print("         block.parameter_parent_block_sequenceid = ",
              block.parameter_parent_block_sequenceid)  # 只有参数块
        print("        block.parameter_ancestor_block_seqenceid = ",
              block.parameter_ancestor_block_seqenceid)  # 非参数块祖宗
        # 2.3 参数块兄弟关系
        print("                    block.parameter_brother_left = ",
              block.parameter_brother_left)  # 上一个兄弟
        print("                   block.parameter_brother_right = ",
              block.parameter_brother_right)  # 下一个兄弟

        # 3. 兄弟父子关系
        # 3.1 兄弟关系
        print("                                block.brother_up = ",
              block.brother_up)  # 上一个兄弟
        print("                              block.brother_down = ",
              block.brother_down)  # 下一个兄弟
        # 3.2 父关系
        print("                              block.indent_depth = ",
              block.indent_depth)  # 缩进层级,2级以后才有父
        print("                   block.father_block_seqeneceid = ",
              block.father_block_seqeneceid)  # 所属父 block 序号
        # 3.3 子关系
        print("                              block.is_container = ",
              block.is_container)  # 是否container,容器才有子关系
        print("                          block.childblock_list1 = ",
              block.childblock_list1)  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目
        print("                          block.childblock_list2 = ", block.
              childblock_list2)  # 子 block 列表(不考虑孙子辈以后),len可以计算子块数目,目前只应用到else

        # 4. 执行时间
        print("                                   block.is_asyn = ",
              block.is_asyn)  # 是否异步执行
        print("                                 block.time_used = ",
              block.time_used)  # 执行用时
        print("                     block.time_used_accumulated = ",
              block.time_used_accumulated)  # 累计执行用时
        print("                      block.time_ralatedvariable = ",
              block.time_ralatedvariable)  # 涉及的变量,这些变量决定了用时

        # 5. check entity
        print("                            block.can_be_excuted = ",
              block.can_be_excuted)  # 是否会被执行
        print("                                block.has_child1 = ",
              block.has_child1)  # 如果是container
        print("                                block.has_child2 = ",
              block.has_child2)  # 如果是container,2 for else
        print("                 block.condition_value_iscontant = ",
              block.condition_value_iscontant)  # 条件值是常量

        print("        ----------------- block -----------------")

        return

    def debug_print_block_dist(self, blockdist):
        print("------ block distribution ------")
        for key in blockdist.dict_block_dist:
            print(key, blockdist.dict_block_dist[key],
                  sb.DictBlockAttribute[key][2])
        print("------ block type distribution ------")
        for key in blockdist.dict_block_type_dist:
            print(key, blockdist.dict_block_type_dist[key])

    def debug_print_ctindex(self, ctindex):
        print("# 1. sprite(3)")
        print("# 1.1. sprite指标: (+)sprite总数 = ", ctindex.sprite_index_totals)
        print("# 1.2. sprite指标: (+)sprite有效数目 = ", ctindex.sprite_index_useful)
        print("# 1.3. sprite指标: (-)sprite无效数目 = ",
              ctindex.sprite_index_useless)

        print("# 2. script(18)")
        print("# 2.1. script指标: (+)script总数 = ", ctindex.script_index_tatals)
        print("# 2.2. script指标: (+)script有触点数目 = ",
              ctindex.script_index_has_detonator)
        print("# 2.3. script指标: (-)script无触点数目detonator = ",
              ctindex.script_index_hasnot_detonator)

        print("# 2.4. script指标: (+)script工程运行时可触发数目 = ",
              ctindex.script_index_trigger_atworking)
        print("# 2.5. script指标: (-)script实际不可触发数目 = ",
              ctindex.script_index_trigger_cannot_be_fired)

        print("# 2.6. script指标: (+)script中最大block数目 = ",
              ctindex.script_index_blocknum_max)
        print("# 2.7. script指标: (+)script中最小block数目 = ",
              ctindex.script_index_blocknum_min)
        print("# 2.8. script指标: (+)script中平均block数目 = ",
              ctindex.script_index_blocknum_avg)

        print("# 2.9. script指标: (+-)script中语句块嵌套最大深度 = ",
              ctindex.script_index_statementblock_nest_depth_max)
        print("# 2.10. script指标: (+-)script中语句块嵌套平均深度 = ",
              ctindex.script_index_statementblock_nest_depth_avg)
        print("# 2.11. script指标: (+-)script中参数块嵌套最大深度 = ",
              ctindex.script_index_paramblock_nest_depth_max)
        print("# 2.12. script指标: (+-)script中参数块嵌套平均深度 = ",
              ctindex.script_index_paramblock_nest_depth_avg)
        print("# 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度 = ",
              ctindex.script_index_stateparamblock_nest_depth_max)
        print("# 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度 = ",
              ctindex.script_index_stateparamblock_nest_depth_avg)
        print("# 2.15. script指标: (-)script中无效的嵌套 = ",
              ctindex.script_index_nest_useless)

        print("# 2.16. script指标: (+)script最大运行时间 = ",
              ctindex.script_index_runtime_max)
        print("# 2.17. script指标: (+)script最小运行时间 = ",
              ctindex.script_index_runtime_min)
        print("# 2.18. script指标: (+)script平均运行时间 = ",
              ctindex.script_index_runtime_avg)

        print("# 3. block(2)")
        print("# 3.1. block数目: (+)block总数 = ", ctindex.block_index_totals)
        print("# 3.2. block数目: (-)block不能被执行的总数 = ",
              ctindex.block_index_nowork)

        print("# 4. trigger(4)")
        print("# 4.1. trigger: (+)工程运行时触发的script数目 = ",
              ctindex.trigger_index_trigger_script_number_atworking)
        print("# 4.2. trigger: (+)同时触发的script数目 = ",
              ctindex.trigger_index_trigger_script_number_meanwhile)
        print("# 4.3. trigger: (+)并发执行的最大script数目 = ",
              ctindex.trigger_index_script_running_number_meanwhile)
        print("# 4.4. trigger: (+)并发执行的script最大重叠时间 = ",
              ctindex.trigger_index_script_running_overlap_maxtime)

        print("# 5. condition(9)")
        print("# 5.1. contain条件: (+)ifelse数目 = ",
              ctindex.condition_index_number_ifelse)
        print("# 5.2. contain条件: (+)if数目 = ",
              ctindex.condition_index_number_if)
        print("# 5.3. contain条件: (+-)条件嵌套最大深度(跳过loop) = ",
              ctindex.condition_index_nest_depth_max)
        print("# 5.4. contain条件: (+-)条件平均嵌套深度(跳过loop) = ",
              ctindex.condition_index_nest_depth_avg)

        print("# 5.5. contain条件: (-)if,if else下面没有block的数目 = ",
              ctindex.condition_index_number_no_statement)
        print("# 5.6. contain条件: (-)if条件表达式及其嵌套缺参数数目(基于嵌套顶层) = ",
              ctindex.condition_index_number_param_imcompleted)
        print("# 5.7. contain条件: (-)条件表达式中的变量外部不变数目(基于嵌套顶层) = ",
              ctindex.condition_index_number_param_variables_nochanged)
        print("# 5.8. contain条件: (-)条件永假数目(基于嵌套顶层) = ",
              ctindex.condition_index_number_true_forever)
        print("# 5.9. contain条件: (-)条件永真数目(基于嵌套顶层) = ",
              ctindex.condition_index_number_false_forever)

        print("# 6. loop(9)")
        print("# 6.1. contain循环: (+)循环数目 = ", ctindex.loop_index_number_totals)
        print("# 6.2. contain循环: (+-)循环嵌套最大深度 = ",
              ctindex.loop_index_nest_depth_max)
        print("# 6.3. contain循环: (+-)循环嵌套平均深度 = ",
              ctindex.loop_index_nest_depth_avg)

        print("# 6.4. contain循环: (+)基于消息(广播)的跨sprite大循环数目 = ",
              ctindex.loop_index_number_cross_sprite_by_broadcast)
        print("# 6.5. contain循环: (+)基于消息(变量)的跨sprite大循环数目 = ",
              ctindex.loop_index_number_cross_sprite_by_variables)
        print("# 6.6. contain循环: (+)基于消息(广播)的跨script大循环数目 = ",
              ctindex.loop_index_number_cross_script_by_broadcast)
        print("# 6.7. contain循环: (+)基于消息(变量)的跨script大循环数目 = ",
              ctindex.loop_index_number_cross_script_by_variables)

        print("# 6.8. contain循环: (*)死循环数目(不能跳出,或者break条件永不为真) = ",
              ctindex.loop_index_endlessloop_nobreak)
        print("# 6.9. contain循环: (-)死循环数目(循环体中没有阻塞) = ",
              ctindex.loop_index_endlessloop_nowait)

        print("# 7. sequenceblock(3)")
        print("# 7.1. 顺序块: (+)一级顺序块最大数目 = ",
              ctindex.sequenceblock_index_number_top_max)
        print("# 7.2. 顺序块: (+)if中的一级顺序块最大数目 = ",
              ctindex.sequenceblock_index_number_if_max)
        print("# 7.3. 顺序块: (+)loop中的一级顺序块最大数目 = ",
              ctindex.sequenceblock_index_number_loop_max)

        print("# 8. clone(5)")
        print("# 8.1. 克隆: (+)克隆点数目 = ", ctindex.clone_index_number_blocks)
        print("# 8.2. 克隆: (+)克隆sprite数量 = ",
              ctindex.clone_index_number_sprites)
        print("# 8.3. 克隆: (+)克隆sprite类型数量 = ",
              ctindex.clone_index_number_sprites_type)
        print("# 8.4. 克隆: (+)克隆sprite触发script数目 = ",
              ctindex.clone_index_number_trigger_script)
        print("# 8.5. 克隆: (-)是否存在递归克隆 = ",
              ctindex.clone_index_recursion_or_unlimited)

        print("# 9. wait(2)")
        print("# 9.1. wait数目: (+)wait数目 = ", ctindex.wait_index_number)
        print("# 9.2. wait数目: (+-)wait最大等待时间 = ",
              ctindex.wait_index_max_waittime)

        print("# 10. broadcast(6)")
        print("# 10.1. broadcast: (+)广播消息ID数目 = ",
              ctindex.broadcast_index_number_messageid)
        print("# 10.2. broadcast: (+)广播点数目 = ",
              ctindex.broadcast_index_number_sendpointer)
        print("# 10.3. broadcast: (-)广播点(不可执行到的)数目 = ",
              ctindex.broadcast_index_number_sendpointer_noreach)
        print("# 10.4. broadcast: (+)广播接收点数目 = ",
              ctindex.broadcast_index_number_recvpointer)
        print("# 10.5. broadcast: (-)广播接收点(不可执行到的)数目 = ",
              ctindex.broadcast_index_number_recvpointer_noreach)
        print("# 10.6. broadcast: (-)广播形成无效死循环(循环体中没有阻塞)数目 = ",
              ctindex.broadcast_index_number_rise_endless_loop)

        print("# 11. logicalexpr(8)")
        print("# 11.1. 逻辑表达式: (+)逻辑表达式数目 = ",
              ctindex.logicalexpr_index_number_totals)
        print("# 11.2. 逻辑表达式: (+)逻辑表达式种类数目 = ",
              ctindex.logicalexpr_index_number_type)
        print("# 11.3. 逻辑表达式: (+-)逻辑表达式参数嵌套最大深度 = ",
              ctindex.logicalexpr_index_number_nest_depth_max)
        print("# 11.4. 逻辑表达式: (+-)逻辑表达式参数嵌套平均深度 = ",
              ctindex.logicalexpr_index_number_nest_depth_avg)
        print("# 11.5. 逻辑表达式: (-)逻辑表达式永真数目(向上传递) = ",
              ctindex.logicalexpr_index_number_true_forever)
        print("# 11.6. 逻辑表达式: (-)逻辑表达式永假数目(向上传递) = ",
              ctindex.logicalexpr_index_number_false_forever)
        print("# 11.7. 逻辑表达式: (-)逻辑表达式缺参数数目(向上传递) = ",
              ctindex.logicalexpr_index_number_param_imcompleted)
        print("# 11.8. 逻辑表达式: (-)逻辑表达式变量外部不变数目(向上传递) = ",
              ctindex.logicalexpr_index_number_variables_nochanged)

        print("# 12. globalvar(11)")
        print("# 12.1. 全局变量: (+)使用数目 = ",
              ctindex.globalvar_index_number_totals)
        print("# 12.2. 全局变量: (+)更改数目 = ",
              ctindex.globalvar_index_number_modified)
        print("# 12.3. 全局变量: (+)跨sprite使用数目 = ",
              ctindex.globalvar_index_number_cross_sprite)
        print("# 12.4. 全局变量: (+)触发script数目 = ",
              ctindex.globalvar_index_number_trigger_script)
        print("# 12.5. 全局变量: (+)变量控制的循环数目 = ",
              ctindex.globalvar_index_number_control_loop)
        print("# 12.6. 全局变量: (+)变量控制的条件数目 = ",
              ctindex.globalvar_index_number_control_condition)

        print("# 12.7. 全局变量: (+)变量修改点数目 = ",
              ctindex.globalvar_index_number_changed_pointer)
        print("# 12.8. 全局变量: (-)变量修改点(不可执行到的)数目 = ",
              ctindex.globalvar_index_number_changed_pointer_noreach)
        print("# 12.9. 全局变量: (+)变量检测点数目(script头) = ",
              ctindex.globalvar_index_number_check_pointer)
        print("# 12.10. 全局变量: (-)变量检测点(不可执行到的)数目(script头) = ",
              ctindex.globalvar_index_number_check_pointer_noreach)
        print("# 12.11. 全局变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目 = ",
              ctindex.globalvar_index_number_rise_endless_loop)

        print("# 13. localvar(10)")
        print("# 13.1. 局部变量: (+)使用数目 = ", ctindex.localvar_index_number_totals)
        print("# 13.2. 局部变量: (+)更改数目 = ",
              ctindex.localvar_index_number_modified)
        print("# 13.3. 局部变量: (+)触发script数目 = ",
              ctindex.localvar_index_number_trigger_script)
        print("# 13.4. 局部变量: (+)变量控制的循环数目 = ",
              ctindex.localvar_index_number_control_loop)
        print("# 13.5. 局部变量: (+)变量控制的条件数目 = ",
              ctindex.localvar_index_number_control_condition)

        print("# 13.6. 局部变量: (+)变量修改点数目 = ",
              ctindex.localvar_index_number_changed_pointer)
        print("# 13.7. 局部变量: (-)变量修改点(不可执行到的)数目 = ",
              ctindex.localvar_index_number_changed_pointer_noreach)
        print("# 13.8. 局部变量: (+)变量检测点数目(script头) = ",
              ctindex.localvar_index_number_check_pointer)
        print("# 13.9. 局部变量: (-)变量检测点(不可执行到的)数目(script头) = ",
              ctindex.localvar_index_number_check_pointer_noreach)
        print("# 13.10. 局部变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目 = ",
              ctindex.localvar_index_number_rise_endless_loop)

        print("# 14. interaction(11)")
        print("# 14.1. 交互: (+)键盘:处理sprite数目 = ",
              ctindex.interaction_index_number_keyboard_sprite)
        print("# 14.2. 交互: (+)键盘:处理点数目 = ",
              ctindex.interaction_index_number_keyboard_checkpointer)
        print("# 14.3. 交互: (-)键盘:无效处理点数目 = ",
              ctindex.interaction_index_number_keyboard_checkpointer_useless)

        print("# 14.4. 交互: (+)手柄:处理sprite数目 = ",
              ctindex.interaction_index_number_joystick_sprite)
        print("# 14.5. 交互: (+)手柄:处理点数目 = ",
              ctindex.interaction_index_number_joystick_checkpointer)
        print("# 14.6. 交互: (-)手柄:无效处理点数目 = ",
              ctindex.interaction_index_number_joystick_checkpointer_useless)

        print("# 14.7. 交互: (+)鼠标:处理sprite数目 = ",
              ctindex.interaction_index_number_mouse_sprite)
        print("# 14.8. 交互: (+)鼠标:处理点数目 = ",
              ctindex.interaction_index_number_mouse_checkpointer)
        print("# 14.9. 交互: (-)鼠标:无效处理点数目 = ",
              ctindex.interaction_index_number_mouse_checkpointer_useless)

        print("# 14.10. 交互: (+)用户输入点数目 = ",
              ctindex.interaction_index_number_user_inputpointer)
        print("# 14.11. 交互: (+)用户输入提示频率 = ",
              ctindex.interaction_index_number_user_inputprompt)

        print("# 15. phycharacteristics(4)")
        print("# 15.1. 物理特性: (+)开启物理引擎的sprite数目 = ",
              ctindex.phycharacteristics_index_number_sripte_open_engine)
        print(
            "# 15.2. 物理特性: (-)开启物理特性动作能否执行到 = ",
            ctindex.phycharacteristics_index_number_sripte_open_engine_useless)
        print("# 15.3. 物理特性: (+)物理引擎窗口内受制block数目 = ",
              ctindex.phycharacteristics_index_number_blocks_in_engine_windows)
        print(
            "# 15.4. 物理特性: (-)物理引擎窗口外受制block数目 = ",
            ctindex.phycharacteristics_index_number_blocks_out_engine_wondows)

        print("# 16. phyaction(12)")
        print("# 16.1. 物理行为: (+)移动的sprite数目 = ",
              ctindex.phyaction_index_moving_sprite_type_number)
        print("# 16.2. 物理行为: (+)移动的sprite指令块数目 = ",
              ctindex.phyaction_index_moving_sprite_blocks)
        print("# 16.3. 物理行为: (-)移动的sprite指令块数目(不能执行到) = ",
              ctindex.phyaction_index_moving_sprite_blocks_useless)
        print("# 16.4. 物理行为: (+)移动的sprite次数 = ",
              ctindex.phyaction_index_moving_sprite_times)

        print("# 16.5. 旋转行为: (+)移动的sprite数目 = ",
              ctindex.phyaction_index_rotate_sprite_type_number)
        print("# 16.6. 旋转行为: (+)移动的sprite指令块数目 = ",
              ctindex.phyaction_index_rotate_sprite_blocks)
        print("# 16.7. 旋转行为: (-)移动的sprite指令块数目(不能执行到) = ",
              ctindex.phyaction_index_rotate_sprite_blocks_useless)
        print("# 16.8. 物理行为: (+)旋转的sprite次数 = ",
              ctindex.phyaction_index_rotate_sprite_times)

        print("# 16.9. 物理行为: (+)播放动画效果的sprite数目 = ",
              ctindex.phyaction_index_play_animation_sprite_type_number)
        print("# 16.10. 物理行为: (+)播放动画效果的sprite指令块数目 = ",
              ctindex.phyaction_index_play_animation_sprite_blocks)
        print("# 16.11. 物理行为: (-)播放动画效果的sprite指令块数目(不能执行到) = ",
              ctindex.phyaction_index_play_animation_sprite_blocks_useless)
        print("# 16.12. 物理行为: (+)播放动画效果的sprite次数 = ",
              ctindex.phyaction_index_play_animation_sprite_times)

        print("# 17. objsetting(22)")
        print("# 17.1. 物体设置: (+)删除sprite数目 = ",
              ctindex.objsetting_index_number_del_sprite)
        print("# 17.2. 物体设置: (+)删除sprite指令块数目 = ",
              ctindex.objsetting_index_number_del_sprite_blocks)
        print("# 17.3. 物体设置: (-)删除sprite指令块数目(不能执行到) = ",
              ctindex.objsetting_index_number_del_sprite_blocks_noreach)

        print("# 17.4. 物体设置: (+)显示sprite数目 = ",
              ctindex.objsetting_index_number_show_sprite)
        print("# 17.5. 物体设置: (+)显示sprite指令块数目 = ",
              ctindex.objsetting_index_number_show_sprite_blocks)
        print("# 17.6. 物体设置: (-)显示sprite指令块数目(不能执行到) = ",
              ctindex.objsetting_index_number_show_sprite_blocks_noreach)

        print("# 17.7. 物体设置: (+)影藏sprite数目 = ",
              ctindex.objsetting_index_number_hide_sprite)
        print("# 17.8. 物体设置: (+)影藏sprite指令块数目 = ",
              ctindex.objsetting_index_number_hide_sprite_blocks)
        print("# 17.9. 物体设置: (-)影藏sprite指令块数目(不能执行到) = ",
              ctindex.objsetting_index_number_hide_sprite_blocks_noreach)

        print("# 17.10. 物体设置: (+)父子关系团数目 = ",
              ctindex.objsetting_index_number_group)
        print("# 17.11. 物体设置: (+)父子团最大sprite数目 = ",
              ctindex.objsetting_index_number_group_max_unit)
        print("# 17.12. 物体设置: (+)父子团平均sprite数目 = ",
              ctindex.objsetting_index_number_group_avg_unit)

        print("# 17.13. 物体设置: (+)父子团移动数目 = ",
              ctindex.objsetting_index_number_group_moving)
        print("# 17.14. 物体设置: (-)父子团不移动数目 = ",
              ctindex.objsetting_index_number_group_not_moving)

        print("# 17.15. 物体设置: (+)父子团旋转数目 = ",
              ctindex.objsetting_index_number_group_rotate)
        print("# 17.16. 物体设置: (-)父子团不旋转数目 = ",
              ctindex.objsetting_index_number_group_not_rotate)

        print("# 17.17. 物体设置: (+)父子团播放动作数目 = ",
              ctindex.objsetting_index_number_group_play_animation)
        print("# 17.18. 物体设置: (-)父子团不播放动作数目 = ",
              ctindex.objsetting_index_number_group_not_play_animation)

        print("# 17.19. 物体设置: (+)父子团子sprite显示数目 = ",
              ctindex.objsetting_index_number_group_show)
        print("# 17.20. 物体设置: (+)父子团子sprite影藏数目 = ",
              ctindex.objsetting_index_number_group_hide)

        print("# 17.21. 物体设置: (+)父子团子sprite动态组团数目 = ",
              ctindex.objsetting_index_number_group_packaged_dynamically)
        print("# 17.22. 物体设置: (+)父子团子sprite动态拆分数目 = ",
              ctindex.objsetting_index_number_group_unpackaged_dynamically)

        print("# 18. music(5)")
        print("# 18.1. 音乐: (+)音乐播放数目 = ",
              ctindex.music_index_number_play_pointer)
        print("# 18.2. 音乐: (-)不能被播放数目 = ",
              ctindex.music_index_number_play_pointer_noreach)
        print("# 18.3. 音乐: (+)音乐播放曲目数目 = ",
              ctindex.music_index_number_play_songs)
        print("# 18.4. 音乐: (-)缺少参数数目 = ",
              ctindex.music_index_number_play_pointer_param_incompleted)
        print("# 18.5. 音乐: (+)主动停止数目 = ",
              ctindex.music_index_number_stop_pointer)

if __name__ == "__main__":
    c = Parser()
    s1 = get_course_list("tb_obj_1474_10004")
    print(c.ParseGame(s1, "63_318_2"))
    # 返回数据格式
    # {0}*||{1}&||{2}&||{3}&||{4}&||{5}&||{6}&||{7}&||{8}^^{9}
