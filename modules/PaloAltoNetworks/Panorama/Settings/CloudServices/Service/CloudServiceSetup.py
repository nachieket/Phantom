#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et
import re


class CloudServiceSetup(PaloAltoNetworks):
	"""
	Class to configure Cloud Services Plugin Service Setup
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ ServiceSetup Class')
		super().__init__(panorama_ip, api_key)
		# print('---- ServiceSetup Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Service Setup xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		setup_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services[@version='1.5.0']"
		)

		data_lake_xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='Service_Conn_Template']"
			"/config/devices/entry[@name='localhost.localdomain']/deviceconfig/setting/logging"
			"/logging-service-forwarding"
		)

		return setup_xpath, data_lake_xpath

	def configure_cloud_service_setup(
		self, action, service_subnet=None, bgp_as='65534', domains=None, hip_redistribution=None, data_lake='americas'
		):
		"""
		Method to configure Cloud Services Service Setup in Panorama

		:param action: Action - add or update
		:type action: str
		:param service_subnet: (mandatory) Prisma Access Service infrastructure subnet - i.e. 10.10.0.0/16
		:type service_subnet: str
		:param bgp_as: (optional) GBP AS number; defaults to 65534
		:type bgp_as: str
		:param domains: (mandatory) Names of internal domain names; Secondary DNS is optional
		:type domains: dict
		:param hip_redistribution: (optional) 'No' by default; select 'yes' if HIP redistribution is required
		:type hip_redistribution: str
		:param data_lake:
		:type data_lake:
		:return: None
		:rtype: None

		Example:

		domains = {
			'domain1': {'name': 'xyz.com', 'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'},
			'domain2': {'name': 'abc.com', 'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'}
		}

		configure_cloud_service_setup(action='add', service_setup=service_setup_parameters)
		"""

		xmx = XMLX()
		setup_xpath, data_lake_xpath = self.__xcode()

		if action == 'add':
			element_root = Element('service-connection')

			# Service Subnet

			tree_service_subnet = Element('service-subnet')
			tree_service_subnet.text = service_subnet
			element_root.append(tree_service_subnet)

			# BGP AS

			tree_bgp_as = Element('infra-bgp-as')
			tree_bgp_as.text = bgp_as
			element_root.append(tree_bgp_as)

			# Internal Domain and DNS

			tree_internal_dns = Element('internal-dns-list')

			for dom in domains.keys():
				domain = domains[dom]

				tree_domain = Element('entry')
				tree_domain.set('name', '%s' % re.sub(r'\.', '-', domain.get('name')))

				tree_domain_name = Element('domain-name')
				tree_domain_name_member = Element('member')
				tree_domain_name_member.text = domain.get('name')

				tree_domain_name.append(tree_domain_name_member)
				tree_domain.append(tree_domain_name)

				if domain.get('primary') is not None:
					tree_primary_dns = Element('primary')
					tree_primary_dns.text = domain.get('primary')
					tree_domain.append(tree_primary_dns)

				if domain.get('secondary') is not None:
					tree_secondary_dns = Element('secondary')
					tree_secondary_dns.text = domain.get('secondary')
					tree_domain.append(tree_secondary_dns)

				tree_internal_dns.append(tree_domain)

			element_root.append(tree_internal_dns)

			if hip_redistribution is not None:
				tree_hip = Element('hip-redistribution')
				tree_hip.text = hip_redistribution
				element_root.append(tree_hip)

			# tree_template_stack = Element('template-stack')
			# tree_template_stack.text = 'Service_Conn_Template_Stack'
			# element_root.append(tree_template_stack)
			#
			# tree_device_group = Element('device-group')
			# tree_device_group.text = 'Service_Conn_Device_Group'
			# element_root.append(tree_device_group)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, setup_xpath, element, self.api_key)
			except Exception as e:
				SLogger.settings.info('{} - Cloud Services: {} - {}'.format(
					'Settings', 'Service Setup', e)
				)
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Settings - Cloud Services', 'Service Setup')

			# Data Lake

			data_lake_root = Element('logging-service-regions')
			data_lake_root.text = data_lake

			data_lake_element = Et.tostring(data_lake_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, data_lake_xpath, data_lake_element, self.api_key)
			except Exception as e:
				SLogger.settings.info('{} - Cloud Services: {} - {}'.format(
					'Settings', 'Data Lake Setup', e)
				)
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Settings - Cloud Services', 'Data Lake Setup')
