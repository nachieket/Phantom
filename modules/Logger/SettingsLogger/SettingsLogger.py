#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..Logger import Logger

import logging


class SettingsLogger(Logger):
	"""
	Settings Logger Class
	"""

	settings = logging.getLogger(__name__)
	settings.setLevel(logging.INFO)

	settings_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	settings_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/local_settings.log')
	settings_handler.setFormatter(settings_formatter)

	settings.addHandler(settings_handler)

	def __init__(self):
		# print('++++ SettingsLogger')
		super().__init__()
		# print('---- SettingsLogger')
