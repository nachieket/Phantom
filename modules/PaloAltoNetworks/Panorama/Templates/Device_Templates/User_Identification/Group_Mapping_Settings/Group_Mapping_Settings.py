#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et

from xml.etree.ElementTree import Element

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger


class GroupMappingSettings(PaloAltoNetworks):
	"""
	Class to configure Panorama Group Mapping Settings under a Template
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ GroupMappingSettings Class')
		super().__init__(panorama_ip, api_key)
		# print('---- GroupMappingSettings Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Panorama Template Group Mapping Settings xpath

		:return: xpath
		:rtype: str, str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/devices/"
			"entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/group-mapping"
		)

		return xpath

	def configure_template_group_mapping_settings(
		self, action='add', template_name=None, group_mapping_name=None, server_profile=None, group_include_list=None,
		domain_name=None, group_filter=None, user_filter=None
	):
		"""
		Method to configure user id agent in Panorama template

		:param action: add or update
		:type action: str
		:param template_name: name of template
		:type template_name: str
		:param group_mapping_name: group mapping profile name
		:type group_mapping_name: str
		:param server_profile: authentication server profile name - i.e. LDAP server profile
		:type server_profile: str
		:param group_include_list: list of groups to be included in this profile
		:type group_include_list: list
		:param domain_name: domain name
		:type domain_name: str
		:param group_filter: group DN filter to apply to this profile
		:type group_filter: str
		:param user_filter: user DN filter to apply to this profile
		:type user_filter: str
		:return: None
		:rtype: None

		Examples:

		group_include_list = ['cn=cal_tech,ou=hvt,DC=acme,DC=com', 'cn=engineering,ou=hvt,DC=acme,DC=com']

		configure_template_group_mapping_settings(
			action='add', template_name='PANW', server_profile='msft-esm-dc', group_mapping_name='new_mapping',
			group_include_list=group_include_list
		)

		configure_template_group_mapping_settings(
			action='add', template_name='PANW', server_profile='msft-esm-dc', group_mapping_name='new_mapping',
			group_include_list=group_include_list, domain_name='micro.com'
		)

		configure_template_group_mapping_settings(
			action='add', template_name='PANW', server_profile='msft-esm-dc', group_mapping_name='new_mapping',
			group_include_list=group_include_list, domain_name='micro.com',
			group_filter='cn=cal_tech,ou=hvt,DC=acme,DC=com', user_filter='cn=engineering,ou=hvt,DC=acme,DC=com'
		)
		"""

		xmx = XMLX()

		xpath = self.__xcode()

		if action == 'add':
			# Entry Name

			element_root = Element('entry')
			element_root.set('name', '%s' % group_mapping_name)

			# Group Object

			tree_group_object = Element('group-object')
			tree_group_object_member = Element('member')
			tree_group_object_member.text = 'group'
			tree_group_object.append(tree_group_object_member)
			element_root.append(tree_group_object)

			# User Object

			tree_user_object = Element('user-object')
			tree_user_object_member = Element('member')
			tree_user_object_member.text = 'person'
			tree_user_object.append(tree_user_object_member)
			element_root.append(tree_user_object)

			# Group Include List

			tree_group_include_list = Element('group-include-list')

			for member in group_include_list:
				tree_member = Element('member')
				tree_member.text = member
				tree_group_include_list.append(tree_member)

			element_root.append(tree_group_include_list)

			# Server Profile

			tree_server_profile = Element('server-profile')
			tree_server_profile.text = server_profile
			element_root.append(tree_server_profile)

			# User Name

			tree_user_name = Element('user-name')
			tree_user_name_member = Element('member')
			tree_user_name_member.text = 'sAMAccountName'
			tree_user_name.append(tree_user_name_member)
			element_root.append(tree_user_name)

			# User Email

			tree_user_email = Element('user-email')
			tree_user_email_member = Element('member')
			tree_user_email_member.text = 'mail'
			tree_user_email.append(tree_user_email_member)
			element_root.append(tree_user_email)

			# Alternate User Name

			tree_alternate_username1 = Element('alternate-user-name-1')
			tree_alternate_username1_member = Element('member')
			tree_alternate_username1_member.text = 'userPrincipalName'
			tree_alternate_username1.append(tree_alternate_username1_member)
			element_root.append(tree_alternate_username1)

			tree_alternate_username2 = Element('alternate-user-name-2')
			element_root.append(tree_alternate_username2)

			tree_alternate_username3 = Element('alternate-user-name-3')
			element_root.append(tree_alternate_username3)

			# Group Name

			tree_group_name = Element('group-name')
			tree_group_name_member = Element('member')
			tree_group_name_member.text = 'name'
			tree_group_name.append(tree_group_name_member)
			element_root.append(tree_group_name)

			# Group Member

			tree_group_member = Element('group-member')
			tree_group_member_member = Element('member')
			tree_group_member_member.text = 'member'
			tree_group_member.append(tree_group_member_member)
			element_root.append(tree_group_member)

			# Group Email

			tree_group_email = Element('group-email')
			tree_group_email_member = Element('member')
			tree_group_email_member.text = 'mail'
			tree_group_email.append(tree_group_email_member)
			element_root.append(tree_group_email)

			# Domain

			if domain_name is not None:
				tree_domain_name = Element('domain')
				tree_domain_name.text = domain_name
				element_root.append(tree_domain_name)

			if group_filter is not None:
				tree_group_filter = Element('group-filter')
				tree_group_filter.text = group_filter
				element_root.append(tree_group_filter)

			if user_filter is not None:
				tree_user_filter = Element('user-filter')
				tree_user_filter.text = user_filter
				element_root.append(tree_user_filter)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Group Mapping Settings: {} - {}'.format(template_name, group_mapping_name, e))
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Group Mapping Settings', group_mapping_name)
