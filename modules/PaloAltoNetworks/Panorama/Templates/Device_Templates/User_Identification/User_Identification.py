#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .User_ID_Agents.User_ID_Agents import UserIDAgent
from .Group_Mapping_Settings.Group_Mapping_Settings import GroupMappingSettings


class UserIdentification(UserIDAgent, GroupMappingSettings):
	"""
	Panorama Template Device Tab Class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ UserIdentification Device Tab Class')
		super().__init__(panorama_ip, api_key)
		super(UserIDAgent, self).__init__(panorama_ip, api_key)
		# print('---- UserIdentification Device Tab Class')
