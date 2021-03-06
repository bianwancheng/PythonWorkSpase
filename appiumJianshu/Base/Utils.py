#!/usr/bin/env python
# encoding: utf-8
'''
@author: wancheng.b
@time: 2018/11/20 17:35
@desc:工具类  封装了logging类等
'''
import time


def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def sleep(s):
    return time.sleep(s)


class Colour:
    @staticmethod
    def c(msg, colour):
        try:
            from termcolor import colored, cprint
            p = lambda x: cprint(x, '%s' % colour)
            return p(msg)
        except:
            print(msg)

    @staticmethod
    def show_verbose(msg):
        Colour.c(msg, 'white')

    @staticmethod
    def show_debug(msg):
        Colour.c(msg, 'blue')

    @staticmethod
    def show_info(msg):
        Colour.c(msg, 'green')

    @staticmethod
    def show_warn(msg):
        Colour.c(msg, 'yellow')

    @staticmethod
    def show_error(msg):
        Colour.c(msg, 'red')


class Logging:
    flag = True

    @staticmethod
    def error(msg):
        if Logging.flag:
            # print get_now_time() + " [Error]:" + "".join(msg)
            Colour.show_error(get_now_time() + " [Error]:" + "".join(msg))

    @staticmethod
    def warn(msg):
        if Logging.flag:
            Colour.show_warn(get_now_time() + " [Warn]:" + "".join(msg))

    @staticmethod
    def info(msg):
        if Logging.flag:
            Colour.show_info(get_now_time() + " [Info]:" + "".join(msg))

    @staticmethod
    def debug(msg):
        if Logging.flag:
            Colour.show_debug(get_now_time() + " [Debug]:" + "".join(msg))

    @staticmethod
    def success(msg):
        if Logging.flag:
            Colour.show_verbose(get_now_time() + " [Success]:" + "".join(msg))
