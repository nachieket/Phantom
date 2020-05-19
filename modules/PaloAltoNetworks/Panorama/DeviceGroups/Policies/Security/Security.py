#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.JSONX.JSONX import JSONX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.PoliciesLogger.PoliciesLogger import PoliciesLogger as Plogger


class Security(PaloAltoNetworks):
	"""
	Class to configure Security Rule under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Security Class')
		super().__init__(panorama_ip, api_key)

		self.security_config = (
			'https://%s/restapi/9.0/Policies/Security%sRules?location=device-group&device-group=%s&name=%s'
		)

		self.security_move = (
			'https://%s/restapi/9.0/Policies/Security%sRules?action=move&location=device-group&device-group=%s'
			'&name=%s&where=%s'
		)
		# print('---- Security Class')

	def __str__(self):
		return self.__class__.__name__

	def configure_security_rule(
		self, action, position, rule_name, device_group, source_zone='any', source_address='any', source_user='any',
		hip_profile='any', destination_zone='any', destination_address='any', application='any', service='any',
		url_category='any', rule_action='allow', virus=None, vulnerability=None, spyware=None,
		url_filtering=None, file_blocking=None, data_filtering='', wildfire=None,
		log_start='', log_forwarding=''
	):
		"""
		Method to add security rule under to a Device Group in Panorama

		:param action: Action - add or update
		:type action: str
		:param position: Pre or Post - position of security rule
		:type position: str
		:param rule_name: Security rule name
		:type rule_name: str
		:param device_group: Device group name
		:type device_group: str
		:param source_zone: Source Zone
		:type source_zone: list
		:param source_address: Source Address
		:type source_address: list
		:param source_user: Source User
		:type source_user: list
		:param hip_profile: HIP Profile
		:type hip_profile: list
		:param destination_zone: Destination Zone
		:type destination_zone: list
		:param destination_address: Destination Address
		:type destination_address: list
		:param application: Layer 7 Application
		:type application: list
		:param service: TCP/UDP Service
		:type service: list
		:param url_category: URL category
		:type url_category: list
		:param rule_action: Allow or Deny
		:type rule_action: str
		:param virus: Anti-Virus security profile
		:type virus: str
		:param vulnerability: Vulnerability/IPS security profile
		:type vulnerability: str
		:param spyware: Anti-Spyware security profile
		:type spyware: str
		:param url_filtering: URL Filtering security profile
		:type url_filtering: str
		:param file_blocking: File Blocking security profile
		:type file_blocking: str
		:param data_filtering: File Blocking security profile
		:type data_filtering: str
		:param wildfire: Wildfire security profile
		:type wildfire: str
		:param log_start: Log at start of the session
		:type log_start: str
		:param log_forwarding: Log forward profile name
		:type log_forwarding: str
		:return: None
		:rtype: None

		Example:

		configure_security_rule(
		action='add', position='Pre', rule_name='rule1', device_group='PANW', source_zone=['trust'],
		source_address=['10.10.10.0/24', '172.16.10.0/24'], source_user=['any'], hip_profile=['any'],
		destination_zone=['untrust'], destination_address=['1.1.1.0/24', '2.2.2.0/24'],
		application=['facebook', 'ssl'], service=['application-default'], url_category=['any'], rule_action='allow',
		data_filtering='something'
		)
		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		if action == 'add':
			try:
				security_rule = dict()

				security_rule['@name'] = rule_name
				security_rule['@location'] = "device-group"
				security_rule['@device-group'] = device_group

				security_rule['from'] = {}
				security_rule['from']['member'] = []

				for zone in source_zone:
					security_rule['from']['member'].append(zone)

				security_rule['source'] = {}
				security_rule['source']['member'] = []

				for address in source_address:
					security_rule['source']['member'].append(address)

				security_rule['source-user'] = {}
				security_rule['source-user']['member'] = []

				for user in source_user:
					security_rule['source-user']['member'].append(user)

				security_rule['hip-profiles'] = {}
				security_rule['hip-profiles']['member'] = []

				for hip in hip_profile:
					security_rule['hip-profiles']['member'].append(hip)

				security_rule['to'] = {}
				security_rule['to']['member'] = []

				for zone in destination_zone:
					security_rule['to']['member'].append(zone)

				security_rule['destination'] = {}
				security_rule['destination']['member'] = []

				for address in destination_address:
					security_rule['destination']['member'].append(address)

				security_rule['application'] = {}
				security_rule['application']['member'] = []

				for app in application:
					security_rule['application']['member'].append(app)

				security_rule['service'] = {}
				security_rule['service']['member'] = []

				for serv in service:
					security_rule['service']['member'].append(serv)

				security_rule['category'] = {}
				security_rule['category']['member'] = []

				for cat in url_category:
					security_rule['category']['member'].append(cat)

				security_rule['action'] = rule_action

				security_rule['profile-setting'] = {}
				security_rule['profile-setting']['profiles'] = {}

				if virus:
					security_rule['profile-setting']['profiles']['virus'] = {}
					security_rule['profile-setting']['profiles']['virus']['member'] = []
					security_rule['profile-setting']['profiles']['virus']['member'].append(virus)

				if vulnerability:
					security_rule['profile-setting']['profiles']['vulnerability'] = {}
					security_rule['profile-setting']['profiles']['vulnerability']['member'] = []
					security_rule['profile-setting']['profiles']['vulnerability']['member'].append(vulnerability)

				if spyware:
					security_rule['profile-setting']['profiles']['spyware'] = {}
					security_rule['profile-setting']['profiles']['spyware']['member'] = []
					security_rule['profile-setting']['profiles']['spyware']['member'].append(spyware)

				if url_filtering:
					security_rule['profile-setting']['profiles']['url-filtering'] = {}
					security_rule['profile-setting']['profiles']['url-filtering']['member'] = []
					security_rule['profile-setting']['profiles']['url-filtering']['member'].append(url_filtering)

				if file_blocking:
					security_rule['profile-setting']['profiles']['file-blocking'] = {}
					security_rule['profile-setting']['profiles']['file-blocking']['member'] = []
					security_rule['profile-setting']['profiles']['file-blocking']['member'].append(file_blocking)

				if wildfire:
					security_rule['profile-setting']['profiles']['wildfire-analysis'] = {}
					security_rule['profile-setting']['profiles']['wildfire-analysis']['member'] = []
					security_rule['profile-setting']['profiles']['wildfire-analysis']['member'].append(wildfire)
			except KeyError as e:
				Plogger.policies.info('{}: {}'.format('Security Rule - Dict KeyError', e))
			except ValueError as e:
				Plogger.policies.info('{}: {}'.format('Security Rule - Dict ValueError', e))
			except Exception as e:
				Plogger.policies.info('{}: {}'.format('Security Rule - Dict Generic Error', e))
			else:
				if data_filtering:
					security_rule['profile-setting']['profiles']['data-filtering'] = {}
					security_rule['profile-setting']['profiles']['data-filtering']['member'] = []
					security_rule['profile-setting']['profiles']['data-filtering']['member'].append(data_filtering)

				if log_start == 'yes':
					security_rule['log-start'] = 'yes'

				if log_forwarding:
					security_rule['log-setting'] = log_forwarding

				entry = dict()
				entry['entry'] = []
				entry['entry'].append(security_rule)

				uri = self.security_config % (self.panorama_ip, position, device_group, rule_name)

				jsx.exec_json_post(uri, header, Plogger.policies, 'Security-Rule', rule_name, entry)

	def move_security_rule(self, position, device_group, rule_name, where):
		"""
		Method to move Panorama security rule under a specific device group

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

		uri = self.security_move % (self.panorama_ip, position, device_group, rule_name, where)

		jsx.exec_json_post(
			uri, header, Plogger.policies, 'Security-Rule', rule_name,
			smsg='Successfully moved to {}'.format(where),
			fmsg='Failed to move to {}'.format(where)
		)

	# @staticmethod
	# def __xcode():
	# 	"""
	# 	Method to return Panorama security rule xpath and element to place in API request string
	# 	:return: xpath and element (XML code)
	# 	"""
	#
	# 	xpath = (
	# 		"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s"
	# 		"']/pre-rulebase/security/rules"
	# 	)
	#
	# 	element = """
	# 				<entry name="%s">
	# 					<profile-setting>
	# 						<profiles>
	# 							<url-filtering>
	# 							<member>%s</member>
	# 							</url-filtering>
	# 							<file-blocking>
	# 							<member>%s</member>
	# 							</file-blocking>
	# 							<virus>
	# 							<member>%s</member>
	# 							</virus>
	# 							<spyware>
	# 							<member>%s</member>
	# 							</spyware>
	# 							<vulnerability>
	# 							<member>%s</member>
	# 							</vulnerability>
	# 							<wildfire-analysis>
	# 							<member>%s</member>
	# 							</wildfire-analysis>
	# 						</profiles>
	# 					</profile-setting>
	# 					<to>
	# 						<member>%s</member>
	# 					</to>
	# 					<from>
	# 						<member>%s</member>
	# 					</from>
	# 					<source>
	# 						%s
	# 					</source>
	# 					<destination>
	# 						%s
	# 					</destination>
	# 					<source-user>
	# 						<member>any</member>
	# 					</source-user>
	# 					<category>
	# 						<member>any</member>
	# 					</category>
	# 					<application>
	# 						<member>%s</member>
	# 					</application>
	# 					<service>
	# 						<member>%s</member>
	# 					</service>
	# 					<hip-profiles>
	# 						<member>any</member>
	# 					</hip-profiles>
	# 					<action>%s</action>
	# 					<log-setting>%s</log-setting>
	# 				</entry>
	# 				"""
	#
	# 	return xpath, re.sub(r'\s\s+|\n', '', element)
	#
	# @staticmethod
	# def __move_xcode():
	# 	"""
	# 	Method to return Panorama xpath to place in API request string to move security rule
	# 	:return: xpath
	# 	"""
	#
	# 	xpath = (
	# 		"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s"
	# 		"']/pre-rulebase/security/rules/entry[@name='%s']"
	# 	)
	#
	# 	return xpath
	#
	# def xadd_security_rule(
	# 	self, ip, key, dg, rule_name, szone, sadd, dzone, dadd, app, service, action, log, url_filtering='default',
	# 	file_blocking='basic file blocking', virus='default', spyware='default', vulnerability='default',
	# 	wildfire='default'
	# ):
	# 	"""
	# 	Method to configure security rule under a specific device group
	#
	# 	:param ip: Panorama ip
	# 	:param key: API key
	# 	:param dg: Device group name
	# 	:param rule_name: Security rule name
	# 	:param szone: Source Zone
	# 	:param sadd: Source Address
	# 	:param dzone: Destination Zone
	# 	:param dadd: Destination Address
	# 	:param app: Layer 7 Application
	# 	:param service: TCP/UDP Service
	# 	:param action: Allow or Deny
	# 	:param log: Log location
	# 	:param url_filtering: URL Filtering security profile
	# 	:param file_blocking: File Blocking security profile
	# 	:param virus: Anti-Virus security profile
	# 	:param spyware: Anti-Spyware security profile
	# 	:param vulnerability: Vulnerability/IPS security profile
	# 	:param wildfire: Wildfire security profile
	# 	:return: Not planning to return success or failure as of now; may change in future
	# 	"""
	#
	# 	xpath, element = self.__xcode()
	#
	# 	response = requests.get(self.configure.format(
	# 		ip,
	# 		xpath % dg,
	# 		element % (
	# 			rule_name, url_filtering, file_blocking, virus, spyware, vulnerability, wildfire, dzone, szone,
	# 			sadd, dadd, app, service, action, log
	# 		),
	# 		key), verify=False)
	#
	# 	self.get_api_status(response, rule_name, '{}: Security-Rule'.format(dg), self.logger)
	#
	# def move_security_rule_to_top(self, ip, key, dg, rule_name):
	# 	"""
	# 	Method to move security rule to top under a specific device group
	#
	# 	:param ip: Panorama ip
	# 	:param key: API key
	# 	:param dg: Device group name
	# 	:param rule_name: Security rule name
	# 	:return: Not planning to return success or failure as of now; may change in future
	# 	"""
	#
	# 	xpath = self.__move_xcode()
	#
	# 	response = requests.get(self.tmove.format(
	# 		ip,
	# 		xpath % (dg, rule_name),
	# 		key
	# 	))
	#
	# 	smsg = 'Successfully moved to top'
	# 	fmsg = 'Failed to move to top'
	#
	# 	self.get_api_status(response, rule_name, '{}: Security-Rule'.format(dg), self.logger, smsg, fmsg)

		# jcode = self.__jcode()

	# @staticmethod
	# def __jcode():
	# 	"""
	# 	Method to return Panorama Security Rule Json Code
	# 	:return: Json code
	# 	:rtype: dict
	# 	"""
	#
	# 	code = {
	# 			"@name": "",
	# 			"@location": "device-group",
	# 			"@device-group": "",
	# 			"from": {
	# 				"member": []
	# 			},
	# 			"source": {
	# 				"member": []
	# 			},
	# 			"source-user": {
	# 				"member": []
	# 			},
	# 			"hip-profiles": {
	# 				"member": []
	# 			},
	# 			"to": {
	# 				"member": []
	# 			},
	# 			"destination": {
	# 				"member": []
	# 			},
	# 			"application": {
	# 				"member": []
	# 			},
	# 			"service": {
	# 				"member": []
	# 			},
	# 			"category": {
	# 				"member": []
	# 			},
	# 			"action": "",
	# 			'profile-setting': {
	# 				'profiles': {
	# 					'virus': {
	# 						'member': []
	# 					},
	# 					'vulnerability': {
	# 						'member': []
	# 					},
	# 					'spyware': {
	# 						'member': []
	# 					},
	# 					'url-filtering': {
	# 						'member': []
	# 					},
	# 					'file-blocking': {
	# 						'member': []
	# 					},
	# 					'wildfire-analysis': {
	# 						'member': []
	# 					}
	# 				}
	# 			},
	# 		}
	#
	# 	return code

# jcode['@name'] = rule_name
# jcode['@device-group'] = device_group
# jcode['from']['member'].append(source_zone)
# jcode['source']['member'].append(source_address)
# jcode['source-user']['member'].append(source_user)
# jcode['hip-profiles']['member'].append(hip_profile)
# jcode['to']['member'].append(destination_zone)
# jcode['destination']['member'].append(destination_address)
# jcode['application']['member'].append(application)
# jcode['service']['member'].append(service)
# jcode['category']['member'].append(url_category)
# jcode['action'] = rule_action
# jcode['profile-setting']['profiles']['virus']['member'].append(virus)
# jcode['profile-setting']['profiles']['vulnerability']['member'].append(vulnerability)
# jcode['profile-setting']['profiles']['spyware']['member'].append(spyware)
# jcode['profile-setting']['profiles']['url-filtering']['member'].append(url_filtering)
# jcode['profile-setting']['profiles']['file-blocking']['member'].append(file_blocking)
# jcode['profile-setting']['profiles']['wildfire-analysis']['member'].append(wildfire)


# jcode['profile-setting']['profiles']['data-filtering'] = {'member': []}
# jcode['profile-setting']['profiles']['data-filtering']['member'].append(data_filtering)

# jcode['log-start'] = 'yes'
# jcode['log-setting'] = log_forwarding
