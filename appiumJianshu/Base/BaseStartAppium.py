import os
import socket
import urllib.request
import time
from multiprocessing import Process
from urllib.error import URLError

import yaml

from Base.BaseThread import RunServer
from app.ApkPath import appium_uiautomator2_server_debug_androidTest, appium_uiautomator2_server


def initApk():
    # 以后可以把apk和路径配置成参数文件方便更新管理
    os.system('adb install -r' + ' ' + appium_uiautomator2_server_debug_androidTest)
    os.system('adb install -r' + ' ' + appium_uiautomator2_server)


def response(url):
    response = None
    time.sleep(2)
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if str(response.getcode()).startswith("2"):
            return True
        else:
            print('访问url失败，返回的状态码为：', response.getcode())
            return False
    except URLError:
        return False
    except socket.timeout:
        return False
    except Exception as e:
        print("appium连接失败")
        raise e
    finally:
        if response:
            response.close()


def cmdOs(cmd):
    os.system(cmd)


def startAppium(mergerYaml):
    # 电脑开启appium服务，需要设置端口和给设备安装两个服务
    # deviceSN = mergerYaml[0]['deviceSN']
    initApk()
    with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml', 'rb')as f:
        getDeviceParaFirst = yaml.load(f)
    port = getDeviceParaFirst[0]['port']
    bport = getDeviceParaFirst[0]['bport']
    # cmd = "appium --session-override  -p %s -bp %s -U %s" % (
    #     port, bport, deviceSN)  # 不执行设备不知道可不可以开启成功,实时证明是可以的
    cmd = "appium --session-override  -p %s -bp %s" % (
        port, bport)
    print(cmd)
    t1 = RunServer(cmd)
    p = Process(target=t1.start())
    p.start()
    url = "http://127.0.0.1:" + port + "/wd/hub/status"
    print(url)
    while True:
        # 成功访问url之前一直是死循环一直循环print的内容，response返回True或者抛出异常结束循环
        print("----------connecting appium server----------")
        if response(url):
            print('start appium success')
            break


def closeAppium():
    os.system("taskkill /f /im node.exe")

# def getPath(self, file_path):
#     # 得到apk的绝对路径,不知道为啥是在base路径下
#     return os.path.abspath(file_path)


if __name__ == '__main__':
    with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml', 'rb')as f:
        print(type(yaml.load(f)))
#     AppiumOperate().startAppium('55cac15d')
