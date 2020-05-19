#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import ssl
import urllib.error
import urllib.request
import urllib.response

from time import sleep
from .....Logger.PanoramaGenericLogger.PanoramaGenericLogger import PanoramaGenericLogger as PanoramaLogger
from .....MultiThreading.MultiThreading import MultiThreading


class Status(object):
	"""
	Panorama Status Class
	"""

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_panorama_status(panorama_ip):
		"""
		Gets the server status by sending an HTTP request and checking for a 200 response code

		:param panorama_ip: Prisma Access parameters
		:type panorama_ip: str
		:return: status
		:rtype: str
		"""

		check = 0
		status = 'down'
		thread = MultiThreading()

		def code():
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.verify_mode = ssl.CERT_NONE

			cmd = urllib.request.Request("https://" + panorama_ip + "/")
			PanoramaLogger.panorama.info('URL request is {}'.format(cmd))

			# Send command to fw and see if it times out or we get a response

			count = 0
			max_count = 160

			while True:
				if count < max_count:
					try:
						count = count + 1
						urllib.request.urlopen(cmd, data=None, context=ctx, timeout=5).read()
					except urllib.error.HTTPError as e:
						# Return code error (e.g. 404, 501, ...)
						PanoramaLogger.panorama.info('Jenkins Server Returned HTTPError: {}'.format(e.code))
						sleep(30)
					except urllib.error.URLError as e:
						PanoramaLogger.panorama.info('No response from FW. Wait 30 secs before retry. {}'.format(e))
						sleep(30)
					except Exception as e:
						PanoramaLogger.panorama.info('Got generic exception: {}'.format(e))
						sleep(30)
					else:
						PanoramaLogger.panorama.info('Jenkins Server responded with HTTP 200 code')
						sleep(60)
						return 'up'
				else:
					break

			return 'down'

		PanoramaLogger.panorama.info('Waiting for Panorama to be up and running before attempting to retrieve API Key.')

		# status = code()

		while status != 'up':
			print('Panorama is not up yet.\n')

			check += 1

			if check == 3:
				break

			status = thread.multithread(func=code, thread=1, hold=5)

			if status == 'down':
				input('\nPlease check and press enter to continue once Panorama is up\n')

		if status == 'up':
			return 'up'
		else:
			print('Panorama did not come up. This will cause issues with rest of the deployment.\n')
			answer = ''

			while answer != ('yes' and 'no'):
				answer = input(
					'Do you want to continue with rest of the infrastructure deployment (Yes/No)[Yes]?: '
				).lower()

				if answer == '':
					answer = 'yes'
					break

			if answer == 'no':
				print('\nExiting the Program.\n')
				exit()
			elif answer == 'yes':
				return 'down'
