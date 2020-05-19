#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et

from xml.etree.ElementTree import Element

from ......API.XMLX.XMLX import XMLX
from ......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from ......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger


class AuthenticationProfile(PaloAltoNetworks):
	"""
	Class to configure Panorama LDAP Server Profile
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ AuthenticationProfile Class')
		super().__init__(panorama_ip, api_key)
		# print('---- AuthenticationProfile Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Authentication Profile xpath

		:return: xpath
		:rtype: str, str
		"""

		shared_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/"
			"shared/authentication-profile"
		)

		vsys1_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/devices"
			"/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/authentication-profile"
		)

		return shared_xpath, vsys1_xpath

	def configure_template_authentication_profile(
		self, action='add', template_name=None, profile_name=None, location='shared', server_profile_name=None,
		login_attribute=None, member_list=None, username_modifier=None, user_domain=None,
		enable_mfa='no', mfa_profiles=None
	):
		"""
		Method to configure authentication profile in Panorama template

		:param action: add or update
		:type action: str
		:param template_name: name of template
		:type template_name: str
		:param profile_name: name of LDAP profile
		:type profile_name: str
		:param location: location of profile; shared or vsys1
		:type location: str
		:param server_profile_name: name of authentication server profile
		:type server_profile_name: str
		:param login_attribute: Active Directory login attribute
		:type login_attribute: str
		:param member_list: List of all user groups allowed access
		:type member_list: list
		:param username_modifier: Username modifier - %USERINPUT%, %USERDOMAIN%\%USERINPUT% or %USERINPUT%@%USERDOMAIN%
		:type username_modifier: str
		:param user_domain: User domain - i.e. micro.com
		:type user_domain: str
		:param enable_mfa: yes if MFA is required
		:type enable_mfa: str
		:param mfa_profiles: list of MFA profiles
		:type mfa_profiles: list
		:return: None
		:rtype: None

		Examples:

		# Without MFA Profile

		configure_template_authentication_profile(
			action='add', template_name='PANW', profile_name='AD_Auth_Profile', location='shared',
			server_profile_name='DC_LDAP', login_attribute='sAMAccountName', member_list=['all'],
			username_modifier='%USERINPUT%', user_domain=None, enable_mfa='no', mfa_profiles=None
		)

		# With MFA Profile

		configure_template_authentication_profile(
			action='add', template_name='PANW', profile_name='AD_Auth_Profile', location='shared',
			server_profile_name='DC_LDAP', login_attribute='sAMAccountName', member_list=['all'],
			username_modifier='%USERINPUT%', user_domain=None, enable_mfa='yes', mfa_profiles=['DUO_MFA']
		)
		"""

		xmx = XMLX()

		shared_xpath, vsys1_xpath = self.__xcode()

		if action == 'add':
			# Entry Name

			element_root = Element('entry')
			element_root.set('name', '%s' % profile_name)

			if enable_mfa == 'yes':
				tree_mfa = Element('multi-factor-auth')
				tree_mfa_enable = Element('mfa-enable')
				tree_mfa_enable.text = 'yes'

				tree_mfa.append(tree_mfa_enable)

				if mfa_profiles is not None:
					tree_mfa_factor = Element('factors')

					for profile in mfa_profiles:
						tree_mfa_profile_member = Element('member')
						tree_mfa_profile_member.text = profile

						tree_mfa_factor.append(tree_mfa_profile_member)

					tree_mfa.append(tree_mfa_factor)

				element_root.append(tree_mfa)
			else:
				tree_mfa = Element('multi-factor-auth')
				tree_mfa_enable = Element('mfa-enable')
				tree_mfa_enable.text = 'no'

				tree_mfa.append(tree_mfa_enable)
				element_root.append(tree_mfa)

			tree_method = Element('method')
			tree_ldap = Element('ldap')

			tree_ldap_profile = Element('server-profile')
			tree_ldap_profile.text = server_profile_name

			tree_ldap.append(tree_ldap_profile)

			tree_login_attrib = Element('login-attribute')

			if login_attribute is not None:
				tree_login_attrib.text = login_attribute
			else:
				tree_login_attrib.text = 'sAMAccountName'

			tree_ldap.append(tree_login_attrib)
			tree_method.append(tree_ldap)
			element_root.append(tree_method)

			tree_allow_list = Element('allow-list')

			if member_list is not None:
				for member in member_list:
					tree_member = Element('member')
					tree_member.text = member
					tree_allow_list.append(tree_member)
			else:
				tree_member = Element('member')
				tree_member.text = 'all'
				tree_allow_list.append(tree_member)

			element_root.append(tree_allow_list)

			tree_username_modifier = Element('username-modifier')

			if username_modifier is not None:
				tree_username_modifier.text = username_modifier
			else:
				tree_username_modifier.text = '%USERINPUT%'

			element_root.append(tree_username_modifier)

			if user_domain is not None:
				tree_user_domain = Element('user-domain')
				tree_user_domain.text = user_domain
				element_root.append(tree_user_domain)

			element = Et.tostring(element_root).decode('UTF-8')

			if location == 'vsys1':
				try:
					uri = xmx.configure.format(self.panorama_ip, vsys1_xpath % template_name, element, self.api_key)
				except Exception as e:
					NLogger.network.info('{} - Authentication Profile: {} - {}'.format(template_name, profile_name, e))
				else:
					xmx.exec_xml_get(uri, NLogger.network, 'Authentication Profile', profile_name)
			else:
				try:
					uri = xmx.configure.format(self.panorama_ip, shared_xpath % template_name, element, self.api_key)
				except Exception as e:
					NLogger.network.info('{} - Authentication Profile: {} - {}'.format(template_name, profile_name, e))
				else:
					xmx.exec_xml_get(uri, NLogger.network, 'Authentication Profile', profile_name)
