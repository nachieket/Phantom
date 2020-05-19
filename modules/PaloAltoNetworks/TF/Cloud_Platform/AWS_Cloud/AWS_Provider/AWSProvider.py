#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import textwrap


class AWSProvider(object):
	"""
	AWS Provider Class
	"""

	def __init__(self):
		self.s3_dir = './playbooks/prisma-access/global/s3/'
		self.stage_dir = './playbooks/prisma-access/stage/'

	def configure_aws_provider(self, section, location):
		"""Method to configure provider settings"""

		directory = ''

		main_tf = """
			/////////////
			// PROVIDER
			/////////////


			provider "aws" {
				region     = var.aws_region
				access_key = var.access_key
				secret_key = var.secret_key
			}

		"""

		vars_tf = """
			/////////////
			// Provider
			/////////////


			variable "access_key" {
				default = "%s"
			}

			variable "secret_key" {
				default = "%s"
			}

			variable "aws_region" {
				default = "%s"
			}

		"""

		if location == 'stage':
			directory = self.stage_dir
		elif location == 'global':
			directory = self.s3_dir

		with open('{}main.tf'.format(directory), 'a') as f:
			f.write(textwrap.dedent(main_tf))

		with open('{}vars.tf'.format(directory), 'a') as f:
			f.write(textwrap.dedent(vars_tf % (
				section['access_key'], section['secret_key'],
				section['aws_region'])
			))
