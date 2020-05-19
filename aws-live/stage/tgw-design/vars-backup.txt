///////////////////////
// Constant Variables
///////////////////////


variable "panorama_license_type_map" {
  type = "map"
  default =
    {
      "byol" = "eclz7j04vu9lf8ont8ta3n17o",
    }
}

variable "fw_license_type_map" {
  type = "map"

  default = {
    "byol"  = "6njl1pau431dv1qxipg63mvah"
    "payg1" = "6kxdw3bbmdeda3o6i1ggqt4km"
    "payg2" = "806j2of0qy5osgjjixq9gqc6g"
  }
}


/////////////
// Provider
/////////////


variable "access_key" {}

variable "secret_key" {}

variable "aws_key" {}

variable "aws_region" {}


//////////////
// Bootstrap
//////////////


variable "bootstrap_s3bucket" {}


//////////////////
// Load Balancer
//////////////////


variable "lb_access_log_bucket" {}


///////////////
// Spoke VPC1
///////////////


variable "spoke-Vpc1-Name" {}

variable "spoke-Vpc1-cidr" {}

variable "spoke1-web-a" {}

variable "spoke1-web-b" {}

variable "web1_private_ip" {}

variable "web2_private_ip" {}


///////////////
// Spoke VPC2
///////////////


variable "spoke-Vpc2-Name" {}

variable "spoke-Vpc2-cidr" {}

variable "spoke2-db-a" {}

variable "spoke2-db-b" {}

variable "ssh1_private_ip" {}

variable "ssh2_private_ip" {}


/////////////////
// Services VPC
/////////////////


variable "services-Vpc-Name" {}

variable "services-Vpc-cidr" {}

variable "Services-a" {}

variable "Services-b" {}


// Panorama Variables //


variable "panorama_version" {}

variable "panorama_license_type" {}

variable "panorama_instance_type" {}

variable "mgmtpanoramaip" {}

variable "panorama_name" {}


////////////////////
// Security-In VPC
////////////////////


variable "security-In-Vpc-Name" {}

variable "security-In-Vpc-cidr" {}

variable "security-In-Mgmt-a" {}

variable "security-In-TGW-a" {}

variable "security-In-Pub-a" {}

variable "security-In-Priv-a" {}

variable "security-In-Mgmt-b" {}

variable "security-In-TGW-b" {}

variable "security-In-Pub-b" {}

variable "security-In-Priv-b" {}

variable "security-In-fw1_name" {}

variable "security-In-fw1_mgmt_ip" {}

variable "security-In-fw1_untrust_ip" {}

variable "security-In-fw1_trust_ip" {}

variable "security-In-fw2_name" {}

variable "security-In-fw2_mgmt_ip" {}

variable "security-In-fw2_untrust_ip" {}

variable "security-In-fw2_trust_ip" {}

variable "security-In-fw_instance_type" {}

variable "security-In-ngfw_license_type" {}

variable "security-In-ngfw_version" {}


////////////////////
// Security-Out VPC
////////////////////


variable "security-Out-Vpc-Name" {}

variable "security-Out-Vpc-cidr" {}

variable "security-Out-Mgmt-a" {}

variable "security-Out-TGW-a" {}

variable "security-Out-Pub-a" {}

variable "security-Out-Mgmt-b" {}

variable "security-Out-TGW-b" {}

variable "security-Out-Pub-b" {}

variable "security-Out-fw1_name" {}

variable "security-Out-fw1_mgmt_ip" {}

variable "security-Out-fw1_untrust_ip" {}

//variable "security-Out-fw1_trust_ip" {
//  default = ""
//}

variable "security-Out-fw2_name" {}

variable "security-Out-fw2_mgmt_ip" {}

variable "security-Out-fw2_untrust_ip" {}

//variable "security-Out-fw2_trust_ip" {
//  default = ""
//}

variable "security-Out-fw_instance_type" {}

variable "security-Out-ngfw_license_type" {}

variable "security-Out-ngfw_version" {}


///////////////////////////
// Security-East-West VPC
///////////////////////////


variable "security-East-West-Vpc-Name" {}

variable "security-East-West-Vpc-cidr" {}

variable "security-East-West-Mgmt-a" {}

variable "security-East-West-TGW-a" {}

variable "security-East-West-Pub-a" {}

variable "security-East-West-Mgmt-b" {}

variable "security-East-West-TGW-b" {}

variable "security-East-West-Pub-b" {}

variable "security-East-West-fw1_name" {}

variable "security-East-West-fw1_mgmt_ip" {}

variable "security-East-West-fw1_untrust_ip" {}

//variable "security-East-West-fw1_trust_ip" {
//  default = ""
//}

variable "security-East-West-fw2_name" {}

variable "security-East-West-fw2_mgmt_ip" {}

variable "security-East-West-fw2_untrust_ip" {}

//variable "security-East-West-fw2_trust_ip" {
//  default = ""
//}

variable "security-East-West-fw_instance_type" {}

variable "security-East-West-ngfw_license_type" {}

variable "security-East-West-ngfw_version" {}


///////////////////////////////
// Customer Gateway Variables
///////////////////////////////


variable "sec-out-asn" {}

variable "sec-east-west-asn" {}


////////////////////
// Transit Gateway
////////////////////


variable "tgw_name" {}

variable "amazon_side_asn" {}
