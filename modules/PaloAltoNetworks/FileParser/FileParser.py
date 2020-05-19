#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .PrismaAccess.PrismaAccessParser import PrismaAccessParser


class FileParser(PrismaAccessParser):
	"""
	FileParser Class
	"""

	def __init__(self):
		# print('++++ FileParser Class')
		super().__init__()
		# print('---- FileParser Class')
