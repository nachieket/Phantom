#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..Logger import Logger

import logging


class PoliciesLogger(Logger):
	"""
	Policies Logger Class
	"""

	policies = logging.getLogger(__name__)
	policies.setLevel(logging.INFO)

	policies_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	policies_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/policies.log')
	policies_handler.setFormatter(policies_formatter)

	policies.addHandler(policies_handler)

	def __init__(self):
		# print('++++ PoliciesLogger')
		super().__init__()
	#
	# 	self.policies = logging.getLogger(__name__)
	# 	self.policies.setLevel(logging.INFO)
	#
	# 	self.policies_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
	#
	# 	self.policies_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/policies.log')
	# 	self.policies_handler.setFormatter(self.policies_formatter)
	#
	# 	self.policies.addHandler(self.policies_handler)
	# 	# print('---- PoliciesLogger')
