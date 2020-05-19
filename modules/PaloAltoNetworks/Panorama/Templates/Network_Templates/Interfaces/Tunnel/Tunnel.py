#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from .......PaloAltoNetworks.Panorama.Templates.Network_Templates.Zones import Zones
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


# TODO: Modify the class to add the interface to Zone and Virtual Router


class TunnelInterface(PaloAltoNetworks):
	"""
	Class to configure Tunnel Interface
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ TunnelInterface Class')
		super().__init__(panorama_ip, api_key)
		# print('---- TunnelInterface Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Tunnel Interface xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/interface/tunnel/units"
		)

		ixpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/import/network/interface"
		)

		return xpath, ixpath

	def configure_tunnel_interface(self, action, template_name, tunnel=None):
		"""
		Method to add TunnelInterface to Panorama

		:param action: Action - Add or Update
		:type action: str
		:param template_name: Name of template to add Tunnel Interface to
		:type template_name: str
		:param tunnel: Dictionary of all Tunnel Interface parameters
		:type tunnel: dict
		:return: None
		:rtype: None

		Example:

		tunnel_parameters = {
		'tunnel_name': 'tunnel.21', 'zone_name': 'dmz',
		'ip_address': {'ip1': '192.168.100.1/24', 'ip2': '192.168.101.1/24'},
		'interface_management_profile': 'allow-all-int-mgmt'
		}

		configure_tunnel_interface(action='add', template_name='PANW', tunnel=tunnel_parameters)

		Parameters:

		Note: All possible parameters are as below. If the parameter is not included, it will be disabled by default.

		tunnel_name (mandatory): Name of the Tunnel Interface
		zone (optional): Name of Zone to add this tunnel interface to
		virtual_router (optional): Name of the virtual router to add this tunnel interface to
		ip_address (mandatory): Dictionary of IP Addresses to be configured; example is above
		interface_management_profile (optional): Interface management profile name

		"""

		xmx = XMLX()
		xpath, ixpath = self.__xcode()

		if action == 'add':
			element_root = Element('entry')
			element_root.set('name', '%s' % tunnel.get('tunnel_name'))

			tree_ip = Element('ip')

			ip_addresses = tunnel.get('ip_address')

			for ip in ip_addresses:
				ip_root = Element('entry')
				ip_root.set('name', '%s' % ip_addresses[ip])

				tree_ip.append(ip_root)

			element_root.append(tree_ip)

			if tunnel.get('interface_management_profile') is not None:
				tree_interface_management_profile = Element('interface-management-profile')
				tree_interface_management_profile.text = tunnel.get('interface_management_profile')

				element_root.append(tree_interface_management_profile)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Tunnel Interface: {} - {}'.format(
					template_name, tunnel.get('tunnel_name'), e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Tunnel Interface', tunnel.get('tunnel_name'))

			# /import/network/interface path

			ielement = '<member>%s</member>' % tunnel.get('tunnel_name')

			try:
				uri = xmx.configure.format(self.panorama_ip, ixpath % template_name, ielement, self.api_key)
			except Exception as e:
				NLogger.network.info('{} - Tunnel Interface: {} - {}'.format(
					template_name, tunnel.get('tunnel_name'), e)
				)
			else:
				xmx.exec_xml_get(uri, NLogger.network, 'Tunnel Interface', tunnel.get('tunnel_name'))

			if tunnel.get('zone_name') is not None:
				zone = Zones(panorama_ip=self.panorama_ip, api_key=self.api_key)

				zone_parameters = {
					'zone_name': '%s' % tunnel.get('zone_name'),
					'interface': {'int1': '%s' % tunnel.get('tunnel_name')}
				}

				zone.configure_zone(action='update', template_name='PANW', zone=zone_parameters)

			if tunnel.get('virtual_router') is not None:
				pass
