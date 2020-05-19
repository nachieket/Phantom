#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import threading


class MultiThread(threading.Thread):
	def __init__(self, func, args, name=''):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
		self.args = args
		self.res = ''

	def run(self):
		self.res = self.func(*self.args)
		print(self.res)
		return self.res
