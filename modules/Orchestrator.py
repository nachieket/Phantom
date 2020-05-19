#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from python_terraform import Terraform
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from modules.tf import TF
from modules.PaloAltoNetworks.Panorama.Panorama import Panorama

import re
import ssl
import urllib.error
import urllib.request
import urllib.response
import xml
import xml.etree.ElementTree as Et
import paramiko
import logging


class Networking(object):
	"""Class for Networking methods and attributes"""

	@staticmethod
	def get_netmask(mask):
		"""Method to get full netmask based on CIDR number"""

		if mask == '32':
			return '255.255.255.255'
		elif mask == '31':
			return '255.255.255.254'
		elif mask == '30':
			return '255.255.255.252'
		elif mask == '29':
			return '255.255.255.248'
		elif mask == '28':
			return '255.255.255.240'
		elif mask == '27':
			return '255.255.255.224'
		elif mask == '26':
			return '255.255.255.192'
		elif mask == '25':
			return '255.255.255.128'
		elif mask == '24':
			return '255.255.255.0'
		elif mask == '23':
			return '255.255.254.0'
		elif mask == '22':
			return '255.255.252.0'
		elif mask == '21':
			return '255.255.248.0'
		elif mask == '20':
			return '255.255.240.0'
		elif mask == '19':
			return '255.255.224.0'
		elif mask == '18':
			return '255.255.192.0'
		elif mask == '17':
			return '255.255.128.0'
		elif mask == '16':
			return '255.255.0.0'
		else:
			return None


class Bootstrap(object):
	"""Class for Bootstrap methods and attributes"""

	def __init__(self):
		"""Bootstrap class constructor to initialize attributes"""

		self.parameters = {
			'type=': 'dhcp-client',
			'ip-address=': '{}-{}_mgmt_ip',
			'default-gateway=': '',
			'netmask=': '',
			'ipv6-address=': '',
			'ipv6-default-gateway=': '',
			'hostname=': '{}-{}_name',
			'vm-auth-key=': '',
			'panorama-server=': '',
			'panorama-server-2=': '',
			'tplname=': '',
			'dgname=': '',
			'dns-primary=': '4.2.2.2',
			'dns-secondary=': '8.8.8.8',
			'op-command-modes=': '',
			'dhcp-send-hostname=': 'yes',
			'dhcp-send-client=': 'yes',
			'dhcp-accept-server-hostname=': 'yes',
			'dhcp-accept-server-domain=': 'yes'
		}

		self.cfg_dirs = {
			'security-In-fw1': './aws-live/packages/firewall/bootstrap/bootstrap_files/security-in/fw1/',
			'security-In-fw2': './aws-live/packages/firewall/bootstrap/bootstrap_files/security-in/fw2/',
			'security-Out-fw1': './aws-live/packages/firewall/bootstrap/bootstrap_files/security-out/fw1/',
			'security-Out-fw2': './aws-live/packages/firewall/bootstrap/bootstrap_files/security-out/fw2/',
			'security-East-West-fw1': './aws-live/packages/firewall/bootstrap/bootstrap_files/east-west/fw1/',
			'security-East-West-fw2': './aws-live/packages/firewall/bootstrap/bootstrap_files/east-west/fw2/'
		}

	def create_init_cfg(self, directory, tgw):
		"""Method to create init-cfg.txt"""

		temp = re.match(r'(\w+-\w+(-\w*)?)-(\w+[1-2])', directory).groups()

		vpc = temp[0]
		fw = temp[2]

		with open('{}config/init-cfg.txt'.format(self.cfg_dirs[directory]), 'w') as f:
			for i in self.parameters:
				if self.parameters[i].format(vpc, fw) in tgw:
					f.write(i + tgw[self.parameters[i].format(vpc, fw)] + '\n')
				elif i == 'default-gateway=':
					dgw = re.sub(r'(\d\d*\d*)$', '1', tgw['{}-{}_mgmt_ip'.format(vpc, fw)])
					f.write(i + dgw + '\n')
				elif i == 'netmask=':
					if fw == 'fw1':
						netmask = Networking.get_netmask(tgw['{}-Mgmt-a'.format(vpc)].split('/')[1])
						f.write(i + netmask + '\n')
					elif fw == 'fw2':
						netmask = Networking.get_netmask(tgw['{}-Mgmt-b'.format(vpc)].split('/')[1])
						f.write(i + netmask + '\n')
				else:
					f.write(i + self.parameters[i] + '\n')

	def create_authcode_file(self, authcodes):
		"""Method to create authcodes file under Terraform directory structure"""

		for i in authcodes:
			dirkey = i.split(':')[0].split('-authcode')[0]
			authcode = i.split(':')[1]

			with open('{}license/authcodes'.format(self.cfg_dirs[dirkey]), 'w') as f:
				f.write(authcode)


class Orchestrate(object):
	"""Class for Terraform methods and attributes"""

	def __init__(self):
		"""Orchestrate class constructor to initialize attributes"""

		self.tf_stage_log_dir = './logs/terraform/stage/'
		self.tf_s3_log_dir = './logs/terraform/global/s3/'

		self.fw_wd = './aws-live/packages/firewall'
		self.lb_wd = './aws-live/packages/load-balancer/application'
		self.tgw_wd = './aws-live/packages/transit-gateway'
		self.ubuntu_wd = './aws-live/packages/ubuntu-ssh'
		self.web_wd = './aws-live/packages/web-server'

		self.sec_in_wd = './aws-live/packages/vpc/security-in'
		self.sec_out_wd = './aws-live/packages/vpc/security-out'
		self.sec_ew_wd = './aws-live/packages/vpc/security-east-west'
		self.services_wd = './aws-live/packages/vpc/services-vpc'

		self.spoke1_wd = './aws-live/packages/vpc/spoke-vpc1'
		self.spoke2_wd = './aws-live/packages/vpc/spoke-vpc2'

		self.stage_wd = './aws-live/stage/tgw-design'
		# self.prod_wd = './aws-live/prod/tgw-design'

		self.global_dirs = {
			'global_s3_wd': './aws-live/global/s3'
		}

		self.dirs = (
			self.fw_wd, self.lb_wd, self.tgw_wd, self.ubuntu_wd, self.web_wd, self.sec_in_wd,
			self.sec_out_wd, self.sec_ew_wd, self.services_wd, self.spoke1_wd, self.spoke2_wd,
			self.stage_wd
		)

		self.kwargs = {'auto-approve': True}

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)

		self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

		self.handler = logging.FileHandler('./logs/PaloAltoNetworks/Orchestrate.log')
		self.handler.setFormatter(self.formatter)

		self.logger.addHandler(self.handler)

	def create_logfiles(self):
		"""Method to create empty log files"""

		with open('{}initiate.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}plan.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}deploy.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}destroy.log'.format(self.tf_stage_log_dir), 'w'):
			pass

	def write_tf_log(self, value, output, logfile, location):
		"""Method to write terraform output to log file"""

		if location == 'global':
			logfile = self.tf_s3_log_dir + logfile

			with open(logfile, 'a') as f:
				f.write('##### {} #####\n'.format(value))
				f.write(output)
				f.write('\n' + '#' * len(value) + '#' * 12 + '\n\n')
		elif location == 'stage':
			logfile = self.tf_stage_log_dir + logfile

			with open(logfile, 'a') as f:
				f.write('##### {} #####\n'.format(value))
				f.write(output)
				f.write('\n' + '#' * len(value) + '#' * 12 + '\n\n')

	def initiate(self, location):
		"""Method to execute 'terraform init' in all required directories"""

		kwargs = {'force-copy': True}

		if location == 'global':
			for item in self.global_dirs.values():
				tf = Terraform(working_dir=item)
				code, output, error = tf.init(capture_output=True, **kwargs)

				self.write_tf_log('INIT-CODE', str(code), 'initiate.log', location)
				self.write_tf_log('INIT-OUTPUT', output, 'initiate.log', location)
				self.write_tf_log('INIT-ERROR', error, 'initiate.log', location)

				if code != 0:
					return 'failure', item
			else:
				return 'success'
		elif location == 'stage':
			for item in self.dirs:
				tf = Terraform(working_dir=item)
				code, output, error = tf.init(capture_output=True)

				self.write_tf_log('INIT-CODE', str(code), 'initiate.log', location)
				self.write_tf_log('INIT-OUTPUT', output, 'initiate.log', location)
				self.write_tf_log('INIT-ERROR', error, 'initiate.log', location)

				if code != 0:
					return 'failure', item
			else:
				return'success'

	def get(self, location):
		"""Method to execute 'terraform get' in all required directories"""

		tf = Terraform(working_dir=self.stage_wd)
		code, output, error = tf.cmd('get', capture_output=True)

		self.write_tf_log('MOD-IMPORT-CODE', str(code), 'initiate.log', location)
		self.write_tf_log('MOD-IMPORT-INIT-OUTPUT', output, 'initiate.log', location)
		self.write_tf_log('MOD-IMPORT-INIT-ERROR', error, 'initiate.log', location)

		if 'Error' in output:
			return 'failure'
		else:
			return 'success'

	def plan(self, location, vals=''):
		"""Method to execute 'terraform plan'"""

		if location == 'global':
			tf = Terraform(working_dir=self.global_dirs['global_s3_wd'])
			code, output, error = tf.plan(capture_output=True)

			self.write_tf_log('TERRAFORM PLAN CODE', str(code), 'plan.log', location)
			self.write_tf_log('TERRAFORM PLAN OUTPUT', output, 'plan.log', location)
			self.write_tf_log('TERRAFORM PLAN ERROR', error, 'plan.log', location)

			if code == 2:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=self.stage_wd)
			code, output, error = tf.plan(capture_output=True, var=vals)

			self.write_tf_log('TERRAFORM PLAN CODE', str(code), 'plan.log', location)
			self.write_tf_log('TERRAFORM PLAN OUTPUT', output, 'plan.log', location)
			self.write_tf_log('TERRAFORM PLAN ERROR', error, 'plan.log', location)

			if code == 2:
				return 'success'
			else:
				return 'failure'

	def apply(self, location, vals=''):
		"""Method to execute 'terraform apply'"""

		if location == 'global':
			tf = Terraform(working_dir=self.global_dirs['global_s3_wd'])
			code, output, error = tf.apply(capture_output=True, skip_plan=True, **self.kwargs)

			self.write_tf_log('TERRAFORM APPLY CODE', str(code), 'deploy.log', location)
			self.write_tf_log('TERRAFORM APPLY OUTPUT', output, 'deploy.log', location)
			self.write_tf_log('TERRAFORM APPLY ERROR', error, 'deploy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=self.stage_wd)
			code, output, error = tf.apply(capture_output=True, skip_plan=True, var=vals, **self.kwargs)

			self.write_tf_log('TERRAFORM APPLY CODE', str(code), 'deploy.log', location)
			self.write_tf_log('TERRAFORM APPLY OUTPUT', output, 'deploy.log', location)
			self.write_tf_log('TERRAFORM APPLY ERROR', error, 'deploy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'

	def destroy(self, location, vals=''):
		"""Method to execute 'terraform destroy"""

		if location == 'global':
			tf = Terraform(working_dir=self.global_dirs['global_s3_wd'])
			code, output, error = tf.destroy(**self.kwargs)

			self.write_tf_log('TERRAFORM DESTROY CODE', str(code), 'destroy.log', location)
			self.write_tf_log('TERRAFORM DESTROY OUTPUT', output, 'destroy.log', location)
			self.write_tf_log('TERRAFORM DESTROY ERROR', error, 'destroy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=self.stage_wd)
			code, output, error = tf.destroy(var=vals, **self.kwargs)

			self.write_tf_log('TERRAFORM DESTROY CODE', str(code), 'destroy.log', location)
			self.write_tf_log('TERRAFORM DESTROY OUTPUT', output, 'destroy.log', location)
			self.write_tf_log('TERRAFORM DESTROY ERROR', error, 'destroy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'

	def run_initiate(self, location):
		"""Method to call self.initiate"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform init\' in {} directory...\n'.format(location))

		future = pool.submit(self.initiate, location)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(1)
		else:
			init_code = future.result()

		if init_code == 'success':
			print('\n\n' + location + ' - Directories successfully initialized.')
		else:
			print('\n\n' + location + ' - Directories could not be initialized.\n')
			print('\nExiting the program.\n')
			exit()

	def run_get(self, location):
		"""Method to call self.get"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform plan\' in {} directory...\n'.format(location))

		future = pool.submit(self.get, location)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(1)
		else:
			get_code = future.result()

		if get_code == 'success':
			print('\n\n' + location + ' - Terraform get was successful.')
		else:
			print('\n\n' + location + ' - Terraform get failed.\n')
			print('Exiting the program.\n')
			exit()

	def run_plan(self, location, vals=''):
		"""Method to call self.plan"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform plan\' in {} directory...\n'.format(location))

		if vals == '':
			future = pool.submit(self.plan, location)
		else:
			future = pool.submit(self.plan, location, vals)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(1)
		else:
			plan_code = future.result()

		if plan_code == 'success':
			print('\n\n' + location + ' - Terraform plan was successful.\n')
		else:
			print('\n\n' + location + ' - Terraform plan failed.\n')
			print('Exiting the program.\n')
			exit()

	def run_apply(self, location, vals=''):
		"""Method to call self.apply"""

		answer = ''
		pool = ThreadPoolExecutor(1)

		while answer != 'yes' and answer != 'no':
			answer = input('Do you want to continue with infrastructure deployment (Yes/No)[Yes]?: ').lower()

			if answer == '':
				answer = 'yes'
				break

		if answer == 'yes':
			print('\nRunning \'terraform apply\' in {} directory to deploy infrastructure...\n'.format(location))

			if vals == '':
				future = pool.submit(self.apply, location)
			else:
				future = pool.submit(self.apply, location, vals)

			while future.done() is False:
				print('#', end='', flush=True)
				sleep(1)
			else:
				exec_code = future.result()

			if exec_code == 'success':
				print('\n\n' + location + ' - Infrastructure successfully deployed.')
			else:
				print('\n\n' + location + ' - Infrastructure deployment failed.\n')
				print('\nExiting the program.\n')
				exit()

	def run_destroy(self, location, vals=''):
		"""Method to call self.destroy"""

		print('\nRunning \'terraform destroy\' to destroy infrastructure...\n')

		pool = ThreadPoolExecutor(1)

		if vals == '':
			future = pool.submit(self.destroy, location)
		else:
			future = pool.submit(self.destroy, location, vals)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(1)
		else:
			destroy_code = future.result()

		if destroy_code == 'success':
			print('\n\n' + location + ' - Terraform successfully destroyed infrastructure.\n')
		elif destroy_code == 'failure':
			print('\n\n' + location + ' - Terraform failed to destroy infrastructure.\n')
			print('\nExiting the program.\n')
			exit()

	def build_tf(self, tgw):
		"""Method to build Terraform main.tf"""

		tf = TF()

		############################################################################
		# This section will create empty main.tf, vars.tf and outputs.tf files
		############################################################################

		tf.create_tgw_tf_files()

		####################################################################################
		# This section creates main.tf and vars.tf under aws-live/global/s3 directory
		# This will be used to created S3 bucket
		# Other global configurations can be added later
		####################################################################################

		print('#' * 50)
		print('#' * 50 + '\n')
		print('Global Terraform Configuration\n')
		print('#' * 50)
		print('#' * 50)

		location = 'global'

		tf.provider(tgw['Provider'], location)
		tf.s3(tgw['S3'], location)

		self.run_initiate(location)

		self.run_plan(location)

		self.run_apply(location)

		################################################
		# This section will add Backend to S3 main.tf
		################################################

		tf.backend(tgw['S3'], tgw['Provider'], location)

		self.run_initiate(location)

		print()
		print('#' * 50)
		print('#' * 50 + '\n')
		print('Global Terraform Configuration Complete\n')
		print('#' * 50)
		print('#' * 50)

		########################################################################################################
		# This section will be used to create main.tf and vars.tf under aws-live/stage/tgw-design directory
		# This will be used to deploy AWS Transit Gateway design as per the configuration provided in tgw.csv
		########################################################################################################

		outputs = []

		for section in tgw:
			if section == 'Provider':
				tf.maps()
				tf.provider(tgw[section], 'stage')
				tf.aws_key(tgw[section])
			elif section == 'S3':
				tf.backend(tgw[section], tgw['Provider'], 'stage')
				tf.iam_role()
				tf.s3(tgw['S3'], 'stage')
			elif section == 'Services':
				outputs.append(tf.services(tgw[section]))
			elif section == 'Panorama':
				if tgw[section]['location'] == 'services-vpc':
					outputs.append(tf.panorama(tgw[section]))
				elif tgw[section]['location'] == 'on-premise':
					pass  # TODO: Implement this section
				elif tgw[section]['location'] == 'no-panorama':
					pass  # TODO: Implement this section
				else:
					print('Invalid Panorama location or value given. Exiting the program.')
					exit()

		return outputs

	def change_panorama_password(self, ip, key, password='Q!w2e3r4T$'):
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
			self.logger.info('Attempting connection to Panorama using {} key'.format(key))
			ssh.connect(ip, username='admin', key_filename=key, look_for_keys=False, allow_agent=False)
		except TimeoutError as e:
			ssh.close()
			self.logger.info('Panorama connection using {} key failed - {}'.format(key, e))
			return 'failure'
		except Exception as e:
			ssh.close()
			self.logger.info('Panorama connection using {} key failed - {}'.format(key, e))
			return 'failure'

		try:
			self.logger.info('Trying to invoke SSH shell on Panorama')
			connection = ssh.invoke_shell(height=9600)
		except Exception as e:
			self.logger.info('SSH shell invoke failed - {}. The below log will show failed commands.'.format(e))
		else:
			self.logger.info('Panorama shell connected')
			sleep(2)

		try:
			self.logger.info('Executing command - configure')
			connection.send('configure\n')
		except Exception as e:
			self.logger.info('Execution of command \'configure\' failed - {}'.format(e))
		else:
			self.logger.info('Execution of command \'configure\' successful - {}')
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
			self.logger.info(line.decode('utf-8'))

		ssh.close()

		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			ssh.connect(ip, username='admin', password=password, look_for_keys=False, allow_agent=False)
		except TimeoutError as e:
			ssh.close()
			self.logger.info('Panorama test connection using newly configured password failed - {}'.format(e))
			return 'failure'
		except Exception as e:
			ssh.close()
			self.logger.info('Panorama test connection using newly configured password failed - {}'.format(e))
			return 'failure'
		else:
			ssh.close()
			self.logger.info('Panorama test connection using newly configured password passed')
			return 'success'

	def get_pa_status(self, ip):
		"""
		Gets the server status by sending an HTTP request and checking for a 200 response code

		:param ip: Panorama IP Address
		:return: Status of Panorama - Up or Down
		"""

		check = 0

		def code():
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.verify_mode = ssl.CERT_NONE

			cmd = urllib.request.Request("https://" + ip + "/")
			self.logger.info('URL request is {}'.format(cmd))

			# Send command to fw and see if it times out or we get a response

			count = 0
			max_count = 80

			while True:
				if count < max_count:
					try:
						count = count + 1
						urllib.request.urlopen(cmd, data=None, context=ctx, timeout=5).read()
					except urllib.error.HTTPError as e:
						# Return code error (e.g. 404, 501, ...)
						self.logger.info('Jenkins Server Returned HTTPError: {}'.format(e.code))
						sleep(30)
					except urllib.error.URLError as e:
						self.logger.info('No response from FW. Wait 30 secs before retry. {}'.format(e))
						sleep(30)
					except Exception as e:
						self.logger.info('Got generic exception: {}'.format(e))
						sleep(30)
					else:
						self.logger.info('Jenkins Server responded with HTTP 200 code')
						return 'up'
				else:
					break

			return 'down'

		self.logger.info('Waiting for Panorama to be up and running before attempting to retrieve API Key.')

		status = code()

		while status != 'up' or check < 3:
			print('\nPanorama is not up yet.')
			input('Please check and press enter to continue once Panorama is up\n')

			check += 1

			if check == 3:
				break

			status = self.multithread(code)

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

	def get_api_key(self, hostname, password, username='admin'):
		"""
		Generate the API key from username / password

		:param hostname: Panorama IP or hostname
		:param password: Panorama password
		:param username: Panorama username; default is admin
		:return: API Key
		"""

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
				self.logger.info("No response from FW. Wait 20 secs before retry")
				sleep(20)
				continue
			else:
				self.logger.info("FW Management plane is Responding so checking if Dataplane is ready")
				self.logger.debug("Response to get_api is {}".format(response))
				return api_key

	def get_tf_output(self, directory, outputs):
		"""
		Method to get Terraform outputs in a dictionary

		:param directory: Directory in which to run terraform output command
		:param outputs: List of output variables to provide to terraform output command
		:return: Output dictionary with variable as key and public IP as value
		"""

		dictionary = {}

		self.logger.info('Getting outputs from {} directory.'.format(directory))

		tf = Terraform(working_dir=directory)

		for o in outputs:
			tf_code, output, error = tf.cmd('output', o)
			dictionary[o] = output.rsplit('\n')[0]

		self.logger.info('Outputs from {} directory generated.'.format(directory))

		return dictionary

	@staticmethod
	def multithread(thread=1, hold=1, *args):
		"""Method to display # while method or function is running"""

		pool = ThreadPoolExecutor(thread)

		future = pool.submit(*args)

		while future.done() is False:
			print('#', end='', flush=True)
			sleep(hold)
		else:
			print('\n')
			result = future.result()

		return result

	def orchestrator(self, vals, action, tgw):
		"""Method to orchestrate terraform stages of initiate, plan and deploy"""

		self.create_logfiles()

		outputs = self.build_tf(tgw)

		bootobj = Bootstrap()

		authcodes = [
			'{}:{}'.format(code, tgw[title][code]) for title in tgw for code in tgw[title] if 'authcode' in code
		]

		bootobj.create_authcode_file(authcodes)

		bootobj.create_init_cfg('security-In-fw1', tgw['security-In'])
		bootobj.create_init_cfg('security-In-fw2', tgw['security-In'])

		bootobj.create_init_cfg('security-Out-fw1', tgw['security-Out'])
		bootobj.create_init_cfg('security-Out-fw2', tgw['security-Out'])

		bootobj.create_init_cfg('security-East-West-fw1', tgw['security-East-West'])
		bootobj.create_init_cfg('security-East-West-fw2', tgw['security-East-West'])

		if action == 'create':
			location = 'stage'
			public_ip_dict = {}

			self.run_initiate(location)

			self.run_get(location)

			self.run_plan(location, vals)

			self.run_apply(location, vals)

			public_ip_dict = self.get_tf_output(self.stage_wd, outputs, public_ip_dict)

			status = self.get_pa_status(public_ip_dict['panorama_mgmt_public_ip'])

			if status == 'up':
				password = tgw['Panorama']['credentials'].split(':')[1]

				status = self.change_panorama_password(
					public_ip_dict['panorama_mgmt_public_ip'], tgw['Panorama']['panorama_aws_key'] + 'pem', password
				)

				if status == 'success':
					api_key = self.get_api_key(public_ip_dict['panorama_mgmt_public_ip'], password)
				else:
					panorama_api_key = input('\nPlease enter Panorama API Key: ')
					panorama_auth_code = input('\nPlease enter Panorama Auth Code for init.cfg: ')
			else:
				panorama_api_key = input('\nPlease enter Panorama API Key: ')
				panorama_auth_code = input('\nPlease enter Panorama Auth Code for init.cfg: ')
		elif action == 'delete':
			self.run_destroy('stage')
		else:
			print('\nThe action provided with runtime parameter is not correct. Check program help.\n')
			print('Exiting the program.\n')
			exit()
