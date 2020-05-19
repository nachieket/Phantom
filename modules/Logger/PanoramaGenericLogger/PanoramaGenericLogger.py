#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..Logger import Logger

import logging


class PanoramaGenericLogger(Logger):
	"""
	Panorama Generic Logs Class
	"""

	panorama = logging.getLogger(__name__)
	panorama.setLevel(logging.INFO)

	panorama_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	panorama_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/panorama_generic.log')
	panorama_handler.setFormatter(panorama_formatter)

	panorama.addHandler(panorama_handler)

	def __init__(self):
		# print('++++ PanoramaGenericLogger')
		super().__init__()
		# print('---- PanoramaGenericLogger')
