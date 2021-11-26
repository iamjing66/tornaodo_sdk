import json
import requests

url = "http://123.57.163.216:9001/postinterface"

data = {"opencode":"3","subcode":"40","UID":"0","username":"","data":'{"pam":"101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125"}'}


res = requests.post(url, json=data).json()
print(res)

# from methods.DBManager import DB

# data = DB.callprocAll('new_deleteaccount', ('18235101805', 'createx_kbe_test', 1))
# print(data)
