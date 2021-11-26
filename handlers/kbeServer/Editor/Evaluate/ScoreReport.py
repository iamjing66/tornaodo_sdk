# -*- coding: utf-8 -*-
"""
  create-x source code grading and score.
  statistics statement for Computing Think.

  Xi'an Feidie VR technology co. LTD
  2019/11/04
"""
import ScoreBase as sb


class ScoreSubstractionRule:
    def __init__(self):
        self.rule_substract = [
            [
                "sprite",
                # 总的sprite数目, 无效的sprite数目
                [
                    "无效的sprite", 0, 0,
                    [[0, "abstraction_and_problem_decomposition", 0.1],
                     [6, "data_representation", 0.1],
                     [7, "visual_auditory", 0.1]],
                    [[0, "abstraction_and_problem_decomposition", 0.1],
                     [6, "data_representation", 0.1],
                     [7, "visual_auditory", 0.1]]
                ]
            ],
            [
                "script",
                # 有效script数目, 无效script数目
                [
                    "无效的script(无触点,实际不可触发,单块)", 0, 0,
                    [[0, "abstraction_and_problem_decomposition", 0.2],
                     [1, "parallelism", 0.2], [2, "logical", 0.2],
                     [3, "synchronization", 0.2],
                     [4, "algorithmic_notions_of_flow_control", 0.2]],
                    [[0, "abstraction_and_problem_decomposition", 0.2],
                     [1, "parallelism", 0.2], [2, "logical", 0.2],
                     [3, "synchronization", 0.2],
                     [4, "algorithmic_notions_of_flow_control", 0.2]]
                ],
                # 临界深度下线,临界深度上限
                [
                    "语句块嵌套太深", 0, 0,
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]],
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]]
                ],
                # 临界深度下线,临界深度上限
                [
                    "参数块嵌套太深", 0, 0,
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]],
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]]
                ],
                # 临界深度下线,临界深度上限
                [
                    "语句/参数块嵌套太深", 0, 0,
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]],
                    [[0, "abstraction_and_problem_decomposition", 0.05],
                     [2, "logical", 0.05],
                     [4, "algorithmic_notions_of_flow_control", 0.05]]
                ],
                # 临界深度下线,临界深度上限
                [
                    "无效的嵌套", 0, 0,
                    [
                        [4, "algorithmic_notions_of_flow_control", 0.1],
                    ],
                    [[0, "abstraction_and_problem_decomposition", 0.1],
                     [2, "logical", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1]]
                ]
            ],
            [
                "condition",
                # 临界深度下线,临界深度上限
                [
                    "条件语句块嵌套太深", 0, 0, [
                        [2, "logical", 0.05],
                    ], [
                        [2, "logical", 0.05],
                    ]
                ],
                # no used,no used
                [
                    "缺参数", 0, 0, [
                        [2, "logical", 0.2],
                    ], [
                        [2, "logical", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "没有块", 0, 0, [
                        [2, "logical", 0.2],
                    ], [
                        [2, "logical", 0.2],
                    ]
                ]
            ],
            [
                "logicalexpression",
                # 临界深度下线,临界深度上限
                [
                    "参数嵌套太深", 0, 0, [
                        [2, "logical", 0.05],
                    ], [
                        [2, "logical", 0.05],
                    ]
                ],
                # no used,no used
                [
                    "缺参数", 0, 0, [
                        [2, "logical", 0.2],
                    ], [
                        [2, "logical", 0.2],
                    ]
                ]
            ],
            [
                "broadcast",
                # no used,no used
                [
                    "发送广播,无接收点", 0, 0,
                    [[1, "parallelism", 0.3], [3, "synchronization", 0.3]],
                    [
                        [3, "synchronization", 0.3],
                    ]
                ],
                # no used,no used
                [
                    "接收广播,无发送者", 0, 0,
                    [[1, "parallelism", 0.3], [3, "synchronization", 0.3]],
                    [
                        [3, "synchronization", 0.3],
                    ]
                ]
            ],
            [
                "wait",
                # 临界时间下线,临界时间上限
                [
                    "等待时间太长", 0, 0, [
                        [3, "synchronization", 0.05],
                    ], [
                        [3, "synchronization", 0.05],
                    ]
                ]
            ],
            [
                "loop",
                # 临界深度下线,临界深度上限
                [
                    "循环语句块嵌套太深", 0, 0,
                    [
                        [4, "algorithmic_notions_of_flow_control", 0.05],
                    ], [
                        [4, "algorithmic_notions_of_flow_control", 0.05],
                    ]
                ],
                # no used,no used
                [
                    "没有块", 0, 0,
                    [
                        [4, "algorithmic_notions_of_flow_control", 0.2],
                    ], [
                        [4, "algorithmic_notions_of_flow_control", 0.2],
                    ]
                ]
            ],
            [
                "music",
                # no used,no used
                [
                    "缺参数", 0, 0,
                    [[5, "user_interactivity", 0.1],
                     [7, "visual_auditory", 0.1]],
                    [[5, "user_interactivity", 0.1],
                     [6, "data_representation", 0.1],
                     [7, "visual_auditory", 0.1]]
                ]
            ],
            [
                "variables",
                # 变量总数,无效数目
                [
                    "定义,但是没有使用", 0, 0,
                    [[2, "logical", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]],
                    [[3, "synchronization", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]]
                ],
                # 变量总数,无效数目
                [
                    "使用,但是没有修改过", 0, 0,
                    [[2, "logical", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]],
                    [[3, "synchronization", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]]
                ],
                # 变量总数,无效数目
                [
                    "修改过,但是没有使用过", 0, 0,
                    [[2, "logical", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]],
                    [[3, "synchronization", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]]
                ],
                # no used,no used
                [
                    "变量块没有选择变量", 0, 0,
                    [[2, "logical", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]],
                    [[3, "synchronization", 0.1],
                     [4, "algorithmic_notions_of_flow_control", 0.1],
                     [6, "data_representation", 0.2]]
                ],
                # no used,no used
                [
                    "没有选择UI资源", 0, 0,
                    [[5, "user_interactivity", 0.1],
                     [7, "visual_auditory", 0.1]],
                    [[5, "user_interactivity", 0.1],
                     [6, "data_representation", 0.1],
                     [7, "visual_auditory", 0.1]]
                ],
                # no used,no used
                [
                    "没有选择动作", 0, 0,
                    [[5, "user_interactivity", 0.1],
                     [7, "visual_auditory", 0.1]],
                    [[5, "user_interactivity", 0.1],
                     [6, "data_representation", 0.1],
                     [7, "visual_auditory", 0.1]]
                ]
            ],
            [
                "phycharacteristics",
                # no used,no used
                [
                    "没有开启物理引擎", 0, 0, [
                        [7, "visual_auditory", 0.1],
                    ], [
                        [7, "visual_auditory", 0.1],
                    ]
                ]
            ],
            # 2019/12/11 add
            [
                "block",
                # no used,no used
                [
                    "list不能为空", 0, 0, [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "list变量不能单独参与计算", 0, 0, [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "非list变量不能不能在此处set值", 0, 0,
                    [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "非list变量不能不能在此处get值", 0, 0,
                    [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "list变量下标越界", 0, 0, [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "list变量下标必须是数字", 0, 0, [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ],
                # no used,no used
                [
                    "list使用位置错误", 0, 0, [
                        [6, "data_representation", 0.2],
                    ], [
                        [6, "data_representation", 0.2],
                    ]
                ]
            ]
        ]


class ScoreCalculator:
    def __init__(self):
        self.score_record = [
            [
                # 第一类评分:单项分,单项占比,累计扣除,累计扣除比例,最大扣除比例
                [
                    0, "abstraction_and_problem_decomposition", 0.0, 0.0, 0.0,
                    0.0, 0.8
                ],
                [1, "parallelism", 0.0, 0.0, 0.0, 0.0, 0.8],
                [2, "logical", 0.0, 0.0, 0.0, 0.0, 0.8],
                [3, "synchronization", 0.0, 0.0, 0.0, 0.0, 0.8],
                [
                    4, "algorithmic_notions_of_flow_control", 0.0, 0.0, 0.0,
                    0.0, 0.8
                ],
                [5, "user_interactivity", 0.0, 0.0, 0.0, 0.0, 0.8],
                [6, "data_representation", 0.0, 0.0, 0.0, 0.0, 0.8],
                [7, "visual_auditory", 0.0, 0.0, 0.0, 0.0, 0.8]
            ],
            [
                # 第二类评分:单项分,单项占比,累计扣除,最大扣除比例
                [
                    0, "abstraction_and_problem_decomposition", 0.0, 0.0, 0.0,
                    0.0, 0.8
                ],
                [1, "parallelism", 0.0, 0.0, 0.0, 0.0, 0.8],
                [2, "logical", 0.0, 0.0, 0.0, 0.0, 0.8],
                [3, "synchronization", 0.0, 0.0, 0.0, 0.0, 0.8],
                [
                    4, "algorithmic_notions_of_flow_control", 0.0, 0.0, 0.0,
                    0.0, 0.8
                ],
                [5, "user_interactivity", 0.0, 0.0, 0.0, 0.0, 0.8],
                [6, "data_representation", 0.0, 0.0, 0.0, 0.0, 0.8],
                [7, "visual_auditory", 0.0, 0.0, 0.0, 0.0, 0.8]
            ]
        ]

    def set_originalscore(self, score1, rule1, score2, rule2):
        for i in range(8):
            self.score_record[0][i][2] = score1[i]
            self.score_record[0][i][3] = rule1[i][1]
            self.score_record[1][i][2] = score2[i]
            self.score_record[1][i][3] = rule2[i][0]

    def calculating(self):
        return_score = []
        score1 = []
        score2 = []

        #      print(self.score_record)
        for i in range(9):
            if 8 == i:
                score1.append(0.0)
                score2.append(0.0)
            else:
                score1.append(self.score_record[0][i][2] *
                              (1 - self.score_record[0][i][5]))
                score2.append(self.score_record[1][i][2] *
                              (1 - self.score_record[1][i][5]))
        for i in range(8):
            score1[8] += (score1[i] * self.score_record[0][i][3])
            score2[8] += (score2[i] * self.score_record[1][i][3])

        return_score.append(score1)
        return_score.append(score2)

        return return_score


class ScoreReporter:
    def __init__(self):
        self.sub_rule = ScoreSubstractionRule()
        self.score_calculator = ScoreCalculator()

        # 主观评分(a%)
        # 趣味性	分数
        # 美观性	分数
        # 创意性	分数
        # 完整性	分数
        # 流畅性	分数
        # 加权分数
        # ["主观评分",分数,["趣味性",比重,分数],["美观性",比重,分数],["创意性",比重,分数],["完整性",比重,分数],["流畅性",比重,分数]]
        # self.subjectivity_score = ["主观评分",0.0,["趣味性",0.2,0.0],["美观性",0.2,0.0],["创意性",0.2,0.0],["完整性",0.2,0.0],["流畅性",0.2,0.0]]

        # 客观评分(1-a%)
        # 抽象和问题分解	分数
        # 并发思想	分数
        # 逻辑思维	分数
        # 同步思想	分数
        # 流程控制	分数
        # 用户交互	分数
        # 数据表示	分数
        # 视听效果	分数
        # 加权分数
        # ["客观评分",分数,["抽象和问题分解",比重,分数],["并发思想",比重,分数],["逻辑思维",比重,分数],["同步思想",比重,分数],["流程控制",比重,分数],["用户交互",比重,分数],["数据表示",比重,分数],["视听效果",比重,分数]]
        self.objectivity_score = [
            "客观评分", 0.0, ["抽象和问题分解", 0.12, 0.0], ["并发思想", 0.12, 0.0],
            ["逻辑思维", 0.12, 0.0], ["同步思想", 0.12, 0.0], ["流程控制", 0.12, 0.0],
            ["用户交互", 0.12, 0.0], ["数据表示", 0.12, 0.0], ["视听效果", 0.16, 0.0]
        ]

        # 最后分数
        # 主观得分
        # 客观得分
        # ["总分",分数,["主观评分",比重,分数],["客观评分",比重,分数]]
        # self.total_score = ["总分",0.0,["主观评分",0.4,0.0],["客观评分",0.6,0.0]]

        # reporting
        # sprite:
        # [warning] 无效的sprite;
        # script:
        # [error  ] 无效的script(无触点,实际不可触发,单个块);
        # [warning] 语句块嵌套太深;
        # [warning] 参数块嵌套太深;
        # [warning] 语句/参数块嵌套太深;
        # [warning] 无效的嵌套;
        # condition:
        # [warning] 条件语句块嵌套太深;
        # [error  ] 缺参数;
        # [warning] 没有块;
        # 逻辑表达式:
        # [warning] 参数嵌套太深;
        # [error  ] 缺参数;
        # 广播:
        # [warning] 发送广播,无接收点;
        # [error  ] 接收广播,无法送者;
        # wait:
        # [warning] 等待时间太长;
        # loop:
        # [warning] 循环语句块嵌套太深;
        # [warning] 没有块;
        # 音乐:
        # [error  ] 缺参数;
        # 变量:
        # [warning] 定义,但是没有使用;
        # [warning] 使用,但是没有修改过;
        # [warning] 修改过,但是没有使用过;
        # [error  ] 变量块没有选择变量;
        # [warning] 没有选择UI资源;
        # [warning] 没有选择动作;
        # 物理特性:
        # [warning] 没有打开物理引擎;
        # 块:
        # [warning] list不能为空;
        # [error  ] list变量不能单独参与计算;
        # [error  ] 非list变量不能不能在此处set值;
        # [error  ] 非list变量不能不能在此处get值;
        # [error  ] list变量下标越界;
        # [error  ] list变量下标必须是数字;
        # [error  ] list使用位置错误;

        # {
        # "sprite":[
        #              [
        #                 "[warning] 无效的sprite",[(sprite id,"sprite name"),...,]
        #              ]
        #          ],
        # "script":[
        #              [
        #                 "[error  ] 无效的script(无触点,实际不可触发,单个块)",[(sprite_id,"sprite name",script_id,first_block_squenceid),...,]
        #              ],
        #              [
        #                 "[warning] 语句块嵌套太深",[(sprite_id,"sprite name",script_id,block_sequenceid,depth),...,]
        #              ],
        #              [
        #                 "[warning] 参数块嵌套太深",[(sprite_id,"sprite name",script_id,block_sequenceid,depth),...,]
        #              ],
        #              [
        #                 "[warning] 语句/参数块嵌套太深",[(sprite_id,"sprite name",script_id,block_sequenceid,depth),...,]
        #              ],
        #              [
        #                 "[warning] 无效的嵌套",[(sprite_id,"sprite name",script_id,block_sequenceid),...,]
        #              ]
        #          ],
        # "condition":[
        #              [
        #                 "[warning] 条件语句块嵌套太深",[(sprite id,"sprite name",script_id,sequence_id,depth),...,]
        #              ],
        #              [
        #                 "[error  ] 缺参数",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[warning] 没有块",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "logicalexpression":[
        #              [
        #                 "[warning] 参数嵌套太深",[(sprite id,"sprite name",script_id,sequence_id,depth),...,]
        #              ],
        #              [
        #                 "[error  ] 缺参数",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "broadcast":[
        #              [
        #                 "[warning] 发送广播,无接收点",[(broadcast_id,sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] 接收广播,无法送者",[(broadcast_id,sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "wait":[
        #              [
        #                 "[warning] 等待时间太长",[(sprite id,"sprite name",script_id,sequence_id,time),...,]
        #              ]
        #          ],
        # "loop":[
        #              [
        #                 "[warning] 循环语句块嵌套太深",[(sprite id,"sprite name",script_id,sequence_id,depth),...,]
        #              ],
        #              [
        #                 "[warning] 没有块",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "music":[
        #              [
        #                 "[error  ] 缺参数",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "variables":[
        #              [
        #                 "[warning] 定义,但是没有使用",[("global/local","varibales name",sprite id,"sprite name"),...,]
        #              ],
        #              [
        #                 "[warning] 使用,但是没有修改过",[("global/local","varibales name",sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[warning] 修改过,但是没有使用过",[("global/local","varibales name",sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] 变量块没有选择变量",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[warning] 没有选择UI资源",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[warning] 没有选择动作",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "phycharacteristics":[
        #              [
        #                 "[warning] 没有打开物理引擎",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #          ],
        # "block":[ # 2019/12/11 add
        #              [
        #                 "[warning] list不能为空",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] list变量不能单独参与计算",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] 非list变量不能不能在此处set值",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] 非list变量不能不能在此处get值",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] list变量下标越界",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] list变量下标必须是数字",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ],
        #              [
        #                 "[error  ] list使用位置错误",[(sprite id,"sprite name",script_id,sequence_id),...,]
        #              ]
        #        ]
        # }

        self.reporting = {
            "sprite": [
                ["[warning] 无效的sprite", []],
            ],
            "script": [["[error  ] 无效的script(无触点,实际不可触发,单个块)", []],
                       ["[warning] 语句块嵌套太深", []], ["[warning] 参数块嵌套太深", []],
                       ["[warning] 语句/参数块嵌套太深", []], ["[warning] 无效的嵌套", []]],
            "condition": [["[warning] 条件语句块嵌套太深", []], ["[error  ] 缺参数c", []],
                          ["[warning] 没有块c", []]],
            "logicalexpression": [["[warning] 参数嵌套太深", []],
                                  ["[error  ] 缺参数l", []]],
            "broadcast": [["[warning] 发送广播,无接收点", []],
                          ["[error  ] 接收广播,无法送者", []]],
            "wait": [
                ["[warning] 等待时间太长", []],
            ],
            "loop": [["[warning] 循环语句块嵌套太深", []], ["[warning] 没有块", []]],
            "music": [
                ["[error  ] 缺参数", []],
            ],
            "variables": [["[warning] 定义,但是没有使用", []],
                          ["[warning] 使用,但是没有修改过", []],
                          ["[warning] 修改过,但是没有使用过", []],
                          ["[error  ] 变量块没有选择变量", []],
                          ["[warning] 没有选择UI资源", []], ["[warning] 没有选择动作",
                                                       []]],
            "phycharacteristics": [
                ["[warning] 没有打开物理引擎", []],
            ],
            # 2019/12/12 add
            "block": [["[warning] list不能为空", []],
                      ["[error  ] list变量不能单独参与计算", []],
                      ["[error  ] 非list变量不能不能在此处set值", []],
                      ["[error  ] 非list变量不能不能在此处get值", []],
                      ["[error  ] list变量下标越界", []],
                      ["[error  ] list变量下标必须是数字", []],
                      ["[error  ] list使用位置错误", []]]
        }

    # 01. sprite
    def add_sprite_unused_sprite(
            self, spriteid,
            sprite_name):  # 无效的sprite; (sprite id,"sprite name")
        self.reporting["sprite"][0][1].append((spriteid, sprite_name))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[0][1][3])
        size2 = len(self.sub_rule.rule_substract[0][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[0][1][3][i][0]
            percent = self.sub_rule.rule_substract[0][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[0][1][4][i][0]
            percent = self.sub_rule.rule_substract[0][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 02. script
    def add_script_useless_script(
        self, sprite_id, sprite_name, script_id, first_block_squenceid
    ):  # 无效的script(无触点,实际不可触发,单个块); (sprite_id,"sprite name",script_id,first_block_squenceid)
        self.reporting["script"][0][1].append(
            (sprite_id, sprite_name, script_id, first_block_squenceid))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[1][1][3])
        size2 = len(self.sub_rule.rule_substract[1][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[1][1][3][i][0]
            percent = self.sub_rule.rule_substract[1][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[1][1][4][i][0]
            percent = self.sub_rule.rule_substract[1][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_script_state_nest(
        self, sprite_id, sprite_name, script_id, block_sequenceid, depth
    ):  # 语句块嵌套太深; (sprite_id,"sprite name",script_id,block_sequenceid,depth)
        self.reporting["script"][1][1].append(
            (sprite_id, sprite_name, script_id, block_sequenceid, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[1][2][3])
        size2 = len(self.sub_rule.rule_substract[1][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[1][2][3][i][0]
            percent = self.sub_rule.rule_substract[1][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[1][2][4][i][0]
            percent = self.sub_rule.rule_substract[1][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_script_param_nest(
        self, sprite_id, sprite_name, script_id, block_sequenceid, depth
    ):  # 参数块嵌套太深; (sprite_id,"sprite name",script_id,block_sequenceid,depth)
        self.reporting["script"][2][1].append(
            (sprite_id, sprite_name, script_id, block_sequenceid, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[1][3][3])
        size2 = len(self.sub_rule.rule_substract[1][3][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[1][3][3][i][0]
            percent = self.sub_rule.rule_substract[1][3][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[1][3][4][i][0]
            percent = self.sub_rule.rule_substract[1][3][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_script_stateparam_nest(
        self, sprite_id, sprite_name, script_id, block_sequenceid, depth
    ):  # 语句/参数块嵌套太深; (sprite_id,"sprite name",script_id,block_sequenceid,depth)
        self.reporting["script"][3][1].append(
            (sprite_id, sprite_name, script_id, block_sequenceid, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[1][4][3])
        size2 = len(self.sub_rule.rule_substract[1][4][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[1][4][3][i][0]
            percent = self.sub_rule.rule_substract[1][4][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[1][4][4][i][0]
            percent = self.sub_rule.rule_substract[1][4][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_script_useless_nest(
        self, sprite_id, sprite_name, script_id, block_sequenceid
    ):  # 无效的嵌套; (sprite_id,"sprite name",script_id,block_sequenceid)
        self.reporting["script"][4][1].append(
            (sprite_id, sprite_name, script_id, block_sequenceid))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[1][5][3])
        size2 = len(self.sub_rule.rule_substract[1][5][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[1][5][3][0][0]
            percent = self.sub_rule.rule_substract[1][5][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[1][5][4][i][0]
            percent = self.sub_rule.rule_substract[1][5][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 03. condition
    def add_condition_nest(
        self, sprite_id, sprite_name, script_id, sequence_id, depth
    ):  # 条件语句块嵌套太深; (sprite id,"sprite name",script_id,sequence_id,depth)
        self.reporting["condition"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[2][1][3])
        size2 = len(self.sub_rule.rule_substract[2][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[2][1][3][i][0]
            percent = self.sub_rule.rule_substract[2][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[2][1][4][i][0]
            percent = self.sub_rule.rule_substract[2][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_condition_noparam(
            self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 缺参数; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["condition"][1][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[2][2][3])
        size2 = len(self.sub_rule.rule_substract[2][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[2][2][3][i][0]
            percent = self.sub_rule.rule_substract[2][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[2][2][4][i][0]
            percent = self.sub_rule.rule_substract[2][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_condition_noblock(
            self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 没有块; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["condition"][2][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[2][3][3])
        size2 = len(self.sub_rule.rule_substract[2][3][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[2][3][3][i][0]
            percent = self.sub_rule.rule_substract[2][3][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[2][3][4][i][0]
            percent = self.sub_rule.rule_substract[2][3][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 04. logical expression
    def add_expression_nest(
        self, sprite_id, sprite_name, script_id, sequence_id, depth
    ):  # 参数嵌套太深; (sprite id,"sprite name",script_id,sequence_id,depth)
        self.reporting["logicalexpression"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[3][1][3])
        size2 = len(self.sub_rule.rule_substract[3][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[3][1][3][i][0]
            percent = self.sub_rule.rule_substract[3][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[3][1][4][i][0]
            percent = self.sub_rule.rule_substract[3][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_expression_noparam(
            self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 缺参数; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["logicalexpression"][1][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[3][2][3])
        size2 = len(self.sub_rule.rule_substract[3][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[3][2][3][i][0]
            percent = self.sub_rule.rule_substract[3][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[3][2][4][i][0]
            percent = self.sub_rule.rule_substract[3][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 05. broadcast
    def add_broadcast_noreceiver(
        self, broadcast_id, sprite_id, sprite_name, script_id, sequence_id
    ):  # 发送广播,无接收点; (broadcast_id,sprite id,"sprite name",script_id,sequence_id)
        self.reporting["broadcast"][0][1].append(
            (broadcast_id, sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[4][1][3])
        size2 = len(self.sub_rule.rule_substract[4][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[4][1][3][i][0]
            percent = self.sub_rule.rule_substract[4][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[4][1][4][i][0]
            percent = self.sub_rule.rule_substract[4][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_broadcast_nosender(
        self, broadcast_id, sprite_id, sprite_name, script_id, sequence_id
    ):  # 接收广播,无法送者; (broadcast_id,sprite id,"sprite name",script_id,sequence_id)
        self.reporting["broadcast"][1][1].append(
            (broadcast_id, sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[4][2][3])
        size2 = len(self.sub_rule.rule_substract[4][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[4][2][3][i][0]
            percent = self.sub_rule.rule_substract[4][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[4][2][4][i][0]
            percent = self.sub_rule.rule_substract[4][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 06. wait
    def add_wait_longtime(
            self, sprite_id, sprite_name, script_id, sequence_id, time
    ):  # 等待时间太长; (sprite id,"sprite name",script_id,sequence_id,time)
        self.reporting["wait"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id, time))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[5][1][3])
        size2 = len(self.sub_rule.rule_substract[5][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[5][1][3][i][0]
            percent = self.sub_rule.rule_substract[5][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[5][1][4][i][0]
            percent = self.sub_rule.rule_substract[5][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 07. loop
    def add_loop_nest(
        self, sprite_id, sprite_name, script_id, sequence_id, depth
    ):  # 循环语句块嵌套太深; (sprite id,"sprite name",script_id,sequence_id,depth)
        self.reporting["loop"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id, depth))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[6][1][3])
        size2 = len(self.sub_rule.rule_substract[6][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[6][1][3][i][0]
            percent = self.sub_rule.rule_substract[6][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[6][1][4][i][0]
            percent = self.sub_rule.rule_substract[6][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_loop_noblock(
            self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 没有块; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["loop"][1][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[6][2][3])
        size2 = len(self.sub_rule.rule_substract[6][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[6][2][3][i][0]
            percent = self.sub_rule.rule_substract[6][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[6][2][4][i][0]
            percent = self.sub_rule.rule_substract[6][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 08. music
    def add_music_noparam(
            self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 缺参数; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["music"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[7][1][3])
        size2 = len(self.sub_rule.rule_substract[7][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[7][1][3][i][0]
            percent = self.sub_rule.rule_substract[7][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[7][1][4][i][0]
            percent = self.sub_rule.rule_substract[7][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 09. vairiables
    def add_variables_free(
        self, scope, varibales_name, sprite_id, sprite_name
    ):  # 定义,但是没有使用; ("global/local","varibales name",sprite id,"sprite name")
        self.reporting["variables"][0][1].append(
            (scope, varibales_name, sprite_id, sprite_name))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][1][3])
        size2 = len(self.sub_rule.rule_substract[8][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][1][3][i][0]
            percent = self.sub_rule.rule_substract[8][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][1][4][i][0]
            percent = self.sub_rule.rule_substract[8][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_variables_nomodified(
        self, scope, varibales_name, sprite_id, sprite_name, script_id,
        sequence_id
    ):  # 使用,但是没有修改过; ("global/local","varibales name",sprite id,"sprite name",script_id,sequence_id)
        self.reporting["variables"][1][1].append(
            (scope, varibales_name, sprite_id, sprite_name, script_id,
             sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][2][3])
        size2 = len(self.sub_rule.rule_substract[8][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][2][3][i][0]
            percent = self.sub_rule.rule_substract[8][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][2][4][i][0]
            percent = self.sub_rule.rule_substract[8][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_variables_noused(
        self, scope, varibales_name, sprite_id, sprite_name, script_id,
        sequence_id
    ):  # 修改过,但是没有使用过; ("global/local","varibales name",sprite id,"sprite name",script_id,sequence_id)
        self.reporting["variables"][2][1].append(
            (scope, varibales_name, sprite_id, sprite_name, script_id,
             sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][3][3])
        size2 = len(self.sub_rule.rule_substract[8][3][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][3][3][i][0]
            percent = self.sub_rule.rule_substract[8][3][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][3][4][i][0]
            percent = self.sub_rule.rule_substract[8][3][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_variables_varblock_noselected(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 变量块没有选择变量; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["variables"][3][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][4][3])
        size2 = len(self.sub_rule.rule_substract[8][4][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][4][3][i][0]
            percent = self.sub_rule.rule_substract[8][4][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][4][4][i][0]
            percent = self.sub_rule.rule_substract[8][4][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_uiresource_noselected(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 没有选择UI资源; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["variables"][4][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][5][3])
        size2 = len(self.sub_rule.rule_substract[8][5][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][5][3][i][0]
            percent = self.sub_rule.rule_substract[8][5][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][5][4][i][0]
            percent = self.sub_rule.rule_substract[8][5][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_action_noselected(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 没有选择动作; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["variables"][5][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[8][6][3])
        size2 = len(self.sub_rule.rule_substract[8][6][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[8][6][3][i][0]
            percent = self.sub_rule.rule_substract[8][6][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[8][6][4][i][0]
            percent = self.sub_rule.rule_substract[8][6][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 10. phycharacteristics 2019/12/04 added
    def add_phycharacteristics_block_noopenengine(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 没有打开物理引擎; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["phycharacteristics"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[9][1][3])
        size2 = len(self.sub_rule.rule_substract[9][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[9][1][3][i][0]
            percent = self.sub_rule.rule_substract[9][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[9][1][4][i][0]
            percent = self.sub_rule.rule_substract[9][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # 11. block 2019/12/11 add
    def add_list_noitem(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # list不能为空; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][0][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][1][3])
        size2 = len(self.sub_rule.rule_substract[10][1][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][1][3][i][0]
            percent = self.sub_rule.rule_substract[10][1][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][1][4][i][0]
            percent = self.sub_rule.rule_substract[10][1][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_cal(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # list变量不能单独参与计算; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][1][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][2][3])
        size2 = len(self.sub_rule.rule_substract[10][2][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][2][3][i][0]
            percent = self.sub_rule.rule_substract[10][2][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][2][4][i][0]
            percent = self.sub_rule.rule_substract[10][2][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_set(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 非list变量不能不能在此处set值; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][2][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][3][3])
        size2 = len(self.sub_rule.rule_substract[10][3][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][3][3][i][0]
            percent = self.sub_rule.rule_substract[10][3][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][3][4][i][0]
            percent = self.sub_rule.rule_substract[10][3][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_get(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # 非list变量不能不能在此处get值; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][3][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][4][3])
        size2 = len(self.sub_rule.rule_substract[10][4][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][4][3][i][0]
            percent = self.sub_rule.rule_substract[10][4][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][4][4][i][0]
            percent = self.sub_rule.rule_substract[10][4][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_subscript_overflow(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # list变量下标越界; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][4][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][5][3])
        size2 = len(self.sub_rule.rule_substract[10][5][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][5][3][i][0]
            percent = self.sub_rule.rule_substract[10][5][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][5][4][i][0]
            percent = self.sub_rule.rule_substract[10][5][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_subscript_nonum(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # list变量下标必须是数字; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][5][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][6][3])
        size2 = len(self.sub_rule.rule_substract[10][6][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][6][3][i][0]
            percent = self.sub_rule.rule_substract[10][6][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][6][4][i][0]
            percent = self.sub_rule.rule_substract[10][6][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    def add_list_invalidated_location(
        self, sprite_id, sprite_name, script_id, sequence_id
    ):  # list使用位置错误; (sprite id,"sprite name",script_id,sequence_id)
        self.reporting["block"][6][1].append(
            (sprite_id, sprite_name, script_id, sequence_id))
        # 开始记录扣分
        size1 = len(self.sub_rule.rule_substract[10][7][3])
        size2 = len(self.sub_rule.rule_substract[10][7][4])
        for i in range(size1):
            index = self.sub_rule.rule_substract[10][7][3][i][0]
            percent = self.sub_rule.rule_substract[10][7][3][i][2]
            if self.score_calculator.score_record[0][index][
                    6] - self.score_calculator.score_record[0][index][
                        5] >= percent:
                self.score_calculator.score_record[0][index][5] += percent
            else:
                self.score_calculator.score_record[0][index][
                    5] = self.score_calculator.score_record[0][index][6]
        for i in range(size2):
            index = self.sub_rule.rule_substract[10][7][4][i][0]
            percent = self.sub_rule.rule_substract[10][7][4][i][2]
            if self.score_calculator.score_record[1][index][
                    6] - self.score_calculator.score_record[1][index][
                        5] >= percent:
                self.score_calculator.score_record[1][index][5] += percent
            else:
                self.score_calculator.score_record[1][index][
                    5] = self.score_calculator.score_record[1][index][6]

    # --- score definition: ---
    # 1: '抽象和问题分解'
    # 2: '并发思想'
    # 3: '逻辑思维'
    # 4: '同步思想'
    # 5: '流程控制'
    # 6: '用户交互'
    # 7: '数据表示'
    # 8: '视听效果'
    # --- grammar check definition:
    # 100 "sprite"
    #    101 "无效的sprite"
    # 200 "script"
    #    201 "无效的script(无触点,实际不可触发,单个块)"
    #    202 "语句块嵌套太深"
    #    203 "参数块嵌套太深"
    #    204 "语句/参数块嵌套太深"
    #    205 "无效的嵌套"
    # 300 "condition"
    #    301 "条件语句块嵌套太深"
    #    302 "缺参数"
    #    303 "没有块"
    # 400 "logicalexpression"
    #    401 "参数嵌套太深"
    #    402 "缺参数"
    # 500 "broadcast"
    #    501 "发送广播,无接收点"
    #    502 "接收广播,无法送者"
    # 600 "wait"
    #    601 "等待时间太长"
    # 700 "loop"
    #    701 "循环语句块嵌套太深"
    #    702 "没有块"
    # 800 "music"
    #    801 "缺参数"
    # 900 "variables"
    #    901 "定义,但是没有使用"
    #    902 "使用,但是没有修改过"
    #    903 "修改过,但是没有使用过"
    #    904 "变量块没有选择变量"
    #    905 "没有选择UI资源"
    #    906 "没有选择动作"
    # 950 "phycharacteristics"
    #    951 "没有打开物理引擎"
    # 150 "block" # 2019/12/11 add
    #    151 "list不能为空"
    #    152 "list变量不能单独参与计算"
    #    153 "非list变量不能不能在此处set值"
    #    154 "非list变量不能不能在此处get值"
    #    155 "list变量下标越界"
    #    156 "list变量下标必须是数字"
    #    157 "list使用位置错误"
    #
    # 0  error
    # 1  warning

    def tostr(self):
        ddict = {
            "sprite": (100, -1),
            "[warning] 无效的sprite": (101, 1),
            "script": (200, -1),
            "[error  ] 无效的script(无触点,实际不可触发,单个块)": (201, 0),
            "[warning] 语句块嵌套太深": (202, 1),
            "[warning] 参数块嵌套太深": (203, 1),
            "[warning] 语句/参数块嵌套太深": (204, 1),
            "[warning] 无效的嵌套": (205, 1),
            "condition": (300, -1),
            "[warning] 条件语句块嵌套太深": (301, 1),
            "[error  ] 缺参数c": (302, 0),
            "[warning] 没有块c": (303, 1),
            "logicalexpression": (400, -1),
            "[warning] 参数嵌套太深": (401, 1),
            "[error  ] 缺参数l": (402, 0),
            "broadcast": (500, -1),
            "[warning] 发送广播,无接收点": (501, 1),
            "[error  ] 接收广播,无法送者": (502, 0),
            "wait": (600, -1),
            "[warning] 等待时间太长": (601, 1),
            "loop": (700, -1),
            "[warning] 循环语句块嵌套太深": (701, 1),
            "[warning] 没有块": (702, 1),
            "music": (800, -1),
            "[error  ] 缺参数": (801, 0),
            "variables": (900, -1),
            "[warning] 定义,但是没有使用": (901, 1),
            "[warning] 使用,但是没有修改过": (902, 1),
            "[warning] 修改过,但是没有使用过": (903, 1),
            "[error  ] 变量块没有选择变量": (904, 0),
            "[warning] 没有选择UI资源": (905, 1),
            "[warning] 没有选择动作": (906, 1),
            "phycharacteristics": (950, -1),
            "[warning] 没有打开物理引擎": (951, 1),
            "block": (150, -1),  # 2019/12/11 add
            "[warning] list不能为空": (151, 1),
            "[error  ] list变量不能单独参与计算": (152, 0),
            "[error  ] 非list变量不能不能在此处set值": (153, 0),
            "[error  ] 非list变量不能不能在此处get值": (154, 0),
            "[error  ] list变量下标越界": (155, 0),
            "[error  ] list变量下标必须是数字": (156, 0),
            "[error  ] list使用位置错误": (157, 0),
        }

        # self.objectivity_score = ["客观评分",0.0,["抽象和问题分解",0.12,0.0],
        #  ["并发思想",0.12,0.0],
        #  ["逻辑思维",0.12,0.0],
        #  ["同步思想",0.12,0.0],
        #  ["流程控制",0.12,0.0],
        #  ["用户交互",0.12,0.0],
        #  ["数据表示",0.12,0.0],
        #  ["视听效果",0.12,0.0]]
        # 52.55*
        # 1|0.12|61.9&
        # 2|0.12|92.0&
        # 3|0.12|39.87&
        # 4|0.12|72.56&
        # 5|0.12|29.72&
        # 6|0.12|12.0&
        # 7|0.12|18.68&
        # 8|0.16|83.42
        strscore = str(
            self.objectivity_score[1]) + sb.SPLIT_SCORE_TOTAL_SUBENTRY
        for i in range(8):
            strscore = strscore + str(
                i + 1) + sb.SPLIT_SCORE_SUBENTRYS_ITEM + str(
                    self.objectivity_score[i + 2][1]
                ) + sb.SPLIT_SCORE_SUBENTRYS_ITEM + str(
                    self.objectivity_score[i +
                                           2][2]) + sb.SPLIT_SCORE_SUBENTRYS
        strscore = strscore[:-1]

        # self.reporting = {
        # "sprite":[
        #              ["[warning] 无效的sprite",[]],
        #          ],
        # "script":[
        #              ["[error  ] 无效的script(无触点,实际不可触发,单个块)",[]],
        #              ["[warning] 语句块嵌套太深",[]],
        #              [ "[warning] 参数块嵌套太深",[]],
        #              [ "[warning] 语句/参数块嵌套太深",[]],
        #              ["[warning] 无效的嵌套",[]]
        #          ],
        # "condition":[
        #              ["[warning] 条件语句块嵌套太深",[]],
        #              ["[error  ] 缺参数",[]],
        #              ["[warning] 没有块",[]]
        #          ],
        # "logicalexpression":[
        #              ["[warning] 参数嵌套太深",[]],
        #              ["[error  ] 缺参数",[]]
        #          ],
        # "broadcast":[
        #              ["[warning] 发送广播,无接收点",[]],
        #              [ "[error  ] 接收广播,无法送者",[]]
        #          ],
        # "wait":[
        #              ["[warning] 等待时间太长",[]],
        #          ],
        # "loop":[
        #              ["[warning] 循环语句块嵌套太深",[]],
        #              ["[warning] 没有块",[]]
        #          ],
        # "music":[
        #              ["[error  ] 缺参数",[]],
        #          ],
        # "variables":[
        #              ["[warning] 定义,但是没有使用",[]],
        #              ["[warning] 使用,但是没有修改过",[]],
        #              ["[warning] 修改过,但是没有使用过",[]],
        #              ["[error  ] 变量块没有选择变量",[]],
        #              ["[warning] 没有选择UI资源",[]],
        #              ["[warning] 没有选择动作",[]]
        #          ]
        # "phycharacteristics":[
        #              ["[warning] 没有打开物理引擎",[]],
        #          ],
        # "block":[ # 2019/12/11 add
        #              ["[warning] list不能为空",[]],
        #              ["[error  ] list变量不能单独参与计算",[]],
        #              ["[error  ] 非list变量不能不能在此处set值",[]],
        #              ["[error  ] 非list变量不能不能在此处get值",[]],
        #              ["[error  ] list变量下标越界",[]],
        #              ["[error  ] list变量下标必须是数字",[]],
        #              ["[error  ] list使用位置错误",[]]
        #          ]
        # }
        #
        # 100@
        #     1%101%
        #         sprite id,"sprite name"
        # *
        # 200@
        #     0%201%
        #         sprite_id,"sprite name",script_id
        #         |
        #         sprite_id,"sprite name",script_id
        #         |...
        #     &
        #     1%202%
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |...
        #     &
        #     1%203%
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |...
        #     &
        #     1%204%
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |
        #         sprite_id,"sprite name",script_id,block_sequenceid,depth
        #         |...
        #     &
        #     1%205%
        #         sprite_id,"sprite name",script_id,block_sequenceid
        #         |
        #         sprite_id,"sprite name",script_id,block_sequenceid
        # *
        # ...
        strgrammar = ""
        str0 = ""
        for key, value in self.reporting.items():
            str1 = ""
            for i in range(len(value)):  # 大项
                str2 = ""
                for j in range(len(value[i][1])):
                    str3 = ""
                    for k in range(len(value[i][1][j])):
                        str3 = str3 + str(
                            value[i][1][j][k]
                        ) + sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS_POINT_ITEM
                    if len(str3) > 0:
                        str3 = str3[:-1]  # # ,,...,
                        str2 = str2 + str3 + sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS_POINT
                if len(str2) > 0:  # |||
                    str2 = str2[:-1]  # ||
                    str2 = str(
                        ddict[value[i][0]]
                        [1]) + sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS + str(
                            ddict[value[i][0]][0]
                        ) + sb.SPLIT_GRAMMAR_REPORTENTRY_DETAILS + str2  # %%||
                    str2 = str2 + sb.SPLIT_GRAMMAR_REPORTENTRY_EACH  # %%|| &
                    str1 = str1 + str2
            if len(str1) > 0:
                str1 = str1[:-1]
                str1 = str(
                    ddict[key][0]) + sb.SPLIT_GRAMMAR_TYPE_REPORTENTRY + str1
                str1 = str1 + sb.SPLIT_GRAMMAR_TYPE
                str0 = str0 + str1
        if len(str0) > 0:
            strgrammar = str0[:-1]

        if len(strgrammar) > 0:
            return strscore + sb.SPLIT_SCORE_GRAMMAR + strgrammar + sb.SPLIT_SCORE_GRAMMAR
        else:
            return strscore + sb.SPLIT_SCORE_GRAMMAR + sb.SPLIT_SCORE_GRAMMAR
