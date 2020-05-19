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


variable "security-In-Mgmt-a" {}

variable "security-In-TGW-a" {}

variable "security-In-Pub-a" {}

variable "security-In-Priv-a" {}

variable "security-In-Mgmt-b" {}

variable "security-In-TGW-b" {}

variable "security-In-Pub-b" {}

variable "security-In-Priv-b" {}


///////
// FW
///////


variable "fw1_name" {}

variable "fw2_name" {}

variable "fw1_mgmt_ip" {}

variable "fw1_untrust_ip" {}

variable "fw1_trust_ip" {}

variable "fw2_mgmt_ip" {}

variable "fw2_untrust_ip" {}

variable "fw2_trust_ip" {}

variable "fw_instance_type" {}

variable "fw_license_type_map" {}

variable "ngfw_license_type" {}

variable "ngfw_version" {}


//////////////
// Bootstrap
//////////////


variable "bootstrap_s3bucket_id" {}

variable "bootstrap_s3bucket_name" {}

variable "bootstrap_role_name" {}


/////////////////
// Load Balancer
/////////////////


variable "lb_access_log_bucket" {}
