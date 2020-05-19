#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Addresses.Addresses import Address
from .AddressGroups.AddressGroups import AddressGroups
from .LogForwarding.LogForwarding import LogForwarding


class Objects(Address, AddressGroups, LogForwarding):
	"""
	Class to configure Objects under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Objects Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Objects Class')
