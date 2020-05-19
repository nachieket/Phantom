#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et

from xml.etree.ElementTree import Element

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger


class LDAPProfile(PaloAltoNetworks):
	"""
	Class to configure Panorama LDAP Server Profile
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ LDAP')
		super().__init__(panorama_ip, api_key)
		# print('---- LDAP')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Panorama Setup > LDAP xpath

		:return: xpath
		:rtype: str, str
		"""

		shared_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/"
			"shared/server-profile/ldap"
		)

		vsys1_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/devices"
			"/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/server-profile/ldap"
		)

		return shared_xpath, vsys1_xpath

	def configure_template_ldap_profile(
		self, action='add', template_name=None, profile_name=None, location='shared', auth_servers=None, ldap_type=None,
		base_dn=None, bind_dn=None, bind_timelimit=None, bind_password=None, require_ssl_connection='no',
		verify_server_certificate='no'
	):
		"""
		Method to configure a setup > services in Panorama

		:param action: add or update
		:type action: str
		:param template_name: name of template
		:type template_name: str
		:param profile_name: name of LDAP profile
		:type profile_name: str
		:param location: location of profile; shared or vsys1
		:type location: str
		:param auth_servers: list of authentication servers
		:type auth_servers: list
		:param ldap_type: active-directory, e-directory or sun
		:type ldap_type: str
		:param base_dn: Base DN - i.e. DC=Micro,DC=Com
		:type base_dn: str
		:param bind_dn: Bind DN - i.e. admin@micro.com
		:type bind_dn: str
		:param bind_timelimit: Bind time limit - default is 30
		:type bind_timelimit: str
		:param bind_password: Bind password
		:type bind_password: str
		:param require_ssl_connection: Yes if require SSL connection
		:type require_ssl_connection: str
		:param verify_server_certificate: Yes if server certificate verification is required
		:type verify_server_certificate: str
		:return: None
		:rtype: None

		Examples:

		# Prepare Authentication Servers list

		auth_server_1 = {'name': 'server1', 'address': '1.1.1.1', 'port': '389'}
		auth_server_2 = {'name': 'server1', 'address': '1.1.1.1', 'port': '389'}

		auth_servers = [auth_server_1, auth_server_2]

		# Location - 'shared'

		configure_template_ldap_profile(
		action='add', template_name='PANW', profile_name='New_Profile', location='shared', auth_servers=auth_servers,
		ldap_type='active_directory', base_dn='DC=micro,DC=com', bind_dn='admin@micro.com', bind_timelimit='30',
		bind_password='password', require_ssl_connection='no', verify_server_certificate='no'
		)

		# Location - 'vsys1'

		configure_template_ldap_profile(
		action='add', template_name='PANW', profile_name='New_Profile', location='vsys1', auth_servers=auth_servers,
		ldap_type='active-directory', base_dn='DC=micro,DC=com', bind_dn='admin@micro.com', bind_timelimit='30',
		bind_password='password', require_ssl_connection='yes', verify_server_certificate='yes'
		)
		"""

		xmx = XMLX()

		shared_xpath, vsys1_xpath = self.__xcode()

		if action == 'add':
			# Entry Name

			element_root = Element('entry')
			element_root.set('name', '%s' % profile_name)

			# Auth Servers

			tree_server = Element('server')

			for auth_server in auth_servers:
				tree_server_entry = Element('entry')
				tree_server_entry.set('name', '%s' % auth_server.get('name'))

				tree_server_address = Element('address')
				tree_server_address.text = auth_server.get('address')

				tree_server_port = Element('port')
				tree_server_port.text = auth_server.get('port')

				tree_server_entry.append(tree_server_address)
				tree_server_entry.append(tree_server_port)

				tree_server.append(tree_server_entry)

			element_root.append(tree_server)

			# LDAP Type

			tree_ldap_type = Element('ldap-type')
			tree_ldap_type.text = ldap_type
			element_root.append(tree_ldap_type)

			# Bind DN

			tree_bind_dn = Element('bind-dn')
			tree_bind_dn.text = bind_dn
			element_root.append(tree_bind_dn)

			# Bind Time Limit

			tree_bind_timelimit = Element('bind-timelimit')

			if bind_timelimit is not None:
				tree_bind_timelimit.text = bind_timelimit
			else:
				tree_bind_timelimit.text = '30'

			element_root.append(tree_bind_timelimit)

			# Bind Password

			tree_bind_password = Element('bind-password')
			tree_bind_password.text = bind_password
			element_root.append(tree_bind_password)

			# SSL Requirement

			tree_ssl = Element('ssl')
			tree_ssl.text = require_ssl_connection
			element_root.append(tree_ssl)

			# Verify SSL Server Certificate

			if verify_server_certificate == 'yes':
				tree_verify_server = Element('verify-server-certificate')
				tree_verify_server.text = verify_server_certificate
				element_root.append(tree_verify_server)

			# Base DN

			tree_base_dn = Element('base')
			tree_base_dn.text = base_dn
			element_root.append(tree_base_dn)

			element = Et.tostring(element_root).decode('UTF-8')

			if location == 'vsys1':
				try:
					uri = xmx.configure.format(self.panorama_ip, vsys1_xpath % template_name, element, self.api_key)
				except Exception as e:
					NLogger.network.info('{} - LDAP Profile: {} - {}'.format(template_name, profile_name, e))
				else:
					xmx.exec_xml_get(uri, NLogger.network, 'LDAP Profile', profile_name)
			else:
				try:
					uri = xmx.configure.format(self.panorama_ip, shared_xpath % template_name, element, self.api_key)
				except Exception as e:
					NLogger.network.info('{} - LDAP Profile: {} - {}'.format(template_name, profile_name, e))
				else:
					xmx.exec_xml_get(uri, NLogger.network, 'LDAP Profile', profile_name)
