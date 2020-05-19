#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..Logger import Logger

import logging


class NetworkLogger(Logger):
	"""
	Panorama Network Tab Logger Class
	"""

	network = logging.getLogger(__name__)
	network.setLevel(logging.INFO)

	network_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	network_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/network.log')
	network_handler.setFormatter(network_formatter)

	network.addHandler(network_handler)

	def __init__(self):
		# print('++++ NetworkLogger')
		super().__init__()
		# print('---- NetworkLogger')
