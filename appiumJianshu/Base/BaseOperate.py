import os
import re
import time
import appium
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Base.BaseElementEnmu import Element


class BaseOperate:

    def __init__(self, driver):
        self.driver = driver

    # 查找元素是否存在
    def findElement(self, testcase):
        try:
            # 自定义检查时间
            t = 10
            WebDriverWait(self.driver, t).until(lambda x: self.elements_by(testcase))
            return {"result": True}
        except Exception as e:
            raise e

    # 操作
    def operate(self, testCase, testInfo, device):
        res = self.findElement(testCase)
        if res["result"]:
            return self.operate_by(testCase, testInfo, device)
        else:
            return res

    # 执行动作
    def operate_by(self, testCase, testInfo, device):
        elements = {
            Element.SWIPE_DOWN: lambda: self.swipeToDown(),
            Element.SWIPE_UP: lambda: self.swipeToUp(),
            Element.CLICK: lambda: self.click(testCase),
            Element.GET_VALUE: lambda: self.get_value(testCase),
            Element.SET_VALUE: lambda: self.set_value(testCase),
            Element.ADB_TAP: lambda: self.adb_tap(testCase, device),
            Element.GET_CONTENT_DESC: lambda: self.get_content_desc(testCase),
            Element.PRESS_KEY_CODE: lambda: self.press_keycode(testCase)

        }
        return elements[testCase.get("operate_type")]()

    # 获取到元素到坐标点击，主要解决浮动层遮档无法触发driver.click的问题
    def adb_tap(self, mOperate, device):

        bounds = self.elements_by(mOperate).location
        x = str(bounds["x"])
        y = str(bounds["y"])

        cmd = "adb -s " + device + " shell input tap " + x + " " + y
        print(cmd)
        os.system(cmd)

        return {"result": True}

    def toast(self, xpath, logTest, testInfo):
        logTest.buildStartLine(testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + "查找弹窗元素_" + xpath)  # 记录日志
        try:
            WebDriverWait(self.driver, 10, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False}

    # 点击事件
    def click(self, mOperate):
        # print(self.driver.page_source)
        if mOperate["find_type"] == Element.find_element_by_id or mOperate[
            "find_type"] == Element.find_element_by_xpath:
            self.elements_by(mOperate).click()
        elif mOperate.get("find_type") == Element.find_elements_by_id:
            self.elements_by(mOperate)[mOperate["index"]].click()
        return {"result": True}

    # code 事件
    def press_keycode(self, mOperate):
        self.driver.press_keycode(mOperate.get("code", 0))
        return {"result": True}

    def get_content_desc(self, mOperate):
        result = self.elements_by(mOperate).get_attribute("contentDescription")
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    '''
    切换native

    '''

    def switchToNative(self):
        self.driver.switch_to.context("NATIVE_APP")  # 切换到native

    '''
    切换webview
    '''

    def switchToWebview(self):
        try:
            n = 1
            while n < 10:
                time.sleep(3)
                n = n + 1
                print(self.driver.contexts)
                for cons in self.driver.contexts:
                    if cons.lower().startswith("webview"):
                        self.driver.switch_to.context(cons)
                        # print(self.driver.page_source)
                        self.driver.execute_script('document.querySelectorAll("html")[0].style.display="block"')
                        self.driver.execute_script('document.querySelectorAll("head")[0].style.display="block"')
                        self.driver.execute_script('document.querySelectorAll("title")[0].style.display="block"')
                        print("切换webview成功")
                        return {"result": True}
            return {"result": False}
        except appium.common.exceptions.NoSuchContextException:
            print("切换webview失败")
            return {"result": False, "text": "appium.common.exceptions.NoSuchContextException异常"}

    # 左滑动
    def swipeLeft(self, mOperate):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x1 = int(width * 0.75)
        y1 = int(height * 0.5)
        x2 = int(width * 0.05)
        self.driver(x1, y1, x2, y1, 600)

    # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    def swipeToDown(self):
        height = self.driver.get_window_size()["height"]
        x1 = int(self.driver.get_window_size()["width"] * 0.5)
        y1 = int(height * 0.25)
        y2 = int(height * 0.75)

        self.driver.swipe(x1, y1, x1, y2, 1000)
        # self.driver.swipe(0, 1327, 500, 900, 1000)
        print("--swipeToDown--")
        return {"result": True}

    def swipeToUp(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
        print("执行上拉")
        return {"result": True}
        # for i in range(n):
        #     self.driver.swipe(540, 800, 540, 560, 0)
        #     time.sleep(2)

    def swipeToRight(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        x1 = int(width * 0.05)
        y1 = int(height * 0.5)
        x2 = int(width * 0.75)
        self.driver.swipe(x1, y1, x1, x2, 1000)
        # self.driver.swipe(0, 1327, 500, 900, 1000)
        print("--swipeToUp--")

    def set_value(self, mOperate):
        """
        输入值，代替过时的send_keys
        :param mOperate:
        :return:
        """
        self.elements_by(mOperate).send_keys(mOperate["msg"])
        return {"result": True}

    def get_value(self, mOperate):
        '''
        读取element的值,支持webview下获取值
        :param mOperate:
        :return:
        '''

        if mOperate.get("find_type") == Element.find_elements_by_id:
            element_info = self.elements_by(mOperate)[mOperate["index"]]
            if mOperate.get("is_webview", "0") == 1:
                result = element_info.text
            else:
                result = element_info.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.elements_by(mOperate)
        if mOperate.get("is_webview", "0") == 1:
            result = element_info.text
        else:
            result = element_info.get_attribute("text")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    def click_windows(self, device):
        try:
            button0 = 'com.huawei.systemmanager:id/btn_allow'
            # button1 = 'com.android.packageinstaller:id/btn_allow_once'
            # button2 = 'com.android.packageinstaller:id/bottom_button_two'
            # button3 = 'com.android.packageinstaller:id/btn_continue_install'
            # button4 = 'android:id/button1'
            # button5 = 'vivo:id/vivo_adb_install_ok_button'
            button_list = [button0]
            for elem in button_list:
                find = self.driver.find_element_by_id(elem)
                WebDriverWait(self.driver, 1).until(lambda x: self.elements_by(find(elem)))
                bounds = find.location
                x = str(bounds["x"])
                y = str(bounds["y"])
                cmd = "adb -s " + device + " shell input tap " + x + " " + y
                print(cmd)
                os.system(cmd)
                print("==点击授权弹框_%s==" % elem)
        except selenium.common.exceptions.TimeoutException:
            # print("==查找元素超时==")
            pass
        except selenium.common.exceptions.NoSuchElementException:
            # print("==查找元素不存在==")
            pass
        except selenium.common.exceptions.WebDriverException:
            # print("WebDriver出现问题了")
            pass

    # 封装常用的获取元素的方法
    def elements_by(self, mOperate):
        # 参数1：lambda：表达式；写法相当于：if 参数1 执行表达式
        elements = {
            Element.find_element_by_id: lambda: self.driver.find_element_by_id(mOperate["element_info"]),
            Element.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(mOperate["element_info"]),
            Element.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(
                mOperate['element_info']),
            Element.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(
                mOperate['element_info']),
            Element.find_elements_by_id: lambda: self.driver.find_elements_by_id(mOperate['element_info'])
        }
        # print(elements[mOperate["find_type"]])
        # 返回的是定位元素
        return elements[mOperate["find_type"]]()
