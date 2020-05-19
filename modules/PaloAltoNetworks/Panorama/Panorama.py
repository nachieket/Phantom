#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Settings.Settings import Settings
from .DeviceGroups.DeviceGroups import DeviceGroups
from .Templates.Templates import Templates

import urllib3

urllib3.disable_warnings()


class Panorama(DeviceGroups, Templates, Settings):
	"""
	Panorama class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Panorama')
		super().__init__(panorama_ip, api_key)
		# print('---- Panorama')
