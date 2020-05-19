//////////////////////
// Provider Variables
//////////////////////


variable "aws_region" {}

variable "access_key" {}

variable "secret_key" {}

variable "ubuntu_aws_key" {}


/////////////////
// VPC Varibales
/////////////////


variable "vpc_name" {
  default = "Services"
}

variable "vpc_cidr" {}


////////////////////
// Subnet Variables
////////////////////


variable "Services-a" {}

variable "Services-b" {}


/////////////////////
// Ubuntu Variables
/////////////////////


variable "ssh_private_ip" {}
