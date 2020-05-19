#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Setup.Setup import Setup
from .Template.Template import Template
from .TemplateStack.TemplateStack import TemplateStack
from .DeviceGroup.DeviceGroup import DeviceGroup
from .CloudServices.CloudServices import CloudServices


class Settings(Setup, Template, TemplateStack, DeviceGroup, CloudServices):
	"""
	Class to configure local Panorama settings on Panorama Tab
	The class is named Settings because another class is already named Panorama

	Parent classes are:
		1. Template
		2. TemplateStack
		3. DeviceGroups
	"""

	def __init__(self, panorama_ip, api_key):
		"""
		Settings class constructor
		"""
		# print('++++ Settings')
		super().__init__(panorama_ip, api_key)
		# print('---- Settings')
