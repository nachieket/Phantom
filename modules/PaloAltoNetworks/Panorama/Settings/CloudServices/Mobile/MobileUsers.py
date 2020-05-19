#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.XMLX.XMLX import XMLX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class MobileUsers(PaloAltoNetworks):
	"""
	Class to configure Cloud Services Plugin Mobile Users
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ MobileUsers Class')
		super().__init__(panorama_ip, api_key)
		# print('---- MobileUsers Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Mobile Users xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services[@version='1.5.0']"
			"/mobile-users/onboarding"
		)

		return xpath

	def configure_mobile_users_onboard(
		self, action='add', portal_name=None, emea_ip_pools=None, amer_ip_pools=None, apac_ip_pools=None,
		world_ip_pools=None, emea_domains=None, amer_domains=None, apac_domains=None, world_domains=None,
		auth_profile=None, authentication_override_cert='Authentication Cookie Cert', emea_region=None,
		amer_region=None, apac_region=None, internal_host_detection=None
	):
		"""
		Method to configure Cloud Services Mobile Users in Panorama

		:param action: action - add or update
		:type action: str
		:param portal_name: (mandatory) Name of Mobile Users Portal
		:type portal_name: str
		:param emea_ip_pools: (mandatory) list of IP Pools
		:type emea_ip_pools: list
		:param amer_ip_pools: (mandatory) list of IP Pools
		:type amer_ip_pools: list
		:param apac_ip_pools: (mandatory) list of IP Pools
		:type apac_ip_pools: list
		:param world_ip_pools: (mandatory) list of IP Pools
		:type world_ip_pools: list
		:param emea_domains: list of company internal DNS domain and servers
		:type emea_domains: list
		:param amer_domains: list of company internal DNS domain and servers
		:type amer_domains: list
		:param apac_domains: list of company internal DNS domain and servers
		:type apac_domains: list
		:param world_domains: list of company internal DNS domain and servers
		:type world_domains: list
		:param auth_profile: (mandatory) authentication profile
		:type auth_profile: str
		:param authentication_override_cert: (mandatory) default is 'Authentication Cookie Cert'
		:type authentication_override_cert: str
		:param emea_region: regions to deploy Mobile Users gateways
		:type emea_region: list
		:param amer_region: regions to deploy Mobile Users gateways
		:type amer_region: list
		:param apac_region: regions to deploy Mobile Users gateways
		:type apac_region: list
		:param internal_host_detection: ip address and fqdn to detect if the endpoint is on internal network
		:type internal_host_detection: list
		:return: None
		:rtype: None

		Example:

		portal_name = 'paloaltonetworks'

		emea_ip_pools = ['10.1.0.0/16', '11.1.0.0/16']
		amer_ip_pools = ['10.2.0.0/16']
		apac_ip_pools = ['10.3.0.0/16']
		world_ip_pools = ['10.4.0.0/14']

		emea_domains = ['xyz.com', '8.8.8.8', '4.2.2.2']
		amer_domains = ['xyz.com', '8.8.8.8', '4.2.2.2']
		apac_domains = ['xyz.com', '8.8.8.8', '4.2.2.2']
		world_domains = ['xyz.com', '8.8.8.8', '4.2.2.2']

		auth_profile = 'Local_Database'

		emea_region = ['eu-west-2', 'belgium', 'netherlands-south', 'eu-west-3']
		amer_region = ['us-east-1', 'us-east-2']
		apac_region = ['india-north', 'india-south']

		internal_host_detection = ['10.10.10.10', 'www.system.com']

		configure_mobile_users_onboard(
			action='add', portal_name=portal_name, emea_ip_pools=emea_ip_pools, amer_ip_pools=amer_ip_pools,
			apac_ip_pools=apac_ip_pools, world_ip_pools=world_ip_pools, emea_domains=emea_domains, amer_domains=amer_domains,
			apac_domains=apac_domains, world_domains=world_domains, auth_profile=auth_profile,
			authentication_override_cert='Authentication Cookie Cert', emea_region=emea_region,
			amer_region=amer_region, apac_region=apac_region, internal_host_detection=internal_host_detection
		)

		mobile_users_parameters = {
			'portal_name': 'paloaltonetworks',
			'ip_pools': {
				'EMEA': {'pool1': '10.1.0.0/16', 'pool2': '11.1.0.0/16'},
				'AMER': {'pool1': '10.2.0.0/16'},
				'APAC': {'pool1': '10.3.0.0/16'},
				'WORLD': {'pool1': '10.4.0.0/14'}
			},
			'dns': {
				'EMEA': {
					'domains': {'domain1': 'xyz.com', 'domain2': 'def.com'},
					'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
				},
				'AMER': {
					'domains': {'domain1': 'abc.com'},
					'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
				},
				'APAC': {
					'domains': {'domain1': 'qwe.com'},
					'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
				},
				'WORLD': {
					'domains': {'domain1': 'wer.com'},
					'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
				}
			},
			'auth_profile': 'Local_Database',
			'authentication_override_cert': 'Authentication Cookie Cert',
			'global_protect_portal': 'GlobalProtect_Portal',
			'global_protect_gateway': 'GlobalProtect_External_Gateway',
			'deployment_region': {
				'EMEA': {
					'loc1': 'eu-west-2', 'loc2': 'belgium', 'loc3': 'netherlands-south', 'loc4': 'eu-west-3'
				},
				'AMER': {
					'loc1': 'us-east-1', 'loc2': 'us-east-2'
				},
				'APAC': {
					'loc1': 'india-north', 'loc2': 'india-south'
				}
			},
			'manual_gateway_region': {
				'EMEA': {
					'loc1': 'eu-west-2', 'loc2': 'belgium', 'loc3': 'netherlands-south', 'loc4': 'eu-west-3'
				},
				'AMER': {
					'loc1': 'us-east-1', 'loc2': 'us-east-2'
				},
				'APAC': {
					'loc1': 'india-north', 'loc2': 'india-south'
				}
			},
			'internal_host_detection': {'ip': '10.10.10.10', 'fqdn': 'www.system.com'}
		}

		configure_mobile_users(action='add', mobile_users_parameters=mobile_users_parameters)
		"""

		xmx = XMLX()
		xpath = self.__xcode()

		if action == 'add':
			element_root = Element('entry')
			element_root.set('name', '%s' % portal_name + '.gpcloudservice.com')

			# Portal Name

			tree_portal_hostname = Element('portal-hostname')

			tree_default_domain = Element('default-domain')

			tree_hostname = Element('hostname')
			tree_hostname.text = portal_name
			tree_default_domain.append(tree_hostname)

			tree_portal_hostname.append(tree_default_domain)

			element_root.append(tree_portal_hostname)

			# IP Pools

			tree_ip_pools = Element('ip-pools')

			if emea_ip_pools is not None:
				tree_emea = Element('entry')
				tree_emea.set('name', 'emea')

				tree_emea_ip_pool = Element('ip-pool')

				for emea_pool in emea_ip_pools:
					tree_emea_ip_pool_member = Element('member')
					tree_emea_ip_pool_member.text = emea_pool
					tree_emea_ip_pool.append(tree_emea_ip_pool_member)

				tree_emea.append(tree_emea_ip_pool)
				tree_ip_pools.append(tree_emea)

			if amer_ip_pools is not None:
				tree_amer = Element('entry')
				tree_amer.set('name', 'americas')

				tree_amer_ip_pool = Element('ip-pool')

				for amer_pool in amer_ip_pools:
					tree_amer_ip_pool_member = Element('member')
					tree_amer_ip_pool_member.text = amer_pool
					tree_amer_ip_pool.append(tree_amer_ip_pool_member)

				tree_amer.append(tree_amer_ip_pool)
				tree_ip_pools.append(tree_amer)

			if apac_ip_pools is not None:
				tree_apac = Element('entry')
				tree_apac.set('name', 'apac')

				tree_apac_ip_pool = Element('ip-pool')

				for apac_pool in apac_ip_pools:
					tree_apac_ip_pool_member = Element('member')
					tree_apac_ip_pool_member.text = apac_pool
					tree_apac_ip_pool.append(tree_apac_ip_pool_member)

				tree_apac.append(tree_apac_ip_pool)
				tree_ip_pools.append(tree_apac)

			if world_ip_pools is not None:
				tree_worldwide = Element('entry')
				tree_worldwide.set('name', 'worldwide')

				tree_worldwide_ip_pool = Element('ip-pool')

				for world_pool in world_ip_pools:
					tree_worldwide_ip_pool_member = Element('member')
					tree_worldwide_ip_pool_member.text = world_pool
					tree_worldwide_ip_pool.append(tree_worldwide_ip_pool_member)

				tree_worldwide.append(tree_worldwide_ip_pool)
				tree_ip_pools.append(tree_worldwide)

			element_root.append(tree_ip_pools)

			# DNS Domain and Servers

			tree_dns_servers = Element('dns-servers')

			if emea_domains is not None:
				tree_dns_emea = Element('entry')
				tree_dns_emea.set('name', 'emea')

				tree_emea_domain_list = Element('domain-list')

				if len(emea_domains[0].split(',')) > 1:
					for dom in emea_domains[0].split(','):
						tree_emea_domain_member = Element('member')
						tree_emea_domain_member.text = dom
						tree_emea_domain_list.append(tree_emea_domain_member)
				else:
					tree_emea_domain_member = Element('member')
					tree_emea_domain_member.text = emea_domains[0]
					tree_emea_domain_list.append(tree_emea_domain_member)

				tree_dns_emea.append(tree_emea_domain_list)

				emea_dns_servers = emea_domains[1].split(',')

				if len(emea_dns_servers) == 1:
					tree_emea_primary_dns = Element('primary')
					tree_emea_primary_dns.text = emea_dns_servers[0]
					tree_dns_emea.append(tree_emea_primary_dns)
				elif len(emea_dns_servers) > 1:
					tree_emea_primary_dns = Element('primary')
					tree_emea_primary_dns.text = emea_dns_servers[0]
					tree_dns_emea.append(tree_emea_primary_dns)

					tree_emea_secondary_dns = Element('secondary')
					tree_emea_secondary_dns.text = emea_dns_servers[1]
					tree_dns_emea.append(tree_emea_secondary_dns)
				else:
					tree_emea_primary_dns = Element('primary')
					tree_emea_primary_dns.text = '8.8.8.8'
					tree_dns_emea.append(tree_emea_primary_dns)

					tree_emea_secondary_dns = Element('secondary')
					tree_emea_secondary_dns.text = '4.2.2.2'
					tree_dns_emea.append(tree_emea_secondary_dns)

				tree_dns_servers.append(tree_dns_emea)

			if amer_domains is not None:
				tree_dns_amer = Element('entry')
				tree_dns_amer.set('name', 'americas')

				tree_amer_domain_list = Element('domain-list')

				if len(amer_domains[0].split(',')) > 1:
					for dom in amer_domains[0].split(','):
						tree_amer_domain_member = Element('member')
						tree_amer_domain_member.text = dom
						tree_amer_domain_list.append(tree_amer_domain_member)
				else:
					tree_amer_domain_member = Element('member')
					tree_amer_domain_member.text = amer_domains[0]
					tree_amer_domain_list.append(tree_amer_domain_member)

				tree_dns_amer.append(tree_amer_domain_list)

				amer_dns_servers = amer_domains[1].split(',')

				if len(amer_dns_servers) == 1:
					tree_amer_primary_dns = Element('primary')
					tree_amer_primary_dns.text = amer_dns_servers[0]
					tree_dns_amer.append(tree_amer_primary_dns)
				elif len(amer_dns_servers) > 1:
					tree_amer_primary_dns = Element('primary')
					tree_amer_primary_dns.text = amer_dns_servers[0]
					tree_dns_amer.append(tree_amer_primary_dns)

					tree_amer_secondary_dns = Element('secondary')
					tree_amer_secondary_dns.text = amer_dns_servers[1]
					tree_dns_amer.append(tree_amer_secondary_dns)
				else:
					tree_amer_primary_dns = Element('primary')
					tree_amer_primary_dns.text = '8.8.8.8'
					tree_dns_amer.append(tree_amer_primary_dns)

					tree_amer_secondary_dns = Element('secondary')
					tree_amer_secondary_dns.text = '4.2.2.2'
					tree_dns_amer.append(tree_amer_secondary_dns)

				tree_dns_servers.append(tree_dns_amer)

			if apac_domains is not None:
				tree_dns_apac = Element('entry')
				tree_dns_apac.set('name', 'apac')

				tree_apac_domain_list = Element('domain-list')

				if len(apac_domains[0].split(',')) > 1:
					for dom in apac_domains[0].split(','):
						tree_apac_domain_member = Element('member')
						tree_apac_domain_member.text = dom
						tree_apac_domain_list.append(tree_apac_domain_member)
				else:
					tree_apac_domain_member = Element('member')
					tree_apac_domain_member.text = apac_domains[0]
					tree_apac_domain_list.append(tree_apac_domain_member)

				tree_dns_apac.append(tree_apac_domain_list)

				apac_dns_servers = apac_domains[1].split(',')

				if len(apac_dns_servers) == 1:
					tree_apac_primary_dns = Element('primary')
					tree_apac_primary_dns.text = apac_dns_servers[0]
					tree_dns_apac.append(tree_apac_primary_dns)
				elif len(apac_dns_servers) > 1:
					tree_apac_primary_dns = Element('primary')
					tree_apac_primary_dns.text = apac_dns_servers[0]
					tree_dns_apac.append(tree_apac_primary_dns)

					tree_apac_secondary_dns = Element('secondary')
					tree_apac_secondary_dns.text = apac_dns_servers[1]
					tree_dns_apac.append(tree_apac_secondary_dns)
				else:
					tree_apac_primary_dns = Element('primary')
					tree_apac_primary_dns.text = '8.8.8.8'
					tree_dns_apac.append(tree_apac_primary_dns)

					tree_apac_secondary_dns = Element('secondary')
					tree_apac_secondary_dns.text = '4.2.2.2'
					tree_dns_apac.append(tree_apac_secondary_dns)

				tree_dns_servers.append(tree_dns_apac)

			if world_domains is not None:
				tree_dns_world = Element('entry')
				tree_dns_world.set('name', 'worldwide')

				tree_world_domain_list = Element('domain-list')

				if len(world_domains[0].split(',')) > 1:
					for dom in world_domains[0].split(','):
						tree_world_domain_member = Element('member')
						tree_world_domain_member.text = dom
						tree_world_domain_list.append(tree_world_domain_member)
				else:
					tree_world_domain_member = Element('member')
					tree_world_domain_member.text = world_domains[0]
					tree_world_domain_list.append(tree_world_domain_member)

				tree_dns_world.append(tree_world_domain_list)

				world_dns_servers = world_domains[1].split(',')

				if len(world_dns_servers) == 1:
					tree_world_primary_dns = Element('primary')
					tree_world_primary_dns.text = world_dns_servers[0]
					tree_dns_world.append(tree_world_primary_dns)
				elif len(world_dns_servers) > 1:
					tree_world_primary_dns = Element('primary')
					tree_world_primary_dns.text = world_dns_servers[0]
					tree_dns_world.append(tree_world_primary_dns)

					tree_world_secondary_dns = Element('secondary')
					tree_world_secondary_dns.text = world_dns_servers[1]
					tree_dns_world.append(tree_world_secondary_dns)
				else:
					tree_world_primary_dns = Element('primary')
					tree_world_primary_dns.text = '8.8.8.8'
					tree_dns_world.append(tree_world_primary_dns)

					tree_world_secondary_dns = Element('secondary')
					tree_world_secondary_dns.text = '4.2.2.2'
					tree_dns_world.append(tree_world_secondary_dns)

				tree_dns_servers.append(tree_dns_world)

			element_root.append(tree_dns_servers)

			# Authentication Profile

			tree_auth_profile = Element('authentication-profile')
			tree_auth_profile.text = auth_profile

			element_root.append(tree_auth_profile)

			# # Authentication Override
			#
			# tree_authentication_override_cert = Element('authentication-override-certificate')
			# tree_authentication_override_cert.text = authentication_override_cert
			#
			# element_root.append(tree_authentication_override_cert)
			#
			# # GlobalProtect Portal
			#
			# tree_global_protect_portal = Element('global-protect-portal')
			# tree_global_protect_portal.text = 'GlobalProtect_Portal'
			#
			# element_root.append(tree_global_protect_portal)
			#
			# # GlobalProtect Gateway
			#
			# tree_global_protect_gateway = Element('global-protect-gateway')
			# tree_global_protect_gateway.text = 'GlobalProtect_External_Gateway'
			#
			# element_root.append(tree_global_protect_gateway)

			# Gateway Deployment

			tree_deployment = Element('deployment')

			tree_region = Element('region')

			if emea_region is not None:
				tree_location_emea = Element('entry')
				tree_location_emea.set('name', 'europe')

				tree_locations = Element('locations')

				for location in emea_region:
					tree_location_emea_member = Element('member')
					tree_location_emea_member.text = location
					tree_locations.append(tree_location_emea_member)

				tree_location_emea.append(tree_locations)
				tree_region.append(tree_location_emea)

			if amer_region is not None:
				tree_location_amer = Element('entry')
				tree_location_amer.set('name', 'americas')

				tree_locations = Element('locations')

				for location in amer_region:
					tree_location_amer_member = Element('member')
					tree_location_amer_member.text = location
					tree_locations.append(tree_location_amer_member)

				tree_location_amer.append(tree_locations)
				tree_region.append(tree_location_amer)

			if apac_region is not None:
				tree_location_apac = Element('entry')
				tree_location_apac.set('name', 'apac')

				tree_locations = Element('locations')

				for location in apac_region:
					tree_location_apac_member = Element('member')
					tree_location_apac_member.text = location
					tree_locations.append(tree_location_apac_member)

				tree_location_apac.append(tree_locations)
				tree_region.append(tree_location_apac)

			tree_deployment.append(tree_region)

			element_root.append(tree_deployment)

			# Manual Gateway

			tree_manual_gateway = Element('manual-gateway')

			tree_region = Element('region')

			if emea_region is not None:
				tree_location_emea = Element('entry')
				tree_location_emea.set('name', 'europe')

				tree_locations = Element('locations')

				for location in emea_region:
					tree_location_emea_member = Element('member')
					tree_location_emea_member.text = location
					tree_locations.append(tree_location_emea_member)

				tree_location_emea.append(tree_locations)
				tree_region.append(tree_location_emea)

			if amer_region is not None:
				tree_location_amer = Element('entry')
				tree_location_amer.set('name', 'americas')

				tree_locations = Element('locations')

				for location in amer_region:
					tree_location_amer_member = Element('member')
					tree_location_amer_member.text = location
					tree_locations.append(tree_location_amer_member)

				tree_location_amer.append(tree_locations)
				tree_region.append(tree_location_amer)

			if apac_region is not None:
				tree_location_apac = Element('entry')
				tree_location_apac.set('name', 'apac')

				tree_locations = Element('locations')

				for location in apac_region:
					tree_location_apac_member = Element('member')
					tree_location_apac_member.text = location
					tree_locations.append(tree_location_apac_member)

				tree_location_apac.append(tree_locations)
				tree_region.append(tree_location_apac)

			tree_manual_gateway.append(tree_region)

			element_root.append(tree_manual_gateway)

			# Internal Host Detection

			tree_internal_host_detection = Element('internal-host-detection')

			tree_ip_address = Element('ip-address')
			tree_ip_address.text = internal_host_detection[1]

			tree_internal_host_detection.append(tree_ip_address)

			tree_internal_hostname = Element('hostname')
			tree_internal_hostname.text = internal_host_detection[0]

			tree_internal_host_detection.append(tree_internal_hostname)

			element_root.append(tree_internal_host_detection)

			element = Et.tostring(element_root).decode('UTF-8')

			try:
				uri = xmx.configure.format(self.panorama_ip, xpath, element, self.api_key)
			except Exception as e:
				SLogger.settings.info('{} - Cloud Services: {} - {}'.format(
					'Settings', 'Mobile Users', e)
				)
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Settings - Cloud Services', 'Mobile Users')
