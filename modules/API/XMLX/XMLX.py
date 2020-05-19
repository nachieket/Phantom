#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from ..API import API

import requests
import urllib3

urllib3.disable_warnings()


class XMLX(API):
	"""
	XML Class
	"""

	def __init__(self):
		# print('++++ XMLX Class')
		super().__init__()

		self.configure = 'https://{0}/api/?type=config&action=set&xpath={1}&element={2}&key={3}'
		self.update = 'https://{0}/api/?type=config&action=edit&xpath={1}&element={2}&key={3}'
		self.tmove = 'https://{}/api?type=config&action=move&xpath={}&where=top&key={}'
		self.commit = 'https://{}/api?type=commit&cmd=<commit></commit>&key={}'
		self.get = 'https://{}/api/?type=op&cmd={}&key={}'
		# print('---- XMLX Class')

	def exec_xml_get(
		self, uri, logger, type_, name, smsg='Successfully configured', fmsg='Failed to configure', ops='no'
	):
		"""
		Method to execute get request using requests module


		:param uri: URL
		:type uri: str
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
		:param ops: Include this as 'yes' if this is operational command
		:type ops: str
		:return: response
		:rtype: xml
		"""

		logger.info('Executing GET request: {}'.format(uri.split('&key=')[0]))

		try:
			response = requests.get(uri, verify=False)
			# print(response.headers['content-type'])
			# print('Text\n')
			# print(response.text)
			# print('\nStatus_Code\n')
			# print(response.status_code)
			# print('\nURL\n')
			# print(response.url)
			# print('\nRequest\n')
			# print(response.request)
			# print('\nReason\n')
			# print(response.reason)
			# print('\nRaw\n')
			# print(response.raw)
			# print('\nOK\n')
			# print(response.ok)
			# print('\nNext\n')
			# print(response.next)
			# print('\nLinks\n')
			# print(response.links)
			# print('\nContent\n')
			# print(response.content)
		except ConnectionError as e:
			logger.info('{}: {} - {}'.format(type_, name, e))
		except Exception as e:
			logger.info('{}: {} - {}'.format(type_, name, e))
		else:
			if response.headers['content-type'] == 'application/xml; charset=UTF-8':
				if ops == 'yes':
					self.request_status('XML', response, logger, type_, name, smsg, fmsg, ops='yes')
					return response
				else:
					self.request_status('XML', response, logger, type_, name, smsg, fmsg)
					return response
