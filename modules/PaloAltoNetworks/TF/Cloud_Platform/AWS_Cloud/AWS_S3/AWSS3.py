#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import textwrap


class AWSS3(object):
	"""
	AWS S3 Class
	"""

	def __init__(self):
		self.s3_dir = './playbooks/prisma-access/global/s3/'
		self.stage_dir = './playbooks/prisma-access/stage/'

	def s3(self, section, location):
		"""Method to configure global S3 Bucket"""

		main_tf = """
			//////////////
			// S3 BUCKET
			//////////////


			resource "aws_s3_bucket" "s3_state" {
				bucket = var.s3_bucket

				versioning {
					enabled = true
				}

				lifecycle {
					prevent_destroy = true
				}
			}

		"""

		vars_tf = """
			//////////////
			// S3 BUCKET
			//////////////


			variable "s3_bucket" {
				default = "%s"
			}

		"""

		if location == 'stage':
			directory = self.stage_dir

			with open('{}vars.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(vars_tf % (
					section['s3_bucket']
				)))
		elif location == 'global':
			directory = self.s3_dir

			with open('{}main.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(main_tf))

			with open('{}vars.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(vars_tf % (
					section['s3_bucket']
				)))




