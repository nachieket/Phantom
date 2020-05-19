#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Device_Templates.Device_Templates import DeviceTemplates
from .Network_Templates.Network_Templates import NetworkTemplates


class Templates(DeviceTemplates, NetworkTemplates):
	"""
	Panorama Templates Tab Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Templates Tab Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Templates Tab Class')
