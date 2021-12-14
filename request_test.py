import json
import requests

url = "http://123.57.163.216:9001/postinterface"

data = {
    "opencode": "3",
    "subcode": "41",
    "UID": "0",
    "username": "",
    "data": '{"code":"107","page":"2","version":"0"}'
}

res = requests.post(url, json=data).json()
with open("./out.txt", "w+", encoding='utf-8') as f:
    f.write(json.dumps(res, ensure_ascii=False))


# print(res)

# from methods.DBManager import DB

# data = DB.callprocAll('new_deleteaccount', ('18235101805', 'createx_kbe_test', 1))
# print(data)
