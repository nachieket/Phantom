#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Policies.Policies import Policies
from .Objects.Objects import Objects


class DeviceGroups(Policies, Objects):
	"""
	Panorama Device Group Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ DeviceGroups Class')
		super().__init__(panorama_ip, api_key)
		# print('---- DeviceGroups Class')
