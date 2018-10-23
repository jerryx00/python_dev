#!/usr/bin/env python
# coding=utf-8
'''
an Simple example.
To ：https://github.com/hustcc/object2json
@author: hzwangzhiwei
@contact: http://50vip.com/
Created on 2014年11月12日
'''


class Msg(object):
	# 消息的id，唯一标示，使用id来进行请求包和返回包的匹配
	id = 0  # id生成必须全局唯一
	'''
	resq:请求消息
	resp:返回消息
	'''
	type = 'resq'  # resq / resp

	cmd = ''
	data = ''
	sender = ''  # 消息的发送者
	recipient = ''  # 消息的接受者
	range = 0  # 消息的范围
	ext = ''  # 扩展信息

	# 默认构造方法，构造一个空的消息
	def __init__(self):
		'''
		Constructor
		'''
		self.id = 5201314
		self.type = 'resp'
		self.cmd = 'sync'
		self.data = {'pos': {'x': 100, 'y': 50}}
		self.sender = '50vip'
		self.recipient = 'atool'
		self.range = 'all'
		self.ext = ''

def p(self):
	print self