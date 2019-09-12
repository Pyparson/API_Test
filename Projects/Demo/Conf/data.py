# 此文件用于存放测试所需的数据
import random

email = str(random.randint(1000000,9999999)) + "@3202.com"

headers = {"Content-Type": "application/json", "Accept": "application/json"}

host = "XXXXXX"

api_info = {
    "login": "/XXX/XXX"
}

data_info = {
    "login": {"uesr":"XXXXXXX","password":"XXXXXX"},
    "code":200,
}
