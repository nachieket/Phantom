#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..API import API

import requests
import json


class JSONX(API):
	"""
	JSON Class
	"""

	def __init__(self):
		# print('++++ JSONX Class')
		super().__init__()
		# print('---- JSONX Class')

	def exec_json_post(
		self, uri, header, logger, type_, name, data='', smsg='Successfully configured', fmsg='Failed to configure'
	):
		"""
		Method to execute post request using requests module

		:param uri: URL
		:type uri: str
		:param data: Data to be submitted to URL
		:type data: dict
		:param header: Header information; in this case it is likely to be API key
		:type header: dict
		:param logger: Logger to log messages to
		:type logger: logging.Logger
		:param type_: Configuration type - e.g. Template, Device Group, Security Rule etc; note '_' in name
		:type type_: str
		:param name: Name of the configuration type - e.g. name of Template or Security/NAT rule
		:type name: str
		:param smsg: Message to display when configuration was successful
		:type smsg: str
		:param fmsg: Message to display when configuration failed
		:type fmsg: str
		:return: None
		:rtype: None
		"""

		logger.info('Executing POST request: {}'.format(uri))

		if data:
			logger.info('POST request with data: {}'.format(data))

			response = requests.post(uri, data=json.dumps(data), headers=header, verify=False)

			self.request_status('JSON', response, logger, type_, name, smsg, fmsg)
		else:
			response = requests.post(uri, headers=header, verify=False)

			self.request_status('JSON', response, logger, type_, name, smsg, fmsg)
