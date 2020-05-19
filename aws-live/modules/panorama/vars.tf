//////////////////////
// Provider Variables
//////////////////////


variable "access_key" {}

variable "secret_key" {}

variable "aws_region" {}

variable "panorama_aws_key" {}


//////////////////////
// Panorama
//////////////////////

//variable "panos_version" {
//  description = "Select which Panorama version to deploy"
//  default = "9.0.3"
//}
//
//variable "panos_license_type" {
//  description = "Select License type (byol only for Panorama)"
//  default = "byol"
//}
//
//variable "panos_license_type_map" {
//  type = "map"
//  default =
//    {
//      "byol" = "eclz7j04vu9lf8ont8ta3n17o",
//    }
//}
//
//variable "panorama_instance_type" {
//  default = "m4.2xlarge"
//}

variable "panorama_version" {}

variable "panorama_license_type" {}

variable "panorama_license_type_map" {}

variable "panorama_instance_type" {}

variable "panorama_mgmt_subnet_id" {}

variable "mgmtpanoramaip" {}

variable "panorama_name" {}

variable "services-Vpc-Name" {}

variable "services_vpc_id" {}
