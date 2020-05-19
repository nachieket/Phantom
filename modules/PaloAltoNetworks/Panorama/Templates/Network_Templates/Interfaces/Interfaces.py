#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Ethernet.Ethernet import EthernetInterface
from .Tunnel.Tunnel import TunnelInterface


class Interfaces(EthernetInterface, TunnelInterface):
	"""
	Panorama Interfaces Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Interfaces Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Interfaces Class')
