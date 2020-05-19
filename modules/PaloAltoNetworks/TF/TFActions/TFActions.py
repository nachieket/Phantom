#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from python_terraform import Terraform
from concurrent.futures import ThreadPoolExecutor
from ..TFLogFiles.TFLogFiles import TFLogFiles as Tfl
from time import sleep

import logging


class TFActions(object):
	"""
	Terraform Actions Class
	"""

	def __init__(self):
		# self.stage_wd = './playbooks/prisma-access/stage'
		# self.prod_wd = './aws-live/prod/tgw-design'

		# self.global_dirs = {
		# 	'global_s3_wd': './playbooks/prisma-access/global/s3'
		# }

		# self.dirs = (
		# 	self.stage_wd
		# )

		self.kwargs = {'auto-approve': True}

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)

		self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

		self.handler = logging.FileHandler('./logs/PaloAltoNetworks/Orchestrate.log')
		self.handler.setFormatter(self.formatter)

		self.logger.addHandler(self.handler)

	@staticmethod
	def initiate(location, directory):
		"""Method to execute 'terraform init' in all required directories"""

		kwargs = {'force-copy': True}
		log = Tfl()

		tf = Terraform(working_dir=directory)
		code, output, error = tf.init(capture_output=True, **kwargs)

		log.write_tf_log('INIT-CODE', str(code), 'initiate.log', location)
		log.write_tf_log('INIT-OUTPUT', output, 'initiate.log', location)
		log.write_tf_log('INIT-ERROR', error, 'initiate.log', location)

		if code != 0:
			return 'failure', directory
		else:
			return 'success'

		# if location == 'global':
		# 	for item in dirs.values():
		# 		tf = Terraform(working_dir=item)
		# 		code, output, error = tf.init(capture_output=True, **kwargs)
		#
		# 		log.write_tf_log('INIT-CODE', str(code), 'initiate.log', location)
		# 		log.write_tf_log('INIT-OUTPUT', output, 'initiate.log', location)
		# 		log.write_tf_log('INIT-ERROR', error, 'initiate.log', location)
		#
		# 		if code != 0:
		# 			return 'failure', item
		# 	else:
		# 		return 'success'
		# elif location == 'stage':
		# 	for item in dirs:
		# 		tf = Terraform(working_dir=item)
		# 		code, output, error = tf.init(capture_output=True)
		#
		# 		log.write_tf_log('INIT-CODE', str(code), 'initiate.log', location)
		# 		log.write_tf_log('INIT-OUTPUT', output, 'initiate.log', location)
		# 		log.write_tf_log('INIT-ERROR', error, 'initiate.log', location)
		#
		# 		if code != 0:
		# 			return 'failure', item
		# 	else:
		# 		return'success'

	@staticmethod
	def get(location, directory):
		"""Method to execute 'terraform get' in all required directories"""

		log = Tfl()

		tf = Terraform(working_dir=directory)
		code, output, error = tf.cmd('get', capture_output=True)

		log.write_tf_log('MOD-IMPORT-CODE', str(code), 'initiate.log', location)
		log.write_tf_log('MOD-IMPORT-INIT-OUTPUT', output, 'initiate.log', location)
		log.write_tf_log('MOD-IMPORT-INIT-ERROR', error, 'initiate.log', location)

		if 'Error' in output:
			return 'failure'
		else:
			return 'success'

	@staticmethod
	def plan(location, directory, vals=''):
		"""Method to execute 'terraform plan'"""

		log = Tfl()

		if location == 'global':
			tf = Terraform(working_dir=directory)
			code, output, error = tf.plan(capture_output=True)

			log.write_tf_log('TERRAFORM PLAN CODE', str(code), 'plan.log', location)
			log.write_tf_log('TERRAFORM PLAN OUTPUT', output, 'plan.log', location)
			log.write_tf_log('TERRAFORM PLAN ERROR', error, 'plan.log', location)

			if code == 2:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=directory)

			if vals == '':
				code, output, error = tf.plan(capture_output=True)
			else:
				code, output, error = tf.plan(capture_output=True, var=vals)

			log.write_tf_log('TERRAFORM PLAN CODE', str(code), 'plan.log', location)
			log.write_tf_log('TERRAFORM PLAN OUTPUT', output, 'plan.log', location)
			log.write_tf_log('TERRAFORM PLAN ERROR', error, 'plan.log', location)

			if code == 2:
				return 'success'
			else:
				return 'failure'

	def apply(self, location, directory, vals=''):
		"""Method to execute 'terraform apply'"""

		log = Tfl()

		if location == 'global':
			tf = Terraform(working_dir=directory)
			code, output, error = tf.apply(capture_output=True, skip_plan=True, **self.kwargs)

			log.write_tf_log('TERRAFORM APPLY CODE', str(code), 'deploy.log', location)
			log.write_tf_log('TERRAFORM APPLY OUTPUT', output, 'deploy.log', location)
			log.write_tf_log('TERRAFORM APPLY ERROR', error, 'deploy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=directory)

			if vals == '':
				code, output, error = tf.apply(capture_output=True, skip_plan=True, **self.kwargs)
			else:
				code, output, error = tf.apply(capture_output=True, skip_plan=True, var=vals, **self.kwargs)

			log.write_tf_log('TERRAFORM APPLY CODE', str(code), 'deploy.log', location)
			log.write_tf_log('TERRAFORM APPLY OUTPUT', output, 'deploy.log', location)
			log.write_tf_log('TERRAFORM APPLY ERROR', error, 'deploy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'

	def destroy(self, location, directory, vals=''):
		"""Method to execute 'terraform destroy"""

		log = Tfl()

		if location == 'global':
			tf = Terraform(working_dir=directory)
			code, output, error = tf.destroy(**self.kwargs)

			log.write_tf_log('TERRAFORM DESTROY CODE', str(code), 'destroy.log', location)
			log.write_tf_log('TERRAFORM DESTROY OUTPUT', output, 'destroy.log', location)
			log.write_tf_log('TERRAFORM DESTROY ERROR', error, 'destroy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'
		elif location == 'stage':
			tf = Terraform(working_dir=directory)

			if vals == '':
				code, output, error = tf.destroy(**self.kwargs)
			else:
				code, output, error = tf.destroy(var=vals, **self.kwargs)

			log.write_tf_log('TERRAFORM DESTROY CODE', str(code), 'destroy.log', location)
			log.write_tf_log('TERRAFORM DESTROY OUTPUT', output, 'destroy.log', location)
			log.write_tf_log('TERRAFORM DESTROY ERROR', error, 'destroy.log', location)

			if code == 0:
				return 'success'
			else:
				return 'failure'

	def run_initiate(self, location, directory):
		"""Method to call self.initiate"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform init\' in {} directory...\n'.format(location))

		future = pool.submit(self.initiate, location, directory)

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

	def run_get(self, location, directory):
		"""Method to call self.get"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform plan\' in {} directory...\n'.format(location))

		future = pool.submit(self.get, location, directory)

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

	def run_plan(self, location, directory, vals=''):
		"""Method to call self.plan"""

		pool = ThreadPoolExecutor(1)

		print('\nRunning \'terraform plan\' in {} directory...\n'.format(location))

		if vals == '':
			future = pool.submit(self.plan, location, directory)
		else:
			future = pool.submit(self.plan, location, directory, vals)

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

	def run_apply(self, location, directory, vals=''):
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
				future = pool.submit(self.apply, location, directory)
			else:
				future = pool.submit(self.apply, location, directory, vals)

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
		else:
			print('\nExiting the program.\n')
			exit()

	def run_destroy(self, location, directory, vals=''):
		"""Method to call self.destroy"""

		print('\nRunning \'terraform destroy\' to destroy infrastructure...\n')

		pool = ThreadPoolExecutor(1)

		if vals == '':
			future = pool.submit(self.destroy, location, directory)
		else:
			future = pool.submit(self.destroy, location, directory, vals)

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
