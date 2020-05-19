#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import json
import xml.etree.ElementTree as Et


class API(object):
	"""
	API Class
	"""

	def __init__(self):
		# print('++++ API Class')
		super().__init__()
		# print('---- API Class')

	@staticmethod
	def request_status(
		method, response, logger, type_, name, smsg='Successfully configured', fmsg='Failed to configure', ops='no'
	):
		"""
		Method to log status of request that was made using requests module


		:param method: XML of Json
		:type method: str
		:param response: Response that was received from a request such as Get or POST
		:type response: Response
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
		:return: None
		:rtype: None
		"""

		if method.upper() == 'XML':
			# print('===================')
			# print(type(response.text))
			# print(response.text)
			# print('===================')
			tree = Et.XML(response.text)

			if ops == 'yes':
				if tree.attrib['status'] == 'success':
					logger.info('{}: {} - {}'.format(type_, smsg, name))
				else:
					logger.info('{}: {} - {}'.format(type_, fmsg, name))
					logger.info('{}: {} - {}'.format(type_, response.reason, name))
			else:
				if tree.attrib['status'] == 'success' and tree.attrib['code'] == '20':
					logger.info('{}: {} - {}'.format(type_, smsg, name))
				else:
					logger.info('{}: {} - {}'.format(type_, fmsg, name))
					logger.info('{}: {} - {}'.format(type_, response.reason, name))
		elif method.upper() == 'JSON':
			code = json.loads(response.text)
			reason = response.reason

			if code['@status'] == 'success' and code['@code'] == '20':
				logger.info('{}: {} - {}'.format(type_, smsg, name))
			else:
				logger.info('{}: {} - {}'.format(type_, fmsg, name))
				logger.info('{}: {} - {}'.format(type_, reason, name))
