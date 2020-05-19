#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class IPSecCrypto(PaloAltoNetworks):
	"""
	Class to configure IPSec Crypto
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ IPSecCrypto Class')
		super().__init__(panorama_ip, api_key)
		# print('---- IPSecCrypto Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return IPSec Crypto xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/ike/crypto-profiles"
		)

		return xpath

	def add_ipsec_crypto_profile(
		self, template_name, profile_name, protocol, encryption=None, authentication=None, dh_group=None,
		lifetime=None
	):
		"""
		Method to add IPSec Crypto profile to Panorama

		:param template_name: Name of template to add configure IPSec Crypto to
		:type template_name: str
		:param profile_name: IPSec Crypto profile name
		:type profile_name: str
		:param protocol: ESP or AH
		:type protocol: str
		:param encryption: Encryption to add to IPSec Crypto
		:type encryption: list
		:param authentication: Hash algorithms to add to IPSec Crypto
		:type authentication: list
		:param dh_group: DH Groups to add to IPSec Crypto
		:type dh_group: str
		:param lifetime: IPSec Crypto lifetime
		:type lifetime: dict
		:return: None
		:rtype: None

		Example:

		ESP:

		add_ipsec_crypto_profile(
		template_name='PANW', profile_name='IPSec_Crypto', protocol='esp', encryption=['aes-128-cbc'],
		authentication=['sha1'], dh_group='group20', lifetime={'hours': '8'}
		)

		AH:

		add_ipsec_crypto_profile(
		template_name='PANW', profile_name='IPSec_Crypto', protocol='AH', authentication=['sha1'],
		dh_group='group20', lifetime={'hours': '8'}
		)
		"""

		xmx = XMLX()
		xpath = self.__xcode()

		element_root = Element('ipsec-crypto-profiles')
		# element_tree = ElementTree(element_root)

		tree_entry = Element('entry')
		tree_entry.set('name', '%s' % profile_name)
		element_root.append(tree_entry)

		if protocol.lower() == 'esp':
			tree_esp = Element('esp')

			tree_encryption = Element('encryption')

			for member_encryption in encryption:
				member = Element('member')
				member.text = member_encryption
				tree_encryption.append(member)
			else:
				tree_esp.append(tree_encryption)

			tree_authentication = Element('authentication')

			for member_authentication in authentication:
				member = Element('member')
				member.text = member_authentication
				tree_authentication.append(member)
			else:
				tree_esp.append(tree_authentication)

			tree_entry.append(tree_esp)
		elif protocol.lower() == 'ah':
			tree_ah = Element('ah')

			tree_authentication = Element('authentication')

			for member_authentication in authentication:
				member = Element('member')
				member.text = member_authentication
				tree_authentication.append(member)
			else:
				tree_ah.append(tree_authentication)

			tree_entry.append(tree_ah)

		tree_dh_group = Element('dh-group')
		tree_dh_group.text = dh_group

		tree_entry.append(tree_dh_group)

		tree_lifetime = Element('lifetime')

		if lifetime.get('seconds'):
			seconds = Element('seconds')
			seconds.text = lifetime['seconds']
			tree_lifetime.append(seconds)
		elif lifetime.get('minutes'):
			minutes = Element('minutes')
			minutes.text = lifetime['minutes']
			tree_lifetime.append(minutes)
		elif lifetime.get('hours'):
			hours = Element('hours')
			hours.text = lifetime['hours']
			tree_lifetime.append(hours)
		elif lifetime.get('days'):
			days = Element('days')
			days.text = lifetime['days']
			tree_lifetime.append(days)

		tree_entry.append(tree_lifetime)

		element = Et.tostring(element_root).decode('UTF-8')

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - IPSecCrypto Profile: {} - {}'.format(template_name, profile_name, e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'IPSecCrypto Profile', profile_name)
