#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import textwrap


class AWSPanoramaTF(object):
	"""
	AWS Panorama Class
	"""

	def __init__(self):
		self.stage_dir = './playbooks/prisma-access/stage/'

	def configure_aws_panorama(self, panorama, aws, location='stage'):
		"""Method to configure Panorama Terraform template"""

		main_tf = """
			//////////////
			// Panorama
			//////////////


			module "panorama" {
			source = "../../../aws-live/modules/panorama"
		
			aws_region = var.aws_region
			access_key = var.access_key
			secret_key = var.secret_key
			panorama_aws_key = var.panorama_aws_key
		
			panorama_mgmt_subnet_id = var.panorama_mgmt_subnet_id
			mgmtpanoramaip = var.mgmtpanoramaip
			panorama_instance_type = var.panorama_instance_type
			panorama_name = var.panorama_name
			panorama_license_type = var.panorama_license_type
			panorama_license_type_map = var.panorama_license_type_map
			panorama_version = var.panorama_version
		
			services-Vpc-Name = var.services-Vpc-Name
			services_vpc_id = var.services_vpc_id
			}

		"""

		vars_tf = """
			//////////////////////
			// Panorama Variables
			//////////////////////


			variable "panorama_license_type_map" {
				default = {
					"byol" = "eclz7j04vu9lf8ont8ta3n17o",
				}
			}
			
			variable "access_key" {
				default = "%s"
			}

			variable "secret_key" {
				default = "%s"
			}
			
			variable "aws_region" {
				default = "%s"
			}
			
			variable "panorama_version" {
				default = "9.0.5"
			}
			
			variable "panorama_license_type" {
				default = "byol"
			}
			
			variable "panorama_instance_type" {
				default = "%s"
			}
			
			variable "mgmtpanoramaip" {
				default = "%s"
			}
			
			variable "panorama_name" {
				default = "%s"
			}
			
			variable "panorama_aws_key" {
				default = "%s"
			}
			
			variable "services-Vpc-Name" {
				default = "%s"
			}
			
			variable "services_vpc_id" {
				default = "%s"
			}
			
			variable "panorama_mgmt_subnet_id" {
				default = "%s"
			}

		"""

		outputs_tf = """
					/////////////////////
					// Output Variables
					/////////////////////


					output "panorama_public_ip" {
						value = module.panorama.panorama_mgmt_eip.public_ip
					}
		"""

		if location == 'stage':
			directory = self.stage_dir

			with open('{}vars.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(vars_tf % (
					aws['access_key'], aws['secret_key'], aws['aws_region'],
					panorama['Instance_Type'], panorama['Panorama_IP'], panorama['Panorama_Name'],
					panorama['AWS_Key'], aws['VPC_Name'], aws['VPC_ID'], aws['Subnet_ID']
				)))

			with open('{}main.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(main_tf))

			with open('{}outputs.tf'.format(directory), 'a') as f:
				f.write(textwrap.dedent(outputs_tf))
