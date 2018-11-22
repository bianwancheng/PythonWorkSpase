import unittest

from Base.BaseAdb import mergerYaml, driver_thread
from Base.BaseStartAppium import startAppium


def addTestCase():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromNames(['CloseTuisong']))


if __name__ == '__main__':
    # 检查设备开启服务
    startAppium(mergerYaml())
    # 获取driver
    driver_thread()
    # 日志啥的先不管，添加测试案例
