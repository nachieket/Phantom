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


variable "spoke1-web-a" {}

variable "spoke1-web-b" {}


/////////////////////////
// Web Server Variables
/////////////////////////


variable "key_name" {}

variable "web1_private_ip" {}

variable "web2_private_ip" {}


////////////////////////////
// Load Balancer Variables
////////////////////////////


variable "lb_access_log_bucket" {}
