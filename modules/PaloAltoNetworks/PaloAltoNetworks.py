#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3


class PaloAltoNetworks(object):
	"""
	Palo Alto Networks base class
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ PaloAltoNetworks Class')
		self.panorama_ip = panorama_ip
		self.api_key = api_key
		# print('---- PaloAltoNetworks Class')

	# @staticmethod
	# def get_api_status(
	# 	response, type_, name, logger, smsg='Successfully configured', fmsg='Failed to configure'
	# ):
	# 	"""
	# 	Method to check if api call was successful or not
	#
	# 	:param response: Response that was received after API execution
	# 	:type response: Response
	# 	:param type_: Configuration type - e.g. Template, Device Group, Security Rule etc.
	# 	:type type_: str
	# 	:param name: Item could be name of template, template-stack, device-group etc. that was attempted to configure
	# 	:type name: str
	# 	:param logger: Logger
	# 	:type logger: logging.Logger
	# 	:param smsg: Message to display when api call was successful
	# 	:type smsg: str
	# 	:param fmsg: Message to display when api call failed
	# 	:type fmsg: str
	# 	:return: None
	# 	:rtype: None
	# 	"""
	#
	# 	if 'status="success" code="20"' in response.content.decode('UTF-8'):
	# 		logger.info('{}: {} - {}'.format(type_, smsg, name))
	# 	else:
	# 		logger.info('{}: {} - {}'.format(type_, fmsg, name))

	# @staticmethod
	# def request_status(
	# 	method, response, logger, type_, name, smsg='Successfully configured', fmsg='Failed to configure'
	# ):
	# 	"""
	# 	Method to log status of request that was made using requests module
	#
	# 	:param method: XML of Json
	# 	:type method: str
	# 	:param response: Response that was received from a request such as Get or POST
	# 	:type response: Response
	# 	:type logger: logging.Logger
	# 	:param type_: Configuration type - e.g. Template, Device Group, Security Rule etc; note '_' in name
	# 	:type type_: str
	# 	:param name: Name of the configuration type - e.g. name of Template or Security/NAT rule
	# 	:type name: str
	# 	:param smsg: Message to display when configuration was successful
	# 	:type smsg: str
	# 	:param fmsg: Message to display when configuration failed
	# 	:type fmsg: str
	# 	:return: None
	# 	:rtype: None
	# 	"""
	#
	# 	if method.upper() == 'XML':
	# 		tree = Et.XML(response.text)
	#
	# 		if tree.attrib['status'] == 'success' and tree.attrib['code'] == '20':
	# 			logger.info('{}: {} - {}'.format(type_, smsg, name))
	# 		else:
	# 			logger.info('{}: {} - {}'.format(type_, fmsg, name))
	# 			logger.info('{}: {} - {}'.format(type_, response.reason, name))
	# 	elif method.upper() == 'JSON':
	# 		code = json.loads(response.text)
	# 		reason = response.reason
	#
	# 		if code['@status'] == 'success' and code['@code'] == '20':
	# 			logger.info('{}: {} - {}'.format(type_, smsg, name))
	# 		else:
	# 			logger.info('{}: {} - {}'.format(type_, fmsg, name))
	# 			logger.info('{}: {} - {}'.format(type_, reason, name))

	# def execute_get_request(
	# 	self, uri, logger, type_, name, smsg='Successfully configured', fmsg='Failed to configure'
	# ):
	# 	"""
	# 	Method to execute get request using requests module
	#
	# 	:param uri: URL
	# 	:type uri: str
	# 	:param logger: Logger to log messages to
	# 	:type logger: logging.Logger
	# 	:param type_: Configuration type - e.g. Template, Device Group, Security Rule etc; note '_' in name
	# 	:type type_: str
	# 	:param name: Name of the configuration type - e.g. name of Template or Security/NAT rule
	# 	:type name: str
	# 	:param smsg: Message to display when configuration was successful
	# 	:type smsg: str
	# 	:param fmsg: Message to display when configuration failed
	# 	:type fmsg: str
	# 	:return: None
	# 	:rtype: None
	# 	"""
	#
	# 	# def status():
	# 	# 	code = json.loads(response.text)
	# 	# 	reason = response.reason
	# 	#
	# 	# 	if code['@status'] == 'success' and code['@code'] == '20':
	# 	# 		logger.info('{}: {} - {}'.format(type_, smsg, name))
	# 	# 	else:
	# 	# 		logger.info('{}: {} - {}'.format(type_, fmsg, name))
	# 	# 		logger.info('{}: {} - {}'.format(type_, reason, name))
	#
	# 	try:
	# 		response = requests.get(uri, verify=False)
	# 	except ConnectionError as e:
	# 		logger.info('{}: {} - {}'.format(type_, name, e))
	# 	except Exception as e:
	# 		logger.info('{}: {} - {}'.format(type_, name, e))
	# 	else:
	# 		self.request_status('XML', response, logger, type_, name, smsg, fmsg)

	# def execute_post_request(
	# 	self, uri, header, logger, type_, name, data='', smsg='Successfully configured', fmsg='Failed to configure'
	# ):
	# 	"""
	# 	Method to execute post request using requests module
	#
	# 	:param uri: URL
	# 	:type uri: str
	# 	:param data: Data to be submitted to URL
	# 	:type data: dict
	# 	:param header: Header information; in this case it is likely to be API key
	# 	:type header: dict
	# 	:param logger: Logger to log messages to
	# 	:type logger: logging.Logger
	# 	:param type_: Configuration type - e.g. Template, Device Group, Security Rule etc; note '_' in name
	# 	:type type_: str
	# 	:param name: Name of the configuration type - e.g. name of Template or Security/NAT rule
	# 	:type name: str
	# 	:param smsg: Message to display when configuration was successful
	# 	:type smsg: str
	# 	:param fmsg: Message to display when configuration failed
	# 	:type fmsg: str
	# 	:return: None
	# 	:rtype: None
	# 	"""
	#
	# 	# def status():
	# 	# 	code = json.loads(response.text)
	# 	# 	reason = response.reason
	# 	#
	# 	# 	if code['@status'] == 'success' and code['@code'] == '20':
	# 	# 		logger.info('{}: {} - {}'.format(type_, smsg, name))
	# 	# 	else:
	# 	# 		logger.info('{}: {} - {}'.format(type_, fmsg, name))
	# 	# 		logger.info('{}: {} - {}'.format(type_, reason, name))
	#
	# 	logger.info('Executing POST request: {}'.format(uri))
	#
	# 	if data:
	# 		logger.info('With data: {}'.format(data))
	#
	# 		response = requests.post(uri, data=json.dumps(data), headers=header, verify=False)
	#
	# 		self.request_status('JSON', response, logger, type_, name, smsg, fmsg)
	# 	else:
	# 		response = requests.post(uri, headers=header, verify=False)
	#
	# 		self.request_status('JSON', response, logger, type_, name, smsg, fmsg)
