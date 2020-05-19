//////////////////////
// Provider Variables
//////////////////////


variable "access_key" {}

variable "secret_key" {}

variable "aws_region" {}

variable "aws_key" {}


//////////////////////
// Firewall Variables
//////////////////////


variable "fw_name" {}

variable "untrust_subnet_id" {}

variable "untrust_security_group_id" {}

variable "untrustfwip" {}

//variable "trust_subnet_id" {}
//variable "trust_security_group_id" {}
//variable "trustfwip" {}

variable "mgmt_subnet_id" {}

variable "mgmt_security_group_id" {}

variable "mgmtfwip" {}

variable "fw_instance_type" {}

variable "ngfw_license_type" {}

variable "ngfw_version" {}

variable "fw_license_type_map" {}

//variable "instance_type" {
//  default = "m4.2xlarge"
//}
//
//variable "ngfw_license_type" {
//  default = "byol"
//}
//
//variable "ngfw_version" {
//  default = "9.0.3.xfr"
//}
//
//variable "license_type_map" {
//  type = "map"
//
//  default = {
//    "byol"  = "6njl1pau431dv1qxipg63mvah"
//    "payg1" = "6kxdw3bbmdeda3o6i1ggqt4km"
//    "payg2" = "806j2of0qy5osgjjixq9gqc6g"
//  }
//}


////////////////////////
// BOOTSTRAP Variables
////////////////////////


variable "bootstrap_s3bucket_id" {}

variable "xml_key" {}

variable "init_cfg_key" {}

variable "software_key" {}

variable "license_key" {}

variable "content_key" {}

variable "xml_source" {}

variable "init_cfg_source" {}

variable "license_source" {}

variable "bootstrap_role_name" {}

variable "bootstrap_s3bucket_name" {}
