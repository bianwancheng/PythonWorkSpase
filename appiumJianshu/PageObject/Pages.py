from Base.BaseOperate import BaseOperate
from Base.BaseElementEnmu import Element


class Pages:
    def __init__(self, app):
        self.test_msg = app["test_msg"]
        self.testInfo = self.test_msg[1]["testinfo"]
        self.testCases = self.test_msg[1]["testcase"]
        self.testchecks = self.test_msg[1]["check"]
        self.device = app["device"]
        self.driver = app['driver']

    def operate(self):
        print(self.testCases)
        if self.test_msg[0] is False:  # 如果用例编写错误
            # self.isOperate = False
            return False
        # 执行yaml里面的testcase的各个动作
        for testCase in self.testCases:
            BaseOperate(self.driver).operate(testCase, self.testInfo, self.device)
        pass

    def checkPoint(self):
        for testcheck in self.testchecks:
            self.check(testcheck, self.testInfo, self.device)
        print(self.device, ':', self.testInfo, 'pass')
        # 日志部分，总结部分

    def check(self, testcheck, testInfo, deviece):
        # res = BaseOperate(self.driver).operate(testcheck, testInfo, deviece)
        checkState = testcheck.get('check', Element.DEFAULT_CHECK)
        if checkState == Element.GRAY:
            # msg = '用例:' + self.testInfo['title'] + testcheck['info']
            # print(msg)
            print('检查开关是否置灰或者是关闭状态')
            return True
        if checkState == Element.DEFAULT_CHECK:
            print('检查是否有某元素存在')
            return True
