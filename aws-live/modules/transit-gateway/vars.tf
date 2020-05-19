//////////////////////
// Provider Variables
//////////////////////

variable "access_key" {
  default = "AKIAVFK6UURB6VTP6LOJ"
}

variable "secret_key" {
  default = "Zo3u7dchqBg6hoZg2jRp0JmeilFvWlbBCc5HVCQN"
}

variable "aws_region" {}


/////////////////////
// Transit Gateway
/////////////////////


variable "tgw_name" {}

variable "amazon_side_asn" {}


/////////////////////////////
// TGW Attachment Variables
/////////////////////////////


// **** Spoke1 VPC **** //

variable "sub_spoke1-web-a_id" {}

variable "sub_spoke1-web-b_id" {}

variable "vpc1_id" {}

// **** Spoke12 VPC **** //

variable "sub_spoke2-web-a_id" {}

variable "sub_spoke2-web-b_id" {}

variable "vpc2_id" {}

// **** Security-In VPC **** //

variable "sub_security-In-TGW-a_id" {}

variable "sub_security-In-TGW-b_id" {}

variable "security_in_vpc_id" {}

// **** Security-Out VPC **** //

variable "sub_security-Out-TGW-a_id" {}

variable "sub_security-Out-TGW-b_id" {}

variable "security_out_vpc_id" {}

// **** East-West VPC **** //

variable "sub_security-East-West-TGW-a_id" {}

variable "sub_security-East-West-TGW-b_id" {}

variable "security_east_west_vpc_id" {}

// **** Services VPC **** //

variable "sub_Services-a_id" {}

variable "sub_Services-b_id" {}

variable "services_vpc_id" {}


/////////////////////////////
// CGW Attachment Variables
/////////////////////////////


//variable "vmfw-sec-out-aza-1_cgw" {}
