# 此文件用于存放接口
import requests
from Projects.Demo.Conf.data import *


def login(user=data_info["login"]):
    url = host + api_info["login"]
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = user
    try:
        res = requests.post(url=url, headers=headers, data=data)
        return res
    except Exception:
        pass

def demo(code=data_info["code"]):
    return code