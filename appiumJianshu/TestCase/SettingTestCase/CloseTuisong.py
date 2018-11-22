import sys
import unittest

from Base.BaseAdb import checkDevices, get_driver
from Base.BaseGetYaml import getYam
from Base.BaseStartAppium import startAppium, closeAppium
from PageObject.Pages import Pages


class CloseTuisong(unittest.TestCase):
    def testCloseTuiSong(self):
        # 设置参数log、yaml和driver等等
        app = {"driver": self.driver, "test_msg": getYam("D:\PythonWorkSpase\\appiumJianshu\yamls\home\\firstOpen.yaml"),
               "device": self.deviceSN, "caseName": sys._getframe().f_code.co_name}

        page = Pages(app)
        page.operate()
        page.checkPoint()
        pass

    @classmethod
    def setUpClass(cls):
        # 检查设备并开启appium服务
        cls.deviceSN = checkDevices()
        startAppium(cls.deviceSN)
        cls.driver = get_driver()
        # 开启服务，# 每个设备实例化一个日志记录器

    @classmethod
    def tearDownClass(cls):
        # 关闭服务，关闭日志 退出app
        closeAppium()
