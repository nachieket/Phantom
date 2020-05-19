#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.JSONX.JSONX import JSONX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.ObjectsLogger.ObjectsLogger import ObjectsLogger as Ologger


class Address(PaloAltoNetworks):
	"""
	Class to configure Addresses under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Address Class')
		super().__init__(panorama_ip, api_key)

		self.dg_address_config = (
			'https://%s/restapi/9.0/Objects/Addresses?location=device-group&device-group=%s&name=%s'
		)

		self.shared_address_config = (
			'https://%s/restapi/9.0/Objects/Addresses?location=shared&name=%s'
		)
		# print('---- Address Class')

	def __str__(self):
		return self.__class__.__name__

	def configure_address(
		self, action='add', device_group=None, name=None, location=None, disable_override=None, description=None,
		type_=None, address_value=None, tag=None
	):
		"""
		Method to add address under a Device Group in Panorama

		:param action: (mandatory) Action - add or update
		:type action: str
		:param device_group: (either device_group or location) Device group name
		:type device_group: str
		:param name: (mandatory) Address name
		:type name: str
		:param location: (either device_group or location) shared or not
		:type location: str
		:param disable_override: (optional) Disable override or not
		:type disable_override: str
		:param description: (optional) Description of the address object
		:type description: str
		:param type_: (mandatory) Type of object - ip-netmask, ip-range, ipp-wildcard, fqdn
		:type type_: str
		:param address_value: (mandatory) IP Address
		:type address_value: str
		:param tag: (optional) List of tags; tags are not allowed in 'ip-wildcard' type
		:type tag: list
		:return: None
		:rtype: None

		Device Group Examples:

		configure_address(
		action='add', device_group='PANW', name='Desktop101', description='Corporate Machine',
		type_='ip-range', address_value='1.1.1.1-1.1.1.10', tag=['Critical', 'Allow'], disable_override='yes'
		)

		configure_address(
			action='add', device_group='PANW', name='Desktop102', description='Corporate Machine',
			type_='ip-wildcard', address_value='10.20.1.0/0.0.248.255', disable_override='yes'
		)

		configure_address(
			action='add', device_group='PANW', name='Desktop103', description='Corporate Machine',
			type_='fqdn', address_value='www.msn.com', tag=['Critical', 'Allow'], disable_override='yes'
		)

		configure_address(
			action='add', device_group='PANW', name='Desktop104', description='Corporate Machine',
			type_='ip-netmask', address_value='2.2.2.0/28', tag=['Critical', 'Allow'], disable_override='yes'
		)

		Shared Examples:

		configure_address(
		action='add', location='shared', name='Desktop101', description='Corporate Machine',
		type_='ip-range', address_value='1.1.1.1-1.1.1.10', tag=['Critical', 'Allow']
		)

		configure_address(
			action='add', location='shared', name='Desktop102', description='Corporate Machine',
			type_='ip-wildcard', address_value='10.20.1.0/0.0.248.255'
		)

		configure_address(
			action='add', location='shared', name='Desktop103', description='Corporate Machine',
			type_='fqdn', address_value='www.msn.com', tag=['Critical', 'Allow']
		)

		configure_address(
			action='add', location='shared', name='Desktop104', description='Corporate Machine',
			type_='ip-netmask', address_value='2.2.2.0/28', tag=['Critical', 'Allow']
		)
		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		if action == 'add':
			try:
				address = dict()

				address['@name'] = name

				if location:
					if location == 'shared':
						address['@location'] = 'shared'
				else:
					address['@location'] = "device-group"
					address['@device-group'] = device_group
					address['@loc'] = device_group

					if disable_override:
						if disable_override == 'yes':
							address['disable-override'] = 'yes'

				if description:
					address['description'] = description

				if type_ == 'ip-netmask':
					address['ip-netmask'] = address_value
				elif type_ == 'ip-range':
					address['ip-range'] = address_value
				elif type_ == 'ip-wildcard':
					address['ip-wildcard'] = address_value
				elif type_ == 'fqdn':
					address['fqdn'] = address_value

				if tag:
					if type_ in ('ip-netmask', 'ip-range', 'fqdn'):
						address['tag'] = {}
						address['tag']['member'] = []

						for t in tag:
							address['tag']['member'].append(t)
			except KeyError as e:
				Ologger.policies.info('{}: {}'.format('Address - Dict KeyError', e))
			except ValueError as e:
				Ologger.policies.info('{}: {}'.format('Address - Dict ValueError', e))
			except Exception as e:
				Ologger.policies.info('{}: {}'.format('Address - Dict Generic Error', e))
			else:
				entry = dict()
				entry['entry'] = []
				entry['entry'].append(address)

				if location:
					uri = self.shared_address_config % (self.panorama_ip, name)
				else:
					uri = self.dg_address_config % (self.panorama_ip, device_group, name)

				jsx.exec_json_post(uri, header, Ologger.policies, 'Address', name, entry)
