#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from ......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from ......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class Zones(PaloAltoNetworks):
	"""
	Class to configure Zones
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Zones Class')
		super().__init__(panorama_ip, api_key)
		# print('---- Zones Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Zone xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/zone"
		)

		return xpath

	def configure_zone(
		self, action, template_name, zone_name=None, zone_type=None, interfaces=None, zone_protection_profile=None,
		log_setting=None, enable_packet_buffer_protection=None, enable_user_identification=None, user_acl=None
	):
		"""
		Method to add Zones to Panorama

		:param action: Action - Add or Update
		:type action: str
		:param template_name: Name of template to add Zone to
		:type template_name: str
		:param zone_name: (mandatory) Name of the Zone
		:type zone_name: str
		:param zone_type: (mandatory) Type pf Zone; only Layer3 as of now is supported
		:type zone_type: str
		:param interfaces: Interface name list - i.e. ethernet1/1 exclude this parameter to not include interfaces
		:type interfaces: list
		:param zone_protection_profile: (optional) Zone Protection Profile; exclude this parameter to disable this option
		:type zone_protection_profile: str
		:param log_setting: (optional) Name of Logging Profile; exclude this parameter to disable this option
		:type log_setting: str
		:param enable_packet_buffer_protection: (optional) yes to include ; exclude this parameter to disable this option
		:type enable_packet_buffer_protection: str
		:param enable_user_identification: (optional) yes to include; exclude this parameter to disable this option
		:type enable_user_identification: str
		:param user_acl: (optional) IP Ranges or IPs as shown in example above
		:type user_acl: dict
		:return: None
		:rtype: None

		Example to add new Zone:

		configure_zone(
			action='add', template_name='PANW', zone_name='dmz', zone_type=layer3',
			interfaces=['ethernet1/1', 'ethernet1/2'], zone_protection_profile='default_zone_protection_profile',
			log_setting='Default-Logging-Profile', enable_packet_buffer_protection='yes', user_acl=user_acl
		)

		Example to update Zone:

		configure_zone(action='update', zone_name='dmz1', interfaces=['ethernet1/1', 'ethernet1/2'])
		"""

		xmx = XMLX()
		xpath = self.__xcode()

		if action == 'add' and template_name != 'Mobile_User_Template':
			element_root = Element('entry')
			element_root.set('name', '%s' % zone_name)

			tree_network = Element('network')

			if zone_type == 'layer3':
				tree_zone_type = Element('layer3')

				if interfaces is not None:
					for interface in interfaces:
						tree_int = Element('member')
						tree_int.text = interface
						tree_zone_type.append(tree_int)

				tree_network.append(tree_zone_type)

			if zone_protection_profile is not None:
				tree_zone_protection_profile = Element('zone-protection-profile')
				tree_zone_protection_profile.text = zone_protection_profile
				tree_network.append(tree_zone_protection_profile)

			if log_setting is not None:
				tree_log_setting = Element('log-setting')
				tree_log_setting.text = log_setting
				tree_network.append(tree_log_setting)

			if enable_packet_buffer_protection is not None:
				tree_enable_packet_buffer_protection = Element('enable-packet-buffer-protection')
				tree_enable_packet_buffer_protection.text = enable_packet_buffer_protection
				tree_network.append(tree_enable_packet_buffer_protection)

			element_root.append(tree_network)

			if enable_user_identification is not None:
				tree_enable_user_identification = Element('enable-user-identification')
				tree_enable_user_identification.text = enable_user_identification

				element_root.append(tree_enable_user_identification)

			if user_acl is not None:
				tree_user_acl = Element('user-acl')

				if user_acl.get('include-list') is not None:
					include_list = user_acl.get('include-list')
					tree_include_list = Element('include-list')

					for item in include_list:
						tree_include_list_member = Element('member')
						tree_include_list_member.text = item
						tree_include_list.append(tree_include_list_member)

					tree_user_acl.append(tree_include_list)

				if user_acl.get('exclude-list') is not None:
					exclude_list = user_acl.get('exclude-list')
					tree_exclude_list = Element('exclude-list')

					for item in exclude_list:
						tree_exclude_list_member = Element('member')
						tree_exclude_list_member.text = item
						tree_exclude_list.append(tree_exclude_list_member)

					tree_user_acl.append(tree_exclude_list)

				element_root.append(tree_user_acl)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Zone: {} - {}'.format(
					template_name, zone_name, e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Zone', zone_name)
		elif action == 'update' and template_name != 'Mobile_User_Template':
			if interfaces is not None:
				xpath += "/entry[@name='%s']/network/layer3" % zone_name

				element = ''

				for interface in interfaces:
					tree_interface = Element('member')
					tree_interface.text = interface
					element += Et.tostring(tree_interface).decode('UTF-8')

				try:
					uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
				except Exception as e:
					NLogger.network.info('{} - Zone: {} - {}'.format(
						template_name, zone_name, e)
					)
				else:
					xmx.exec_xml_get(
						uri, NLogger.network, 'Zone', zone_name,
						smsg='Successfully added %s to zone' % interfaces,
						fmsg='Failed to add %s to zone' % interfaces
					)
		elif action == 'add' and template_name == 'Mobile_User_Template':
			element_root = Element('entry')
			element_root.set('name', '%s' % zone_name)

			tree_network = Element('network')
			tree_tap = Element('tap')

			tree_network.append(tree_tap)
			element_root.append(tree_network)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Zone: {} - {}'.format(
					template_name, zone_name, e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Zone', zone_name)
