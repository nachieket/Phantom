#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3


class TFConfigFiles(object):
	"""
	Class to create Terraform Files
	"""

	def __init__(self):
		self.s3_dir = './playbooks/prisma-access/global/s3/'
		self.stage_dir = './playbooks/prisma-access/stage/'

	def create_tf_config_files(self):
		"""Method to create empty main.tf, vars.tf and outputs.tf files"""

		try:
			f = open('{}main.tf'.format(self.s3_dir), 'w')
			f.close()
			f = open('{}vars.tf'.format(self.s3_dir), 'w')
			f.close()
			f = open('{}outputs.tf'.format(self.s3_dir), 'w')
			f.close()

			f = open('{}main.tf'.format(self.stage_dir), 'w')
			f.close()
			f = open('{}vars.tf'.format(self.stage_dir), 'w')
			f.close()
			f = open('{}outputs.tf'.format(self.stage_dir), 'w')
			f.close()
		except IOError as e:
			print('\nError - {}\n'.format(e))
			print('The program could not create main.tf, vars.tf and/or outputs.tf file/s.\n')
			print('Exiting the Program\n')
			exit()
		except Exception as e:
			print('\nError - {}\n'.format(e))
			print('The program could not create main.tf, vars.tf and/or outputs.tf file/s.\n')
			print('Exiting the Program\n')
			exit()
