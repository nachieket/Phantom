#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ......API.JSONX.JSONX import JSONX
from .....PaloAltoNetworks import PaloAltoNetworks
from ......Logger.ObjectsLogger.ObjectsLogger import ObjectsLogger as Ologger


class AddressGroups(PaloAltoNetworks):
	"""
	Class to configure Address Groups under Device Group
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Address Group Class')
		super().__init__(panorama_ip, api_key)

		self.dg_address_group_config = (
			'https://%s/restapi/9.0/Objects/AddressGroups?location=device-group&device-group=%s&name=%s'
		)

		self.shared_address_group_config = (
			'https://%s/restapi/9.0/Objects/AddressGroups?location=shared&name=%s'
		)
		# print('---- Address Group Class')

	def __str__(self):
		return self.__class__.__name__

	def configure_address_group(
		self, action='add', device_group=None, name=None, location=None, disable_override=None, description=None,
		type_=None, address_group_value=None, tag=None
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
		:param type_: (mandatory) Type of object - static (dynamic not supported as of now)
		:type type_: str
		:param address_group_value: (mandatory) List of addresses
		:type address_group_value: list
		:param tag: (optional) List of tags
		:type tag: list
		:return: None
		:rtype: None

		Device Group Examples:

		configure_address_group(
		action='add', device_group='PANW', name='group101', description='Corporate Group',
		type_='static', address_group_value=['Desktop101', 'Desktop103'], tag=['Critical', 'Allow']
		)

		Shared Examples:

		configure_address_group(
		action='add', location='shared', name='group102', description='Corporate Group',
		type_='static', address_group_value=['Desktop111', 'Desktop112'], tag=['Allow']
		)


		"""

		header = dict()
		header['X-PAN-KEY'] = self.api_key

		jsx = JSONX()

		if action == 'add':
			try:
				address_group = dict()

				address_group['@name'] = name

				if location:
					if location == 'shared':
						address_group['@location'] = 'shared'
				else:
					address_group['@location'] = "device-group"
					address_group['@device-group'] = device_group
					address_group['@loc'] = device_group

					if disable_override:
						if disable_override == 'yes':
							address_group['disable-override'] = 'yes'

				if description:
					address_group['description'] = description

				if type_ == 'static':
					address_group['static'] = {}
					address_group['static']['member'] = []

					for value in address_group_value:
						address_group['static']['member'].append(value)
				elif type_ == 'dynamic':
					# TODO: to be implemented in future
					pass

				if tag:
					address_group['tag'] = {}
					address_group['tag']['member'] = []

					for t in tag:
						address_group['tag']['member'].append(t)
			except KeyError as e:
				Ologger.policies.info('{}: {}'.format('Address Group - Dict KeyError', e))
			except ValueError as e:
				Ologger.policies.info('{}: {}'.format('Address Group - Dict ValueError', e))
			except Exception as e:
				Ologger.policies.info('{}: {}'.format('Address Group - Dict Generic Error', e))
			else:
				entry = dict()
				entry['entry'] = []
				entry['entry'].append(address_group)

				if location:
					uri = self.shared_address_group_config % (self.panorama_ip, name)
				else:
					uri = self.dg_address_group_config % (self.panorama_ip, device_group, name)

				jsx.exec_json_post(uri, header, Ologger.policies, 'Address Group', name, entry)
