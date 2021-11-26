from methods.DBManager import DBManager
import logging
import re


class StringReplacer:
    def __init__(self, replacements, ignore_case=False):
        patterns = sorted(replacements, key=len, reverse=True)
        self.replacements = [replacements[k] for k in patterns]
        re_mode = re.IGNORECASE if ignore_case else 0
        self.pattern = re.compile(
            '|'.join(("({})".format(p) for p in patterns)), re_mode)

        def tr(matcher):
            index = next((index for index, value in enumerate(matcher.groups()) if value), None)
            return self.replacements[index]

        self.tr = tr

    def __call__(self, string):
        return self.pattern.sub(self.tr, string)


dimension_list = [
    'abstraction and problem decomposition',
    'parallelism',
    'logical thinking',
    'synchronization',
    'algorithmic notions of flow control',
    'user interactivity',
    'data representation',
    'visual auditory'
]

str_dict = {
    "<2c>": ",",
    "<2e>": ".",
    "<2f>": "/",
    "<2d>": "-",
    "<2b>": "+",
    "<3d>": "=",
    "<5b>": "[",
    "<efbc81>": "！",
    "<21>": "!",
    "<efbc9a>": "：",
    "<3a>": ":",
    "<3b>": ";",
    "<efbc9b>": "；",
    "<e2809c>": "“",
    "<e28098>": "‘",
    "<e28099>": "’",
    "<27>": "'",
    "<e2809d>": "”",
    "<3f>": "?",
    "<efbd9f>": "？",
    "<e38090>": "【",
    "<e38091>": "】",
    "<7b>": "{",
    "<7d>": "}",
    "<29>": ")",
    "<efbc8c>": "，",
    "<e38082>": "。",
    "<e38081>": "、",
    "<2a>": "*",
    "<5d>": "]",
    "<40>": "@",
    "<23>": "#",
    "<25>": "%",
    "<5e>": "^",
    "<26>": "&",
    "<5f>": "_",
    "<5c>": "\\",
    "<24>": "$",
}


def get_course_list(table_name):
    DB = DBManager()
    sql = f"select * from {table_name}"
    data = DB.fetchall(sql)
    DB.destroy()
    l1 = []
    if data:
        for i in data:
            # 红气球&90201&0&&1@6@-375,450,0@D:2|I1:3@@~2@102@@@5$4@~3@46@@@5$15@&0,400&*
            l1.append(i[2] + "&" + str(i[1]) + "&0&&" +
                      str(i[15], encoding="utf-8"))
        s1 = "*".join(l1)
        s1 = "^C:1|G:1^" + s1
        return s1
    else:
        return 0


def get_rule_data(course_id, dimension_id):
    DB = DBManager()
    sql = """
    select t.name, g.type_percent, g.quota_id
    from eval_dimension_grammar as g
    inner join eval_grammar_type as t
    where g.course_id = %s
    and g.dimension_id = %s
    and g.type_id = t.id
    order by g.dimension_id;
    """
    data = DB.fetchall(sql, params=(course_id, dimension_id))
    DB.destroy()
    rule_list = []
    for i in data:
        sub_rule_list = [i[0], i[1]]
        sql1 = """
        select
        quota_name, add_subtr_mark, quota_precent,
        primary_rule, middle_rule, senior_rule
        from eval_grammar_quota_standard
        where id in (%s);
        """ % i[2]
        data1 = DB.fetchall(sql1)
        [
            sub_rule_list.append(
                [j[0], j[1], j[2],
                eval(j[3]),
                eval(j[4]),
                eval(j[5])]) for j in data1
        ]
        rule_list.append(sub_rule_list)
    return rule_list


def get_persent(course_id, p_type):
    sql = """
    select
    {0}_abstraction_percent,
    {0}_parallelism_percent,
    {0}_logical_percent,
    {0}_sync_percent,
    {0}_flow_percent,
    {0}_interactivity_percent,
    {0}_data_percent,
    {0}_visual_percent
    from eval_dimension_course where course_id = %s;
    """.format(p_type)
    DB = DBManager()
    data = DB.fetchone(sql, params=course_id)
    DB.destroy()
    return data


def get_block_score(dimension_name, course_id, dimension_id, percent_list):
    level_list = [
        dimension_name,
        percent_list[dimension_id-1],
        [0, set()],
        [0, set()],
        [0, set()]
    ]
    DB = DBManager()
    sql = """
    select course_id, level, level_score, contain_block
    from eval_dimension_score
    where course_id = %s
    and dimension_id = %s
    order by dimension_id, level;
    """
    data = DB.fetchall(sql, params=(course_id, dimension_id))
    sub_index = 2
    if data:
        for i in data:
            if i[-1]:
                block_list = i[-1].split(",")
                block_set = set([int(j) for j in block_list])
                level_list[sub_index][0] = int(i[-2])
                level_list[sub_index][1] = block_set
            sub_index += 1
    DB.destroy()
    level_list.append(0.0)
    return level_list


def get_all_rule(course_id):
    rule = []
    percent_list = get_persent(course_id, "b")
    for i in range(1, 9):
        data = get_block_score(dimension_list[i-1], course_id, i, percent_list)
        rule.append(data)
    return rule


def str_replace(source):
    replacer = StringReplacer(str_dict, True)
    return replacer(source)


if __name__ == "__main__":
    # print(get_rule_data("63_318_1", "1"))
    get_course_list("tb_obj_1465_10018")
    get_all_rule("63_318_1")
