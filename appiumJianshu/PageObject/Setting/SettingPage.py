# from Base.BaseOperate import BaseOperate
#
#
# class SettingPage:
#     def __init__(self, app):
#         self.test_msg = app["test_msg"]
#         self.testInfo = self.test_msg[1]["testinfo"]
#         self.testCases = self.test_msg[1]["testcase"]
#         self.testcheck = self.test_msg[1]["check"]
#         self.device = app["device"]
#         self.driver = app['driver']
#
#     def operate(self):
#         print(self.testCases)
#         if self.test_msg[0] is False:  # 如果用例编写错误
#             # self.isOperate = False
#             return False
#         # 执行yaml里面的testcase的各个动作
#         for testCase in self.testCases:
#             BaseOperate(self.driver).operate(testCase, self.testInfo, self.device)
#         pass
#
#     def checkPoint(self):
#         pass
