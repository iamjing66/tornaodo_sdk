import json
import requests

url = "http://192.168.0.9:9001/postinterface"

data = {"opencode":"100","subcode":"1052","UID":"9","username":"lyy","data":'{"uid":"9","resTypeName":"1l","resTypeID":"2","desc":""}'}

res = requests.post(url, json=data).json()
print(res)

# from methods.DBManager import DB

# data = DB.callprocAll('new_deleteaccount', ('18235101805', 'createx_kbe_test', 1))
# print(data)
