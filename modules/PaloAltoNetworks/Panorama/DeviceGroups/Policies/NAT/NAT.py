#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.JSONX.JSONX import JSONX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.PoliciesLogger.PoliciesLogger import PoliciesLogger as Plogger


class NAT(PaloAltoNetworks):
	"""
	Class to configure NAT Rule under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ NAT Class')
		super().__init__(panorama_ip, api_key)

		self.nat_config = (
			'https://%s/restapi/9.0/Policies/NAT%sRules?location=device-group&device-group=%s&name=%s'
		)

		self.nat_move = (
			'https://%s/restapi/9.0/Policies/NAT%sRules?action=move&location=device-group&device-group=%s'
			'&name=%s&where=%s'
		)

		# self.logger = PoliciesLogger()
		# print('---- NAT Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __jcode():
		"""
		Method to return Panorama NAT Rule Json Code for Source NAT

		:return: NAT Rule Json code
		:rtype: dict
		"""

		code = {
				'@name': '',
				'@location': 'device-group',
				'@device-group': '',
				'from': {
					'member': []
				},
				'to': {
					'member': []
				},
				'service': '',
				'source': {
					'member': []
				},
				'destination': {
					'member': []
				}
			}

		return code

	def add_nat_rule(
		self, position, rule_name, device_group, source_zone='any', destination_zone='any',
		destination_interface='any', service='any', source_address='any', destination_address='any',
		snat_interface_ip='', snat_interface_name='', snat_translated_address='', destination_translated_address='',
		destination_translated_port=''
	):
		"""
		Method to add NAT Rule to a Device Group in Panorama

		SNAT Usage: Use either snat_interface_ip + snat_interface_name OR snat_translated_address

		DNAT Usage: User destination_translated_address and destination_translated_port together

		Examples:

		1. Source NAT Example:

		add_nat_rule(
		position='Pre', rule_name='rule31', device_group='PANW', source_zone='trust', destination_zone='untrust',
		destination_interface='any', service='service-http', source_address='any', destination_address='any',
		snat_interface_ip='192.168.55.20', snat_interface_name='ethernet1/1'
		)

		2. Destination NAT Example:

		add_nat_rule(
		position='Pre', rule_name='rule32', device_group='PANW', source_zone='untrust', destination_zone='trust',
		destination_interface='any', service='service-http', source_address='any', destination_address='any',
		snat_interface_ip='192.168.45.20', snat_interface_name='ethernet1/2',
		destination_translated_address='192.168.45.150', destination_translated_port='8080'
		)

		Limitations:

		1. Source NAT supports only dynamic-ip-and-port method
		2. Destination NAT supports only static-ip method

		:param position: Pre or Post - position of NAT rule
		:type position: str
		:param rule_name: Security rule name
		:type rule_name: str
		:param device_group: Device group name
		:type device_group: str
		:param source_zone: Source Zone
		:type source_zone: str
		:param destination_zone: Destination Zone
		:type destination_zone: str
		:param destination_interface: (Optional) Destination Interface
		:type destination_interface: str
		:param service: TCP/UDP Service
		:type service: str
		:param source_address: Source address
		:type source_address: str
		:param destination_address: Destination Address
		:type destination_address: str
		:param snat_interface_ip: (Optional) Interface IP that will be used to translate source address
		:type snat_interface_ip: str
		:param snat_interface_name: (Optional) Interface name such as ethernet1/1
		:type snat_interface_name: str
		:param snat_translated_address: (Optional) IP Address that will be used to translate source address
		:type snat_translated_address: str
		:param destination_translated_address: (Optional) Destination address to translate to
		:type destination_translated_address: str
		:param destination_translated_port: (Optional) Destination port to translate to
		:type destination_translated_port: str
		:return: None
		:rtype: None
		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		jcode = self.__jcode()

		try:
			jcode['@name'] = rule_name
			jcode['@device-group'] = device_group
			jcode['from']['member'].append(source_zone)
			jcode['to']['member'].append(destination_zone)
			jcode['to-interface'] = destination_interface
			jcode['service'] = service
			jcode['source']['member'].append(source_address)
			jcode['destination']['member'].append(destination_address)
		except KeyError as e:
			Plogger.policies.info('{}: {}'.format('NAT Rule - Dict KeyError', e))
		except Exception as e:
			Plogger.policies.info('{}: {}'.format('NAT Rule - Dict Generic Error', e))
		else:
			if snat_interface_ip and snat_interface_name:
				jcode['source-translation'] = {}
				jcode['source-translation']['dynamic-ip-and-port'] = {}
				jcode['source-translation']['dynamic-ip-and-port']['interface-address'] = {}
				jcode['source-translation']['dynamic-ip-and-port']['interface-address']['ip'] = snat_interface_ip
				jcode['source-translation']['dynamic-ip-and-port']['interface-address']['interface'] = \
					snat_interface_name
			elif snat_translated_address:
				jcode['source-translation'] = {}
				jcode['source-translation']['dynamic-ip-and-port'] = {}
				jcode['source-translation']['dynamic-ip-and-port']['translated-address'] = {}
				jcode['source-translation']['dynamic-ip-and-port']['translated-address']['member'].append(
					snat_translated_address
				)

			if destination_translated_address and destination_translated_port:
				jcode['destination-translation'] = {}
				jcode['destination-translation']['translated-port'] = destination_translated_port
				jcode['destination-translation']['translated-address'] = destination_translated_address

			entry = dict()
			entry['entry'] = []
			entry['entry'].append(jcode)

			uri = self.nat_config % (self.panorama_ip, position, device_group, rule_name)

			jsx.exec_json_post(uri, header, Plogger.policies, 'NAT-Rule', rule_name, entry)

	def move_nat_rule(self, position, device_group, rule_name, where):
		"""
		Method to move Panorama NAT rule under a specific device group

		Examples:

		1. Move to Top:

		p.move_nat_rule('Pre', 'PANW', 'rule32', 'top')

		2. Move to Bottom:

		p.move_nat_rule('Pre', 'PANW', 'rule31', 'bottom')

		:param position: Pre or Post - position of security rule
		:type position: str
		:param device_group: Device group name
		:type device_group: str
		:param rule_name: Security rule name
		:type rule_name: str
		:param where: top or bottom; position where security rule needs to be moved to
		:type where: str
		:return: None
		:rtype: None
		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		uri = self.nat_move % (self.panorama_ip, position, device_group, rule_name, where)

		jsx.exec_json_post(
			uri, header, Plogger.policies, 'NAT-Rule', rule_name,
			smsg='Successfully moved to {}'.format(where),
			fmsg='Failed to move to {}'.format(where)
		)

	# @staticmethod
	# def __dnat_xcode():
	# 	"""
	# 	Method to return Panorama DNAT rule xpath and element to place in API request string
	# 	:return: xpath, dnat_element (XML code) and snat_element (XML code)
	# 	:rtype: str
	# 	"""
	#
	# 	xpath = (
	# 		"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s"
	# 		"']/pre-rulebase/nat/rules"
	# 	)
	#
	# 	dnat_element = """
	# 		<entry name="%s">
	# 			<to>
	# 				<member>%s</member>
	# 			</to>
	# 			<from>
	# 				<member>%s</member>
	# 			</from>
	# 			<source>
	# 				<member>%s</member>
	# 			</source>
	# 			<destination>
	# 				<member>%s</member>
	# 			</destination>
	# 			<service>%s</service>
	# 			<target>
	# 				<negate>no</negate>
	# 			</target>
	# 			<dynamic-destination-translation>
	# 				<translated-address>%s</translated-address>
	# 				<translated-port>%s</translated-port>
	# 			</dynamic-destination-translation>
	# 			%s
	# 		</entry>
	# 	"""
	#
	# 	snat_element = """
	# 		<source-translation>
	# 			<dynamic-ip-and-port>
	# 				<interface-address>
	# 					<ip>%s</ip>
	# 					<interface>%s</interface>
	# 				</interface-address>
	# 			</dynamic-ip-and-port>
	# 		</source-translation>
	# 	"""
	#
	# 	return xpath, re.sub(r'\s\s+|\n', '', dnat_element), re.sub(r'\s\s+|\n', '', snat_element)
	#
	# def add_dnat_rule(
	# 	self, ip, key, dg, rule_name, source_address, source_zone, destination_address, destination_zone,
	# 	service, tgt_addr, tgt_port,
	# 	enable_snat, snat_type, snat_addr, snat_interface='ethernet1/2'
	# ):
	# 	"""
	#
	# 	:param ip: Panorama IP
	# 	:type ip: str
	# 	:param key: API key
	# 	:type key: str
	# 	:param dg: Device group name
	# 	:type dg: str
	# 	:param rule_name: NAT rule name
	# 	:type rule_name: str
	# 	:param source_address: Source address
	# 	:type source_address: str
	# 	:param source_zone: Source zone
	# 	:type source_zone: str
	# 	:param destination_address: Destination address
	# 	:type destination_address: str
	# 	:param destination_zone: Destination zone
	# 	:type destination_zone: str
	# 	:param service: TCP/UDP service
	# 	:type service: str
	# 	:param tgt_addr: Target address to forward packets to
	# 	:type tgt_addr: str
	# 	:param tgt_port: Target tcp/udp port to forward packets to
	# 	:type tgt_port: str
	# 	:param enable_snat: Enable/Disable SNAT on source interface; valid values are 'yes' or 'no'
	# 	:type enable_snat: str
	# 	:param snat_type: 'Translated' or 'Interface'
	# 	:type snat_type: str
	# 	:param snat_addr: SNAT address - i.e. 1.1.1.1
	# 	:type snat_addr: str
	# 	:param snat_interface: SNAT interface - i.e. ethernet1/2; this is default value
	# 	:type snat_interface: str
	# 	:return: None
	# 	:rtype: str
	# 	"""
	#
	# 	xpath, dnat_element, snat_element = self.__dnat_xcode()
	#
	# 	if enable_snat == 'yes':
	# 		if snat_type == 'Interface':
	# 			# TODO: Define a method to change hard cording of 1.1.1.1 and ethernet1/2
	#
	# 			response = requests.get(self.configure_nat.format(
	# 				ip,
	# 				xpath % dg,
	# 				dnat_element % (
	# 					rule_name, destination_zone, source_zone, source_address, destination_address, service,
	# 					tgt_addr, tgt_port,
	# 					snat_element % (
	# 						snat_addr, snat_interface
	# 					)
	# 				),
	# 				key
	# 			))
	# 		elif snat_type == 'Translated':
	# 			# TODO: Implement a method to define a specific source IP for SNAT
	# 			response = ''
	# 		else:
	# 			response = ''
	# 	else:
	# 		response = requests.get(self.configure_nat.format(
	# 			ip,
	# 			xpath % dg,
	# 			dnat_element % (
	# 				rule_name, destination_zone, source_zone, source_address, destination_address, service,
	# 				tgt_addr, tgt_port, ''
	# 			),
	# 			key
	# 		))
	#
	# 	self.get_api_status(response, rule_name, '{}: NAT-Rule'.format(dg), self.logger)
	#
	# @staticmethod
	# def __move_xcode():
	# 	"""
	# 	Method to return Panorama xpath to move NAT rule
	# 	:return: xpath (XML code)
	# 	"""
	#
	# 	xpath = (
	# 		"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s"
	# 		"']/pre-rulebase/nat/rules/entry[@name='%s']"
	# 	)
	#
	# def move_nat_rule(self):
	# 	pass
