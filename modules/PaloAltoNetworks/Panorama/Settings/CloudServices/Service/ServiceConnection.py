#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class ServiceConnection(PaloAltoNetworks):
	"""
	Class to configure Cloud Services Plugin Service Connection
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ ServiceConnection Class')
		super().__init__(panorama_ip, api_key)
		# print('---- ServiceConnection Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Service Connection xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services[@version='1.5.0']"
			"/service-connection/onboarding"
		)

		return xpath

	def configure_service_connection(self, action, service_connection=None):
		"""
		Method to configure Cloud Services Service Connection in Panorama

		:param action: Action - add or update
		:type action: str
		:param service_connection: Service connection parameters
		:type service_connection: dict
		:return: None
		:rtype: None

		Example:

		service_connection_parameters = {
			'name': 'Primary-Service-Connection', 'enable_bgp': 'yes',
			'bgp': {'peer_as': '65544', 'peer_ip': '1.1.1.1', 'local_ip': '192.168.100.1',
			'advertise_prisma_access_routes': 'yes', 'secret': 'q1w2e3r4'},
			'subnets': {'subnet1': '10.10.10.0/24', 'subnet2': '172.16.10.0/24'}, 'region': 'eu-west-2',
			'primary_ipsec_tunnel': 'SilverPeak-IPSec-Tunnel-Default', 'enable_secondary_wan': 'yes',
			'secondary_ipsec_tunnel': 'Riverbed-IPSec-Tunnel-Default'
		}

		configure_service_connection(action='add', service_connection=service_connection_parameters)

		Parameters:

		Note: All possible parameters are as below. If the parameter is not included, it will be disabled by default.

		name (mandatory): Service connection name
		enable_bgp (optional): 'yes' default is 'no'
		bgp (mandatory if enable_bgp == 'yes') : Dictionary of BGP parameters
		peer_as (mandatory): BGP Peer AS number
		peer_ip (mandatory): BGP peer IP address
		local_ip (optional): BGP local IP address
		advertise_prisma_access_routes (optional): 'yes' to advertise prisma access routes to service connection
		secret (optional): Password to encrypt BGP communications
		subnets (mandatory): Dictionary of subnets to be added to service connection
		region (mandatory): Region to create service connection in
		primary_ipsec_tunnel (mandatory): Name of primary IPSec tunnel
		enable_secondary_wan (optional): select to enable secondary IPSec tunnel - 'yes'; defaults to 'no'
		secondary_ipsec_tunnel (optional): Name of secondary IPSec tunnel

		"""

		xmx = XMLX()
		xpath = self.__xcode()

		if action == 'add':
			element_root = Element('entry')
			element_root.set('name', '%s' % service_connection.get('name'))

			tree_protocol = Element('protocol')
			tree_bgp = Element('bgp')
			tree_bgp_enable = Element('enable')

			if service_connection.get('enable_bgp') is not None:
				if service_connection.get('enable_bgp') == 'yes':
					tree_bgp_enable.text = 'yes'

					tree_bgp.append(tree_bgp_enable)

					tree_peer_as = Element('peer-as')
					tree_peer_as.text = service_connection.get('bgp')['peer_as']

					tree_bgp.append(tree_peer_as)

					tree_peer_ip = Element('peer-ip-address')
					tree_peer_ip.text = service_connection.get('bgp')['peer_ip']

					tree_bgp.append(tree_peer_ip)

					if service_connection.get('bgp')['local_ip'] is not None:
						tree_local_ip = Element('local-ip-address')
						tree_local_ip.text = service_connection.get('bgp')['local_ip']

						tree_bgp.append(tree_local_ip)

					if service_connection.get('bgp')['advertise_prisma_access_routes'] is not None:
						tree_advertise_prisma_access_routes = Element('do-not-export-routes')
						tree_advertise_prisma_access_routes.text = service_connection.get('bgp')['advertise_prisma_access_routes']

						tree_bgp.append(tree_advertise_prisma_access_routes)

					if service_connection.get('bgp')['secret'] is not None:
						tree_secret = Element('secret')
						tree_secret.text = service_connection.get('bgp')['secret']

						tree_bgp.append(tree_secret)
				elif service_connection.get('enable_bgp') == 'no':
					tree_bgp_enable.text = 'no'
			else:
				tree_bgp_enable.text = 'no'

				tree_bgp.append(tree_bgp_enable)

			tree_protocol.append(tree_bgp)
			element_root.append(tree_protocol)

			tree_subnets = Element('subnets')

			subnets = service_connection.get('subnets')

			for subnet in subnets:
				tree_subnet_member = Element('member')
				tree_subnet_member.text = subnet
				tree_subnets.append(tree_subnet_member)

			# for subnet in subnets.keys():
			# 	tree_subnet_member = Element('member')
			# 	tree_subnet_member.text = subnets[subnet]
			# 	tree_subnets.append(tree_subnet_member)

			element_root.append(tree_subnets)

			tree_region = Element('region')
			tree_region.text = service_connection.get('region')
			element_root.append(tree_region)

			tree_primary_ipsec_tunnel = Element('ipsec-tunnel')
			tree_primary_ipsec_tunnel.text = service_connection.get('primary_ipsec_tunnel')
			element_root.append(tree_primary_ipsec_tunnel)

			if service_connection.get('enable_secondary_wan') is not None:
				tree_secondary_wan = Element('secondary-wan-enabled')
				tree_secondary_wan.text = service_connection.get('enable_secondary_wan')
				element_root.append(tree_secondary_wan)

				if service_connection.get('secondary_ipsec_tunnel') is not None:
					tree_secondary_ipsec_tunnel = Element('secondary-ipsec-tunnel')
					tree_secondary_ipsec_tunnel.text = service_connection.get('secondary_ipsec_tunnel')
					element_root.append(tree_secondary_ipsec_tunnel)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath, element, self.api_key)
			except Exception as e:
				SLogger.settings.info('{} - Cloud Services: {} - {}'.format(
					'Settings', 'Service Connection', e)
				)
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Settings - Cloud Services', 'Service Connection')
