#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3


class TFLogFiles(object):
	"""
	Class to create Terraform Files
	"""

	def __init__(self):
		self.tf_stage_log_dir = './playbooks/prisma-access/logs/terraform/stage/'
		self.tf_s3_log_dir = './playbooks/prisma-access/logs/terraform/stage/'

	def create_tf_log_files(self):
		"""Method to create empty log files"""

		with open('{}initiate.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}plan.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}deploy.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}destroy.log'.format(self.tf_stage_log_dir), 'w'):
			pass

		with open('{}initiate.log'.format(self.tf_s3_log_dir), 'w'):
			pass

		with open('{}plan.log'.format(self.tf_s3_log_dir), 'w'):
			pass

		with open('{}deploy.log'.format(self.tf_s3_log_dir), 'w'):
			pass

		with open('{}destroy.log'.format(self.tf_s3_log_dir), 'w'):
			pass

	def write_tf_log(self, value, output, logfile, location='stage'):
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
