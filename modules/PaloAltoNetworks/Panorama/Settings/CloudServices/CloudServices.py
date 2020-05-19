#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Service.CloudServiceSetup import CloudServiceSetup
from .Service.ServiceConnection import ServiceConnection
from .Mobile.MobileSetup import MobileSetup
from .Mobile.MobileUsers import MobileUsers


class CloudServices(CloudServiceSetup, ServiceConnection, MobileSetup, MobileUsers):
	"""
	Panorama Cloud Services Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Cloud Services Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Cloud Services Class')
