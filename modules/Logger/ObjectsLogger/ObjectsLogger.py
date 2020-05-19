#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import logging


class ObjectsLogger(object):
	"""
	Objects Logger Class
	"""

	policies = logging.getLogger(__name__)
	policies.setLevel(logging.INFO)

	policies_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

	policies_handler = logging.FileHandler('./logs/PaloAltoNetworks/Panorama/objects.log')
	policies_handler.setFormatter(policies_formatter)

	policies.addHandler(policies_handler)
