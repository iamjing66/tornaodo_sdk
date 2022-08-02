# -*- coding: utf-8 -*-
"""
  create-x source code grading and score.
  statistics statement for Computing Think.

  Xi'an Feidie VR technology co. LTD
  2019/11/08
"""
import re

import ScoreBase as sb
from get_sql import get_all_rule, get_persent, get_rule_data


class BlockDistribution:
    def __init__(self):
        self.dict_block_dist = {}  # 每种块的数目[总数,有效数目,无效数目]
        self.dict_block_type_dist = {}  # 每类块的数目[总数,有效数目,无效数目]

        self.dict_block_dist = sb.DictBlockAttribute.copy()
        for key in self.dict_block_dist:
            self.dict_block_dist[key] = [0, 0, 0]

        self.dict_block_type_dist = {
                sb.BLKTYPE_TRIGGER: [0, 0, 0],
                sb.BLKTYPE_LOGICFLOW: [0, 0, 0],
                sb.BLKTYPE_OBJECTACTION: [0, 0, 0],
                sb.BLKTYPE_OBJECTSETTING: [0, 0, 0],
                sb.BLKTYPE_CONDITION: [0, 0, 0],
                sb.BLKTYPE_VARIABLES: [0, 0, 0],
                sb.BLKTYPE_PHYSICSFEATHER: [0, 0, 0],
                sb.BLKTYPE_SOUND: [0, 0, 0],
                sb.BLKTYPE_DATACAL: [0, 0, 0],
                sb.BLKTYPE_FUNCTION: [0, 0, 0],
                sb.BLKTYPE_DRAW: [0, 0, 0],
        }

    def add_block(self, block_refid):  # block dict:  1,1,0   block type dict: 1,1,0
        value = self.dict_block_dist.get(block_refid, "")
        if value:
            value[0] += 1
            value[1] += 1
            self.dict_block_dist[block_refid] = value

            key = sb.DictBlockAttribute[block_refid][sb.BLKATTR_CATEGORY]
            value = self.dict_block_type_dist[key]
            value[0] += 1
            value[1] += 1
            self.dict_block_type_dist[key] = value

    def add_block_e(self, block_refid):  # block disct: 1,0,1   block type dict: 1,0,1
        value = self.dict_block_dist[block_refid]
        value[0] += 1
        value[2] += 1
        self.dict_block_dist[block_refid] = value

        key = sb.DictBlockAttribute[block_refid][sb.BLKATTR_CATEGORY]
        value = self.dict_block_type_dist[key]
        value[0] += 1
        value[2] += 1
        self.dict_block_type_dist[key] = value

    def adjust_right2wrong(self, block_refid):  # block disct: 0,-1,1   block type dict: 0,-1,1
        value = self.dict_block_dist[block_refid]
        value[1] -= 1
        value[2] += 1
        self.dict_block_dist[block_refid] = value

        key = sb.DictBlockAttribute[block_refid][sb.BLKATTR_CATEGORY]
        value = self.dict_block_type_dist[key]
        value[1] -= 1
        value[2] += 1
        self.dict_block_type_dist[key] = value

    def adjust_wrong2right(
            self,
            block_refid):  # block disct: 0,1,-1   block type dict: 0,1,-1
        value = self.dict_block_dist[block_refid]
        value[1] += 1
        value[2] -= 1
        self.dict_block_dist[block_refid] = value

        key = sb.DictBlockAttribute[block_refid][sb.BLKATTR_CATEGORY]
        value = self.dict_block_type_dist[key]
        value[1] += 1
        value[2] -= 1
        self.dict_block_type_dist[key] = value

    # 2019/12/19 add
    def tostr(self):
        target_str = ""
        for key in self.dict_block_dist:
            target_str = target_str + str(key) + sb.SPLIT_BLOCKDIST2 + str(
                    self.dict_block_dist[key][0]) + sb.SPLIT_BLOCKDIST1
        if len(target_str) > 0:
            target_str = target_str[:-1]
        return target_str


class ComputingThinkIndex:
    indexid_dict = {}

    def __init__(self):  # 18项, 144条;
        # 1. sprite(3)
        self.sprite_index_totals = 0  # 1.1. sprite指标: (+)sprite总数
        self.sprite_index_useful = 0  # 1.2. sprite指标: (+)sprite有效数目
        self.sprite_index_useless = 0  # 1.3. sprite指标: (-)sprite无效数目

        # 2. script(18)
        self.script_index_tatals = 0  # 2.1. script指标: (+)script总数
        self.script_index_has_detonator = 0  # 2.2. script指标: (+)script有触点数目
        self.script_index_hasnot_detonator = 0  # 2.3. script指标: (-)script无触点数目  detonator

        self.script_index_trigger_atworking = 0  # 2.4. script指标: (+)script工程运行时可触发数目
        self.script_index_trigger_cannot_be_fired = 0  # 2.5. script指标: (-)script实际不可触发数目

        self.script_index_blocknum_max = 0  # 2.6. script指标: (+)script中最大block数目
        self.script_index_blocknum_min = 0  # 2.7. script指标: (+)script中最小block数目
        self.script_index_blocknum_avg = 0.0  # 2.8. script指标: (+)script中平均block数目

        self.script_index_statementblock_nest_depth_max = 0  # 2.9. script指标: (+-)script中语句块嵌套最大深度
        self.script_index_statementblock_nest_depth_avg = 0.0  # 2.10. script指标: (+-)script中语句块嵌套平均深度
        self.script_index_paramblock_nest_depth_max = 0  # 2.11. script指标: (+-)script中参数块嵌套最大深度
        self.script_index_paramblock_nest_depth_avg = 0.0  # 2.12. script指标: (+-)script中参数块嵌套平均深度
        self.script_index_stateparamblock_nest_depth_max = 0  # 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度
        self.script_index_stateparamblock_nest_depth_avg = 0.0  # 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度
        self.script_index_nest_useless = 0  # 2.15. script指标: (-)script中无效的嵌套

        self.script_index_runtime_max = 0.0  # 2.16. script指标: (+)script最大运行时间
        self.script_index_runtime_mix = 0.0  # 2.17. script指标: (+)script最小运行时间
        self.script_index_runtime_avg = 0.0  # 2.18. script指标: (+)script平均运行时间

        # 3. block(2)
        self.block_index_totals = 0  # 3.1. block数目: (+)block总数
        self.block_index_nowork = 0  # 3.2. block数目: (-)block不能被执行的总数

        # 4. trigger(4)
        self.trigger_index_trigger_script_number_atworking = 0  # 4.1. trigger: (+)工程运行时触发的script数目
        self.trigger_index_trigger_script_number_meanwhile = 0  # 4.2. trigger: (+)同时触发的script数目
        self.trigger_index_script_running_number_meanwhile = 0  # 4.3. trigger: (+)并发执行的最大script数目
        self.trigger_index_script_running_overlap_maxtime = 0  # 4.4. trigger: (+)并发执行的script最大重叠时间

        # 5. condition(9)
        self.condition_index_number_ifelse = 0  # 5.1. contain条件: (+)ifelse数目
        self.condition_index_number_if = 0  # 5.2. contain条件: (+)if数目
        self.condition_index_nest_depth_max = 0  # 5.3. contain条件: (+-)条件嵌套最大深度(跳过loop)
        self.condition_index_nest_depth_avg = 0  # 5.4. contain条件: (+-)条件平均嵌套深度(跳过loop)

        self.condition_index_number_no_statement = 0  # 5.5. contain条件: (-)if,if else下面没有block的数目
        self.condition_index_number_param_imcompleted = 0  # 5.6. contain条件: (-)if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
        self.condition_index_number_param_variables_nochanged = 0  # 5.7. contain条件: (-)条件表达式中的变量外部不变数目(基于嵌套顶层)
        self.condition_index_number_true_forever = 0  # 5.8. contain条件: (-)条件永假数目(基于嵌套顶层)
        self.condition_index_number_false_forever = 0  # 5.9. contain条件: (-)条件永真数目(基于嵌套顶层)

        # 6. loop(9)
        self.loop_index_number_totals = 0  # 6.1. contain循环: (+)循环数目
        self.loop_index_nest_depth_max = 0  # 6.2. contain循环: (+-)循环嵌套最大深度
        self.loop_index_nest_depth_avg = 0  # 6.3. contain循环: (+-)循环嵌套平均深度

        self.loop_index_number_cross_sprite_by_broadcast = 0  # 6.4. contain循环: (+)基于消息(广播)的跨sprite大循环数目
        self.loop_index_number_cross_sprite_by_variables = 0  # 6.5. contain循环: (+)基于消息(变量)的跨sprite大循环数目
        self.loop_index_number_cross_script_by_broadcast = 0  # 6.6. contain循环: (+)基于消息(广播)的跨script大循环数目
        self.loop_index_number_cross_script_by_variables = 0  # 6.7. contain循环: (+)基于消息(变量)的跨script大循环数目

        self.loop_index_endlessloop_nobreak = 0  # 6.8. contain循环: (*)死循环数目(不能跳出,或者break条件永不为真)
        self.loop_index_endlessloop_nowait = 0  # 6.9. contain循环: (-)死循环数目(循环体中没有阻塞)

        # 7. sequenceblock(3)
        self.sequenceblock_index_number_top_max = 0  # 7.1. 顺序块: (+)一级顺序块最大数目
        self.sequenceblock_index_number_if_max = 0  # 7.2. 顺序块: (+)if中的一级顺序块最大数目
        self.sequenceblock_index_number_loop_max = 0  # 7.3. 顺序块: (+)loop中的一级顺序块最大数目

        # 8. clone(5)
        self.clone_index_number_blocks = 0  # 8.1. 克隆: (+)克隆点数目
        self.clone_index_number_sprites = 0  # 8.2. 克隆: (+)克隆sprite数量
        self.clone_index_number_sprites_type = 0  # 8.3. 克隆: (+)克隆sprite类型数量
        self.clone_index_number_trigger_script = 0  # 8.4. 克隆: (+)克隆sprite触发script数目
        self.clone_index_recursion_or_unlimited = 0  # 8.5. 克隆: (-)是否存在递归克隆

        # 9. wait(2)
        self.wait_index_number = 0  # 9.1. wait数目: (+)wait数目
        self.wait_index_max_waittime = 0  # 9.2. wait数目: (+-)wait最大等待时间

        # 10. broadcast(6)
        self.broadcast_index_number_messageid = 0  # 10.1. broadcast: (+)广播消息ID数目
        self.broadcast_index_number_sendpointer = 0  # 10.2. broadcast: (+)广播点数目
        self.broadcast_index_number_sendpointer_noreach = 0  # 10.3. broadcast: (-)广播点(不可执行到的)数目
        self.broadcast_index_number_recvpointer = 0  # 10.4. broadcast: (+)广播接收点数目
        self.broadcast_index_number_recvpointer_noreach = 0  # 10.5. broadcast: (-)广播接收点(不可执行到的)数目
        self.broadcast_index_number_rise_endless_loop = 0  # 10.6. broadcast: (-)广播形成无效死循环(循环体中没有阻塞)数目

        # 11. logicalexpr(8)
        self.logicalexpr_index_number_totals = 0  # 11.1. 逻辑表达式: (+)逻辑表达式数目
        self.logicalexpr_index_number_type = [0, 0, 0, 0,
                                              0]  # 11.2. 逻辑表达式: (+)逻辑表达式种类数目
        self.logicalexpr_index_number_nest_depth_max = 0  # 11.3. 逻辑表达式: (+-)逻辑表达式参数嵌套最大深度
        self.logicalexpr_index_number_nest_depth_avg = 0  # 11.4. 逻辑表达式: (+-)逻辑表达式参数嵌套平均深度
        self.logicalexpr_index_number_true_forever = 0  # 11.5. 逻辑表达式: (-)逻辑表达式永真数目(向上传递)
        self.logicalexpr_index_number_false_forever = 0  # 11.6. 逻辑表达式: (-)逻辑表达式永假数目(向上传递)
        self.logicalexpr_index_number_param_imcompleted = 0  # 11.7. 逻辑表达式: (-)逻辑表达式缺参数数目(向上传递)
        self.logicalexpr_index_number_variables_nochanged = 0  # 11.8. 逻辑表达式: (-)逻辑表达式变量外部不变数目(向上传递)

        # 12. globalvar(11)
        self.globalvar_index_number_totals = 0  # 12.1. 全局变量: (+)使用数目
        self.globalvar_index_number_modified = 0  # 12.2. 全局变量: (+)更改数目
        self.globalvar_index_number_cross_sprite = 0  # 12.3. 全局变量: (+)跨sprite使用数目
        self.globalvar_index_number_trigger_script = 0  # 12.4. 全局变量: (+)触发script数目
        self.globalvar_index_number_control_loop = 0  # 12.5. 全局变量: (+)变量控制的循环数目
        self.globalvar_index_number_control_condition = 0  # 12.6. 全局变量: (+)变量控制的条件数目

        self.globalvar_index_number_changed_pointer = 0  # 12.7. 全局变量: (+)变量修改点数目
        self.globalvar_index_number_changed_pointer_noreach = 0  # 12.8. 全局变量: (-)变量修改点(不可执行到的)数目
        self.globalvar_index_number_check_pointer = 0  # 12.9. 全局变量: (+)变量检测点数目(script头)
        self.globalvar_index_number_check_pointer_noreach = 0  # 12.10. 全局变量: (-)变量检测点(不可执行到的)数目(script头)
        self.globalvar_index_number_rise_endless_loop = 0  # 12.11. 全局变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目

        # 13. localvar(10)
        self.localvar_index_number_totals = 0  # 13.1. 局部变量: (+)使用数目
        self.localvar_index_number_modified = 0  # 13.2. 局部变量: (+)更改数目
        self.localvar_index_number_trigger_script = 0  # 13.3. 局部变量: (+)触发script数目
        self.localvar_index_number_control_loop = 0  # 13.4. 局部变量: (+)变量控制的循环数目
        self.localvar_index_number_control_condition = 0  # 13.5. 局部变量: (+)变量控制的条件数目

        self.localvar_index_number_changed_pointer = 0  # 13.6. 局部变量: (+)变量修改点数目
        self.localvar_index_number_changed_pointer_noreach = 0  # 13.7. 局部变量: (-)变量修改点(不可执行到的)数目
        self.localvar_index_number_check_pointer = 0  # 13.8. 局部变量: (+)变量检测点数目(script头)
        self.localvar_index_number_check_pointer_noreach = 0  # 13.9. 局部变量: (-)变量检测点(不可执行到的)数目(script头)
        self.localvar_index_number_rise_endless_loop = 0  # 13.10. 局部变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目

        # 14. interaction(11)
        self.interaction_index_number_keyboard_sprite = 0  # 14.1. 交互: (+)键盘:处理sprite数目
        self.interaction_index_number_keyboard_checkpointer = 0  # 14.2. 交互: (+)键盘:处理点数目
        self.interaction_index_number_keyboard_checkpointer_useless = 0  # 14.3. 交互: (-)键盘:无效处理点数目

        self.interaction_index_number_joystick_sprite = 0  # 14.4. 交互: (+)手柄:处理sprite数目
        self.interaction_index_number_joystick_checkpointer = 0  # 14.5. 交互: (+)手柄:处理点数目
        self.interaction_index_number_joystick_checkpointer_useless = 0  # 14.6. 交互: (-)手柄:无效处理点数目

        self.interaction_index_number_mouse_sprite = 0  # 14.7. 交互: (+)鼠标:处理sprite数目
        self.interaction_index_number_mouse_checkpointer = 0  # 14.8. 交互: (+)鼠标:处理点数目
        self.interaction_index_number_mouse_checkpointer_useless = 0  # 14.9. 交互: (-)鼠标:无效处理点数目

        self.interaction_index_number_user_inputpointer = 0  # 14.10. 交互: (+)用户输入点数目
        self.interaction_index_number_user_inputprompt = 0  # 14.11. 交互: (+)用户输入提示频率

        # 15. phycharacteristics(4)
        self.phycharacteristics_index_number_sripte_open_engine = 0  # 15.1. 物理特性: (+)开启物理引擎的sprite数目
        self.phycharacteristics_index_number_sripte_open_engine_useless = 0  # 15.2. 物理特性: (-)开启物理特性动作能否执行到
        self.phycharacteristics_index_number_blocks_in_engine_windows = 0  # 15.3. 物理特性: (+)物理引擎窗口内受制block数目
        self.phycharacteristics_index_number_blocks_out_engine_wondows = 0  # 15.4. 物理特性: (-)物理引擎窗口外受制block数目

        # 16. phyaction(12)
        self.phyaction_index_moving_sprite_type_number = 0  # 16.1. 物理行为: (+)移动的sprite数目
        self.phyaction_index_moving_sprite_blocks = 0  # 16.2. 物理行为: (+)移动的sprite指令块数目
        self.phyaction_index_moving_sprite_blocks_useless = 0  # 16.3. 物理行为: (-)移动的sprite指令块数目(不能执行到)
        self.phyaction_index_moving_sprite_times = 0  # 16.4. 物理行为: (+)移动的sprite次数

        self.phyaction_index_rotate_sprite_type_number = 0  # 16.5. 旋转行为: (+)移动的sprite数目
        self.phyaction_index_rotate_sprite_blocks = 0  # 16.6. 旋转行为: (+)移动的sprite指令块数目
        self.phyaction_index_rotate_sprite_blocks_useless = 0  # 16.7. 旋转行为: (-)移动的sprite指令块数目(不能执行到)
        self.phyaction_index_rotate_sprite_times = 0  # 16.8. 物理行为: (+)旋转的sprite次数

        self.phyaction_index_play_animation_sprite_type_number = 0  # 16.9. 物理行为: (+)播放动画效果的sprite数目
        self.phyaction_index_play_animation_sprite_blocks = 0  # 16.10. 物理行为: (+)播放动画效果的sprite指令块数目
        self.phyaction_index_play_animation_sprite_blocks_useless = 0  # 16.11. 物理行为: (-)播放动画效果的sprite指令块数目(不能执行到)
        self.phyaction_index_play_animation_sprite_times = 0  # 16.12. 物理行为: (+)播放动画效果的sprite次数

        # 17. objsetting(22)
        self.objsetting_index_number_del_sprite = 0  # 17.1. 物体设置: (+)删除sprite数目
        self.objsetting_index_number_del_sprite_blocks = 0  # 17.2. 物体设置: (+)删除sprite指令块数目
        self.objsetting_index_number_del_sprite_blocks_noreach = 0  # 17.3. 物体设置: (-)删除sprite指令块数目(不能执行到)

        self.objsetting_index_number_show_sprite = 0  # 17.4. 物体设置: (+)显示sprite数目
        self.objsetting_index_number_show_sprite_blocks = 0  # 17.5. 物体设置: (+)显示sprite指令块数目
        self.objsetting_index_number_show_sprite_blocks_noreach = 0  # 17.6. 物体设置: (-)显示sprite指令块数目(不能执行到)

        self.objsetting_index_number_hide_sprite = 0  # 17.7. 物体设置: (+)影藏sprite数目
        self.objsetting_index_number_hide_sprite_blocks = 0  # 17.8. 物体设置: (+)影藏sprite指令块数目
        self.objsetting_index_number_hide_sprite_blocks_noreach = 0  # 17.9. 物体设置: (-)影藏sprite指令块数目(不能执行到)

        self.objsetting_index_number_group = 0  # 17.10. 物体设置: (+)父子关系团数目
        self.objsetting_index_number_group_max_unit = 0  # 17.11. 物体设置: (+)父子团最大sprite数目
        self.objsetting_index_number_group_avg_unit = 0  # 17.12. 物体设置: (+)父子团平均sprite数目

        self.objsetting_index_number_group_moving = 0  # 17.13. 物体设置: (+)父子团移动数目
        self.objsetting_index_number_group_not_moving = 0  # 17.14. 物体设置: (-)父子团不移动数目

        self.objsetting_index_number_group_rotate = 0  # 17.15. 物体设置: (+)父子团旋转数目
        self.objsetting_index_number_group_not_rotate = 0  # 17.16. 物体设置: (-)父子团不旋转数目

        self.objsetting_index_number_group_play_animation = 0  # 17.17. 物体设置: (+)父子团播放动作数目
        self.objsetting_index_number_group_not_play_animation = 0  # 17.18. 物体设置: (-)父子团不播放动作数目

        self.objsetting_index_number_group_show = 0  # 17.19. 物体设置: (+)父子团子sprite显示数目
        self.objsetting_index_number_group_hide = 0  # 17.20. 物体设置: (+)父子团子sprite影藏数目

        self.objsetting_index_number_group_packaged_dynamically = 0  # 17.21. 物体设置: (+)父子团子sprite动态组团数目
        self.objsetting_index_number_group_unpackaged_dynamically = 0  # 17.22. 物体设置: (+)父子团子sprite动态拆分数目

        # 18. music(5)
        self.music_index_number_play_pointer = 0  # 18.1. 音乐: (+)音乐播放数目
        self.music_index_number_play_pointer_noreach = 0  # 18.2. 音乐: (-)不能被播放数目
        self.music_index_number_play_songs = 0  # 18.3. 音乐: (+)音乐播放曲目数目
        self.music_index_number_play_pointer_param_incompleted = 0  # 18.4. 音乐: (-)缺少参数数目
        self.music_index_number_stop_pointer = 0  # 18.5. 音乐: (+)主动停止数目

        # 0. 无
        self.no_gramer = 0

    def create_map(self):  # 该函数必须在数据不再变动的情况下调用, 调用后数值的变动无效.
        # 1. sprite(3)
        self.indexid_dict[
            "1.1"] = self.sprite_index_totals  # 1.1. sprite指标: (+)sprite总数
        self.indexid_dict[
            "1.2"] = self.sprite_index_useful  # 1.2. sprite指标: (+)sprite有效数目
        self.indexid_dict[
            "1.3"] = self.sprite_index_useless  # 1.3. sprite指标: (-)sprite无效数目

        # 2. script(18)
        self.indexid_dict[
            "2.1"] = self.script_index_tatals  # 2.1. script指标: (+)script总数
        self.indexid_dict[
            "2.2"] = self.script_index_has_detonator  # 2.2. script指标: (+)script有触点数目
        self.indexid_dict[
            "2.3"] = self.script_index_hasnot_detonator  # 2.3. script指标: (-)script无触点数目  detonator
        self.indexid_dict[
            "2.4"] = self.script_index_trigger_atworking  # 2.4. script指标: (+)script工程运行时可触发数目
        self.indexid_dict[
            "2.5"] = self.script_index_trigger_cannot_be_fired  # 2.5. script指标: (-)script实际不可触发数目
        self.indexid_dict[
            "2.6"] = self.script_index_blocknum_max  # 2.6. script指标: (+)script中最大block数目
        self.indexid_dict[
            "2.7"] = self.script_index_blocknum_min  # 2.7. script指标: (+)script中最小block数目
        self.indexid_dict[
            "2.8"] = self.script_index_blocknum_avg  # 2.8. script指标: (+)script中平均block数目
        self.indexid_dict[
            "2.9"] = self.script_index_statementblock_nest_depth_max  # 2.9. script指标: (+-)script中语句块嵌套最大深度
        self.indexid_dict[
            "2.10"] = self.script_index_statementblock_nest_depth_avg  # 2.10. script指标: (+-)script中语句块嵌套平均深度
        self.indexid_dict[
            "2.11"] = self.script_index_paramblock_nest_depth_max  # 2.11. script指标: (+-)script中参数块嵌套最大深度
        self.indexid_dict[
            "2.12"] = self.script_index_paramblock_nest_depth_avg  # 2.12. script指标: (+-)script中参数块嵌套平均深度
        self.indexid_dict[
            "2.13"] = self.script_index_stateparamblock_nest_depth_max  # 2.13. script指标: (+-)script中语句块和参数块嵌套最大深度
        self.indexid_dict[
            "2.14"] = self.script_index_stateparamblock_nest_depth_avg  # 2.14. script指标: (+-)script中语句块和参数块嵌套平均深度
        self.indexid_dict[
            "2.15"] = self.script_index_nest_useless  # 2.15. script指标: (-)script中无效的嵌套
        self.indexid_dict[
            "2.16"] = self.script_index_runtime_max  # 2.16. script指标: (+)script最大运行时间
        self.indexid_dict[
            "2.17"] = self.script_index_runtime_mix  # 2.17. script指标: (+)script最小运行时间
        self.indexid_dict[
            "2.18"] = self.script_index_runtime_avg  # 2.18. script指标: (+)script平均运行时间

        # 3. block(2)
        self.indexid_dict[
            "3.1"] = self.block_index_totals  # 3.1. block数目: (+)block总数
        self.indexid_dict[
            "3.2"] = self.block_index_nowork  # 3.2. block数目: (-)block不能被执行的总数

        # 4. trigger(4)
        self.indexid_dict[
            "4.1"] = self.trigger_index_trigger_script_number_atworking  # 4.1. trigger: (+)工程运行时触发的script数目
        self.indexid_dict[
            "4.2"] = self.trigger_index_trigger_script_number_meanwhile  # 4.2. trigger: (+)同时触发的script数目
        self.indexid_dict[
            "4.3"] = self.trigger_index_script_running_number_meanwhile  # 4.3. trigger: (+)并发执行的最大script数目
        self.indexid_dict[
            "4.4"] = self.trigger_index_script_running_overlap_maxtime  # 4.4. trigger: (+)并发执行的script最大重叠时间

        # 5. condition(9)
        self.indexid_dict[
            "5.1"] = self.condition_index_number_ifelse  # 5.1. contain条件: (+)ifelse数目
        self.indexid_dict[
            "5.2"] = self.condition_index_number_if  # 5.2. contain条件: (+)if数目
        self.indexid_dict[
            "5.3"] = self.condition_index_nest_depth_max  # 5.3. contain条件: (+-)条件嵌套最大深度(跳过loop)
        self.indexid_dict[
            "5.4"] = self.condition_index_nest_depth_avg  # 5.4. contain条件: (+-)条件平均嵌套深度(跳过loop)
        self.indexid_dict[
            "5.5"] = self.condition_index_number_no_statement  # 5.5. contain条件: (-)if,if else下面没有block的数目
        self.indexid_dict[
            "5.6"] = self.condition_index_number_param_imcompleted  # 5.6. contain条件: (-)if条件表达式及其嵌套缺参数数目(基于嵌套顶层)
        self.indexid_dict[
            "5.7"] = self.condition_index_number_param_variables_nochanged  # 5.7. contain条件: (-)条件表达式中的变量外部不变数目(基于嵌套顶层)
        self.indexid_dict[
            "5.8"] = self.condition_index_number_true_forever  # 5.8. contain条件: (-)条件永假数目(基于嵌套顶层)
        self.indexid_dict[
            "5.9"] = self.condition_index_number_false_forever  # 5.9. contain条件: (-)条件永真数目(基于嵌套顶层)

        # 6. loop(9)
        self.indexid_dict[
            "6.1"] = self.loop_index_number_totals  # 6.1. contain循环: (+)循环数目
        self.indexid_dict[
            "6.2"] = self.loop_index_nest_depth_max  # 6.2. contain循环: (+-)循环嵌套最大深度
        self.indexid_dict[
            "6.3"] = self.loop_index_nest_depth_avg  # 6.3. contain循环: (+-)循环嵌套平均深度
        self.indexid_dict[
            "6.4"] = self.loop_index_number_cross_sprite_by_broadcast  # 6.4. contain循环: (+)基于消息(广播)的跨sprite大循环数目
        self.indexid_dict[
            "6.5"] = self.loop_index_number_cross_sprite_by_variables  # 6.5. contain循环: (+)基于消息(变量)的跨sprite大循环数目
        self.indexid_dict[
            "6.6"] = self.loop_index_number_cross_script_by_broadcast  # 6.6. contain循环: (+)基于消息(广播)的跨script大循环数目
        self.indexid_dict[
            "6.7"] = self.loop_index_number_cross_script_by_variables  # 6.7. contain循环: (+)基于消息(变量)的跨script大循环数目
        self.indexid_dict[
            "6.8"] = self.loop_index_endlessloop_nobreak  # 6.8. contain循环: (*)死循环数目(不能跳出,或者break条件永不为真)
        self.indexid_dict[
            "6.9"] = self.loop_index_endlessloop_nowait  # 6.9. contain循环: (-)死循环数目(循环体中没有阻塞)

        # 7. sequenceblock(3)
        self.indexid_dict[
            "7.1"] = self.sequenceblock_index_number_top_max  # 7.1. 顺序块: (+)一级顺序块最大数目
        self.indexid_dict[
            "7.2"] = self.sequenceblock_index_number_if_max  # 7.2. 顺序块: (+)if中的一级顺序块最大数目
        self.indexid_dict[
            "7.3"] = self.sequenceblock_index_number_loop_max  # 7.3. 顺序块: (+)loop中的一级顺序块最大数目

        # 8. clone(5)
        self.indexid_dict[
            "8.1"] = self.clone_index_number_blocks  # 8.1. 克隆: (+)克隆点数目
        self.indexid_dict[
            "8.2"] = self.clone_index_number_sprites  # 8.2. 克隆: (+)克隆sprite数量
        self.indexid_dict[
            "8.3"] = self.clone_index_number_sprites_type  # 8.3. 克隆: (+)克隆sprite类型数量
        self.indexid_dict[
            "8.4"] = self.clone_index_number_trigger_script  # 8.4. 克隆: (+)克隆sprite触发script数目
        self.indexid_dict[
            "8.5"] = self.clone_index_recursion_or_unlimited  # 8.5. 克隆: (-)是否存在递归克隆

        # 9. wait(2)
        self.indexid_dict[
            "9.1"] = self.wait_index_number  # 9.1. wait数目: (+)wait数目
        self.indexid_dict[
            "9.2"] = self.wait_index_max_waittime  # 9.2. wait数目: (+-)wait最大等待时间

        # 10. broadcast(6)
        self.indexid_dict[
            "10.1"] = self.broadcast_index_number_messageid  # 10.1. broadcast: (+)广播消息ID数目
        self.indexid_dict[
            "10.2"] = self.broadcast_index_number_sendpointer  # 10.2. broadcast: (+)广播点数目
        self.indexid_dict[
            "10.3"] = self.broadcast_index_number_sendpointer_noreach  # 10.3. broadcast: (-)广播点(不可执行到的)数目
        self.indexid_dict[
            "10.4"] = self.broadcast_index_number_recvpointer  # 10.4. broadcast: (+)广播接收点数目
        self.indexid_dict[
            "10.5"] = self.broadcast_index_number_recvpointer_noreach  # 10.5. broadcast: (-)广播接收点(不可执行到的)数目
        self.indexid_dict[
            "10.6"] = self.broadcast_index_number_rise_endless_loop  # 10.6. broadcast: (-)广播形成无效死循环(循环体中没有阻塞)数目

        # 11. logicalexpr(8)
        self.indexid_dict[
            "11.1"] = self.logicalexpr_index_number_totals  # 11.1. 逻辑表达式: (+)逻辑表达式数目
        self.indexid_dict[
            "11.2"] = self.logicalexpr_index_number_type  # 11.2. 逻辑表达式: (+)逻辑表达式种类数目
        self.indexid_dict[
            "11.3"] = self.logicalexpr_index_number_nest_depth_max  # 11.3. 逻辑表达式: (+-)逻辑表达式参数嵌套最大深度
        self.indexid_dict[
            "11.4"] = self.logicalexpr_index_number_nest_depth_avg  # 11.4. 逻辑表达式: (+-)逻辑表达式参数嵌套平均深度
        self.indexid_dict[
            "11.5"] = self.logicalexpr_index_number_true_forever  # 11.5. 逻辑表达式: (-)逻辑表达式永真数目(向上传递)
        self.indexid_dict[
            "11.6"] = self.logicalexpr_index_number_false_forever  # 11.6. 逻辑表达式: (-)逻辑表达式永假数目(向上传递)
        self.indexid_dict[
            "11.7"] = self.logicalexpr_index_number_param_imcompleted  # 11.7. 逻辑表达式: (-)逻辑表达式缺参数数目(向上传递)
        self.indexid_dict[
            "11.8"] = self.logicalexpr_index_number_variables_nochanged  # 11.8. 逻辑表达式: (-)逻辑表达式变量外部不变数目(向上传递)

        # 12. globalvar(11)
        self.indexid_dict[
            "12.1"] = self.globalvar_index_number_totals  # 12.1. 全局变量: (+)使用数目
        self.indexid_dict[
            "12.2"] = self.globalvar_index_number_modified  # 12.2. 全局变量: (+)更改数目
        self.indexid_dict[
            "12.3"] = self.globalvar_index_number_cross_sprite  # 12.3. 全局变量: (+)跨sprite使用数目
        self.indexid_dict[
            "12.4"] = self.globalvar_index_number_trigger_script  # 12.4. 全局变量: (+)触发script数目
        self.indexid_dict[
            "12.5"] = self.globalvar_index_number_control_loop  # 12.5. 全局变量: (+)变量控制的循环数目
        self.indexid_dict[
            "12.6"] = self.globalvar_index_number_control_condition  # 12.6. 全局变量: (+)变量控制的条件数目
        self.indexid_dict[
            "12.7"] = self.globalvar_index_number_changed_pointer  # 12.7. 全局变量: (+)变量修改点数目
        self.indexid_dict[
            "12.8"] = self.globalvar_index_number_changed_pointer_noreach  # 12.8. 全局变量: (-)变量修改点(不可执行到的)数目
        self.indexid_dict[
            "12.9"] = self.globalvar_index_number_check_pointer  # 12.9. 全局变量: (+)变量检测点数目(script头)
        self.indexid_dict[
            "12.10"] = self.globalvar_index_number_check_pointer_noreach  # 12.10. 全局变量: (-)变量检测点(不可执行到的)数目(script头)
        self.indexid_dict[
            "12.11"] = self.globalvar_index_number_rise_endless_loop  # 12.11. 全局变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目

        # 13. localvar(10)
        self.indexid_dict[
            "13.1"] = self.localvar_index_number_totals  # 13.1. 局部变量: (+)使用数目
        self.indexid_dict[
            "13.2"] = self.localvar_index_number_modified  # 13.2. 局部变量: (+)更改数目
        self.indexid_dict[
            "13.3"] = self.localvar_index_number_trigger_script  # 13.3. 局部变量: (+)触发script数目
        self.indexid_dict[
            "13.4"] = self.localvar_index_number_control_loop  # 13.4. 局部变量: (+)变量控制的循环数目
        self.indexid_dict[
            "13.5"] = self.localvar_index_number_control_condition  # 13.5. 局部变量: (+)变量控制的条件数目
        self.indexid_dict[
            "13.6"] = self.localvar_index_number_changed_pointer  # 13.6. 局部变量: (+)变量修改点数目
        self.indexid_dict[
            "13.7"] = self.localvar_index_number_changed_pointer_noreach  # 13.7. 局部变量: (-)变量修改点(不可执行到的)数目
        self.indexid_dict[
            "13.8"] = self.localvar_index_number_check_pointer  # 13.8. 局部变量: (+)变量检测点数目(script头)
        self.indexid_dict[
            "13.9"] = self.localvar_index_number_check_pointer_noreach  # 13.9. 局部变量: (-)变量检测点(不可执行到的)数目(script头)
        self.indexid_dict[
            "13.10"] = self.localvar_index_number_rise_endless_loop  # 13.10. 局部变量: (-)变量控制形成无效死循环(循环体中没有阻塞)数目

        # 14. interaction(11)
        self.indexid_dict[
            "14.1"] = self.interaction_index_number_keyboard_sprite  # 14.1. 交互: (+)键盘:处理sprite数目
        self.indexid_dict[
            "14.2"] = self.interaction_index_number_keyboard_checkpointer  # 14.2. 交互: (+)键盘:处理点数目
        self.indexid_dict[
            "14.3"] = self.interaction_index_number_keyboard_checkpointer_useless  # 14.3. 交互: (-)键盘:无效处理点数目
        self.indexid_dict[
            "14.4"] = self.interaction_index_number_joystick_sprite  # 14.4. 交互: (+)手柄:处理sprite数目
        self.indexid_dict[
            "14.5"] = self.interaction_index_number_joystick_checkpointer  # 14.5. 交互: (+)手柄:处理点数目
        self.indexid_dict[
            "14.6"] = self.interaction_index_number_joystick_checkpointer_useless  # 14.6. 交互: (-)手柄:无效处理点数目
        self.indexid_dict[
            "14.7"] = self.interaction_index_number_mouse_sprite  # 14.7. 交互: (+)鼠标:处理sprite数目
        self.indexid_dict[
            "14.8"] = self.interaction_index_number_mouse_checkpointer  # 14.8. 交互: (+)鼠标:处理点数目
        self.indexid_dict[
            "14.9"] = self.interaction_index_number_mouse_checkpointer_useless  # 14.9. 交互: (-)鼠标:无效处理点数目
        self.indexid_dict[
            "14.10"] = self.interaction_index_number_user_inputpointer  # 14.10. 交互: (+)用户输入点数目
        self.indexid_dict[
            "14.11"] = self.interaction_index_number_user_inputprompt  # 14.11. 交互: (+)用户输入提示频率

        # 15. phycharacteristics(4)
        self.indexid_dict[
            "15.1"] = self.phycharacteristics_index_number_sripte_open_engine  # 15.1. 物理特性: (+)开启物理引擎的sprite数目
        self.indexid_dict[
            "15.2"] = self.phycharacteristics_index_number_sripte_open_engine_useless  # 15.2. 物理特性: (-)开启物理特性动作能否执行到
        self.indexid_dict[
            "15.3"] = self.phycharacteristics_index_number_blocks_in_engine_windows  # 15.3. 物理特性: (+)物理引擎窗口内受制block数目
        self.indexid_dict[
            "15.4"] = self.phycharacteristics_index_number_blocks_out_engine_wondows  # 15.4. 物理特性: (-)物理引擎窗口外受制block数目

        # 16. phyaction(12)
        self.indexid_dict[
            "16.1"] = self.phyaction_index_moving_sprite_type_number  # 16.1. 物理行为: (+)移动的sprite数目
        self.indexid_dict[
            "16.2"] = self.phyaction_index_moving_sprite_blocks  # 16.2. 物理行为: (+)移动的sprite指令块数目
        self.indexid_dict[
            "16.3"] = self.phyaction_index_moving_sprite_blocks_useless  # 16.3. 物理行为: (-)移动的sprite指令块数目(不能执行到)
        self.indexid_dict[
            "16.4"] = self.phyaction_index_moving_sprite_times  # 16.4. 物理行为: (+)移动的sprite次数
        self.indexid_dict[
            "16.5"] = self.phyaction_index_rotate_sprite_type_number  # 16.5. 旋转行为: (+)移动的sprite数目
        self.indexid_dict[
            "16.6"] = self.phyaction_index_rotate_sprite_blocks  # 16.6. 旋转行为: (+)移动的sprite指令块数目
        self.indexid_dict[
            "16.7"] = self.phyaction_index_rotate_sprite_blocks_useless  # 16.7. 旋转行为: (-)移动的sprite指令块数目(不能执行到)
        self.indexid_dict[
            "16.8"] = self.phyaction_index_rotate_sprite_times  # 16.8. 物理行为: (+)旋转的sprite次数
        self.indexid_dict[
            "16.9"] = self.phyaction_index_play_animation_sprite_type_number  # 16.9. 物理行为: (+)播放动画效果的sprite数目
        self.indexid_dict[
            "16.10"] = self.phyaction_index_play_animation_sprite_blocks  # 16.10. 物理行为: (+)播放动画效果的sprite指令块数目
        self.indexid_dict[
            "16.11"] = self.phyaction_index_play_animation_sprite_blocks_useless  # 16.11. 物理行为: (-)播放动画效果的sprite指令块数目(不能执行到)
        self.indexid_dict[
            "16.12"] = self.phyaction_index_play_animation_sprite_times  # 16.12. 物理行为: (+)播放动画效果的sprite次数

        # 17. objsetting(22)
        self.indexid_dict[
            "17.1"] = self.objsetting_index_number_del_sprite  # 17.1. 物体设置: (+)删除sprite数目
        self.indexid_dict[
            "17.2"] = self.objsetting_index_number_del_sprite_blocks  # 17.2. 物体设置: (+)删除sprite指令块数目
        self.indexid_dict[
            "17.3"] = self.objsetting_index_number_del_sprite_blocks_noreach  # 17.3. 物体设置: (-)删除sprite指令块数目(不能执行到)
        self.indexid_dict[
            "17.4"] = self.objsetting_index_number_show_sprite  # 17.4. 物体设置: (+)显示sprite数目
        self.indexid_dict[
            "17.5"] = self.objsetting_index_number_show_sprite_blocks  # 17.5. 物体设置: (+)显示sprite指令块数目
        self.indexid_dict[
            "17.6"] = self.objsetting_index_number_show_sprite_blocks_noreach  # 17.6. 物体设置: (-)显示sprite指令块数目(不能执行到)
        self.indexid_dict[
            "17.7"] = self.objsetting_index_number_hide_sprite  # 17.7. 物体设置: (+)影藏sprite数目
        self.indexid_dict[
            "17.8"] = self.objsetting_index_number_hide_sprite_blocks  # 17.8. 物体设置: (+)影藏sprite指令块数目
        self.indexid_dict[
            "17.9"] = self.objsetting_index_number_hide_sprite_blocks_noreach  # 17.9. 物体设置: (-)影藏sprite指令块数目(不能执行到)
        self.indexid_dict[
            "17.10"] = self.objsetting_index_number_group  # 17.10. 物体设置: (+)父子关系团数目
        self.indexid_dict[
            "17.11"] = self.objsetting_index_number_group_max_unit  # 17.11. 物体设置: (+)父子团最大sprite数目
        self.indexid_dict[
            "17.12"] = self.objsetting_index_number_group_avg_unit  # 17.12. 物体设置: (+)父子团平均sprite数目
        self.indexid_dict[
            "17.13"] = self.objsetting_index_number_group_moving  # 17.13. 物体设置: (+)父子团移动数目
        self.indexid_dict[
            "17.14"] = self.objsetting_index_number_group_not_moving  # 17.14. 物体设置: (-)父子团不移动数目
        self.indexid_dict[
            "17.15"] = self.objsetting_index_number_group_rotate  # 17.15. 物体设置: (+)父子团旋转数目
        self.indexid_dict[
            "17.16"] = self.objsetting_index_number_group_not_rotate  # 17.16. 物体设置: (-)父子团不旋转数目
        self.indexid_dict[
            "17.17"] = self.objsetting_index_number_group_play_animation  # 17.17. 物体设置: (+)父子团播放动作数目
        self.indexid_dict[
            "17.18"] = self.objsetting_index_number_group_not_play_animation  # 17.18. 物体设置: (-)父子团不播放动作数目
        self.indexid_dict[
            "17.19"] = self.objsetting_index_number_group_show  # 17.19. 物体设置: (+)父子团子sprite显示数目
        self.indexid_dict[
            "17.20"] = self.objsetting_index_number_group_hide  # 17.20. 物体设置: (+)父子团子sprite影藏数目
        self.indexid_dict[
            "17.21"] = self.objsetting_index_number_group_packaged_dynamically  # 17.21. 物体设置: (+)父子团子sprite动态组团数目
        self.indexid_dict[
            "17.22"] = self.objsetting_index_number_group_unpackaged_dynamically  # 17.22. 物体设置: (+)父子团子sprite动态拆分数目

        # 18. music(5)
        self.indexid_dict[
            "18.1"] = self.music_index_number_play_pointer  # 18.1. 音乐: (+)音乐播放数目
        self.indexid_dict[
            "18.2"] = self.music_index_number_play_pointer_noreach  # 18.2. 音乐: (-)不能被播放数目
        self.indexid_dict[
            "18.3"] = self.music_index_number_play_songs  # 18.3. 音乐: (+)音乐播放曲目数目
        self.indexid_dict[
            "18.4"] = self.music_index_number_play_pointer_param_incompleted  # 18.4. 音乐: (-)缺少参数数目
        self.indexid_dict[
            "18.5"] = self.music_index_number_stop_pointer  # 18.5. 音乐: (+)主动停止数目

        # 0.无
        self.indexid_dict["0.0"] = self.no_gramer


# 评分规则 0-1
class ScoreGradeSubjectivity:
    def __init__(self):
        self.rule = [["趣味性", 0.2, 100, 0], ["美观性", 0.2, 100, 0],
                     ["创意性", 0.2, 100, 0], ["完整性", 0.2, 100, 0],
                     ["流畅性", 0.2, 100, 0]]

    def set_subscore(self, subscore_list):
        if len(self.rule) != len(subscore_list):
            return 1
        for i in range(len(self.rule)):
            self.rule[i][3] = subscore_list[i]

        return 0

    def calculate_score(self):
        total_score = 0.0
        for i in range(len(self.rule)):
            total_score += (self.rule[i][1] * self.rule[i][3])
        return total_score


# 评分规则 1-0
# [ ["ct-subentity", persent,[score,{}],[score,{}],[score,{}],score], ... ,]
class ScoreGradeObjectivity1:
    def __init__(self, course_id):
        self.course_id = course_id
        self.rule = get_all_rule(self.course_id)

    def calculate_score_with_balance(self, dict_block_dist):
        alpha1 = 0.9
        alpha2 = 0.7
        alpha3 = 0.5
        beta1 = 0.7
        beta2 = 0.9
        beta3 = 0.9
        gama1 = 0.5
        gama2 = 0.5
        gama3 = 0.7
        delta = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        # delta1 = 0.8 # abstraction and problem decomposition
        # delta2 = 0.8 # parallelism
        # delta3 = 0.8 # logical thinking
        # delta4 = 0.8 # synchronization
        # delta5 = 0.8 # algorithmic notions of flow control
        # delta6 = 0.8 # user interactivity
        # delta7 = 0.8 # data representation
        # delta8 = 0.8 # visual and auditory sense related

        # 规则:
        # 1. 组内分值自动调整规则;
        # 1.1. 三项都没有 --> 0,组内不调整
        # 1.2. 一项没有:
        #      没有[入门]: alpha1 = 90%, [成长][熟练]都有,[入门]贡献原有值的 90%;
        #      没有[成长]: alpha2 = 70%, [入门][熟练]都有,[成长]贡献原有值的 70%;
        #      没有[熟练]: alpha3 = 50%, [入门][成长]都有,[熟练]贡献原有值的 50%;
        # 1.3. 两项没有:
        #      只有[入门]: beta1  = 70%, gama1 = 50%, [成长]贡献原有值的 70%, [熟练]贡献原有值的 50%;
        #      只有[成长]: beta2  = 90%, gama2 = 50%, [入门]贡献原有值的 90%, [熟练]贡献原有值的 50%;
        #      只有[熟练]: beta3  = 90%, gama3 = 70%, [入门]贡献原有值的 90%, [成长]贡献原有值的 70%;
        # 1.4. 三项都有,不调整;
        # 2. 组间百分比自动调整规则;
        #    注: 只对8项中为0的项的占比进行分配;
        #      delta1 = 80% # abstraction and problem decomposition,占比的80%按照比例分配给其他非0项;
        #      delta2 = 80% # parallelism,                          占比的80%按照比例分配给其他非0项;
        #      delta3 = 80% # logical thinking,                     占比的80%按照比例分配给其他非0项;
        #      delta4 = 80% # synchronization,                      占比的80%按照比例分配给其他非0项;
        #      delta5 = 80% # algorithmic notions of flow control,  占比的80%按照比例分配给其他非0项;
        #      delta6 = 80% # user interactivity,                   占比的80%按照比例分配给其他非0项;
        #      delta7 = 80% # data representation,                  占比的80%按照比例分配给其他非0项;
        #      delta8 = 80% # visual and auditory sense related,    占比的80%按照比例分配给其他非0项;

        # dict_block_dist 每种块的数目[总数,有效数目,无效数目])
        block_set = set()
        for key in dict_block_dist:
            if dict_block_dist[key][0] > 0:
                block_set.add(key)
        # # [ ["ct-subentity", persent,[score,{}],[score,{}],[score,{}],score], ... ,]
        total_score = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(len(self.rule)):
            hit1 = False
            hit2 = False
            hit3 = False
            if 0 != len(self.rule[i][2][1] & block_set):
                hit1 = True
                self.rule[i][5] += self.rule[i][2][0]
            if 0 != len(self.rule[i][3][1] & block_set):
                hit2 = True
                self.rule[i][5] += self.rule[i][3][0]
            if 0 != len(self.rule[i][4][1] & block_set):
                hit3 = True
                self.rule[i][5] += self.rule[i][4][0]

            # 1. 组内分值自动调整
            # 1.2. 一项没有:
            #  没有[入门]: alpha1 = 90%, [成长][熟练]都有,[入门]贡献原有值的 90%;
            if False == hit1 and True == hit2 and True == hit3:
                self.rule[i][5] += (self.rule[i][2][0] * alpha1)
            #  没有[成长]: alpha2 = 70%, [入门][熟练]都有,[成长]贡献原有值的 70%;
            if True == hit1 and False == hit2 and True == hit3:
                self.rule[i][5] += (self.rule[i][3][0] * alpha2)
            #  没有[熟练]: alpha3 = 50%, [入门][成长]都有,[熟练]贡献原有值的 50%;
            if True == hit1 and True == hit2 and False == hit3:
                self.rule[i][5] += (self.rule[i][4][0] * alpha3)
            # 1.3. 两项没有:
            #  只有[入门]: beta1  = 70%, gama1 = 50%, [成长]贡献原有值的 70%, [熟练]贡献原有值的 50%;
            if True == hit1 and False == hit2 and False == hit3:
                self.rule[i][5] += (self.rule[i][3][0] * beta1)
                self.rule[i][5] += (self.rule[i][4][0] * gama1)
            #  只有[成长]: beta2  = 90%, gama2 = 50%, [入门]贡献原有值的 90%, [熟练]贡献原有值的 50%;
            if False == hit1 and True == hit2 and False == hit3:
                self.rule[i][5] += (self.rule[i][2][0] * beta2)
                self.rule[i][5] += (self.rule[i][4][0] * gama2)
            #  只有[熟练]: beta3  = 90%, gama3 = 70%, [入门]贡献原有值的 90%, [成长]贡献原有值的 70%;
            if False == hit1 and False == hit2 and True == hit3:
                self.rule[i][5] += (self.rule[i][2][0] * beta3)
                self.rule[i][5] += (self.rule[i][3][0] * gama3)

            total_score[i] = self.rule[i][5]

        # 2. 组间百分比自动调整规则,重新调整后的实际比例实际小于 100%, 因为有 alpha,beta,gama等因子;
        persent2redistribution = 0.0
        persent2adjustment = 0.0
        for i in range(8):
            if 0.0 == total_score[i]:
                persent2redistribution += (self.rule[i][1] * delta[i])
            else:
                persent2adjustment += self.rule[i][1]
        if 0.0 != persent2adjustment:
            for i in range(8):
                if 0.0 != total_score[i]:
                    self.rule[i][1] = self.rule[i][
                                          1] + persent2redistribution * self.rule[i][
                                          1] / persent2adjustment
                    total_score[8] += (self.rule[i][5] * self.rule[i][1])
                else:
                    self.rule[i][1] = self.rule[i][1] * (1 - delta[i])

        return total_score

    def calculate_score(self, dict_block_dist):
        # dict_block_dist 每种块的数目[总数,有效数目,无效数目])
        block_set = set()
        for key in dict_block_dist:
            if dict_block_dist[key][0] > 0:
                block_set.add(key)
        # # [ ["ct-subentity", persent,[score,{}],[score,{}],[score,{}],score], ... ,]
        total_score = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(len(self.rule)):
            if 0 != len(self.rule[i][2][1] & block_set):
                self.rule[i][5] += self.rule[i][2][0]
            if 0 != len(self.rule[i][3][1] & block_set):
                self.rule[i][5] += self.rule[i][3][0]
            if 0 != len(self.rule[i][4][1] & block_set):
                self.rule[i][5] += self.rule[i][4][0]
            total_score[i] = self.rule[i][5]
            total_score[8] += self.rule[i][5] * self.rule[i][1]

        return total_score


# 评分规则 1-1
class ScoreGradeObjectivity2:
    def __init__(self, course_id):  # 2019/12/05 扣分项去掉占比
        # 根据不同的 dimension_id 获取相应的指标参数
        self.rule_abstraction = get_rule_data(course_id, "1")

        self.rule_parallelism = get_rule_data(course_id, "2")

        self.rule_logical = get_rule_data(course_id, "3")

        self.rule_sync = get_rule_data(course_id, "4")

        self.rule_flowcontrol = get_rule_data(course_id, "5")
        # 手柄 + 用户输入 = 键盘 + 鼠标 + 用户输入
        self.rule_userinteractivity = get_rule_data(course_id, "6")

        self.rule_datarepresentation = get_rule_data(course_id, "7")

        self.rule_va = get_rule_data(course_id, "8")

        # 重大减分项
        grammer_persent = get_persent(course_id, "g")
        self.rule = [[grammer_persent[0], self.rule_abstraction, 0.0],
                     [grammer_persent[1], self.rule_parallelism, 0.0],
                     [grammer_persent[2], self.rule_logical, 0.0],
                     [grammer_persent[3], self.rule_sync, 0.0],
                     [grammer_persent[4], self.rule_flowcontrol, 0.0],
                     [grammer_persent[5], self.rule_userinteractivity, 0.0],
                     [grammer_persent[6], self.rule_datarepresentation, 0.0],
                     [grammer_persent[7], self.rule_va, 0.0]]

    def calculate_score_with_balance_and_deduction(self, ct_index):
        #  规则:
        #    1. 第一层百分比自动调整规则;
        #       注: 只对8项中为0的项的占比进行分配;
        #       alpha[0] = 80% # abstraction and problem decomposition,占比的80%按照比例分配给其他非0项;
        #       alpha[1] = 80% # parallelism,                          占比的80%按照比例分配给其他非0项;
        #       alpha[2] = 80% # logical thinking,                     占比的80%按照比例分配给其他非0项;
        #       alpha[3] = 80% # synchronization,                      占比的80%按照比例分配给其他非0项;
        #       alpha[4] = 80% # algorithmic notions of flow control,  占比的80%按照比例分配给其他非0项;
        #       alpha[5] = 80% # user interactivity,                   占比的80%按照比例分配给其他非0项;
        #       alpha[6] = 80% # data representation,                  占比的80%按照比例分配给其他非0项;
        #       alpha[7] = 80% # visual and auditory sense related,    占比的80%按照比例分配给其他非0项;
        #    2. 第二层百分比自动调整规则;
        #       注: 每一项(8项)为0的子项(占比为0的项不进行均衡)的占比进行分配;
        #       beta[0] = 90% # abstraction and problem decomposition,所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[1] = 90% # parallelism,                          所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[2] = 90% # logical thinking,                     所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[3] = 90% # synchronization,                      所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[4] = 90% # algorithmic notions of flow control,  所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[5] = 90% # user interactivity,                   所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[6] = 90% # data representation,                  所有0分子项占比的90%按照比例分配给其他非0项;
        #       beta[7] = 90% # visual and auditory sense related,    所有0分子项占比的90%按照比例分配给其他非0项;

        alpha = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        beta = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]

        score = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        score1 = 0.0
        for i in range(len(self.rule)):  # 8大子项
            score2 = 0.0
            score3_list = []
            for j in range(
                    len(self.rule[i][1])
            ):  # 每个 ["xxx",0.x,["17.1","+", "删除sprite数目",0.05,  [70,">",0,0], [85,">",0,0],[100,">",0,0]],...,]
                score3 = 0.0
                for k in range(
                        len(self.rule[i][1][j])
                ):  # ["17.1","+", "删除sprite数目",0.05,  [70,">",0,0], [85,">",0,0],[100,">",0,0]]
                    if k < 2:
                        continue
                    # self.rule[i][1][j][k][0] --> key:"17.1"
                    pattern = re.compile(r'^(\-|\+)?\d+(\.\d+)?')
                    str = self.rule[i][1][j][k][0]
                    re_obj = pattern.search(str)
                    index_name = re_obj.group(0)
                    index_value = ct_index.indexid_dict[index_name]
                    if "11.2" == index_name:  # [0,0,0,0,0] # 11.2. 逻辑表达式: (+)逻辑表达式种类数目
                        index_value = index_value[0] + index_value[1] + index_value[2] + index_value[3] + index_value[4]
                    score4 = 0.0
                    while True:
                        if "+" == self.rule[i][1][j][k][1] or "+-" == self.rule[i][1][j][k][1]:  # 从后向前检查,优先得高分
                            # first
                            if index_value > self.rule[i][1][j][k][4][2]:
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            elif index_value == self.rule[i][1][j][k][4][2]:
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            elif index_value >= self.rule[i][1][j][k][4][2] and index_value <= self.rule[i][1][j][k][4][3]:
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            elif "o" == self.rule[i][1][j][k][4][1]:  # others
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            else:
                                pass
                            # second
                            if index_value > self.rule[i][1][j][k][3][2]:
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            elif index_value == self.rule[i][1][j][k][3][2]:
                                score4 = self.rule[i][1][j][k][5][0]
                                break
                            elif index_value >= self.rule[i][1][j][3][3][2] and index_value <= self.rule[i][1][j][k][3][2]:
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            elif "o" == self.rule[i][1][j][k][5][1]:  # others
                                score4 = self.rule[i][1][j][k][5][0]
                                break
                            else:
                                pass
                            # last
                            if index_value > self.rule[i][1][j][k][3][1]:
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            elif index_value == self.rule[i][1][j][k][3][1]:
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            elif index_value >= self.rule[i][1][j][k][3][1] and index_value <= self.rule[i][1][j][k][3][2]:
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            elif "o" == self.rule[i][1][j][k][3][1]:  # others
                                score4 = self.rule[i][1][j][k][3][0]
                                break
                            else:
                                pass
                            break
                        else:
                            break
                    # end: while
                    # socre4是底层指标的得分
                    # 1.1.(+)sprite总数(50%)	>2	70	>10	85	>20	100
                    score4 = score4 * self.rule[i][1][j][k][2]  # 乘以权重
                    score3 += score4
                # end: for k in range(len(self.rule[i][1][j])):
                # socre3 是一个分项指标的得分
                # sprite指标: (20%)
                score3 *= 1.0
                score3_list.append([score3, self.rule[i][1][j][1]])
            # end: for j in range(len(self.rule[i][1]))
            # 均衡第二层
            persent2redistribution = 0.0
            persent2adjustment = 0.0
            for m in range(len(score3_list)):
                if 0.0 == score3_list[m][0]:
                    persent2redistribution += (score3_list[m][1] * beta[i])
                else:
                    persent2adjustment += score3_list[m][1]
            if 0.0 != persent2adjustment:
                for m in range(len(score3_list)):
                    if 0.0 != score3_list[m][0]:
                        score2 += (
                                score3_list[m][0] *
                                (score3_list[m][1] + persent2redistribution *
                                 score3_list[m][1] / persent2adjustment))

            score[i] = score2
            self.rule[i][2] = score2
        # end: for i in range(len(self.rule))

        # 均衡第一层
        persent2redistribution = 0.0
        persent2adjustment = 0.0
        for i in range(8):
            if 0.0 == score[i]:
                persent2redistribution += (self.rule[i][0] * alpha[i])
            else:
                persent2adjustment += self.rule[i][0]
        if 0.0 != persent2adjustment:
            for i in range(8):
                if 0.0 != score[i]:
                    self.rule[i][0] = self.rule[i][
                                          0] + persent2redistribution * self.rule[i][
                                          0] / persent2adjustment
                    score1 += (score[i] * self.rule[i][0])
                else:
                    self.rule[i][0] = self.rule[i][0] * (1 - alpha[i])
        score[8] = score1

        return score

    def calculate_score(self, ct_index):  # 2019/12/04 扣分项通过修改参数表比重为0.0,不再计入分值
        DEFAULT_MIN_SCORE = 30.0
        score = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        score1 = 0.0
        for i in range(len(self.rule)):  # 8大子项
            score2 = 0.0
            for j in range(
                    len(self.rule[i][1])
            ):  # 每个 ["xxx",0.x,["17.1","+", "删除sprite数目",0.05,  [70,">",0,0], [85,">",0,0],[100,">",0,0]],...,]
                score3 = 0.0
                for k in range(
                        len(self.rule[i][1][j])
                ):  # ["17.1","+", "删除sprite数目",0.05,  [70,">",0,0], [85,">",0,0],[100,">",0,0]]
                    if k < 2:
                        continue
                    # self.rule[i][1][j][k][0] --> key:"17.1"
                    index_name = re.match(r"^(\-|\+)?\d+(\.\d+)?", self.rule[i][1][j][k][0])
                    index_value = ct_index.indexid_dict[index_name]
                    if "11.2" == self.rule[i][1][j][k][
                        0]:  # [0,0,0,0,0] # 11.2. 逻辑表达式: (+)逻辑表达式种类数目
                        index_value = index_value[0] + index_value[
                            1] + index_value[2] + index_value[3] + index_value[
                                          4]
                    score4 = 0.0
                    while True:
                        if "+" == self.rule[i][1][j][k][1] or "+-" == self.rule[i][1][j][k][1]:  # 从后向前检查,优先得高分
                            # first
                            if ">" == self.rule[i][1][j][k][6][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][6][2]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][6][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][6][2]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][6][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][6][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][6][3]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][6][1]:  # others
                                score4 = self.rule[i][1][j][k][6][0]
                                break
                            else:
                                pass
                            # second
                            if ">" == self.rule[i][1][j][k][5][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][5][2]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][5][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][5][2]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][5][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][5][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][5][3]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][5][1]:  # others
                                score4 = self.rule[i][1][j][k][5][0]
                                break
                            else:
                                pass
                            # last
                            if ">" == self.rule[i][1][j][k][4][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][4][2]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][4][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][4][2]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][4][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][4][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][4][3]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][4][1]:  # others
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            else:
                                pass
                            if 5 != i:  # 交互不给最低分,允许得 0 分
                                score4 = DEFAULT_MIN_SCORE
                            break
                        elif "-" == self.rule[i][1][j][k][
                            1]:  # 从前向后检查,优先得低分; 2019/12/05 扣分项不在此处作,占比统一调整为0
                            # first
                            if ">" == self.rule[i][1][j][k][4][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][4][2]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][4][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][4][2]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][4][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][4][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][4][3]:
                                    score4 = self.rule[i][1][j][k][4][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][4][1]:  # others
                                score4 = self.rule[i][1][j][k][4][0]
                                break
                            else:
                                pass
                            # second
                            if ">" == self.rule[i][1][j][k][5][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][5][2]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][5][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][5][2]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][5][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][5][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][5][3]:
                                    score4 = self.rule[i][1][j][k][5][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][5][1]:  # others
                                score4 = self.rule[i][1][j][k][5][0]
                                break
                            else:
                                pass
                            # last
                            if ">" == self.rule[i][1][j][k][6][1]:  # 大于
                                if index_value > self.rule[i][1][j][k][6][2]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "=" == self.rule[i][1][j][k][6][1]:  # 等于
                                if index_value == self.rule[i][1][j][k][6][2]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "r" == self.rule[i][1][j][k][6][1]:  # 区间
                                if index_value >= self.rule[i][1][j][k][6][
                                    2] and index_value <= self.rule[i][1][
                                    j][k][6][3]:
                                    score4 = self.rule[i][1][j][k][6][0]
                                    break
                            elif "o" == self.rule[i][1][j][k][6][1]:  # others
                                score4 = self.rule[i][1][j][k][6][0]
                                break
                            else:
                                pass
                            break
                        else:
                            break
                    # end: while
                    score4 = score4 * self.rule[i][1][j][k][3]  # 乘以权重
                    score3 += score4
                # end: for k in range(len(self.rule[i][1][j])):
                score3 = score3 * self.rule[i][1][j][1]
                score2 += score3
            # end: for j in range(len(self.rule[i][1]))
            score[i] = score2
            self.rule[i][2] = score2
            score2 = score2 * self.rule[i][0]
            score1 += score2
        # end: for i in range(len(self.rule))
        score[8] = score1

        return score
