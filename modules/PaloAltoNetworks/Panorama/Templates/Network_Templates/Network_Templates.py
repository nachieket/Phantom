#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Interfaces.Interfaces import Interfaces
from .IPSecTunnels.IPSecTunnels import IPSecTunnel
from .GlobalProtect.GlobalProtect import GlobalProtect
from .NetworkProfiles.NetworkProfiles import NetworkProfiles
from .Zones.Zones import Zones


class NetworkTemplates(Interfaces, IPSecTunnel, GlobalProtect, NetworkProfiles, Zones):
	"""
	Panorama Template Device Tab Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Template Network Tab Class')
		super().__init__(panorama_ip, api_key)
		super(Interfaces, self).__init__(panorama_ip, api_key)
		super(IPSecTunnel, self).__init__(panorama_ip, api_key)
		super(GlobalProtect, self).__init__(panorama_ip, api_key)
		super(NetworkProfiles, self).__init__(panorama_ip, api_key)
		# print('---- Template Network Tab Class')
