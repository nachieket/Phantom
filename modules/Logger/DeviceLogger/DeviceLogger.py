#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..Logger import Logger

import logging


class DeviceLogger(Logger):
	"""
	Panorama Network Tab Logger Class
	"""

	device = logging.getLogger(__name__)
	device.setLevel(logging.INFO)

	device_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	device_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/device.log')
	device_handler.setFormatter(device_formatter)

	device.addHandler(device_handler)

	def __init__(self):
		# print('++++ DeviceLogger')
		super().__init__()
		# print('---- DeviceLogger')
