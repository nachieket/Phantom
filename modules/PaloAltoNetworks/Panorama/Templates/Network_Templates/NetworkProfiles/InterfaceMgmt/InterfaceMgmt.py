#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class InterfaceMgmt(PaloAltoNetworks):
	"""
	Class to configure Interface Management Profile
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ InterfaceMgmt Class')
		super().__init__(panorama_ip, api_key)
		# print('---- InterfaceMgmt Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Interface Management Profile xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/profiles/interface-management-profile"
		)

		return xpath

	def add_interface_mgmt(self, template_name, int_mgmt=None):
		"""
		Method to add Interface Management Profile to Panorama

		:param template_name: Name of template to add Interface Management Profile to
		:type template_name: str
		:param int_mgmt: Dictionary of all Interface Management Profile parameters
		:type int_mgmt: dict
		:return: None
		:rtype: None

		Example:

		int_mgmt = {'int_mgmt_name': 'allow-all', 'enable_https': 'yes', 'enable_ping': 'yes', 'enable_ssh': 'yes',
					'enable_permitted_ip': {'ip1': '10.10.10.0/24', 'ip2': '172.16.10.0/24'}}

		add_interface_mgmt(template_name='PANW', int_mgmt=int_mgmt)

		Parameters:

		Note: All possible parameters are as below. If the parameter is not included, it will be disabled by default.

		'enable_http': 'yes'
		'enable_https': 'yes'
		'enable_ping': 'yes'
		'enable_response_pages': 'yes'
		'enable_http_ocsp': 'yes'
		'enable_ssh': 'yes'
		'enable_snmp': 'yes'
		'enable_user_id_service': 'yes'
		'enable_user_id_syslog_listener_ssl': 'yes'
		'enable_user_id_syslog_listener_udp': 'yes'
		'enable_telnet': 'yes'
		'enable_permitted_ip': {'ip1': '10.10.10.0/24', 'ip2': '172.16.10.0/24'}

		"""

		xmx = XMLX()
		xpath = self.__xcode()

		element_root = Element('entry')
		element_root.set('name', '%s' % int_mgmt.get('int_mgmt_name'))

		if int_mgmt.get('enable_http') is not None:
			tree_http = Element('http')
			tree_http.text = int_mgmt.get('enable_http')
			element_root.append(tree_http)

		if int_mgmt.get('enable_https') is not None:
			tree_https = Element('https')
			tree_https.text = int_mgmt.get('enable_https')
			element_root.append(tree_https)

		if int_mgmt.get('enable_ping') is not None:
			tree_ping = Element('ping')
			tree_ping.text = int_mgmt.get('enable_ping')
			element_root.append(tree_ping)

		if int_mgmt.get('enable_response_pages') is not None:
			tree_response_pages = Element('response-pages')
			tree_response_pages.text = int_mgmt.get('enable_response_pages')
			element_root.append(tree_response_pages)

		if int_mgmt.get('enable_http_ocsp') is not None:
			tree_http_ocsp = Element('http-ocsp')
			tree_http_ocsp.text = int_mgmt.get('enable_http_ocsp')
			element_root.append(tree_http_ocsp)

		if int_mgmt.get('enable_ssh') is not None:
			tree_ssh = Element('ssh')
			tree_ssh.text = int_mgmt.get('enable_ssh')
			element_root.append(tree_ssh)

		if int_mgmt.get('enable_snmp') is not None:
			tree_snmp = Element('snmp')
			tree_snmp.text = int_mgmt.get('enable_snmp')
			element_root.append(tree_snmp)

		if int_mgmt.get('enable_user_id_service') is not None:
			tree_user_id_service = Element('userid-service')
			tree_user_id_service.text = int_mgmt.get('enable_user_id_service')
			element_root.append(tree_user_id_service)

		if int_mgmt.get('enable_user_id_syslog_listener_ssl') is not None:
			tree_user_id_syslog_listener_ssl = Element('userid-syslog-listener-ssl')
			tree_user_id_syslog_listener_ssl.text = int_mgmt.get('enable_user_id_syslog_listener_ssl')
			element_root.append(tree_user_id_syslog_listener_ssl)

		if int_mgmt.get('enable_user_id_syslog_listener_udp') is not None:
			tree_user_id_syslog_listener_udp = Element('userid-syslog-listener-udp')
			tree_user_id_syslog_listener_udp.text = int_mgmt.get('enable_user_id_syslog_listener_udp')
			element_root.append(tree_user_id_syslog_listener_udp)

		if int_mgmt.get('enable_telnet') is not None:
			tree_telnet = Element('telnet')
			tree_telnet.text = int_mgmt.get('enable_telnet')
			element_root.append(tree_telnet)

		if int_mgmt.get('enable_permitted_ip') is not None:
			tree_permitted_ip = Element('permitted-ip')

			ip_ranges = int_mgmt.get('enable_permitted_ip')

			for ip in ip_ranges.keys():
				tree_ip_range = Element('entry')
				tree_ip_range.set('name', '%s' % ip_ranges[ip])
				tree_permitted_ip.append(tree_ip_range)

			element_root.append(tree_permitted_ip)

		element = Et.tostring(element_root).decode('UTF-8')

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - Interface Management: {} - {}'.format(
				template_name, int_mgmt.get('int_mgmt_name'), e)
			)
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'Interface Management', int_mgmt.get('int_mgmt_name'))
