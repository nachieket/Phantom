#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et

from xml.etree.ElementTree import Element

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger


class UserIDAgent(PaloAltoNetworks):
	"""
	Class to configure User ID Agent in Panorama template
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ UserIDAgent Class')
		super().__init__(panorama_ip, api_key)
		# print('---- UserIDAgent Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Panorama Template User ID Agent xpath

		:return: xpath
		:rtype: str, str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']/config/devices/"
			"entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/user-id-agent"
		)

		return xpath

	def configure_template_user_id_agent(
		self, action='add', template_name=None, agent_name=None, agent_address=None,
		agent_port=None, enable_ldap_proxy='no', enable_ntlm_auth='no', enable_hip_collection='no'
	):
		"""
		Method to configure user id agent in Panorama template

		:param action: add or update
		:type action: str
		:param template_name: name of template
		:type template_name: str
		:param agent_name: User id agent name
		:type agent_name: str
		:param agent_address: User id agent IP Address
		:type agent_address: str
		:param agent_port: User id agent port
		:type agent_port: str
		:param enable_ldap_proxy: enable user id agent for ldap proxy
		:type enable_ldap_proxy: str
		:param enable_ntlm_auth: enable user id agent for ntml authentication
		:type enable_ntlm_auth: str
		:param enable_hip_collection: enable user id agent for hip collection
		:type enable_hip_collection: str
		:return: None
		:rtype: None

		Examples:

		configure_template_user_id_agent(
			action='add', template_name='PANW', agent_name='new_agent', agent_address='1.1.1.1',
			agent_port='5007', enable_hip_collection='yes'
		)

		configure_template_user_id_agent(
			action='add', template_name='PANW', agent_name='new_agent2', agent_address='1.1.1.1',
			agent_port='5007', enable_ldap_proxy='yes', enable_ntlm_auth='yes', enable_hip_collection='yes'
		)

		"""

		xmx = XMLX()

		xpath = self.__xcode()

		if action == 'add':
			# Entry Name

			element_root = Element('entry')
			element_root.set('name', '%s' % agent_name)

			# Host Port

			tree_host = Element('host-port')

			# Agent Port

			tree_host_port = Element('port')
			tree_host_port.text = agent_port
			tree_host.append(tree_host_port)

			# Agent Address

			tree_host_address = Element('host')
			tree_host_address.text = agent_address
			tree_host.append(tree_host_address)

			# LDAP Proxy

			if enable_ldap_proxy == 'yes':
				tree_ldap_proxy = Element('ldap-proxy')
				tree_ldap_proxy.text = enable_ldap_proxy
				tree_host.append(tree_ldap_proxy)

			# NTML Auth

			if enable_ntlm_auth == 'yes':
				tree_ntml_auth = Element('ntlm-auth')
				tree_ntml_auth.text = enable_ntlm_auth
				tree_host.append(tree_ntml_auth)

			element_root.append(tree_host)

			# HIP Collection

			if enable_hip_collection == 'yes':
				tree_hip_collection = Element('enable-hip-collection')
				tree_hip_collection.text = enable_hip_collection
				element_root.append(tree_hip_collection)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - User ID Agent: {} - {}'.format(template_name, agent_name, e))
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'User ID Agent', agent_name)
