//////////////////////
// Provider Variables
//////////////////////


variable "access_key" {
  default = "AKIAVFK6UURB6VTP6LOJ"
}

variable "secret_key" {
  default = "Zo3u7dchqBg6hoZg2jRp0JmeilFvWlbBCc5HVCQN"
}


//////////////////
// VPC Variables
//////////////////


variable "aws_region" {}

variable "vpc_id" {}

variable "vpc_name" {}


////////////////////////////
// Load Balancer Variables
////////////////////////////


variable "security_group_id" {}

variable "subnet_a_id" {}

variable "subnet_b_id" {}

variable "instance1_ip" {}

variable "instance2_ip" {}

variable "lb_internal" {}

variable "lb_access_log_bucket" {}
