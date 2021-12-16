import json
import requests

url = "http://192.168.0.9:9001/postinterface"

data = {
    "opencode": "100",
    "subcode": "1051",
    "UID": "9",
    "username": "lyy",
    "data": '{"uid":"9", "page": "1"}'
}

res = requests.post(url, json=data).json()
# with open("./out.txt", "w+", encoding='utf-8') as f:
#     f.write(json.dumps(res, ensure_ascii=False))

print(res)

# from methods.DBManager import DB

# data = DB.callprocAll('new_deleteaccount', ('18235101805', 'createx_kbe_test', 1))
# print(data)
