#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .LDAP.LDAP import LDAPProfile


class ServerProfiles(LDAPProfile):
	"""
	Panorama Template Server Profiles Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Template ServerProfiles Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Template ServerProfiles Class')
