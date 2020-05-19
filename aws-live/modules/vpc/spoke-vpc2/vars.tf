///////////////////////
// Provider Variables
///////////////////////


variable "access_key" {}

variable "secret_key" {}

variable "vpc_name" {}

variable "vpc_cidr" {}

variable "aws_region" {}


////////////////////
// Subnet Variables
////////////////////


variable "spoke2-db-a" {}

variable "spoke2-db-b" {}


/////////////////////////
// SSH Server Variables
/////////////////////////


variable "key_name" {}

variable "ssh1_private_ip" {}

variable "ssh2_private_ip" {}
