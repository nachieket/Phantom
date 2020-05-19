#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et

from xml.etree.ElementTree import Element

from ......API.XMLX.XMLX import XMLX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger


class Services(PaloAltoNetworks):
	"""
	Class to configure Panorama Setup > Services
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Services')
		super().__init__(panorama_ip, api_key)
		# print('---- Services')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Panorama Setup > Services xpath

		:return: xpath
		:rtype: str
		"""

		xpath = "/config/devices/entry[@name='localhost.localdomain']/deviceconfig"

		return xpath

	def configure_setup_services(self, action='add', dns=None, ntp=None, proxy=None):
		"""
		Method to configure a setup > services in Panorama

		:param action: add or update
		:type action: str
		:param dns: DNS servers
		:type dns: dict
		:param ntp: NTP servers
		:type ntp: dict
		:param proxy: Proxy server information
		:type proxy: dict
		:return: None
		:rtype: None

		dns = {'primary': '8.8.8.8', 'secondary': '4.2.2.2'}
		ntp = {'primary': 'time.google.com', 'secondary': 'time2.google.com'}
		proxy = {'proxy_server_ip': '1.1.1.1', 'proxy_server_port': '8080', 'proxy_user': 'user',
				'proxy_password': 'password'}

		Example: configure_setup_services (action='add', dns=dns, ntp=ntp, proxy=proxy)
		"""

		xmx = XMLX()

		xpath = self.__xcode()

		if action == 'add':
			element_root = Element('system')

			# DNS

			if dns is not None:
				if dns.get('primary') is not None:
					tree_dns = Element('dns-setting')
					tree_dns_servers = Element('servers')

					tree_dns_servers_primary = Element('primary')
					tree_dns_servers_primary.text = dns.get('primary')
					tree_dns_servers.append(tree_dns_servers_primary)

					if dns.get('secondary') is not None:
						tree_dns_servers_secondary = Element('secondary')
						tree_dns_servers_secondary.text = dns.get('secondary')
						tree_dns_servers.append(tree_dns_servers_secondary)

					tree_dns.append(tree_dns_servers)

					element_root.append(tree_dns)

			# NTP

			if ntp is not None:
				if ntp.get('primary') is not None:
					tree_ntp = Element('ntp-servers')
					tree_ntp_primary = Element('primary-ntp-server')
					tree_ntp_primary_address = Element('ntp-server-address')
					tree_ntp_primary_address.text = ntp.get('primary')

					tree_ntp_authentication_type = Element('authentication-type')
					tree_ntp_authentication_type_none = Element('none')
					tree_ntp_authentication_type.append(tree_ntp_authentication_type_none)

					tree_ntp_primary.append(tree_ntp_primary_address)
					tree_ntp_primary.append(tree_ntp_authentication_type)

					tree_ntp.append(tree_ntp_primary)

					if ntp.get('secondary') is not None:
						tree_ntp_secondary = Element('secondary-ntp-server')
						tree_ntp_secondary_address = Element('ntp-server-address')
						tree_ntp_secondary_address.text = ntp.get('secondary')

						tree_ntp_authentication_type = Element('authentication-type')
						tree_ntp_authentication_type_none = Element('none')
						tree_ntp_authentication_type.append(tree_ntp_authentication_type_none)

						tree_ntp_secondary.append(tree_ntp_secondary_address)
						tree_ntp_secondary.append(tree_ntp_authentication_type)

						tree_ntp.append(tree_ntp_secondary)

					element_root.append(tree_ntp)

			# Proxy

			if proxy is not None:
				if proxy.get('proxy_server_ip') is not None:
					tree_proxy_server = Element('secure-proxy-server')
					tree_proxy_server.text = proxy.get('proxy_server_ip')

					element_root.append(tree_proxy_server)

					if proxy.get('proxy_server_port') is not None:
						tree_proxy_port = Element('secure-proxy-port')
						tree_proxy_port.text = proxy.get('proxy_server_port')

						element_root.append(tree_proxy_port)

						if proxy.get('proxy_user') is not None:
							tree_proxy_user = Element('secure-proxy-user')
							tree_proxy_user.text = proxy.get('proxy_user')

							element_root.append(tree_proxy_user)

							if proxy.get('proxy_password') is not None:
								tree_proxy_pass = Element('secure-proxy-password')
								tree_proxy_pass.text = proxy.get('proxy_password')

								element_root.append(tree_proxy_pass)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath, element, self.api_key)
			except Exception as e:
				SLogger.settings.info('Panorama - Setup > Services - {}'.format(e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Setup > Services', 'Panorama')
