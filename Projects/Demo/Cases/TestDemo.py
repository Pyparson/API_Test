import unittest
from Projects.Demo.BaseApi.Base import *
import json


class TestDemo(unittest.TestCase):

    def test_01_demo(self):
        """demo接口传入默认参数,执行通过"""
        result_code = demo()
        assert result_code == 200, "返回码:%s" % (result_code)

    def test_02_demo(self):
        """demo接口传入默认参数,执行通过"""
        result_code = demo(300)
        assert result_code == 200, "返回码:%s" % (result_code)

