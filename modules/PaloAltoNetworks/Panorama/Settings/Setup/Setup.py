#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Services.Services import Services


class Setup(Services):
	"""
	Class to configure Panorama > Setup
	"""

	def __init__(self, panorama_ip, api_key):
		"""
		Settings class constructor
		"""
		# print('++++ Setup')
		super().__init__(panorama_ip, api_key)
		# print('---- Setup')
