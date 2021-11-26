import logging
import json

from handlers.base import BaseHandler

from get_sql import get_course_list
from ParseGameObject import Parser


class EvaluateHandler(BaseHandler):  # 继承base.py中的类BaseHandler
    def post(self):
        data = self.request.body.decode('utf-8')
        print(data)
        g_data = json.loads(data)
        table_id = g_data["table_id"]
        course_id = g_data["course_id"]
        logging.info("课程id：%s, 课程表名：%s" % (course_id, table_id))
        if not (table_id and course_id):
            self.return_data = {"code": 400, "msg": "错误的课程信息", "data": ""}
            self.write(self.return_data)

        report = Parser()
        course_content = get_course_list(table_id)
        if course_content:
            get_report, msg = report.ParseGame(course_content, course_id)
            print(get_report)
            if get_report:
                logging.info(get_report)
                self.return_data["data"] = get_report
            else:
                self.return_data["code"] = 400
                self.return_data["msg"] = f"{msg}, 请联系管理员"
            self.write(self.return_data)
        else:
            self.return_data = {"code": 400, "msg": "错误的课程信息", "data": ""}
            self.write(self.return_data)
