#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.JSONX.JSONX import JSONX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.ObjectsLogger.ObjectsLogger import ObjectsLogger as Ologger


class LogForwarding(PaloAltoNetworks):
	"""
	Class to configure Log Forwarding Profile under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Log Forwarding Profile Class')
		super().__init__(panorama_ip, api_key)

		self.dg_log_forward_config = (
			'https://%s/restapi/9.0/Objects/LogForwardingProfiles?location=device-group&device-group=%s&name=%s'
		)

		self.shared_log_forward_config = (
			'https://%s/restapi/9.0/Objects/LogForwardingProfiles?location=shared&name=%s'
		)
		# print('---- Log Forwarding Profile Class')

	def __str__(self):
		return self.__class__.__name__

	def configure_log_forwarding_profile(
		self, action='add', device_group=None, name=None, location=None, disable_override=None, description=None,
		log_types=None
	):
		"""
		Method to add address under a Device Group in Panorama


		:param action: (mandatory) Action - add or update
		:type action: str
		:param device_group: (either device_group or location) Device group name
		:type device_group: str
		:param name: (mandatory) Address group name
		:type name: str
		:param location: (either device_group or location) shared or not
		:type location: str
		:param disable_override: (optional) Disable override or not
		:type disable_override: str
		:param description: (optional) Description of the address group object
		:type description: str
		:param log_types: (mandatory) Log types to be added to the profile; look examples below
		:type log_types: list
		# :param enhanced_app_logging: Enable enhanced app logging
		# :type enhanced_app_logging: str
		:return: None
		:rtype: None

		Log Types List Example:

		auth = {
			'name': 'Auth_Logs', 'type': 'auth', 'filter': 'All Logs', 'Desc': 'All Auth Logs', 'Panorama': 'yes',
			'snmp': ['1.1.1.1'], 'email': ['someone@xyz.com'], 'syslog': ['2.2.2.2'], 'http': ['3.3.3.3']
		}

		data = {
			'name': 'Data_Logs', 'type': 'data', 'filter': 'All Logs', 'Desc': 'All Data Logs', 'Panorama': 'yes'
		}

		threat = {
			'name': 'Threat_Logs', 'type': 'threat', 'filter': 'All Logs', 'Desc': 'All Threat Logs', 'Panorama': 'yes'
		}

		traffic = {
			'name': 'Traffic_Logs', 'type': 'traffic', 'filter': 'All Logs', 'Desc': 'All Traffic Logs', 'Panorama': 'yes'
		}

		tunnel = {
			'name': 'Tunnel_Logs', 'type': 'tunnel', 'filter': 'All Logs', 'Desc': 'All Tunnel Logs', 'Panorama': 'yes'
		}

		url = {
			'name': 'URL_Logs', 'type': 'url', 'filter': 'All Logs', 'Desc': 'All URL Logs', 'Panorama': 'yes'
		}

		wildfire = {
			'name': 'Wildfire_Logs', 'type': 'wildfire', 'filter': 'All Logs', 'Desc': 'All Wildfire Logs', 'Panorama': 'yes'
		}

		Device Group Examples:

		configure_log_forwarding_profile(
			action='add', device_group='PANW', name='PA_Log_Forwarding_Profile', disable_override='yes',
			description='Prisma Access Log Forwarding Profile',
			log_types=[auth, data, threat, traffic, tunnel, url, wildfire], enhanced_app_logging='yes'
		)

		Shared Examples:

		auth = {
		'name': 'Auth_Logs', 'type': 'auth', 'filter': 'All Logs', 'Desc': 'All Auth Logs', 'Panorama': 'yes'
		}

		data = {
			'name': 'Data_Logs', 'type': 'data', 'filter': 'All Logs', 'Desc': 'All Data Logs', 'Panorama': 'yes'
		}

		threat = {
			'name': 'Threat_Logs', 'type': 'threat', 'filter': 'All Logs', 'Desc': 'All Threat Logs', 'Panorama': 'yes'
		}

		traffic = {
			'name': 'Traffic_Logs', 'type': 'traffic', 'filter': 'All Logs', 'Desc': 'All Traffic Logs', 'Panorama': 'yes'
		}

		tunnel = {
			'name': 'Tunnel_Logs', 'type': 'tunnel', 'filter': 'All Logs', 'Desc': 'All Tunnel Logs', 'Panorama': 'yes'
		}

		url = {
			'name': 'URL_Logs', 'type': 'url', 'filter': 'All Logs', 'Desc': 'All URL Logs', 'Panorama': 'yes'
		}

		wildfire = {
			'name': 'Wildfire_Logs', 'type': 'wildfire', 'filter': 'All Logs', 'Desc': 'All Wildfire Logs',
			'Panorama': 'yes'
		}

		p.configure_log_forwarding_profile(
			action='add', location='shared', name='GA_Log_Forwarding_Profile',
			description='Prisma Access Log Forwarding Profile',
			log_types=[auth, data, threat, traffic, tunnel, url, wildfire], enhanced_app_logging='yes'
		)


		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		if action == 'add':
			try:
				log_forward = dict()

				log_forward['@name'] = name

				if location:
					if location == 'shared':
						log_forward['@location'] = 'shared'
				else:
					log_forward['@location'] = "device-group"
					log_forward['@device-group'] = device_group
					log_forward['@loc'] = device_group

					if disable_override:
						if disable_override == 'yes':
							log_forward['disable-override'] = 'yes'

				if description:
					log_forward['description'] = description

				sub_entry = []

				for log_type in log_types:
					logs = dict()

					logs['@name'] = log_type.get('name')
					logs['log-type'] = log_type.get('type')

					if log_type.get('filter') is not None:
						logs['filter'] = log_type.get('filter')
					else:
						logs['filter'] = 'All Logs'

					if log_type.get('Panorama') is not None:
						logs['send-to-panorama'] = log_type.get('Panorama')

					if log_type.get('Desc') is not None:
						logs['action-desc'] = log_type.get('Desc')

					if log_type.get('snmp') is not None:
						logs['send-snmptrap'] = {}
						logs['send-snmptrap']['member'] = []

						for snmp in log_type.get('snmp'):
							logs['send-snmptrap']['member'].append(snmp)

					if log_type.get('email') is not None:
						logs['send-email'] = {}
						logs['send-email']['member'] = []

						for email in log_type.get('email'):
							logs['send-email']['member'].append(email)

					if log_type.get('syslog') is not None:
						logs['send-syslog'] = {}
						logs['send-syslog']['member'] = []

						for syslog in log_type.get('syslog'):
							logs['send-syslog']['member'].append(syslog)

					if log_type.get('http') is not None:
						logs['send-http'] = {}
						logs['send-http']['member'] = []

						for http in log_type.get('http'):
							logs['send-http']['member'].append(http)

					sub_entry.append(logs)

				log_forward['match-list'] = {}
				log_forward['match-list']['entry'] = sub_entry
				# log_forward['match-list']['entry'].append(sub_entry)

				# if enhanced_app_logging:
				# 	log_forward['enhanced-application-logging'] = enhanced_app_logging
			except KeyError as e:
				Ologger.policies.info('{}: {}'.format('Log Forwarding Profile - Dict KeyError', e))
			except ValueError as e:
				Ologger.policies.info('{}: {}'.format('Log Forwarding Profile - Dict ValueError', e))
			except Exception as e:
				Ologger.policies.info('{}: {}'.format('Log Forwarding Profile - Dict Generic Error', e))
			else:
				entry = dict()
				entry['entry'] = []
				entry['entry'].append(log_forward)

				# print(entry)
				# exit()

				if location:
					uri = self.shared_log_forward_config % (self.panorama_ip, name)
				else:
					uri = self.dg_log_forward_config % (self.panorama_ip, device_group, name)

				jsx.exec_json_post(uri, header, Ologger.policies, 'Log Forwarding Profile', name, entry)
