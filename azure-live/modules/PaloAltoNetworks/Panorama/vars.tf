
//////////////////////
// Panorama Variables
//////////////////////

variable "subscription_id" {
	default = ""
}

variable "tenant_id" {
	default = ""
}

variable "client_id" {
	default = ""
}

variable "client_secret" {
	default = ""
}

variable "Location" {
	description = "Location"
	default     = "East US"
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
	default     = "Panorama"
}

variable "virtualMachineSize" {
	description = "Virtual Machine Size"
	default     = "Standard_D4s_v3"
}

variable "panoramaVersion" {
	description = "Panorama Version"
	default     = "8.1.2"
}

variable "panorama_ip_address" {
	default = "10.0.0.100"
}

variable "adminUsername" {
	description = "Admin Username"
	default     = "panadmin"
}

variable "adminPassword" {
	description = "Admin Password"
	default     = "JAqnS7ALnv#*4DFd"
}

variable "resourcegroup_location" {
	default = "East US"
}

variable "resourcegroup_name" {
	default = "PANW"
}

variable "azure_subnet_id" {
	default = "/subscriptions/87278e-7f1-454-9c4-453bfa6c53/resourceGroups/PANW/providers/Microsoft.Network/virtualNetworks/Corporate/subnets/default"
}
