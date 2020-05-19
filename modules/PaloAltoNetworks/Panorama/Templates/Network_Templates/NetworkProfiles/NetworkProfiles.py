#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .IKECrypto.IKECrypto import IKECrypto
from .IPSecCrypto.IPSecCrypto import IPSecCrypto
from .IKEGateways.IKEGateways import IKEGateway
from .InterfaceMgmt.InterfaceMgmt import InterfaceMgmt


class NetworkProfiles(IKECrypto, IPSecCrypto, IKEGateway, InterfaceMgmt):
	"""
	Network Profiles Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ NetworkProfiles Class')
		super().__init__(panorama_ip, api_key)
		# print('---- NetworkProfiles Class')
