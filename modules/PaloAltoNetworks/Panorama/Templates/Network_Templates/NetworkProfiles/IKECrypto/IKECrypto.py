#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class IKECrypto(PaloAltoNetworks):
	"""
	Class to configure IKE Crypto
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ IKECrypto Class')
		super().__init__(panorama_ip, api_key)
		# print('---- IKECrypto Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return IKE Crypto xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/network/ike/crypto-profiles"
		)

		return xpath

	def add_ike_crypto_profile(self, template_name, profile_name, hash_, dh_group, encryption, lifetime):
		"""
		Method to add IKE Crypto profile to Panorama

		:param template_name: Name of template to add configure IKE Crypto to
		:type template_name: str
		:param profile_name: IKE Crypto profile name
		:type profile_name: str
		:param hash_: Hash algorithms to add to IKE Crypto
		:type hash_: list
		:param dh_group: DH Groups to add to IKE Crypto
		:type dh_group: list
		:param encryption: Encryption to add to IKE Crypto
		:type encryption: list
		:param lifetime: IKE Crypto lifetime
		:type lifetime: dict
		:return: None
		:rtype: None

		Example:

		add_ike_crypto_profile(
		template_name='PANW', profile_name='PA_Crypto', hash_=['sha1', 'sha256'], dh_group=['group2', 'group5'],
		encryption=['aes-128-cbc'], lifetime={'hours': '8'}
		)
		"""

		xmx = XMLX()
		xpath = self.__xcode()

		element_root = Element('ike-crypto-profiles')
		# element_tree = ElementTree(element_root)

		tree_entry = Element('entry')
		tree_entry.set('name', '%s' % profile_name)
		element_root.append(tree_entry)

		tree_hash = Element('hash')

		for member_hash in hash_:
			member = Element('member')
			member.text = member_hash
			tree_hash.append(member)

		tree_entry.append(tree_hash)

		tree_dh_group = Element('dh-group')

		for member_dh_group in dh_group:
			member = Element('member')
			member.text = member_dh_group
			tree_dh_group.append(member)

		tree_entry.append(tree_dh_group)

		tree_encryption = Element('encryption')

		for member_encryption in encryption:
			member = Element('member')
			member.text = member_encryption
			tree_encryption.append(member)

		tree_entry.append(tree_encryption)

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
			NLogger.network.info('{} - IKECrypto Profile: {} - {}'.format(template_name, profile_name, e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'IKECrypto Profile', profile_name)

	# def add_ike_crypto_profile(self, template_name, profile_name, hash, dh_group, encryption, lifetime):
	# 	"""
	#
	# 	:param template_name:
	# 	:type template_name:
	# 	:param profile_name:
	# 	:type profile_name:
	# 	:param hash:
	# 	:type hash:
	# 	:param dh_group:
	# 	:type dh_group:
	# 	:param encryption:
	# 	:type encryption:
	# 	:param lifetime:
	# 	:type lifetime:
	# 	:return:
	# 	:rtype:
	# 	"""
	#
	# 	element = ''
	# 	xmx = XMLX()
	#
	# 	xpath = self.__xcode()[0]
	#
	# 	try:
	# 		element += '<ike-crypto-profiles><entry name="%s"><hash>' % profile_name
	#
	# 		for value in hash:
	# 			element += '<member>%s</member>' % value
	# 		else:
	# 			element += '</hash><dh-group>'
	#
	# 		for value in dh_group:
	# 			element += '<member>%s</member>' % value
	# 		else:
	# 			element += '</dh-group><encryption>'
	#
	# 		for value in encryption:
	# 			element += '<member>%s</member>' % value
	# 		else:
	# 			element += '</encryption><lifetime>'
	#
	# 		if lifetime['seconds']:
	# 			element += '<seconds>%s</seconds></lifetime>' % lifetime['seconds']
	# 		elif lifetime['minutes']:
	# 			element += '<minutes>%s</minutes></lifetime>' % lifetime['minutes']
	# 		elif lifetime['hours']:
	# 			element += '<hours>%s</hours></lifetime>' % lifetime['hours']
	# 		elif lifetime['days']:
	# 			element += '<days>%s</days></lifetime>' % lifetime['days']
	#
	# 		element += '</entry></ike-crypto-profiles>'
	# 	except Exception as e:
	# 		NLogger.network.info('{} - IKECrypto Profile: {} - {}'.format(template_name, profile_name, e))
	#
	# 	try:
	# 		uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
	# 		print(uri)
	# 		exit()
	# 	except Exception as e:
	# 		NLogger.network.info('{} - IKECrypto Profile: {} - {}'.format(template_name, profile_name, e))
	# 	else:
	# 		xmx.exec_xml_get(uri, NLogger.network, 'IKECrypto Profile', profile_name)
