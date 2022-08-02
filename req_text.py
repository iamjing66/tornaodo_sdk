# import requests
# url = "http://121.36.14.89:9101/getnowtime"

# # data = """
# # {
# #     "course_id": "63_349_2",
# #     "table_id": "tb_obj_1381_10012"
# # }
# # """
# res = requests.get(url)
# print(res)

# # 24@98@@D:25@1$1<2e>5|1$0|1$0|1$<2d>4|2$0@

from Global import get_config
from handlers.redisServer.RedisInterface import RedisData


def p(mss):
    redis_data = RedisData(0)
    rr = redis_data.redis_pool()
    p = rr.publish('test', mss)
    print("p:", mss)


if __name__ == "__main__":
    while True:
        my_input = input('请输入发布内容：')  # 发布的数据
        p(my_input)
