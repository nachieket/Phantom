#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Portals.Portals import GlobalProtectPortal
from .Gateways.Gateways import GlobalProtectGateway


class GlobalProtect(GlobalProtectPortal, GlobalProtectGateway):
	"""
	GlobalProtect Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ GlobalProtect Class')
		super().__init__(panorama_ip, api_key)
		super(GlobalProtectPortal, self).__init__(panorama_ip, api_key)
		# print('---- GlobalProtect Class')
