#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .AuthenticationProfile.AuthenticationProfile import AuthenticationProfile
from .User_Identification.User_Identification import UserIdentification
from .ServerProfiles.ServerProfiles import ServerProfiles


class DeviceTemplates(AuthenticationProfile, UserIdentification, ServerProfiles):
	"""
	Panorama Template Device Tab Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Template Device Tab Class')
		super().__init__(panorama_ip, api_key)
		super(AuthenticationProfile, self).__init__(panorama_ip, api_key)
		super(UserIdentification, self).__init__(panorama_ip, api_key)
		# print('---- Template Device Tab Class')
