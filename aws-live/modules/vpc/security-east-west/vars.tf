//////////////////////
// Provider Variables
//////////////////////


variable "access_key" {}

variable "secret_key" {}

variable "aws_key" {}

variable "aws_region" {}

/////////////////
// VPC Varibales
/////////////////


variable "vpc_name" {}

variable "vpc_cidr" {}


////////////////////
// Subnet Variables
////////////////////


variable "security-East-West-Mgmt-a" {}

variable "security-East-West-TGW-a" {}

variable "security-East-West-Pub-a" {}

variable "security-East-West-Mgmt-b" {}

variable "security-East-West-TGW-b" {}

variable "security-East-West-Pub-b" {}


///////
// FW
///////


variable "fw1_name" {}

variable "fw2_name" {}

variable "fw1_mgmt_ip" {}

variable "fw1_untrust_ip" {}

//variable "fw1_trust_ip" {}

variable "fw2_mgmt_ip" {}

variable "fw2_untrust_ip" {}

//variable "fw2_trust_ip" {}

variable "fw_instance_type" {}

variable "fw_license_type_map" {}

variable "ngfw_license_type" {}

variable "ngfw_version" {}


//////////////
// Bootstrap
//////////////


variable "bootstrap_s3bucket_id" {}

variable "bootstrap_role_name" {}

variable "bootstrap_s3bucket_name" {}
