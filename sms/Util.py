#!/usr/bin/env python
# coding:utf-8
import re
import sys
import datetime
import json
import logging.handlers
import os
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class Util:

    def __init__(self, data):
        self.data = data
        # self.text = text
        # self.logfile = logfile

    def getMobile(self):
        #^1表示以1开头，[3578]表示第二位的数字为3578中的任意一个，\d{9}表示0~9范围内的数字匹配九次,$表示结束，12位以上的数字不匹配。
        regex = ur"(1[3456789]\d{9})"  # 正则表达式
        match = re.search(regex, self.data)
        if match:
            result = match.group(1)
        else:
            result = ''
        return result

    def getFluxnum(self):
        #^1表示以1开头，[3578]表示第二位的数字为3578中的任意一个，\d{9}表示0~9范围内的数字匹配九次,$表示结束，12位以上的数字不匹配。
        # regex = ur"(\d{2,5})[M|G]"  # 正则表达式
        regex = ur"(\d{1,5})[M|G]"  # 正则表达式
        match = re.search(regex, self.data)
        if match:
            result = match.group(1)
            result = int(result)
            if (result < 10 or result == 11):
                result = result * 1024
            result = str(result)
        else:
            result = ''
        return result

    def getResult(self):
        regex = r"成功"  # 正则表达式
        match = re.search(regex, self.data)
        if match:
            result = '0'
        else:
            result = '1'
        return result

    def writeOrderInfo(self):
        file_object = open(self.logfile, 'w')
        file_object.write(self.text)
        file_object.close()

