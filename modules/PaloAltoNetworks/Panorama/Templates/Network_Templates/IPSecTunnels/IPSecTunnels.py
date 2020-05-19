#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from ......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from ......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class IPSecTunnel(PaloAltoNetworks):
	"""
	Class to configure IPSec Tunnel
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ IPSecTunnel Class')
		super().__init__(panorama_ip, api_key)
		# print('---- IPSecTunnel Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return IPSec Tunnel xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/tunnel/ipsec"
		)

		return xpath

	def add_ipsec_tunnel(self, template_name, general=None, proxy_ids=None):
		"""
		Method to add IPSec Tunnel to Panorama

		:param template_name: Name of template to add IPSec Tunnel to
		:type template_name: str
		:param general: IKE Gateway general parameters
		:type general: dict
		:param proxy_ids: IKE Gateway advanced options
		:type proxy_ids: dict
		:return: None
		:rtype: None

		General Tab Example:

		general = {
		'tunnel_name': 'Madrid-IPSec-Tunnel', 'tunnel_interface': 'tunnel.11', 'key_type': 'auto-key',
		'ike_gateway_name': 'London-GW', 'ipsec_crypto_profile': 'IPSec_Crypto', 'enable_replay_protection': 'yes',
		'copy_tos_header': 'yes', 'enable_gre_encapsulation': 'yes', 'enable_tunnel_monitor': 'yes',
		'tunnel_monitor_destination_ip': '172.16.10.1', 'tunnel_monitor_profile': 'default'
		}

		General Tab Parameters:

		tunnel_name=str IPSec tunnel name
		tunnel_interface=str Tunnel interface name
		key_type=str Key exchange type (only auto key supported)
		ike_gateway_name=str IKE Gateway name
		ipsec_crypto_profile=str IPSec Crypto profile name
		enable_replay_protection=str (Optional) - Yes or No; default is No
		copy_tos_header=str (Optional) - Yes or No; default is No
		enable_gre_encapsulation=str (Optional) - Yes or No; default is No
		enable_tunnel_monitor=str (Optional) - Yes or No; default is No
		tunnel_monitor_destination_ip=str (Optional) - Destination IP to monitor tunnel
		tunnel_monitor_profile=str (Optional) - Tunnel monitor profile

		Proxy ID Tab Example:

		proxy_ids = {

		'proxy_id1': {
			'proxy_id_name': 'proxy-id1', 'proxy_id_local_address': '10.10.10.0/24',
			'proxy_id_remote_address': '172.16.10.0/24', 'proxy_id_protocol': {'protocol': 'any'}},

		'proxy_id2': {
			'proxy_id_name': 'proxy-id2', 'proxy_id_local_address': '10.10.10.0/24',
			'proxy_id_remote_address': '172.16.20.0/24',
			'proxy_id_protocol': {'protocol': 'tcp', 'local_port': '0', 'remote_port': '8080'}}
		}

		Proxy ID Tab Parameters:

		proxy_id_name=str Proxy ID name
		proxy_id_local_address=str Proxy ID local address
		proxy_id_remote_address=str Proxy ID remote address
		proxy_id_protocol=dict Four protocol options as below

		Option I: {'protocol': 'any'}
		Option II: {'protocol': 'tcp', 'local_port': '0', 'remote_port': '8080'}
		Option III: {'protocol': 'udp', 'local_port': '0', 'remote_port': '53'}
		Option IV: {'protocol': 'number', 'number': '8'}

		Method Example:

		add_ipsec_tunnel(template_name='PANW', general=general, proxy_ids=proxy_ids)


		"""

		xmx = XMLX()
		xpath = self.__xcode()

		# General Tab

		# Name

		element_root = Element('entry')
		element_root.set('name', '%s' % general.get('tunnel_name'))

		# Key Type

		if general.get('key_type') == 'auto-key':

			# Auto Key

			tree_key = Element('auto-key')

			# IKE Gateway

			tree_ike_gateway = Element('ike-gateway')
			tree_ike_gateway_entry = Element('entry')
			tree_ike_gateway_entry.set('name', '%s' % general.get('ike_gateway_name'))
			tree_ike_gateway.append(tree_ike_gateway_entry)
			tree_key.append(tree_ike_gateway)

			# IPSec Crypto Profile

			tree_ipsec_crypto_profile = Element('ipsec-crypto-profile')
			tree_ipsec_crypto_profile.text = general.get('ipsec_crypto_profile')
			tree_key.append(tree_ipsec_crypto_profile)

			# Proxy ID

			if proxy_ids is not None:
				tree_proxy_id = Element('proxy-id')

				for proxy_id in proxy_ids:
					proxy_key = proxy_ids.get(proxy_id)

					tree_proxy_id_entry = Element('entry')
					tree_proxy_id_entry.set('name', '%s' % proxy_key.get('proxy_id_name'))

					tree_protocol = Element('protocol')

					if proxy_key.get('proxy_id_protocol').get('protocol') == 'any':
						tree_protocol_type = Element('any')
						tree_protocol.append(tree_protocol_type)
					elif proxy_key.get('proxy_id_protocol').get('protocol') == ('tcp' or 'udp'):
						tree_protocol_type = Element(proxy_key.get('proxy_id_protocol').get('protocol'))

						tree_protocol_local_port = Element('local-port')
						tree_protocol_local_port.text = proxy_key.get('proxy_id_protocol').get('local_port')

						tree_protocol_remote_port = Element('remote-port')
						tree_protocol_remote_port.text = proxy_key.get('proxy_id_protocol').get('remote_port')

						tree_protocol_type.append(tree_protocol_local_port)
						tree_protocol_type.append(tree_protocol_remote_port)

						tree_protocol.append(tree_protocol_type)
					elif proxy_key.get('proxy_id_protocol').get('protocol') == 'number':
						tree_protocol_type = Element('number')
						tree_protocol_type.text = proxy_key.get('proxy_id_protocol').get('number')

						tree_protocol.append(tree_protocol_type)

					tree_proxy_id_entry.append(tree_protocol)

					tree_proxy_id_local_address = Element('local')
					tree_proxy_id_local_address.text = proxy_key.get('proxy_id_local_address')

					tree_proxy_id_entry.append(tree_proxy_id_local_address)

					tree_proxy_id_remote_address = Element('remote')
					tree_proxy_id_remote_address.text = proxy_key.get('proxy_id_remote_address')

					tree_proxy_id_entry.append(tree_proxy_id_remote_address)

					tree_proxy_id.append(tree_proxy_id_entry)

				tree_key.append(tree_proxy_id)

				element_root.append(tree_key)
			else:
				element_root.append(tree_key)

		# Tunnel Monitor

		if general.get('enable_tunnel_monitor') == 'yes':
			tree_tunnel_monitor = Element('tunnel-monitor')

			tree_tunnel_monitor_enable = Element('enable')
			tree_tunnel_monitor_enable.text = general.get('enable_tunnel_monitor')
			tree_tunnel_monitor.append(tree_tunnel_monitor_enable)

			tree_tunnel_monitor_destination_ip = Element('destination-ip')
			tree_tunnel_monitor_destination_ip.text = general.get('tunnel_monitor_destination_ip')
			tree_tunnel_monitor.append(tree_tunnel_monitor_destination_ip)

			if general.get('tunnel_monitor_profile') is not None:
				tree_tunnel_monitor_profile = Element('tunnel-monitor-profile')
				tree_tunnel_monitor_profile.text = general.get('tunnel_monitor_profile')
				tree_tunnel_monitor.append(tree_tunnel_monitor_profile)

			element_root.append(tree_tunnel_monitor)

		# Tunnel Interface

		if general.get('tunnel_interface') is not None:
			tree_tunnel_interface = Element('tunnel-interface')
			tree_tunnel_interface.text = general.get('tunnel_interface')
			element_root.append(tree_tunnel_interface)

		# Enable Replay Protection

		if general.get('enable_replay_protection') is not None:
			tree_replay_protection = Element('anti-replay')
			tree_replay_protection.text = general.get('enable_replay_protection')
			element_root.append(tree_replay_protection)

		# Enable GRE Encapsulation

		if general.get('enable_gre_encapsulation') is not None:
			tree_gre_encapsulation = Element('enable-gre-encapsulation')
			tree_gre_encapsulation.text = general.get('enable_gre_encapsulation')
			element_root.append(tree_gre_encapsulation)

		# TOS Header

		if general.get('copy_tos_header') is not None:
			tree_tos_header = Element('copy-tos')
			tree_tos_header.text = general.get('copy_tos_header')
			element_root.append(tree_tos_header)

		element = Et.tostring(element_root).decode('UTF-8')

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - IPSec Tunnel: {} - {}'.format(template_name, general.get('tunnel_name'), e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'IPSec Tunnel', general.get('tunnel_name'))
