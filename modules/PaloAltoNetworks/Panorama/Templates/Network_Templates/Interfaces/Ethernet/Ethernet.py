#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from .......PaloAltoNetworks.Panorama.Templates.Network_Templates.Zones import Zones
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


# TODO: Modify the class to add the interface to Zone and Virtual Router


class EthernetInterface(PaloAltoNetworks):
	"""
	Class to configure Ethernet Interface
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ EthernetInterface Class')
		super().__init__(panorama_ip, api_key)
		# print('---- EthernetInterface Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Ethernet Interface xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/interface/ethernet"
		)

		ixpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/import/network/interface"
		)

		return xpath, ixpath

	def configure_ethernet_interface(self, action, template_name, ethernet=None):
		"""
		Method to add EthernetInterface to Panorama

		:param action: Action - Add or Update
		:type action: str
		:param template_name: Name of template to add Ethernet Interface to
		:type template_name: str
		:param ethernet: Dictionary of all Ethernet Interface parameters
		:type ethernet: dict
		:return: None
		:rtype: None

		Example:

		ethernet_parameters = {
			'ethernet_name': 'ethernet1/1', 'zone_name': 'dmz', 'virtual_router': 'default',
			'ip_address': {'ip1': '192.168.100.1/24', 'ip2': '192.168.101.1/24'},
			'enable_router_advertisement': 'yes', 'interface_management_profile': 'allow-all-int-mgmt'
		}

		configure_ethernet_interface(action='add', template_name='PANW', ethernet=ethernet_parameters)

		Parameters:

		Note: All possible parameters are as below. If the parameter is not included, it will be disabled by default.

		ethernet_name (mandatory): Name of the Ethernet Interface
		zone (optional): Name of Zone to add this ethernet interface to
		virtual_router (optional): Name of the virtual router to add this ethernet interface to
		ip_address (mandatory): Dictionary of IP Addresses to be configured; example is above
		interface_management_profile (optional): Interface management profile name

		"""

		xmx = XMLX()
		xpath, ixpath = self.__xcode()

		if action == 'add':
			element_root = Element('entry')
			element_root.set('name', '%s' % ethernet.get('ethernet_name'))

			tree_layer3 = Element('layer3')
			tree_ipv6 = Element('ipv6')
			tree_neighbor_discovery = Element('neighbor-discovery')
			tree_router_advertisement = Element('router-advertisement')

			if ethernet.get('enable_router_advertisement') is not None:
				if ethernet.get('enable_router_advertisement') == 'yes':
					tree_router_advertisement_enable = Element('enable')
					tree_router_advertisement_enable.text = 'yes'

					tree_router_advertisement.append(tree_router_advertisement_enable)
				else:
					tree_router_advertisement_enable = Element('enable')
					tree_router_advertisement_enable.text = 'no'

					tree_router_advertisement.append(tree_router_advertisement_enable)
			else:
				tree_router_advertisement_enable = Element('enable')
				tree_router_advertisement_enable.text = 'no'

				tree_router_advertisement.append(tree_router_advertisement_enable)

			tree_neighbor_discovery.append(tree_router_advertisement)

			tree_ipv6.append(tree_neighbor_discovery)

			tree_layer3.append(tree_ipv6)

			tree_ndp_proxy = Element('ndp-proxy')
			tree_ndp_proxy_enable = Element('enabled')
			tree_ndp_proxy_enable.text = 'no'
			tree_ndp_proxy.append(tree_ndp_proxy_enable)

			tree_layer3.append(tree_ndp_proxy)

			tree_ip = Element('ip')

			ip_addresses = ethernet.get('ip_address')

			for ip in ip_addresses:
				ip_root = Element('entry')
				ip_root.set('name', '%s' % ip_addresses[ip])

				tree_ip.append(ip_root)

			tree_layer3.append(tree_ip)

			if ethernet.get('interface_management_profile') is not None:
				tree_interface_management_profile = Element('interface-management-profile')
				tree_interface_management_profile.text = ethernet.get('interface_management_profile')

				tree_layer3.append(tree_interface_management_profile)

			tree_lldp = Element('lldp')
			tree_lldp_enable = Element('enable')
			tree_lldp_enable.text = 'no'
			tree_lldp.append(tree_lldp_enable)

			tree_layer3.append(tree_lldp)

			element_root.append(tree_layer3)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Ethernet Interface: {} - {}'.format(
					template_name, ethernet.get('ethernet_name'), e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Ethernet Interface', ethernet.get('ethernet_name'))

			# /import/network/interface path

			ielement = '<member>%s</member>' % ethernet.get('ethernet_name')

			try:
				uri = xmx.configure.format(self.panorama_ip, ixpath % template_name, ielement, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Ethernet Interface: {} - {}'.format(
					template_name, ethernet.get('ethernet_name'), e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Ethernet Interface', ethernet.get('ethernet_name'))

			if ethernet.get('zone_name') is not None:
				zone = Zones(panorama_ip=self.panorama_ip, api_key=self.api_key)

				zone_parameters = {
					'zone_name': '%s' % ethernet.get('zone_name'),
					'interface': {'int1': '%s' % ethernet.get('ethernet_name')}
				}

				zone.configure_zone(action='update', template_name='PANW', zone=zone_parameters)

			if ethernet.get('virtual_router') is not None:
				pass
