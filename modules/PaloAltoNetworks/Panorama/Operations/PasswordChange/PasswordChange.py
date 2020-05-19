#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import paramiko

from time import sleep
from .....Logger.PanoramaGenericLogger.PanoramaGenericLogger import PanoramaGenericLogger as PanoramaLogger


class PasswordChange(object):
	"""
	Panorama Password Change Class
	"""

	def __init__(self):
		super().__init__()

	@staticmethod
	def change_panorama_password(ip, key, password='Q!w2e3r4T$'):
		"""
		Method to change Panorama password on AWS

		:param ip: Panorama IP address
		:param key: Panorama instance AWS .pem key
		:param password: Panorama password to be configured on AWS Panorama instance; default is Q!w2e3r4T$
		:return:
		"""

		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			PanoramaLogger.panorama.info('Attempting connection to Panorama using {} key'.format(key))
			ssh.connect(ip, username='admin', key_filename=key, look_for_keys=False, allow_agent=False)
		except TimeoutError as e:
			ssh.close()
			PanoramaLogger.panorama.info('Panorama connection using {} key failed - {}'.format(key, e))
			return 'failure'
		except Exception as e:
			ssh.close()
			PanoramaLogger.panorama.info('Panorama connection using {} key failed - {}'.format(key, e))
			return 'failure'

		try:
			PanoramaLogger.panorama.info('Trying to invoke SSH shell on Panorama')
			connection = ssh.invoke_shell(height=9600)
		except Exception as e:
			PanoramaLogger.panorama.info('SSH shell invoke failed - {}. The below log will show failed commands.'.format(e))
		else:
			PanoramaLogger.panorama.info('Panorama shell connected')
			sleep(2)

			try:
				PanoramaLogger.panorama.info('Executing command - configure')
				connection.send('configure\n')
			except Exception as e:
				PanoramaLogger.panorama.info('Execution of command \'configure\' failed - {}'.format(e))
			else:
				PanoramaLogger.panorama.info('Execution of command \'configure\' successful - {}')
				sleep(2)

				connection.send('set mgt-config users admin password\n')
				sleep(2)

				connection.send('{}\n'.format(password))
				sleep(2)

				connection.send('{}\n'.format(password))
				sleep(2)

				connection.send('set deviceconfig system dns-setting servers primary 8.8.8.8\n')
				sleep(2)

				connection.send('commit\n')
				sleep(10)

				output = connection.recv(65536).splitlines()

				for line in output:
					PanoramaLogger.panorama.info(line.decode('utf-8'))

				ssh.close()

				ssh = paramiko.SSHClient()
				ssh.load_system_host_keys()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

				try:
					ssh.connect(ip, username='admin', password=password, look_for_keys=False, allow_agent=False)
				except TimeoutError as e:
					ssh.close()
					PanoramaLogger.panorama.info(
						'Panorama test connection using newly configured password failed - {}'.format(e)
					)
					return 'failure'
				except Exception as e:
					ssh.close()
					PanoramaLogger.panorama.info(
						'Panorama test connection using newly configured password failed - {}'.format(e)
					)
					return 'failure'
				else:
					ssh.close()
					PanoramaLogger.panorama.info('Panorama test connection using newly configured password passed')
					return 'success'
