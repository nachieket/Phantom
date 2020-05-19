#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class IKEGateway(PaloAltoNetworks):
	"""
	Class to configure IKE Gateway
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ IKEGateway Class')
		super().__init__(panorama_ip, api_key)
		# print('---- IKEGateway Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return IKE Gateway xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/ike/gateway"
		)

		return xpath

	def add_ike_gateway(self, template_name, general=None, advanced_options=None):
		"""
		Method to add IKE Gateway to Panorama

		:param template_name: Name of template to add configure IKE Gateway to
		:type template_name: str
		:param general: IKE Gateway general parameters
		:type general: dict

		name=str
		version=str use advanced_options to change IKE version
		interface=str
		local_ip_address=str
		peer_ip_address_type=str (ip, fqdn, dynamic)
		peer_address=str
		authentication=str (pre-shared-key only)
		pre_shared_key=str
		local_identification=dict (optional) {type=ipaddr, id=1.1.1.1} OR {type=fqdn, id=www.xyz.com}
		peer_identification=str (optional) {type=ipaddr, id=1.1.1.1} OR {type=fqdn, id=www.xyz.com}

		:param advanced_options: IKE Gateway advanced options
		:type advanced_options: dict

		enable_passive_mode=str (optional yes, no; default is no)
		enable_nat_traversal=str (optional yes, no; default is no)
		enable_fragmentation=str (optional yes, no; default is no)
		ikev1_dpd_interval=str (optional numeric value; default is 5)
		ikev1_dpd_retry=str (optional numeric value; default is 5)
		ikev1_ike_crypto_profile=str (optional profile name; default is default)
		ikev1_exchange_mode=str (optional auto, main, aggressive; default is auto)
		ikev2_dpd_interval=str (optional numeric value; default is 5)
		ikev2_ike_crypto_profile=str (optional profile name; default is default)
		ikev2_require_cookie=str (optional yes or no; default is no)
		version=str (optional ikev2 or ikev2-preferred; default is ikev1)

		:return: None
		:rtype: None

		Example:

		general={
		'name': 'London-GW', 'interface': 'ethernet1/1', 'local_ip_address': '192.168.55.20/24',
		'peer_ip_address_type': 'ip', 'peer_address': '1.1.1.1', 'authentication': 'pre-shared-key',
		'pre_shared_key': 'q1w2e3r4t5', 'local_identification': {'type': 'ipaddr', 'id': '192.168.55.20'},
		'peer_identification': {'type': 'ipaddr', 'id': '1.1.1.1'}}

		advanced_options={
		'enable_passive_mode': 'yes', 'enable_nat_traversal': 'yes', 'ikev1_dpd_interval': '10', 'ikev1_dpd_retry': '10',
		'ikev1_ike_crypto_profile': 'PA_Crypto', 'ikev1_exchange_mode': 'main', 'ikev2_dpd_interval': '10',
		'ikev2_ike_crypto_profile': 'PA_Crypto', 'ikev2_require_cookie': 'yes', 'version': 'ikev2-preferred'
		}

		add_ike_gateway(template_name='PANW', general=general, advanced_options=advanced_options)

		add_ike_gateway(template_name='PANW',

		general={
		'name': 'London-GW', 'interface': 'ethernet1/1', 'local_ip_address': '192.168.55.20/24',
		'peer_ip_address_type': 'ip', 'peer_address': '1.1.1.1', 'authentication': 'pre-shared-key',
		'pre_shared_key': 'q1w2e3r4t5', 'local_identification': {'type': 'ipaddr', 'id': '192.168.55.20'},
		'peer_identification': {'type': 'ipaddr', 'id': '1.1.1.1'}},

		advanced_options={
		'enable_passive_mode': 'yes', 'enable_nat_traversal': 'yes', 'ikev1_dpd_interval': '10', 'ikev1_dpd_retry': '10',
		'ikev1_ike_crypto_profile': 'PA_Crypto', 'ikev1_exchange_mode': 'main', 'ikev2_dpd_interval': '10',
		'ikev2_ike_crypto_profile': 'PA_Crypto', 'ikev2_require_cookie': 'yes', 'version': 'ikev2-preferred'
		})

		add_ike_gateway(template_name='PANW',

		general={
		'name': 'London-GW', 'interface': 'ethernet1/1', 'local_ip_address': '192.168.55.20/24',
		'peer_ip_address_type': 'ip', 'peer_address': '1.1.1.1', 'authentication': 'pre-shared-key',
		'pre_shared_key': 'q1w2e3r4t5', 'local_identification': {'type': 'ipaddr', 'id': '192.168.55.20'},
		'peer_identification': {'type': 'ipaddr', 'id': '1.1.1.1'}},

		advanced_options={'version': 'ikev2-preferred'}
		)

		add_ike_gateway(template_name='PANW',

		general={
		'name': 'London-GW', 'interface': 'ethernet1/1', 'local_ip_address': '192.168.55.20/24',
		'peer_ip_address_type': 'ip', 'peer_address': '1.1.1.1', 'authentication': 'pre-shared-key',
		'pre_shared_key': 'q1w2e3r4t5', 'local_identification': {'type': 'ipaddr', 'id': '192.168.55.20'},
		'peer_identification': {'type': 'ipaddr', 'id': '1.1.1.1'}}
		)
		"""

		xmx = XMLX()
		xpath = self.__xcode()

		# General Tab
		# Name

		element_root = Element('entry')
		element_root.set('name', '%s' % general.get('name'))
		# element_tree = ElementTree(element_root)

		# Interface & Local IP Address

		tree_local_address = Element('local-address')

		if general.get('interface') is not None:
			tree_local_address_interface = Element('interface')
			tree_local_address_interface.text = general.get('interface')
			tree_local_address.append(tree_local_address_interface)

		if general.get('local_ip_address') is not None:
			tree_local_address_ip = Element('ip')
			tree_local_address_ip.text = general.get('local_ip_address')
			tree_local_address.append(tree_local_address_ip)

		element_root.append(tree_local_address)

		# Peer IP Address Type & Peer Address

		tree_peer_address = Element('peer-address')

		if general.get('peer_ip_address_type') == 'ip':
			tree_peer_address_ip = Element('ip')
			tree_peer_address_ip.text = general.get('peer_address')
			tree_peer_address.append(tree_peer_address_ip)
		elif general.get('peer_ip_address_type') == 'fqdn':
			tree_peer_address_fqdn = Element('fqdn')
			tree_peer_address_fqdn.text = general.get('peer_address')
			tree_peer_address.append(tree_peer_address_fqdn)
		elif general.get('peer_ip_address_type') == 'dynamic':
			tree_peer_address_fqdn = Element('dynamic')
			tree_peer_address.append(tree_peer_address_fqdn)

		element_root.append(tree_peer_address)

		# Authentication & Pre-share-key

		tree_authentication = Element('authentication')

		if general.get('authentication') == 'pre-shared-key':
			tree_pre_shared_key = Element('pre-shared-key')
			tree_key = Element('key')
			tree_key.text = general.get('pre_shared_key')
			tree_pre_shared_key.append(tree_key)
			tree_authentication.append(tree_pre_shared_key)
		else:
			# Include certificate authentication in future
			pass

		element_root.append(tree_authentication)

		# Local Identification

		if general.get('local_identification'):
			tree_local_identification = Element('local-id')
			tree_local_identification_type = Element('type')
			tree_local_identification_id = Element('id')

			# local_identification = general.get('local_identification')

			tree_local_identification_type.text = general.get('local_identification').get('type')
			tree_local_identification_id.text = general.get('local_identification').get('id')

			tree_local_identification.append(tree_local_identification_type)
			tree_local_identification.append(tree_local_identification_id)

			element_root.append(tree_local_identification)

		# Peer Identification

		if general.get('peer_identification'):
			tree_peer_identification = Element('peer-id')
			tree_peer_identification_type = Element('type')
			tree_peer_identification_id = Element('id')

			# peer_identification = general.get('peer_identification')

			tree_peer_identification_type.text = general.get('peer_identification').get('type')
			tree_peer_identification_id.text = general.get('peer_identification').get('id')

			tree_peer_identification.append(tree_peer_identification_type)
			tree_peer_identification.append(tree_peer_identification_id)

			element_root.append(tree_peer_identification)

		# Advanced Options Tab

		if advanced_options is not None:
			tree_protocol_common = Element('protocol-common')

			# NAT Traversal

			tree_nat_traversal = Element('nat-traversal')
			tree_nat_traversal_enable = Element('enable')

			if advanced_options.get('enable_nat_traversal'):
				tree_nat_traversal_enable.text = advanced_options.get('enable_nat_traversal').lower()
			else:
				tree_nat_traversal_enable.text = 'no'

			tree_nat_traversal.append(tree_nat_traversal_enable)
			tree_protocol_common.append(tree_nat_traversal)

			# Fragmentation

			if general.get('authentication') != 'pre-shared-key' and advanced_options.get('exchange_mode') != 'aggressive':
				tree_fragmentation = Element('fragmentation')
				tree_fragmentation_enable = Element('enable')

				if advanced_options.get('enable_fragmentation'):
					tree_fragmentation_enable.text = advanced_options.get('enable_fragmentation').lower()
				else:
					tree_fragmentation_enable.text = 'no'

				tree_fragmentation.append(tree_fragmentation_enable)
				tree_protocol_common.append(tree_fragmentation)

			# Passive Mode

			if advanced_options.get('enable_passive_mode'):
				tree_passive_mode = Element('passive-mode')
				tree_passive_mode.text = advanced_options.get('enable_passive_mode').lower()
				tree_protocol_common.append(tree_passive_mode)

			element_root.append(tree_protocol_common)

			# IKEv1

			tree_protocol = Element('protocol')
			tree_ikev1 = Element('ikev1')
			tree_ikev1_dpd = Element('dpd')
			tree_ikev1_dpd_enable = Element('enable')
			tree_ikev1_dpd_enable.text = 'yes'

			tree_ikev1_dpd.append(tree_ikev1_dpd_enable)
			tree_ikev1.append(tree_ikev1_dpd)
			tree_protocol.append(tree_ikev1)

			if advanced_options.get('ikev1_dpd_interval'):
				tree_ikev1_dpd_interval = Element('interval')
				tree_ikev1_dpd_interval.text = advanced_options.get('ikev1_dpd_interval')
				tree_ikev1_dpd.append(tree_ikev1_dpd_interval)

			if advanced_options.get('ikev1_dpd_retry'):
				tree_ikev1_dpd_retry = Element('retry')
				tree_ikev1_dpd_retry.text = advanced_options.get('ikev1_dpd_retry')
				tree_ikev1_dpd.append(tree_ikev1_dpd_retry)

			if advanced_options.get('ikev1_ike_crypto_profile'):
				tree_ikev1_ike_crypto_profile = Element('ike-crypto-profile')
				tree_ikev1_ike_crypto_profile.text = advanced_options.get('ikev1_ike_crypto_profile')
				tree_ikev1.append(tree_ikev1_ike_crypto_profile)

			if advanced_options.get('ikev1_exchange_mode'):
				tree_ikev1_exchange_mode = Element('exchange-mode')
				tree_ikev1_exchange_mode.text = advanced_options.get('ikev1_exchange_mode')
				tree_ikev1.append(tree_ikev1_exchange_mode)

			# IKEv2

			tree_ikev2 = Element('ikev2')
			tree_ikev2_dpd = Element('dpd')
			tree_ikev2_dpd_enable = Element('enable')
			tree_ikev2_dpd_enable.text = 'yes'

			tree_ikev2_dpd.append(tree_ikev2_dpd_enable)

			if advanced_options.get('ikev2_dpd_interval'):
				tree_ikev2_dpd_interval = Element('interval')
				tree_ikev2_dpd_interval.text = advanced_options.get('ikev2_dpd_interval')
				tree_ikev2_dpd.append(tree_ikev2_dpd_interval)

			if advanced_options.get('ikev2_ike_crypto_profile'):
				tree_ikev2_ike_crypto_profile = Element('ike-crypto-profile')
				tree_ikev2_ike_crypto_profile.text = advanced_options.get('ikev2_ike_crypto_profile')
				tree_ikev2.append(tree_ikev2_ike_crypto_profile)

			if advanced_options.get('ikev2_require_cookie'):
				tree_ikev2_require_cookie = Element('require-cookie')
				tree_ikev2_require_cookie.text = advanced_options.get('ikev2_require_cookie')
				tree_ikev2.append(tree_ikev2_require_cookie)

			tree_ikev2.append(tree_ikev2_dpd)
			tree_protocol.append(tree_ikev2)

			# Version

			if advanced_options.get('version') == 'ikev2':
				tree_version = Element('version')
				tree_version.text = advanced_options.get('version')
				tree_protocol.append(tree_version)
			elif advanced_options.get('version') == 'ikev2-preferred':
				tree_version = Element('version')
				tree_version.text = advanced_options.get('version')
				tree_protocol.append(tree_version)

			element_root.append(tree_protocol)

		element = Et.tostring(element_root).decode('UTF-8')

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - IKE Gateway: {} - {}'.format(template_name, general.get('name'), e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'IKE Gateway', general.get('name'))
