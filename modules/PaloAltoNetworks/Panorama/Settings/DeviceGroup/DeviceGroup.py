#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re

from .....API.XMLX.XMLX import XMLX
from ....PaloAltoNetworks import PaloAltoNetworks
from .....Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger


# TODO: Change code so that a device group can be added as a child group to another parent group; the current code
#  is not working


class DeviceGroup(PaloAltoNetworks):
	"""
	Class to configure Panorama Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ DeviceGroup')
		super().__init__(panorama_ip, api_key)

	# print('---- DeviceGroup')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode(caller):
		"""
		Method to return Panorama device group xpath and element to place in API request string

		:param caller: Caller of this method; decides what to return
		:type caller: str
		:return: xpath, element (XML code) and member element (XML code); xpath is same for both
		:rtype: tuple
		"""

		xpath = "/config/devices/entry[@name='localhost.localdomain']"

		fwxpath = "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s']"

		element = """
			<device-group>
				<entry name="%s">
					<devices/>
				</entry>
			</device-group>
		"""

		melement = """
			<device-group>
				<entry name="%s">
					<devices type="array"/>
				</entry>
			</device-group>
		"""

		fwelement = """
			<devices>
				<entry name="%s">
					<vsys>
						<entry name="vsys1"/>
					</vsys>
				</entry>
			</devices>
		"""

		if caller == 'device_group':
			return xpath, re.sub(r'\s\s+|\n', '', element), re.sub(r'\s\s+|\n', '', melement)
		elif caller == 'add_firewall':
			return fwxpath, re.sub(r'\s\s+|\n', '', fwelement)

	def add_device_group(self, device_group, parent_group='Shared'):
		"""
		Method to configure a template stack and optionally add templates to it

		Example: add_device_group('Sample')

		:param device_group: Device Group to configure
		:type device_group: str
		:param parent_group: Parent Device Group under which to add Device Group; 'Shared' by default
		:type parent_group: str
		:return: Not planning to return success or failure as of now; may change in future
		:rtype: None

		Note: A group to add as child to any group other than Shared is not working as of now.
		"""

		xmx = XMLX()

		xpath, element, melement = self.__xcode('device_group')

		if parent_group == 'Shared':
			try:
				uri = xmx.configure.format(
					self.panorama_ip, xpath, element % device_group, self.api_key
				)
			except Exception as e:
				SLogger.settings.info('DeviceGroups: {} - {}'.format(device_group, e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'DeviceGroups', device_group)
		else:
			try:
				uri = xmx.configure.format(
					self.panorama_ip, xpath, melement % device_group, self.api_key
				)
			except Exception as e:
				SLogger.settings.info('DeviceGroup: {} - {}'.format(device_group, e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'DeviceGroups', device_group)

	def add_fw_to_device_group(self, device_group, firewalls):
		"""
		Method to configure a template stack and optionally add templates to it

		Example: add_fw_to_device_group(device_group='DGSample', firewalls=['015351000024056'])

		:param device_group: Device group name
		:type device_group: str
		:param firewalls: List of firewalls to add to device group
		:type firewalls: list
		:return: None
		:rtype: None
		"""

		xmx = XMLX()

		fwxpath, fwelement = self.__xcode('add_firewall')

		for firewall in firewalls:
			try:
				uri = xmx.configure.format(
					self.panorama_ip, fwxpath % device_group, fwelement % firewall, self.api_key
				)
			except Exception as e:
				SLogger.settings.info('DeviceGroups: {}, {} - {}'.format(device_group, firewall, e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'DeviceGroups', firewall)
