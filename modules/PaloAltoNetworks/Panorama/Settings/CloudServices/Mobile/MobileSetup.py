#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class MobileSetup(PaloAltoNetworks):
	"""
	Class to configure Cloud Services Plugin Mobile Users Setup
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ MobileSetup Class')
		super().__init__(panorama_ip, api_key)
		# print('---- MobileSetup Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Mobile Users Setup xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services[@version='1.5.0']"
		)

		return xpath

	def configure_mobile_users_trusted_zones(self, action, trusted_zones=None):
		"""
		Method to configure Cloud Services Mobile Users in Panorama

		:param action: Action - add or update
		:type action: str
		:param trusted_zones: Mobile users zones setup parameters
		:type trusted_zones: list
		:return: None
		:rtype: None

		Example:

		trusted_zones = ['trust', 'dmz']

		configure_mobile_users_setup(action='add', trusted_zones=trusted_zones)

		Parameters:

		trusted_zones (mandatory): Dictionary of trusted zones

		"""

		xmx = XMLX()
		xpath = self.__xcode()

		if action == 'add':
			element_root = Element('mobile-users')

			tree_template_stack = Element('template-stack')
			tree_template_stack.text = 'Mobile_User_Template_Stack'
			element_root.append(tree_template_stack)

			tree_device_group = Element('device-group')
			tree_device_group.text = 'Mobile_User_Device_Group'
			element_root.append(tree_device_group)

			tree_trusted_zone = Element('trusted-zones')

			for zone in trusted_zones:
				tree_trusted_zone_member = Element('member')
				tree_trusted_zone_member.text = zone
				tree_trusted_zone.append(tree_trusted_zone_member)

			element_root.append(tree_trusted_zone)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath, element, self.api_key)
			except Exception as e:
				SLogger.settings.info('{} - Cloud Services: {} - {}'.format(
					'Settings', 'Mobile Users Zones Setup', e)
				)
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Settings - Cloud Services', 'Mobile Users Zones Setup')
