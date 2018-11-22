'''
adb操作
'''
import os
import random
import threading

import yaml
from appium import webdriver
import subprocess


def getDeviceParameter():
    '''
        获取每个设备的非固定的参数,以数组的格式存入yaml
    :return:
    '''
    device_para = []
    for i in range(0, len(getDevices())):
        device_para.append({'deviceSN': getDevices()[i], 'port': str(random.randint(4700, 4900)),
                            'bport': str(random.randint(4700, 4900)),
                            'platformVersion': (
                                subprocess.getoutput('adb shell getprop ro.build.version.release')).replace(
                                '\n', '')})
    with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml', 'w') as f:
        yaml.dump(device_para, f)
        f.close()


def getDevices():
    '''
    :return: devices_list
    '''
    devices = []
    devicesName = subprocess.getoutput('adb devices')
    devicesName = devicesName.split("\n")[1: -1]
    for deviceName in devicesName:
        deviceName = deviceName.split('\tdevice')
        devices.append(deviceName[0])
    return devices


# 检查adb是否被占用,关闭然后再开启adb

# def checkPort():
#     subprocess.run('adb kill -server')
#     subprocess.run('adb start -server')


def mergerYaml():
    '''
     获取device.yaml和getDevicePara.yaml的参数并合并成一个device_lists
    :return:
    '''
    if not os.path.exists('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml'):
        getDeviceParameter()
    with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\device.yaml', 'rb')as f:
        deviceYaml = yaml.load(f)
        f.close()
    with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml', 'rb')as f:
        getDevicePara = yaml.load(f)
        f.close()
    # 开启多线程，每个设备都单独运行，单独得到driver
    device_lists = []
    for i in range(0, len(getDevicePara)):
        device_dict = dict(getDevicePara[i], **deviceYaml)  # 合并getDevicePara中每个元素和deviceYaml然后添加到一个新的list
        device_lists.append(device_dict)
    print(device_lists)
    return device_lists


def get_driver(device_dict):
    '''
    pareameter:每个设备的所有参数字典
    获取driver
    '''
    try:
        desired_caps = {}
        desired_caps['platformName'] = device_dict['platformName']  # 设备系统
        desired_caps['platformVersion'] = device_dict['platformVersion']  # 设备系统版本
        desired_caps[
            'app'] = device_dict['appPath']  # 指向.apk文件，如果设置appPackage和appActivity，那么这项就不用设置了
        # desired_caps['appPackage'] = 'com.verifone.scb.presentation'  # APK包名，在appium中可以获取到
        # desired_caps['appActivity'] = 'com.verifone.adc.presentation.view.activities.SplashActivity'  # 被测程序启动时的Activity
        desired_caps['unicodeKeyboard'] = device_dict['unicodeKeyboard']  # 是否支持unicode的键盘。如果需要输入中文，要设置为“true”
        desired_caps['resetKeyboard'] = device_dict['resetKeyboard']  # 是否在测试结束后将键盘重轩为系统默认的输入法。
        desired_caps['newCommandTimeout'] = device_dict['newCommandTimeout']  # Appium服务器待appium客户端发送新消息的时间。默认为60秒
        desired_caps['deviceName'] = device_dict['deviceSN']  # 手机sn号
        desired_caps['noReset'] = device_dict['noReset']  # true:不重新安装APP，false:重新安装app
        driver = webdriver.Remote("http://127.0.0.1:{}/wd/hub".format(device_dict['port']), desired_caps)
        return driver
    except Exception as e:
        raise e


# 多线程执行，每个设备得到driver
class driverThread(threading.Thread):
    def __init__(self, device_dict):
        threading.Thread.__init__(self)
        self.device_dict = device_dict

    def run(self):
        get_driver(self.device_dict)


# 多线程执行得到每个设备的到driver
def driver_thread():
    for device_dict in mergerYaml():
        driver = driverThread(device_dict)
        driver.start()
        driver.join()


if __name__ == '__main__':
    # getDevices()
    # print(mergerYaml())
    getDeviceParameter()
    driver_thread()