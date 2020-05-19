#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Security.Security import Security
from .NAT.NAT import NAT


class Policies(Security, NAT):
	"""
	Class to configure Policies under Device Group

	Parent classes are:
		1. Security
		2. NAT
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Policies Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Policies Class')
