#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from concurrent.futures import ThreadPoolExecutor
from time import sleep


class MultiThreading(object):
	"""
	MultiThreading Class
	"""

	def __init__(self):
		super().__init__()

	@staticmethod
	def multithread(func, thread=1, hold=1, *args):
		"""Method to display # while method or function is running"""

		pool = ThreadPoolExecutor(1)

		future = pool.submit(func, *args)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(hold)
		else:
			print('\n')
			result = future.result()

		return result
