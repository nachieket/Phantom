#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import ssl
import urllib.error
import urllib.request
import urllib.response
import xml

from time import sleep
from .....Logger.PanoramaGenericLogger.PanoramaGenericLogger import PanoramaGenericLogger as PanoramaLogger


class GetAPIKey(object):
	"""
	Panorama Get API Class
	"""

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_api_key(hostname, password, username='admin'):
		"""
		Generate the API key from username / password

		:param hostname: Panorama IP or hostname
		:param password: Panorama password
		:param username: Panorama username; default is admin
		:return: API Key
		"""

		count = 0

		data = {
			'type': 'keygen',
			'user': username,
			'password': password
		}

		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE

		url = "https://" + hostname + "/api"
		encoded_data = urllib.parse.urlencode(data).encode('utf-8')

		while True:
			try:
				response = urllib.request.urlopen(url, data=encoded_data, context=ctx).read()
				api_key = xml.etree.ElementTree.XML(response)[0][0].text
			except urllib.error.URLError:
				PanoramaLogger.panorama.info("No response from FW. Wait 20 secs before retry")
				sleep(20)

				if count < 10:
					count += 1
					continue
				else:
					return 'no_key'
			else:
				PanoramaLogger.panorama.info("FW Management plane is Responding so checking if Dataplane is ready")
				PanoramaLogger.panorama.debug("Response to get_api is {}".format(response))
				return api_key
