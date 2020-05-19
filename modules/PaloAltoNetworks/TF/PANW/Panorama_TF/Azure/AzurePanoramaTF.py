#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import textwrap


class AzurePanoramaTF(object):
	"""
	Azure Panorama Class
	"""

	def __init__(self):
		self.module_dir = './azure-live/modules/PaloAltoNetworks/Panorama/'

	def configure_azure_panorama(self, panorama, azure):
		"""Method to configure Azure Panorama Terraform vars template file"""

		vars_tf = """
			//////////////////////
			// Panorama Variables
			//////////////////////


			variable "Location" {
				description = "Location"
				default     = "%s"
			}
			
			variable "publicIpAddressName" {
				description = "Public Ip Address Name"
				default     = "Panorama_Public_IP"
			}
			
			variable "networkInterfaceName" {
				description = "Network Interface Name"
				default     = "Panorama_Int"
			}
			
			variable "diagnosticsStorageAccountName" {
				description = "Diagnostics Storage Account Name"
				default     = "panorama"
			}
			
			variable "diagnosticsStorageAccountTier" {
				description = "Diagnostics Storage Account Tier"
				default     = "Standard"
			}
			
			variable "diagnosticsStorageAccountReplication" {
				description = "Diagnostics Storage Account Replication"
				default     = "LRS"
			}
			
			variable "virtualMachineName" {
				description = "Virtual Machine Name"
				default     = "%s"
			}
			
			variable "virtualMachineSize" {
				description = "Virtual Machine Size"
				default     = "%s"
			}
			
			variable "panoramaVersion" {
				description = "Panorama Version"
				default     = "8.1.2"
			}
			
			variable "adminUsername" {
				description = "Admin Username"
				default     = "%s"
			}
			
			variable "adminPassword" {
				description = "Admin Password"
				default     = "%s"
			}
			
			variable "resourcegroup_location" {
				default = "%s"
			}
			
			variable "resourcegroup_name" {
				default = "%s"
			}
			
			variable "azure_subnet_id" {
				default = "%s"
			}
			
			variable "panorama_ip_address" {
				default = "%s"
			}

		"""

		directory = self.module_dir

		with open('{}vars.tf'.format(directory), 'w') as f:
			f.write(textwrap.dedent(vars_tf % (
				azure['azure_region'], panorama['panorama_name'], panorama['instance_type'],
				panorama['panorama_username'], panorama['panorama_password'], azure['resourcegroup_location'],
				azure['resourcegroup_name'], azure['azure_subnet_id'], panorama['panorama_ip']
			)))
