# -*- coding: utf-8 -*-
"""
  create-x source code grading and score.
  statistics statement for Computing Think.
  
  Xi'an Feidie VR technology co. LTD
  2019/12/18
"""

import ScoreBase as sb

SUBITEM_RATING_HIGH = 0
SUBITEM_RATING_MIDDLE = 1
SUBITEM_RATING_LOW = 2
SCORE_FULL_MARK = 1
SCORE_NO_FULL_MARK = 0

MAX_ERROR_REPROT = 4
MAX_GRASP_REPORT = 4
MAX_INFREQUENT_REPORT = 4


class EvaluateingResult:
    def __init__(self):
        # I.基本数据
        # 主观总分按照绝对分值计算
        self.subjectiveTotalScore = 20  # 主观总分,与客观总分相加等于100
        self.subjectiveScore = 0.0  # 主观总分分数, 各个分项得分相加
        self.subjectiveScoreItem = []  # 主观分数, 分项: [分项总分,分项得分]

        # 客观部分分项按照百分制计算
        self.objectiveTotalScore = 80  # 客观总分,与主观总分相加等于100
        self.objectiveScore = [0.0, 0.0]  # 客观总分分数, 分项:[分数(百分制),客观占比调整后分数]
        self.objectiveScoreItem = []  # 客观分项分数, 分项:[分项分数(百分制),分项占比]
        self.objectiveWarning = ""  # 客观评分语法检查结果
        self.objectiveBlockDist = ""  # 客观评分语句块分布

        # II. 主观评述
        # 主观评述产生规则定义
        # TODO 目前不存在主观评价
        self.subject_grading_rule = [[
            "完整性", 0.0, [0.85, 1.0], [0.7, 0.85], [0.0, 0.7],
            SUBITEM_RATING_MIDDLE, SCORE_NO_FULL_MARK
        ],
                                     [
                                         "美观性", 0.0, [0.85, 1.0], [0.7, 0.85],
                                         [0.0, 0.7], SUBITEM_RATING_MIDDLE,
                                         SCORE_NO_FULL_MARK
                                     ],
                                     [
                                         "创意性", 0.0, [0.85, 1.0], [0.7, 0.85],
                                         [0.0, 0.7], SUBITEM_RATING_MIDDLE,
                                         SCORE_NO_FULL_MARK
                                     ],
                                     [
                                         "知识性", 0.0, [0.85, 1.0], [0.7, 0.85],
                                         [0.0, 0.7], SUBITEM_RATING_MIDDLE,
                                         SCORE_NO_FULL_MARK
                                     ],
                                     [
                                         "趣味性", 0.0, [0.85, 1.0], [0.7, 0.85],
                                         [0.0, 0.7], SUBITEM_RATING_MIDDLE,
                                         SCORE_NO_FULL_MARK
                                     ]]
        # 主观评述模板
        self.subject_grading_statement = {
            "1001":
            "作品总体主观表现优秀,在<HIGH-ITEMS>表现优异，<FULLMARK-ITEMS>得到了满分。",
            "1000":
            "作品总体主观表现优秀,在<HIGH-ITEMS>表现优异。",
            "0101":
            "作品总体主观表现尚可,在<MIDDLE-ITEMS>都没有特别优异或者较差的表现。",
            "0100":
            "作品总体主观表现尚可,在<MIDDLE-ITEMS>都没有特别优异或者较差的表现。",
            "0011":
            "作品总体主观表现较差,<LOW-ITEMS-SCORE>。",
            "0010":
            "作品总体主观表现较差,<LOW-ITEMS-SCORE>。",
            "0111":
            "作品总体主观表现尚可,在<MIDDLE-ITEMS>没有特别优异或者较差的表现，<LOW-ITEMS-SCORE>。",
            "0110":
            "作品总体主观表现尚可,在<MIDDLE-ITEMS>没有特别优异或者较差的表现，<LOW-ITEMS-SCORE>。",
            "1011":
            "作品总体主观表现尚可,在<HIGH-ITEMS>表现优异，<FULLMARK-ITEMS>得到了满分，但是<LOW-ITEMS-SCORE>。",
            "1010":
            "作品总体主观表现尚可,在<HIGH-ITEMS>表现良好，但是<LOW-ITEMS-SCORE>。",
            "1101":
            "作品总体主观表现优良,在<HIGH-ITEMS>表现优异，<FULLMARK-ITEMS>得到了满分，但是<MIDDLE-ITEMS>表现一般。",
            "1100":
            "作品总体主观表现优良,在<HIGH-ITEMS>表现优异，但是<MIDDLE-ITEMS>表现一般。",
            "1111":
            "作品总体主观表现优良,在<HIGH-ITEMS>表现优秀，<FULLMARK-ITEMS>得到了满分，<MIDDLE-ITEMS>表现尚可，<LOW-ITEMS>方面表现欠佳，<LOW-ITEMS-SCORE>。",
            "1110":
            "作品总体主观表现优良,在<HIGH-ITEMS>表现优秀，<MIDDLE-ITEMS>表现尚可，<LOW-ITEMS>方面表现欠佳，<LOW-ITEMS-SCORE>。"
        }
        # 主观评述模板语素
        # <HIGH-ITEMS>
        self.subject_morpheme_high_items = ""
        # <MIDDLE-ITEMS>
        self.subject_morpheme_middle_items = ""
        # <LOW-ITEMS>
        self.subject_morpheme_low_items = ""
        # <LOW-ITEMS-SCORE>
        self.subject_morpheme_low_items_score = ""
        # <FULLMARK-ITEMS>
        self.subject_morpheme_fullmard_items = ""

        # III. 客观评述
        # 客观评述产生规则定义
        self.object_grading_rule = [
            [
                "抽象和问题分解", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE,
                0.0
            ],
            ["并发思想", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["逻辑思维", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["同步思想", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["流程控制", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["用户交互", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["数据表示", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0],
            ["视听效果", [80, 100], [60, 80], [0, 60], SUBITEM_RATING_MIDDLE, 0.0]
        ]
        # 客观评述模板
        self.object_grading_statement = {
            "10000":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。",
            "10001":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。",
            "10010":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能，但是有一些细小错误，如: <GRM-EW-STD>。",
            "10011":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能，但是有一些细小错误，如: <GRM-EW-STD>。",
            "01000":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。",
            "01001":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。",
            "01010":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能，但是有一些细小错误，如: <GRM-EW-STD>。",
            "01011":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能，但是有一些细小错误，如: <GRM-EW-STD>。",
            "00100":
            "VR编程能力总结：<L-ITMS-STD>等方面表现欠佳。",
            "00101":
            "VR编程能力总结：<L-ITMS-STD>等方面表现欠佳，体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。",
            "00110":
            "VR编程能力总结：<L-ITMS-STD>等方面表现欠佳，编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "00111":
            "VR编程能力总结：<L-ITMS-STD>等方面表现欠佳，体现<INF-GRM-STD>等相关编程能力的语法元素使用较少,同时编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "01100":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。",
            "01101":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳，体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。",
            "01110":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "01111":
            "VR编程能力总结：<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。另外,编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "10100":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。",
            "10101":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。",
            "10110":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "10111":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。另外，编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "11000":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。",
            "11001":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。",
            "11010":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "11011":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。另外，编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "11100":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。",
            "11101":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。",
            "11110":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳。编程中的语法错误比较多，如: <GRM-EW-STD>。",
            "11111":
            "VR编程能力总结：<H-ITMS-STD>等方面表现突出，熟练掌握了<H-GRSP-ITMS-STD>等方面编程技能。<M-ITMS-STD>等方面表现尚可，基本掌握了<M-GRSP-ITMS-STD>等方面编程技能。<L-ITMS-STD>等方面表现欠佳, 体现<INF-GRM-STD>等相关编程能力的语法元素使用较少。另外，编程中的语法错误比较多，如: <GRM-EW-STD>。"
        }
        # 客观评述模板语素
        # <H-ITMS-STD>
        self.object_morpheme_high_items = ""
        # <H-GRSP-ITMS-STD>
        self.object_morpheme_high_grasp_items = ""
        # <M-ITMS-STD>
        self.object_morpheme_middle_items = ""
        # <M-GRSP-ITMS-STD>
        self.object_morpheme_middle_grasp_items = ""
        # <L-ITMS-STD>
        self.object_morpheme_low_items = ""
        # <GRM-EW-STD>
        self.object_morpheme_error_warning = ""
        # <INF-GRM-STD>
        self.object_morpheme_infrequent_items = ""

        # 客观评述错误统计
        self.object_errorwarning_items = [[1, 201, 0, "程序块不能被执行"],
                                          [2, 302, 0, "条件语句块没有参数"],
                                          [3, 402, 0, "逻辑表达式缺参数"],
                                          [4, 502, 0, "接收没有发送的广播消息"],
                                          [5, 801, 0, "没有选择音乐"],
                                          [6, 904, 0, "没有选择变量"],
                                          [7, 905, 0, "没有选择UI资源"],
                                          [8, 906, 0, "没有选择动作"],
                                          [9, 152, 0, "list变量非法使用"],
                                          [10, 153, 0, "非list变量非法赋值"],
                                          [11, 154, 0, "非list变量非法取值"],
                                          [12, 155, 0, "list变量下标越界"],
                                          [13, 156, 0, "list变量下标非法"],
                                          [14, 157, 0, "list非法嵌入"],
                                          [15, 501, 0, "发送无效的广播消息"],
                                          [16, 702, 0, "循环块中缺少语句块"],
                                          [17, 303, 0, "条件块中缺少语句块"],
                                          [18, 901, 0, "定义的变量没有被使用"],
                                          [19, 902, 0, "定义的变量没有被修改"],
                                          [20, 903, 0, "定义的变量有修改无使用"],
                                          [21, 951, 0, "没有开启物理引擎"],
                                          [22, 151, 0, "List变量不能为空"],
                                          [23, 101, 0, "无效的资源"],
                                          [24, 202, 0, "语句块嵌套太深"],
                                          [25, 203, 0, "参数块嵌套太深"],
                                          [26, 204, 0, "语句/参数块嵌套太深"],
                                          [27, 205, 0, "无效的嵌套"],
                                          [28, 301, 0, "条件语句块嵌套太深"],
                                          [29, 401, 0, "逻辑表达式参数嵌套太深"],
                                          [30, 701, 0, "循环语句块嵌套太深"],
                                          [31, 601, 0, "等待时间太长"]]

        # 客观评述掌握程度汇总
        self.object_grasp_level_items = [
            [
                "用户交互",
                {
                    sb.BLKREFID_TRG_WHENMOUSEMOVING,
                    sb.BLKREFID_TRG_WHENMOUSELEFTKEYACTION,
                    sb.BLKREFID_TRG_WHENKEYBOARDACTION,
                    sb.BLKREFID_TRG_WHENPICOHANDLECURSOR,
                    sb.BLKREFID_TRG_WHENPICOHANDLEACTION,
                    sb.BLKREFID_TRG_WHENSELFBEENCLICK,
                    sb.BLKREFID_CND_ADSORPTION, sb.BLKREFID_CND_CAPTURE,
                    sb.BLKREFID_CND_POCIKEYDOWNRELEASE
                },
                0,  # 累计数目
                {"用户交互"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "循环的使用",
                {
                    sb.BLKREFID_LF_LOOPUNLIMITED, sb.BLKREFID_LF_LOOPNUMBER,
                    sb.BLKREFID_LF_LOOPSTOP
                },
                0,  # 累计数目
                {"逻辑思维", "流程控制"},  # 体现思想
                {701, 702},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "条件分支的使用",
                {
                    sb.BLKREFID_TRG_WHENCONDITION, sb.BLKREFID_LF_IF,
                    sb.BLKREFID_LF_IFELSE
                },
                0,  # 累计数目
                {"逻辑思维", "流程控制"},  # 体现思想
                {301, 302, 303},  #  错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "同步等待的使用",
                {sb.BLKREFID_LF_WAITNUMBERSECONDS},
                0,  # 累计数目
                {"同步思想"},  # 体现思想
                {601},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体移动的控制",
                {
                    sb.BLKREFID_OA_MOVINGRXYZINTIMEBYCOORDINATE,
                    sb.BLKREFID_OA_MOVINGRXYZBYCOORDINATE,
                    sb.BLKREFID_OA_MOVINGAXYZINTIMEBYCOORDINATE
                },
                0,  # 累计数目
                {"视听效果"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体旋转的控制",
                {
                    sb.BLKREFID_OA_ROTATERXYZINTIMEBYCOORDINATE,
                    sb.BLKREFID_OA_ROTATERXYZBYCOORDINATE,
                    sb.BLKREFID_OA_ROTATEAXYZINTIMEBYCOORDINATE
                },
                0,  # 累计数目
                {"视听效果"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体缩放的控制",
                {sb.BLKREFID_OA_RESIZEPERSENT},
                0,  # 累计数目
                {"视听效果"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体动作的控制",
                {
                    sb.BLKREFID_OA_PLAYRESOURCEACTION,
                    sb.BLKREFID_OA_STOPRESOURCEACTION
                },
                0,  # 累计数目
                {"视听效果"},  # 体现思想
                {906},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "信息交互",
                {
                    sb.BLKREFID_OA_DISPLAYTEXTONTOP,
                    sb.BLKREFID_OA_UNDISPLAYTEXTONTOP,
                    sb.BLKREFID_OA_DISPLAYTEXTINUIRESOURCE,
                    sb.BLKREFID_DC_TEXTOFRESOUREUI, sb.BLKREFID_VAR_LOG
                },
                0,  # 累计数目
                {"用户交互"},  # 体现思想
                {905},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体显示控制",
                {
                    sb.BLKREFID_OS_DELETESELF, sb.BLKREFID_OS_DISPLAYRESOURCE,
                    sb.BLKREFID_OS_HIDERESOURCE, sb.BLKREFID_OS_DISPLAY,
                    sb.BLKREFID_OS_HIDE
                },
                0,  # 累计数目
                {"抽象和问题分解", "视听效果"},  # 体现思想
                {101},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "父子物体的控制",
                {
                    sb.BLKREFID_OS_TOBESUBRESOURCEOFPICOFACILITYINOVERLAPPING,
                    sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINOVERLAPPING, sb.
                    BLKREFID_OS_TOBESUBRESOURCEOFPICOFACILITYINORIGINALSTATE,
                    sb.BLKREFID_OS_TOBESUBRESOURCEOFRESOURCEINORIGINALSTATE,
                    sb.BLKREFID_OS_BREADAWAYFROWPARENTRESOURCE
                },
                0,  # 累计数目
                {"抽象和问题分解", "视听效果"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "广播消息的使用",
                {
                    sb.BLKREFID_OS_BROADCASTMESSAGE,
                    sb.BLKREFID_OS_BROADCASTMESSAGE_P2P,
                    sb.BLKREFID_TRG_WHENRECIEVEBROADCASTMESSAGE,
                    sb.BLKREFID_VAR_OBJECT
                },
                0,  # 累计数目
                {"并发思想", "同步思想"},  # 体现思想
                {501, 502},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "物体物理特征控制",
                {
                    sb.BLKREFID_PF_STARTPHYSICSENGINE,
                    sb.BLKREFID_PF_STOPPHYSICSENGINE,
                    sb.BLKREFID_PF_SETTINGMASS, sb.BLKREFID_PF_OPENGRAVITY,
                    sb.BLKREFID_PF_CLOSEGRAVITY,
                    sb.BLKREFID_PF_FORCEFROMXYZBYCOORDINATE,
                    sb.BLKREFID_PF_TOBETRIGGER, sb.BLKREFID_PF_TOBECOLLIDER,
                    sb.BLKREFID_CND_CRACHRESOURCE
                },
                0,  # 累计数目
                {"抽象和问题分解", "视听效果"},  # 体现思想
                {951},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "数字变量的使用",
                {
                    sb.BLKREFID_VAR_VARIABLES, sb.BLKREFID_VAR_VARIABLESINCDEC,
                    sb.BLKREFID_VAR_VARIABLESASSIGNMENT
                },
                0,  # 累计数目
                {"数据表示"},  # 体现思想
                {901, 902, 903, 904},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "字符串变量的使用",
                {sb.BLKREFID_VAR_STRING},
                0,  # 累计数目
                {"数据表示"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "List变量的使用",
                {
                    sb.BLKREFID_VAR_LIST, sb.BLKREFID_VAR_LIST_SET,
                    sb.BLKREFID_VAR_LIST_GET
                },
                0,  # 累计数目
                {"数据表示"},  # 体现思想
                {151, 152, 153, 154, 155, 156, 157},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "音效控制",
                {
                    sb.BLKREFID_SD_PLAYSOUNDREPEAT,
                    sb.BLKREFID_SD_PLAYSOUNDONCE, sb.BLKREFID_SD_STOPSOUND
                },
                0,  # 累计数目
                {"视听效果"},  # 体现思想
                {801},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "数据运算的使用",
                {
                    sb.BLKREFID_DC_VARIABLECELL, sb.BLKREFID_DC_ARITHMETIC,
                    sb.BLKREFID_DC_FUNCTION, sb.BLKREFID_DC_RANDOMNUMBER,
                    sb.BLKREFID_DC_REMAINDER, sb.BLKREFID_DC_TRIFUNCTION
                },
                0,  # 累计数目
                {"数据表示"},  # 体现思想
                {205},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "条件表达式的使用",
                {
                    sb.BLKREFID_CND_NUMBERISOJZZZF,
                    sb.BLKREFID_CND_EXACTDIVISION, sb.BLKREFID_CND_BOOLANDOR,
                    sb.BLKREFID_CND_BOOLCOMPARE, sb.BLKREFID_CND_BOOLNOT
                },
                0,  # 累计数目
                {"逻辑思维"},  # 体现思想
                {401, 402},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "资源克隆",
                {
                    sb.BLKREFID_OA_BREAKRESOURCE2XYZ,
                    sb.BLKREFID_OS_CLONERESOURCE,
                    sb.BLKREFID_TRG_WHENRUNNINGASCLONE
                },
                0,  # 累计数目
                {"抽象和问题分解", "并发思想"},  # 体现思想
                {-1},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ],
            [
                "并发控制",
                {
                    sb.BLKREFID_TRG_WHENPROJECTSTART,
                    sb.BLKREFID_TRG_WHENCONDITION,
                    sb.BLKREFID_LF_TELLOBJECT2EXCUTING
                },
                0,  # 累计数目
                {"并发思想"},  # 体现思想
                {201},  # 错误影响
                0,  # 是否发生错误
                0  # 是否使用过
            ]
        ]

        # IV. 结论
        # 阈值: 优|良|中|差，通过/不通过
        self.test_result_threshold_value = [[[80, 100], "优", "通过"],
                                            [[70, 80], "良", "通过"],
                                            [[50, 70], "中", "通过"],
                                            [[0, 50], "差", "不通过"]]

    # 主观
    # set
    def set_subjective_total_score(self, sub_score):
        self.subjectiveTotalScore = sub_score

    def set_subjective_score(self, item):  # [[,],[,],...,[,]]
        self.subjectiveScoreItem = []
        for i in range(len(item)):
            self.subjectiveScoreItem.append(item)

    def set_subjective_fullscore(self, item_score):  # [,,...,]
        self.subjectiveScoreItem = []
        for i in range(len(item_score)):
            self.subjectiveScoreItem.append([item_score[i], 0.0])

    def set_subjective_realscore(self, item_score):  # [,,...,]
        for i in range(len(item_score)):
            self.subjectiveScoreItem[i][1] = item_score[i]

    # calculating
    def cal_subjective_score(self):
        self.subjectiveScore = 0.0
        for i in range(len(self.subjectiveScoreItem)):
            self.subjectiveScore += self.subjectiveScoreItem[i][1]

    # 客观
    # set
    def set_objective_total_score(self, obj_score):
        self.objectiveTotalScore = obj_score

    def set_objective_score(self,
                            item):  # [[,],[,],...,[,]],分项:[分项分数(百分制),分项占比]
        self.objectiveScoreItem = []
        for i in range(len(item)):
            self.objectiveScoreItem.append(item[i])

    def set_objective_checkresult_blockdist(self, warningerror, dist):
        self.objectiveWarning = warningerror
        self.objectiveBlockDist = dist

    # calculating
    def cal_objective_score(self, sub_real_score):
        ratio = self.objectiveTotalScore / (self.subjectiveTotalScore +
                                            self.objectiveTotalScore)
        self.objectiveScore = [
            sub_real_score, round(sub_real_score * ratio, 2)
        ]

    # 获取显示元素
    # 1. 获取评分方式的主客观百分比
    def get_scale_of_marks(self):
        return [str(self.subjectiveTotalScore), str(self.objectiveTotalScore)]

    # 2. 获取评测总分
    def get_total_score(self):
        return str(round(self.subjectiveScore + self.objectiveScore[1], 2))

    # 3. 获取主观分数sum
    def get_subjective_total_score(self):
        return [str(self.subjectiveTotalScore), str(self.subjectiveScore)]

    # 4. 获取主观得分分项分数
    def get_subjective_score_detail(self):
        detail_score = []
        for i in range(len(self.subjectiveScoreItem)):
            detail_score.append([
                str(round(self.subjectiveScoreItem[i][0], 2)),
                str(round(self.subjectiveScoreItem[i][1], 2))
            ])
        return detail_score

    # 5. 获取客观分数sum
    def get_objective_total_score(self):
        ratio = self.objectiveTotalScore / (self.subjectiveTotalScore +
                                            self.objectiveTotalScore)
        return [
            str(round(self.objectiveTotalScore, 2)),
            str(round(self.objectiveScore[1], 2)),
            str(round(self.objectiveScore[0], 2)),
            str(round(ratio, 2))
        ]

    # 6. 获取客观分数分项分值
    def get_objective_score_detail(self):
        detail_score = []
        for i in range(len(self.objectiveScoreItem)):
            detail_score.append(str(round(self.objectiveScoreItem[i][0], 2)))
        return detail_score

    # 7. 获取主观评价评述
    def get_subject_statement(self):
        # 1. 单项分级
        for i in range(len(self.subject_grading_rule)):
            # 1.1. 计算得分比重,每个分项的实际得分与该分项满分的比
            if 0 != self.subjectiveScoreItem[i][0] != 0:
                self.subject_grading_rule[i][1] = self.subjectiveScoreItem[i][
                    1] / self.subjectiveScoreItem[i][0]
            else:
                self.subject_grading_rule[i][1] = 0.0
            # 1.2. 根据规则,评价该分项等级: 高(优秀),中(尚可),低(欠佳)
            if self.subject_grading_rule[i][1] > self.subject_grading_rule[i][
                    2][0] and self.subject_grading_rule[i][
                        1] <= self.subject_grading_rule[i][2][1]:
                self.subject_grading_rule[i][5] = SUBITEM_RATING_HIGH
            elif self.subject_grading_rule[i][1] > self.subject_grading_rule[
                    i][3][0] and self.subject_grading_rule[i][
                        1] <= self.subject_grading_rule[i][3][1]:
                self.subject_grading_rule[i][5] = SUBITEM_RATING_MIDDLE
            else:
                self.subject_grading_rule[i][5] = SUBITEM_RATING_LOW
            # 1.3. 判断该分项是否得到满分
            if self.subjectiveScoreItem[i][0] == self.subjectiveScoreItem[i][
                    1]:
                self.subject_grading_rule[i][6] = SCORE_FULL_MARK
            else:
                self.subject_grading_rule[i][6] = SCORE_NO_FULL_MARK
        # 2. 析取词素
        self.subject_morpheme_high_items = ""
        self.subject_morpheme_middle_items = ""
        self.subject_morpheme_low_items = ""
        self.subject_morpheme_low_items_score = ""
        self.subject_morpheme_fullmard_items = ""
        for i in range(len(self.subject_grading_rule)):
            if self.subject_grading_rule[i][5] == SUBITEM_RATING_HIGH:
                self.subject_morpheme_high_items = self.subject_morpheme_high_items + self.subject_grading_rule[
                    i][0] + "、"
            elif self.subject_grading_rule[i][5] == SUBITEM_RATING_MIDDLE:
                self.subject_morpheme_middle_items = self.subject_morpheme_middle_items + self.subject_grading_rule[
                    i][0] + "、"
            else:
                self.subject_morpheme_low_items = self.subject_morpheme_low_items + self.subject_grading_rule[
                    i][0] + "、"
                self.subject_morpheme_low_items_score = self.subject_morpheme_low_items_score + self.subject_grading_rule[
                    i][0] + "只得到了" + str(self.subjectiveScoreItem[i][1]) + "分、"
            if self.subject_grading_rule[i][6] == SCORE_FULL_MARK:
                self.subject_morpheme_fullmard_items = self.subject_morpheme_fullmard_items + self.subject_grading_rule[
                    i][0] + "、"
        if len(self.subject_morpheme_high_items) > 0:
            self.subject_morpheme_high_items = self.subject_morpheme_high_items[:
                                                                                -1]
        if len(self.subject_morpheme_middle_items) > 0:
            self.subject_morpheme_middle_items = self.subject_morpheme_middle_items[:
                                                                                    -1]
        if len(self.subject_morpheme_low_items) > 0:
            self.subject_morpheme_low_items = self.subject_morpheme_low_items[:
                                                                              -1]
        if len(self.subject_morpheme_low_items_score) > 0:
            self.subject_morpheme_low_items_score = self.subject_morpheme_low_items_score[:
                                                                                          -1]
        if len(self.subject_morpheme_fullmard_items) > 0:
            self.subject_morpheme_fullmard_items = self.subject_morpheme_fullmard_items[:
                                                                                        -1]
        # 3. 生成主观评述
        # 3.1. 生成 KEY
        key = 0
        if len(self.subject_morpheme_high_items) > 0:
            key += 1000
        if len(self.subject_morpheme_middle_items) > 0:
            key += 100
        if len(self.subject_morpheme_low_items) > 0:
            key += 10
        if len(self.subject_morpheme_fullmard_items) > 0:
            key += 1

        # 3.2. 获取评述模板
        if key < 10:
            return ""
        subjective_statement = self.subject_grading_statement["%04d" % key]
        # 3.3. 替换语素
        # <HIGH-ITEMS>, self.subject_morpheme_high_items
        subjective_statement = subjective_statement.replace(
            "<HIGH-ITEMS>", self.subject_morpheme_high_items)
        # <MIDDLE-ITEMS>, self.subject_morpheme_middle_items
        subjective_statement = subjective_statement.replace(
            "<MIDDLE-ITEMS>", self.subject_morpheme_middle_items)
        # <LOW-ITEMS>, self.subject_morpheme_low_items
        subjective_statement = subjective_statement.replace(
            "<LOW-ITEMS>", self.subject_morpheme_low_items)
        # <LOW-ITEMS-SCORE>, self.subject_morpheme_low_items_score
        subjective_statement = subjective_statement.replace(
            "<LOW-ITEMS-SCORE>", self.subject_morpheme_low_items_score)
        # <FULLMARK-ITEMS>, self.subject_morpheme_fullmard_items
        subjective_statement = subjective_statement.replace(
            "<FULLMARK-ITEMS>", self.subject_morpheme_fullmard_items)

        return subjective_statement

    # 8. 获取客观评述评述
    def get_object_statement(self):
        # 1. 单项分级
        # 1.1. set单项百分制分值
        for i in range(len(self.object_grading_rule)):
            self.object_grading_rule[i][5] = self.objectiveScoreItem[i][0]
        # 1.2. 分级
        for i in range(len(self.object_grading_rule)):
            if self.object_grading_rule[i][5] > self.object_grading_rule[i][1][
                    0] and self.object_grading_rule[i][
                        5] <= self.object_grading_rule[i][1][1]:
                self.object_grading_rule[i][4] = SUBITEM_RATING_HIGH
            elif self.object_grading_rule[i][5] > self.object_grading_rule[i][
                    2][0] and self.object_grading_rule[i][
                        5] <= self.object_grading_rule[i][2][1]:
                self.object_grading_rule[i][4] = SUBITEM_RATING_MIDDLE
            else:
                self.object_grading_rule[i][4] = SUBITEM_RATING_LOW
        # 1.3. 按照单项分值降序排序
        self.object_grading_rule.sort(key=lambda x: x[5], reverse=True)

        # 2. 析取词素
        # 2.1. 分级块
        self.object_morpheme_high_items = ""
        self.object_morpheme_middle_items = ""
        self.object_morpheme_low_items = ""
        for i in range(len(self.object_grading_rule)):
            if self.object_grading_rule[i][4] == SUBITEM_RATING_HIGH:
                self.object_morpheme_high_items = self.object_morpheme_high_items + self.object_grading_rule[
                    i][0] + "、"
            elif self.object_grading_rule[i][4] == SUBITEM_RATING_MIDDLE:
                self.object_morpheme_middle_items = self.object_morpheme_middle_items + self.object_grading_rule[
                    i][0] + "、"
            else:
                self.object_morpheme_low_items = self.object_morpheme_low_items + self.object_grading_rule[
                    i][0] + "、"
        # 2.2. 错误
        self.object_morpheme_error_warning = ""
        if 0 != len(self.objectiveWarning):
            split100 = self.objectiveWarning.split(sb.SPLIT_GRAMMAR_TYPE)
            split100_count = len(split100)
            for i in range(split100_count):
                split100_tail = split100[i].split(
                    sb.SPLIT_GRAMMAR_TYPE_REPORTENTRY)
                split100_detail = split100_tail[1]
                split100xx_tail = split100_detail.split(
                    sb.SPLIT_GRAMMAR_REPORTENTRY_EACH)
                split100xx_tail_count = len(split100xx_tail)
                for j in range(split100xx_tail_count):
                    splitxxx = split100xx_tail[j].split(
                        sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS)
                    errorcode = int(splitxxx[1])
                    errorcount = len(splitxxx[2].split(
                        sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS_POINT))
                    for m in range(len(self.object_errorwarning_items)):
                        if self.object_errorwarning_items[m][1] == errorcode:
                            self.object_errorwarning_items[m][2] += errorcount

        count = 0
        for i in range(len(self.object_errorwarning_items)):
            if self.object_errorwarning_items[i][2] > 0:
                self.object_morpheme_error_warning = self.object_morpheme_error_warning + self.object_errorwarning_items[
                    i][3] + "、"
                count += 1
                if -1 == MAX_ERROR_REPROT:
                    continue
                if count >= MAX_ERROR_REPROT:
                    break
        # 2.3. 知识掌握
        self.object_morpheme_high_grasp_items = ""
        self.object_morpheme_middle_grasp_items = ""
        self.object_morpheme_infrequent_items = ""
        # 2.3.1. block distribution
        block_dist = []
        split_block1 = self.objectiveBlockDist.split(sb.SPLIT_BLOCKDIST1)
        for i in range(len(split_block1)):
            split_block2 = split_block1[i].split(sb.SPLIT_BLOCKDIST2)
            block_dist.append([split_block2[0], split_block2[1]])
        # 2.3.2. statistics
        for i in range(len(block_dist)):
            for j in range(len(self.object_grasp_level_items)):
                if block_dist[i][0] in self.object_grasp_level_items[j][1]:
                    self.object_grasp_level_items[j][2] += block_dist[i][0]
        # 2.3.3. check error
        for i in range(len(self.object_errorwarning_items)):
            if 0 != self.object_errorwarning_items[i][2]:
                for j in range(len(self.object_grasp_level_items)):
                    if self.object_errorwarning_items[i][
                            1] in self.object_grasp_level_items[j][4]:
                        self.object_grasp_level_items[j][5] = 1
        # 2.3.4. 生成
        high_grasp_ct_item = set()
        middle_grasp_ct_item = set()
        for i in range(len(self.object_grading_rule)):
            if self.object_grading_rule[i][4] == SUBITEM_RATING_HIGH:
                high_grasp_ct_item.add(self.object_grading_rule[i][0])
            elif self.object_grading_rule[i][4] == SUBITEM_RATING_MIDDLE:
                middle_grasp_ct_item.add(self.object_grading_rule[i][0])
            else:
                pass
        self.object_grasp_level_items.sort(key=lambda x: x[2], reverse=False)
        high_item_count = 0
        middle_item_count = 0
        for i in range(len(self.object_grasp_level_items)):
            if 0 == self.object_grasp_level_items[i][
                    5] and 0 == self.object_grasp_level_items[i][6] and len(
                        self.object_grasp_level_items[i][3]
                        & high_grasp_ct_item):
                high_item_count += 1
                if high_item_count <= MAX_GRASP_REPORT:
                    self.object_morpheme_high_grasp_items = self.object_morpheme_high_grasp_items + self.object_grasp_level_items[
                        i][0] + "、"
                    self.object_grasp_level_items[i][6] = 1
            if 0 == self.object_grasp_level_items[i][
                    5] and 0 == self.object_grasp_level_items[i][6] and len(
                        self.object_grasp_level_items[i][3]
                        & middle_grasp_ct_item):
                middle_item_count += 1
                if middle_item_count <= MAX_GRASP_REPORT:
                    self.object_morpheme_middle_grasp_items = self.object_morpheme_middle_grasp_items + self.object_grasp_level_items[
                        i][0] + "、"
                    self.object_grasp_level_items[i][6] = 1
        self.object_grasp_level_items.sort(key=lambda x: x[2], reverse=True)
        infrequent_item_count = 0
        for i in range(len(self.object_grasp_level_items)):
            if 0 == self.object_grasp_level_items[i][6]:
                infrequent_item_count += 1
                if infrequent_item_count <= MAX_INFREQUENT_REPORT:
                    self.object_morpheme_infrequent_items = self.object_morpheme_infrequent_items + self.object_grasp_level_items[
                        i][0] + "、"
                    self.object_grasp_level_items[i][6] = 1
        if len(self.object_morpheme_high_items) > 0:
            self.object_morpheme_high_items = self.object_morpheme_high_items[:
                                                                              -1]
        if len(self.object_morpheme_high_grasp_items) > 0:
            self.object_morpheme_high_grasp_items = self.object_morpheme_high_grasp_items[:
                                                                                          -1]
        if len(self.object_morpheme_middle_items) > 0:
            self.object_morpheme_middle_items = self.object_morpheme_middle_items[:
                                                                                  -1]
        if len(self.object_morpheme_middle_grasp_items) > 0:
            self.object_morpheme_middle_grasp_items = self.object_morpheme_middle_grasp_items[:
                                                                                              -1]
        if len(self.object_morpheme_low_items) > 0:
            self.object_morpheme_low_items = self.object_morpheme_low_items[:
                                                                            -1]
        if len(self.object_morpheme_error_warning) > 0:
            self.object_morpheme_error_warning = self.object_morpheme_error_warning[:
                                                                                    -1]
        if len(self.object_morpheme_infrequent_items) > 0:
            self.object_morpheme_infrequent_items = self.object_morpheme_infrequent_items[:
                                                                                          -1]
        # 3. 生成客观评述
        # 3.1. 生成 KEY
        key = 0
        if len(self.object_morpheme_high_items) > 0:
            key += 10000
        if len(self.object_morpheme_middle_items) > 0:
            key += 1000
        if len(self.object_morpheme_low_items) > 0:
            key += 100
        if len(self.object_morpheme_error_warning) > 0:
            key += 10
        if len(self.object_morpheme_infrequent_items) > 0:
            key += 1

        # 3.2. 获取评述模板
        if key < 100:
            return ""
        objective_statement = self.object_grading_statement["%05d" % key]
        # 3.3. 替换语素
        # <H-ITMS-STD>, self.object_morpheme_high_items
        objective_statement = objective_statement.replace(
            "<H-ITMS-STD>", self.object_morpheme_high_items)
        # <H-GRSP-ITMS-STD>, self.object_morpheme_high_grasp_items
        objective_statement = objective_statement.replace(
            "<H-GRSP-ITMS-STD>", self.object_morpheme_high_grasp_items)
        # <M-ITMS-STD>, self.object_morpheme_middle_items
        objective_statement = objective_statement.replace(
            "<M-ITMS-STD>", self.object_morpheme_middle_items)
        # <M-GRSP-ITMS-STD>, self.object_morpheme_middle_grasp_items
        objective_statement = objective_statement.replace(
            "<M-GRSP-ITMS-STD>", self.object_morpheme_middle_grasp_items)
        # <L-ITMS-STD>, self.object_morpheme_low_items
        objective_statement = objective_statement.replace(
            "<L-ITMS-STD>", self.object_morpheme_low_items)
        # <GRM-EW-STD>, self.object_morpheme_error_warning
        objective_statement = objective_statement.replace(
            "<GRM-EW-STD>", self.object_morpheme_error_warning)
        # <INF-GRM-STD>, self.object_morpheme_infrequent_items
        objective_statement = objective_statement.replace(
            "<INF-GRM-STD>", self.object_morpheme_infrequent_items)

        return objective_statement

    # 9. 评价结果: 优|良|中|差，通过/不通过
    def get_last_test_result(self):
        last_score = self.subjectiveScore + self.objectiveScore[1]
        for i in range(len(self.test_result_threshold_value)):
            if last_score > self.test_result_threshold_value[i][0][
                    0] and last_score <= self.test_result_threshold_value[i][
                        0][1]:
                return [
                    self.test_result_threshold_value[i][1],
                    self.test_result_threshold_value[i][2]
                ]
