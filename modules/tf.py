#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import textwrap


class TF(object):
	"""Class to create main.tf and vars.tf file"""

	def __init__(self):
		self.s3_dir = './aws-live/global/s3/'
		self.stage_dir = './aws-live/stage/tgw-design/'

	def create_tgw_tf_files(self):
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

	def maps(self):
		"""Method to write constant map variables to vars.tf"""

		vars_tf = """
					/////////////////
					// GENERIC MAPS
					/////////////////


					variable "panorama_license_type_map" {
						default = {
							"byol" = "eclz7j04vu9lf8ont8ta3n17o",
						}
					}

					variable "fw_license_type_map" {			
						default = {
							"byol"  = "6njl1pau431dv1qxipg63mvah"
							"payg1" = "6kxdw3bbmdeda3o6i1ggqt4km"
							"payg2" = "806j2of0qy5osgjjixq9gqc6g"
						}
					}

				"""

		with open('{}vars.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(vars_tf))

	def provider(self, section, location):
		"""Method to configure provider settings"""

		directory = ''
		# action = ''

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

	def aws_key(self, section):
		"""Method to write aws_key variable to vars.tf"""

		vars_tf = """
					variable "aws_key" {
						default = "%s"
					}

				"""

		with open('{}vars.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(vars_tf % (
				section['aws_key']
			)))

	def backend(self, section, provider, location):
		"""Method to inject backend code to main.tf store tfstate files"""

		directory = ''
		key = ''

		main_tf = """
			////////////
			// BACKEND
			////////////
			

			terraform {
				backend "s3" {
					bucket     = "%s"
					key        = "%s"
					region     = "%s"
					encrypt    = true
					access_key = "%s"
					secret_key = "%s"
				}
			}
			
		"""

		if location == 'stage':
			directory = self.stage_dir
			key = 'stage/transit-gateway/terraform.tfstate'
		elif location == 'global':
			directory = self.s3_dir
			key = 'global/s3/terraform.tfstate'

		with open('{}main.tf'.format(directory), 'a') as f:
			f.write(textwrap.dedent(main_tf % (
				section['s3_bucket'], key, provider['aws_region'],
				provider['access_key'], provider['secret_key']
			)))

	def lb_access_log_bucket(self, section):
		"""Method to configure access log bucket for Load Balancer"""

		main_tf = """
					////////////
					// BACKEND
					////////////


					resource "aws_s3_bucket" "lb_access_log_bucket" {
						bucket        = var.lb_access_log_bucket
						acl           = "private"
						force_destroy = true

						tags = {
							Name = "lb_access_log_bucket"
						}
					}

				"""

		vars_tf = """
					//////////////////
					// Load Balancer
					//////////////////


					variable "lb_access_log_bucket" {
						default = "%s"
					}

				"""

		with open('{}main.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(main_tf))

		with open('{}vars.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(vars_tf % (
				section['s3_bucket']
			)))

	def iam_role(self):
		"""Method to inject IAM Role code in main.tf"""

		main_tf = """
			/////////////
			// IAM Role
			/////////////
			
			
			resource "aws_iam_role" "bootstrap_role" {
				name = "ngfw_bootstrap_role"
			
				assume_role_policy = <<EOF
			{
				"Version": "2012-10-17",
				"Statement": [
				{
					"Effect": "Allow",
					"Principal": {
					"Service": "ec2.amazonaws.com"
				},
					"Action": "sts:AssumeRole"
				}
				]
			}
			EOF
			}
			
			resource "aws_iam_role_policy" "bootstrap_policy" {
				name = "ngfw_bootstrap_policy"
				role = aws_iam_role.bootstrap_role.id
			
				policy = <<EOF
			{
				"Version" : "2012-10-17",
				"Statement": [
				{
					"Effect": "Allow",
					"Action": "s3:ListBucket",
					"Resource": "arn:aws:s3:::${var.s3_bucket}"
				},
				{
				"Effect": "Allow",
				"Action": "s3:GetObject",
				"Resource": "arn:aws:s3:::${var.s3_bucket}/*"
				}
				]
			}
			EOF
			}
			
		"""

		with open('{}main.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(main_tf))

	def services(self, section):
		"""Method to inject services vpc code in main.tf"""

		main_tf = """
			/////////////////
			// SERVICES VPC
			/////////////////


			module "services_vpc" {
				source = "../../packages/vpc/services-vpc"
		
				aws_region = var.aws_region
				access_key = var.access_key
				secret_key = var.secret_key
				ubuntu_aws_key = var.ubuntu_aws_key
		
				vpc_name = var.services-Vpc-Name
				vpc_cidr = var.services-Vpc-cidr
		
				Services-a = var.Services-a
				Services-b = var.Services-b
		
				ssh_private_ip = var.js_services_private_ip
			}
		
		"""

		vars_tf = """
			/////////////////
			// Services VPC
			/////////////////
			
			
			variable "services-Vpc-Name" {
				default = "%s"
			}
			
			variable "services-Vpc-cidr" {
				default = "%s"
			}
			
			variable "Services-a" {
				default = "%s"
			}
			
			variable "Services-b" {
				default = "%s"
			}
			
			variable "js_services_private_ip" {
				default = "%s"
			}
			
			variable "ubuntu_aws_key" {
				default = "%s"
			}
			
		"""

		outputs_tf = """
			output "services_ubuntu_public_ip" {
				value = module.services_vpc.services_ubuntu_ip.public_ip
			}
		"""

		with open('{}main.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(main_tf))

		with open('{}vars.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(vars_tf % (
				section['services-Vpc-Name'], section['services-Vpc-cidr'], section['Services-a'],
				section['Services-b'], section['js_services_private_ip'], section['ubuntu_aws_key']
			)))

		with open('{}outputs.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(outputs_tf))

		return 'services_ubuntu_public_ip'

	def panorama(self, section):
		"""Method to inject panorama code in main.tf"""

		main_tf = """
			/////////////
			// PANORAMA
			/////////////


			module "panorama" {
				source = "../../packages/panorama"
			
				aws_region = var.aws_region
				access_key = var.access_key
				secret_key = var.secret_key
				panorama_aws_key = var.panorama_aws_key
			
				panorama_mgmt_subnet_id = module.services_vpc.Services-a_id
				mgmtpanoramaip = var.mgmtpanoramaip
				panorama_instance_type = var.panorama_instance_type
				panorama_name = var.panorama_name
				panorama_license_type = var.panorama_license_type
				panorama_license_type_map = var.panorama_license_type_map
				panorama_version = var.panorama_version
			
				services-Vpc-Name = var.services-Vpc-Name
				services_vpc_id = module.services_vpc.vpc_id
			}
			
		"""

		vars_tf = """
			/////////////
			// Panorama
			///////////// 
			
			
			variable "panorama_version" {
				default = "%s"
			}

			variable "panorama_license_type" {
				default = "%s"
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
			
		"""

		outputs_tf = """
					output "panorama_mgmt_public_ip" {
						value = module.panorama.panorama_mgmt_eip.public_ip
					}
				"""

		with open('{}main.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(main_tf))

		with open('{}vars.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(vars_tf % (
				section['panorama_version'], section['panorama_license_type'], section['panorama_instance_type'],
				section['mgmtpanoramaip'], section['panorama_name'], section['panorama_aws_key']
			)))

		with open('{}outputs.tf'.format(self.stage_dir), 'a') as f:
			f.write(textwrap.dedent(outputs_tf))

		return 'panorama_mgmt_public_ip'

	@staticmethod
	def security_in():
		"""Method to inject security-In vpc code in main.tf"""

		main_tf = """
			///////////////////////////////
			// Security Inbound VPC Module
			///////////////////////////////
			
			
			module "security_in_vpc" {
				source = "../../packages/vpc/security-in"
			
				access_key = var.access_key
				secret_key = var.secret_key
				aws_key    = var.aws_key
				aws_region = var.aws_region
			
				fw_instance_type = var.security-In-fw_instance_type
				fw_license_type_map = var.fw_license_type_map
				ngfw_license_type = var.security-In-ngfw_license_type
				ngfw_version = var.security-In-ngfw_version
			
				s3_bucket_id   = aws_s3_bucket.bootstrap_bucket.id
				bootstrap_role_name     = aws_iam_role.bootstrap_role.name
				s3_bucket_name = aws_s3_bucket.bootstrap_bucket.bucket
			
				vpc_name             = var.security-In-Vpc-Name
				vpc_cidr             = var.security-In-Vpc-cidr
				lb_access_log_bucket = aws_s3_bucket.lb_access_log_bucket.bucket
			
				security-In-Mgmt-a = var.security-In-Mgmt-a
				security-In-TGW-a  = var.security-In-TGW-a
				security-In-Pub-a  = var.security-In-Pub-a
				security-In-Priv-a = var.security-In-Priv-a
			
				security-In-Mgmt-b = var.security-In-Mgmt-b
				security-In-TGW-b  = var.security-In-TGW-b
				security-In-Pub-b  = var.security-In-Pub-b
				security-In-Priv-b = var.security-In-Priv-b
			
				fw1_name       = var.security-In-fw1_name
				fw1_mgmt_ip    = var.security-In-fw1_mgmt_ip
				fw1_untrust_ip = var.security-In-fw1_untrust_ip
				fw1_trust_ip   = var.security-In-fw1_trust_ip
			
				fw2_name       = var.security-In-fw2_name
				fw2_mgmt_ip    = var.security-In-fw2_mgmt_ip
				fw2_untrust_ip = var.security-In-fw2_untrust_ip
				fw2_trust_ip   = var.security-In-fw2_trust_ip
			}
		"""

		vars_tf = """
			////////////////////
			// Security-In VPC
			////////////////////
			
			
			variable "security-In-Vpc-Name" {}
			
			variable "security-In-Vpc-cidr" {}
			
			variable "security-In-Mgmt-a" {}
			
			variable "security-In-TGW-a" {}
			
			variable "security-In-Pub-a" {}
			
			variable "security-In-Priv-a" {}
			
			variable "security-In-Mgmt-b" {}
			
			variable "security-In-TGW-b" {}
			
			variable "security-In-Pub-b" {}
			
			variable "security-In-Priv-b" {}
			
			variable "security-In-fw1_name" {}
			
			variable "security-In-fw1_mgmt_ip" {}
			
			variable "security-In-fw1_untrust_ip" {}
			
			variable "security-In-fw1_trust_ip" {}
			
			variable "security-In-fw2_name" {}
			
			variable "security-In-fw2_mgmt_ip" {}
			
			variable "security-In-fw2_untrust_ip" {}
			
			variable "security-In-fw2_trust_ip" {}
			
			variable "security-In-fw_instance_type" {}
			
			variable "security-In-ngfw_license_type" {}
			
			variable "security-In-ngfw_version" {}
		"""

		return main_tf, vars_tf

	@staticmethod
	def security_out():
		"""Method to inject security out vpc code in main.tf"""

		main_tf = """
			module "security_out_vpc" {
			source = "../../packages/vpc/security-out"
		
			access_key = var.access_key
			secret_key = var.secret_key
			aws_key    = var.aws_key
			aws_region = var.aws_region
		
			fw_instance_type = var.security-Out-fw_instance_type
			fw_license_type_map = var.fw_license_type_map
			ngfw_license_type = var.security-Out-ngfw_license_type
			ngfw_version = var.security-Out-ngfw_version
		
			s3_bucket_id   = aws_s3_bucket.bootstrap_bucket.id
			bootstrap_role_name     = aws_iam_role.bootstrap_role.name
			s3_bucket_name = aws_s3_bucket.bootstrap_bucket.bucket
		
			vpc_name = var.security-Out-Vpc-Name
			vpc_cidr = var.security-Out-Vpc-cidr
		
			security-Out-Mgmt-a = var.security-Out-Mgmt-a
			security-Out-TGW-a  = var.security-Out-TGW-a
			security-Out-Pub-a  = var.security-Out-Pub-a
			security-Out-Mgmt-b = var.security-Out-Mgmt-b
			security-Out-TGW-b  = var.security-Out-TGW-b
			security-Out-Pub-b  = var.security-Out-Pub-b
		
			fw1_name       = var.security-Out-fw1_name
			fw1_mgmt_ip    = var.security-Out-fw1_mgmt_ip
			fw1_untrust_ip = var.security-Out-fw1_untrust_ip
			//  fw1_trust_ip = "${var.security-Out-fw1_trust_ip}"
		
			fw2_name       = var.security-Out-fw2_name
			fw2_mgmt_ip    = var.security-Out-fw2_mgmt_ip
			fw2_untrust_ip = var.security-Out-fw2_untrust_ip
			//  fw2_trust_ip = "${var.security-Out-fw2_trust_ip}"
			}
		"""

		vars_tf = """
			////////////////////
			// Security-Out VPC
			////////////////////
			
			
			variable "security-Out-Vpc-Name" {}
			
			variable "security-Out-Vpc-cidr" {}
			
			variable "security-Out-Mgmt-a" {}
			
			variable "security-Out-TGW-a" {}
			
			variable "security-Out-Pub-a" {}
			
			variable "security-Out-Mgmt-b" {}
			
			variable "security-Out-TGW-b" {}
			
			variable "security-Out-Pub-b" {}
			
			variable "security-Out-fw1_name" {}
			
			variable "security-Out-fw1_mgmt_ip" {}
			
			variable "security-Out-fw1_untrust_ip" {}
			
			//variable "security-Out-fw1_trust_ip" {
			//  default = ""
			//}
			
			variable "security-Out-fw2_name" {}
			
			variable "security-Out-fw2_mgmt_ip" {}
			
			variable "security-Out-fw2_untrust_ip" {}
			
			//variable "security-Out-fw2_trust_ip" {
			//  default = ""
			//}
			
			variable "security-Out-fw_instance_type" {}
			
			variable "security-Out-ngfw_license_type" {}
			
			variable "security-Out-ngfw_version" {}
		"""

		return main_tf, vars_tf

	@staticmethod
	def security_ew():
		"""Method to inject security-East-West vpc code in to main.tf"""

		main_tf = """
			/////////////////////////////////
			// East-West Security VPC Module
			/////////////////////////////////
			
			
			module "security_east_west_vpc" {
				source = "../../packages/vpc/security-east-west"
			
				access_key = var.access_key
				secret_key = var.secret_key
				aws_key    = var.aws_key
				aws_region = var.aws_region
			
				fw_instance_type = var.security-East-West-fw_instance_type
				fw_license_type_map = var.fw_license_type_map
				ngfw_license_type = var.security-East-West-ngfw_license_type
				ngfw_version = var.security-East-West-ngfw_version
			
				s3_bucket_id   = aws_s3_bucket.bootstrap_bucket.id
				bootstrap_role_name     = aws_iam_role.bootstrap_role.name
				s3_bucket_name = aws_s3_bucket.bootstrap_bucket.bucket
			
				vpc_name = var.security-East-West-Vpc-Name
				vpc_cidr = var.security-East-West-Vpc-cidr
			
				security-East-West-Mgmt-a = var.security-East-West-Mgmt-a
				security-East-West-TGW-a  = var.security-East-West-TGW-a
				security-East-West-Pub-a  = var.security-East-West-Pub-a
				security-East-West-Mgmt-b = var.security-East-West-Mgmt-b
				security-East-West-TGW-b  = var.security-East-West-TGW-b
				security-East-West-Pub-b  = var.security-East-West-Pub-b
			
				fw1_name       = var.security-East-West-fw1_name
				fw1_mgmt_ip    = var.security-East-West-fw1_mgmt_ip
				fw1_untrust_ip = var.security-East-West-fw1_untrust_ip
				//  fw1_trust_ip = "${var.security-East-West-fw1_trust_ip}"
			
				fw2_name       = var.security-East-West-fw2_name
				fw2_mgmt_ip    = var.security-East-West-fw2_mgmt_ip
				fw2_untrust_ip = var.security-East-West-fw2_untrust_ip
				//  fw2_trust_ip = "${var.security-East-West-fw2_trust_ip}"
			}
		"""

		vars_tf = """
			///////////////////////////
			// Security-East-West VPC
			///////////////////////////
			
			
			variable "security-East-West-Vpc-Name" {}
			
			variable "security-East-West-Vpc-cidr" {}
			
			variable "security-East-West-Mgmt-a" {}
			
			variable "security-East-West-TGW-a" {}
			
			variable "security-East-West-Pub-a" {}
			
			variable "security-East-West-Mgmt-b" {}
			
			variable "security-East-West-TGW-b" {}
			
			variable "security-East-West-Pub-b" {}
			
			variable "security-East-West-fw1_name" {}
			
			variable "security-East-West-fw1_mgmt_ip" {}
			
			variable "security-East-West-fw1_untrust_ip" {}
			
			//variable "security-East-West-fw1_trust_ip" {
			//  default = ""
			//}
			
			variable "security-East-West-fw2_name" {}
			
			variable "security-East-West-fw2_mgmt_ip" {}
			
			variable "security-East-West-fw2_untrust_ip" {}
			
			//variable "security-East-West-fw2_trust_ip" {
			//  default = ""
			//}
			
			variable "security-East-West-fw_instance_type" {}
			
			variable "security-East-West-ngfw_license_type" {}
			
			variable "security-East-West-ngfw_version" {}
		"""

		return main_tf, vars_tf

	@staticmethod
	def vpc1():
		"""Method to inject vpc1 code in main.tf"""

		main_tf = """
				///////////////
				// Spoke1 VPC
				///////////////


				module "spoke_vpc1" {
					source = "../../packages/vpc/spoke-vpc1"

					access_key = var.access_key
					secret_key = var.secret_key

					aws_region = var.aws_region
					key_name   = var.aws_key

					vpc_name = var.spoke-Vpc1-Name
					vpc_cidr = var.spoke-Vpc1-cidr

					lb_access_log_bucket = aws_s3_bucket.lb_access_log_bucket.bucket

					spoke1-web-a = var.spoke1-web-a
					spoke1-web-b = var.spoke1-web-b

					web1_private_ip = var.web1_private_ip
					web2_private_ip = var.web2_private_ip
				}

				resource "aws_route" "spoke1_tgw_route" {
					route_table_id         = module.spoke_vpc1.Spoke1_RT_id
					destination_cidr_block = "0.0.0.0/0"
					transit_gateway_id     = module.transit_gateway.tgw_id
				}
			"""

		vars_tf = """
				///////////////
				// Spoke VPC1
				///////////////


				variable "spoke-Vpc1-Name" {}

				variable "spoke-Vpc1-cidr" {}

				variable "spoke1-web-a" {}

				variable "spoke1-web-b" {}

				variable "web1_private_ip" {}

				variable "web2_private_ip" {}
			"""

		return main_tf, vars_tf

	@staticmethod
	def vpc2():
		"""Method to inject vpc1 code in main.tf"""

		main_tf = """
				///////////////
				// Spoke2 VPC
				///////////////


				module "spoke_vpc2" {
					source = "../../packages/vpc/spoke-vpc2"

					access_key = var.access_key
					secret_key = var.secret_key

					aws_region = var.aws_region
					key_name   = var.aws_key

					vpc_name = var.spoke-Vpc2-Name
					vpc_cidr = var.spoke-Vpc2-cidr

					spoke2-db-a = var.spoke2-db-a
					spoke2-db-b = var.spoke2-db-b

					ssh1_private_ip = var.ssh1_private_ip
					ssh2_private_ip = var.ssh2_private_ip
				}

				resource "aws_route" "spoke2_tgw_route" {
					route_table_id         = module.spoke_vpc2.Spoke2_RT_id
					destination_cidr_block = "0.0.0.0/0"
					transit_gateway_id     = module.transit_gateway.tgw_id
				}
			"""

		vars_tf = """
				///////////////
				// Spoke VPC2
				///////////////


				variable "spoke-Vpc2-Name" {}

				variable "spoke-Vpc2-cidr" {}

				variable "spoke2-db-a" {}

				variable "spoke2-db-b" {}

				variable "ssh1_private_ip" {}

				variable "ssh2_private_ip" {}
			"""

		return main_tf, vars_tf

	@staticmethod
	def security_out_vpn_attachment():
		"""Method to inject security-Out vpc vpn attachment code in main.tf"""

		main_tf = """
			// **** security-Out VPC FW1 CGW<->TGW VPN Attachment **** //

			resource "aws_customer_gateway" "vmfw-sec-out-aza-1_cgw" {
				bgp_asn    = var.sec-out-asn
				ip_address = module.security_out_vpc.sec_out_fw1_vpn_ip
				type       = "ipsec.1"
			
				tags = {
					Name = "vmfw-sec-out-aza-1"
				}
			}
			
			resource "aws_vpn_connection" "sec_out_fw1_vpn_conn" {
				customer_gateway_id = aws_customer_gateway.vmfw-sec-out-aza-1_cgw.id
				transit_gateway_id  = module.transit_gateway.tgw_id
				type                = aws_customer_gateway.vmfw-sec-out-aza-1_cgw.type
			}
			
			data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_out_fw1_attach" {
				vpn_connection_id  = aws_vpn_connection.sec_out_fw1_vpn_conn.id
				transit_gateway_id = module.transit_gateway.tgw_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_association" "sec_out_fw1_tgw_asso" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw1_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_propagation" "sec_out_fw1_tgw_propo" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw1_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			// **** security-Out VPC FW2 CGW<->TGW VPN Attachment **** //
			
			resource "aws_customer_gateway" "vmfw-sec-out-azb-1_cgw" {
				bgp_asn    = var.sec-out-asn
				ip_address = module.security_out_vpc.sec_out_fw2_vpn_ip
				type       = "ipsec.1"
			
				tags = {
					Name = "vmfw-sec-out-azb-1"
				}
			}
			
			resource "aws_vpn_connection" "sec_out_fw2_vpn_conn" {
				customer_gateway_id = aws_customer_gateway.vmfw-sec-out-azb-1_cgw.id
				transit_gateway_id  = module.transit_gateway.tgw_id
				type                = aws_customer_gateway.vmfw-sec-out-azb-1_cgw.type
			}
			
			data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_out_fw2_attach" {
				vpn_connection_id  = aws_vpn_connection.sec_out_fw2_vpn_conn.id
				transit_gateway_id = module.transit_gateway.tgw_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_association" "sec_out_fw2_tgw_asso" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw2_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_propagation" "sec_out_fw2_tgw_propo" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw2_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
		"""

		vars_tf = """
					variable "sec-out-asn" {}
				"""

		return main_tf, vars_tf

	@staticmethod
	def security_ew_vpn_attachment():
		"""Method to inject security-Out vpc vpn attachment code in main.tf"""

		main_tf = """
			// **** security-East-West VPC FW1 CGW<->TGW VPN Attachment **** //

			resource "aws_customer_gateway" "vmfw-sec-east-west-aza-1_cgw" {
				bgp_asn    = var.sec-east-west-asn
				ip_address = module.security_east_west_vpc.sec_east_west_fw1_vpn_ip
				type       = "ipsec.1"
			
				tags = {
					Name = "vmfw-sec-east-west-aza-1"
				}
			}
			
			resource "aws_vpn_connection" "sec_east_west_fw1_vpn_conn" {
				customer_gateway_id = aws_customer_gateway.vmfw-sec-east-west-aza-1_cgw.id
				transit_gateway_id  = module.transit_gateway.tgw_id
				type                = aws_customer_gateway.vmfw-sec-east-west-aza-1_cgw.type
			}
			
			data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_east_west_fw1_attach" {
				vpn_connection_id  = aws_vpn_connection.sec_east_west_fw1_vpn_conn.id
				transit_gateway_id = module.transit_gateway.tgw_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_association" "sec_east_west_fw1_tgw_asso" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw1_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_propagation" "sec_east_west_fw1_tgw_propo" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw1_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			// **** security-East-West VPC FW2 CGW<->TGW VPN Attachment **** //
			
			resource "aws_customer_gateway" "vmfw-sec-east-west-azb-1_cgw" {
				bgp_asn    = var.sec-east-west-asn
				ip_address = module.security_east_west_vpc.sec_east_west_fw2_vpn_ip
				type       = "ipsec.1"
			
				tags = {
					Name = "vmfw-sec-east-west-azb-1"
				}
			}
			
			resource "aws_vpn_connection" "sec_east_west_fw2_vpn_conn" {
				customer_gateway_id = aws_customer_gateway.vmfw-sec-east-west-azb-1_cgw.id
				transit_gateway_id  = module.transit_gateway.tgw_id
				type                = aws_customer_gateway.vmfw-sec-east-west-azb-1_cgw.type
			}
			
			data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_east_west_fw2_attach" {
				vpn_connection_id  = aws_vpn_connection.sec_east_west_fw2_vpn_conn.id
				transit_gateway_id = module.transit_gateway.tgw_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_association" "sec_east_west_fw2_tgw_asso" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw2_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
			}
			
			resource "aws_ec2_transit_gateway_route_table_propagation" "sec_east_west_fw2_tgw_propo" {
				transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw2_attach.id
				transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
		"""

		vars_tf = """
					variable "sec-east-west-asn" {}
				"""

		return main_tf, vars_tf

	@staticmethod
	def customer_gateways():
		"""Method to create customer gateways"""

		main_tf = """
			//////////////////////
			// Customer Gateways
			//////////////////////
			
			
			
		"""

		vars_tf = """
			///////////////////////////////
			// Customer Gateway Variables
			///////////////////////////////
			
			
			
		"""

		return main_tf, vars_tf

	@staticmethod
	def security_in_tgw():
		"""Method to inject security-In vpc code in to tgw section in main.tf"""

		main_tf = """
			security_in_vpc_id       = module.security_in_vpc.vpc_id
			sub_security-In-TGW-a_id = module.security_in_vpc.security-In-TGW-a_id
			sub_security-In-TGW-b_id = module.security_in_vpc.security-In-TGW-b_id
		"""

		return main_tf

	@staticmethod
	def security_out_tgw():
		"""Method to inject security-Out vpc code in to tgw section in main.tf"""

		main_tf = """
			security_out_vpc_id       = module.security_out_vpc.vpc_id
			sub_security-Out-TGW-a_id = module.security_out_vpc.security-Out-TGW-a_id
			sub_security-Out-TGW-b_id = module.security_out_vpc.security-Out-TGW-b_id
		"""

		return main_tf

	@staticmethod
	def security_ew_tgw():
		"""Method to inject security-East-West vpc code in tgw section in man.tf"""

		main_tf = """
			security_east_west_vpc_id       = module.security_east_west_vpc.vpc_id
			sub_security-East-West-TGW-a_id = module.security_east_west_vpc.security-East-West-TGW-a_id
			sub_security-East-West-TGW-b_id = module.security_east_west_vpc.security-East-West-TGW-b_id
		"""

		return main_tf

	@staticmethod
	def services_tgw():
		"""Method to inject services vpc code in tgw section in main.tf"""

		main_tf = """
			services_vpc_id   = module.services_vpc.vpc_id
			sub_Services-a_id = module.services_vpc.Services-a_id
			sub_Services-b_id = module.services_vpc.Services-b_id
		"""

		return main_tf

	@staticmethod
	def vpc1_tgw():
		"""Method to inject vpc1 code in tgw section in main.tf"""

		main_tf = """
			vpc1_id             = module.spoke_vpc1.vpc_id
			sub_spoke1-web-a_id = module.spoke_vpc1.spoke1-web-a_id
			sub_spoke1-web-b_id = module.spoke_vpc1.spoke1-web-b_id
		"""

		return main_tf

	@staticmethod
	def vpc2_tgw():
		"""Method to inject vpc2 code in tgw section in main.tf"""

		main_tf = """
			vpc2_id             = module.spoke_vpc2.vpc_id
			sub_spoke2-web-a_id = module.spoke_vpc2.spoke2-web-a_id
			sub_spoke2-web-b_id = module.spoke_vpc2.spoke2-web-b_id
		"""

		return main_tf

	@staticmethod
	def tgw():
		"""Method to inject tgw code in main.tf"""

		main_tf = """
			module "transit_gateway" {
				source = "../../packages/transit-gateway"
			
				tgw_name = var.tgw_name
			
				aws_region      = var.aws_region
				amazon_side_asn = var.amazon_side_asn
		"""

		vars_tf = """
			////////////////////
			// Transit Gateway
			////////////////////
			
			
			variable "tgw_name" {}
			
			variable "amazon_side_asn" {}
		"""

		return main_tf, vars_tf
