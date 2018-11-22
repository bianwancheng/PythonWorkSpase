# import os
# # 返回当前文件的绝对路径
# print(os.path.abspath('testNode.py'))
import os
# os模块
# res = os.popen('adb devices').read()
# print(type(res))
# os.system('adb devices')
# os.system('cmd')

# subprocess模块
import subprocess


# subprocess.call('adb devices')
# subprocess.run('adb devices')
# subprocess.check_call('adb devices')
# res = subprocess.Popen('adb devices')
# print(type(res))
import yaml

with open('D:\PythonWorkSpase\\appiumJianshu\\app\parameter\getDevicePara.yaml', 'rb')as f:
    deviceYaml = yaml.load(f)
    print(type(deviceYaml))
    f.close()

print(deviceYaml)