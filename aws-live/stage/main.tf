///////////////////////
// PROVIDER DEFINITION
///////////////////////


provider "aws" {
  region     = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


//////////////////////////////////
// BACKEND TO STORE TFSTATE FILES
//////////////////////////////////


terraform {
  backend "s3" {
    bucket     = "aws-transit-gateway-s3-phantom-bucket"
    key        = "stage/transit-gateway/terraform.tfstate"
    region     = "eu-west-2"
    encrypt    = true
    access_key = "AKIAVFK6UURB6VTP6LOJ"
    secret_key = "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"
  }
}

resource "aws_s3_bucket" "bootstrap_bucket" {
  bucket        = var.bootstrap_s3bucket
  acl           = "private"
  force_destroy = true

  tags = {
    Name = "bootstrap_bucket"
  }
}

resource "aws_s3_bucket" "lb_access_log_bucket" {
  bucket        = var.lb_access_log_bucket
  acl           = "private"
  force_destroy = true

  tags = {
    Name = "lb_access_log_bucket"
  }
}


/////////////
// IAM Role
/////////////


resource "aws_iam_role" "bootstrap_role" {
  name = "ngfw_bootstrap_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
      "Service": "ec2.amazonaws.com"
    },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "bootstrap_policy" {
  name = "ngfw_bootstrap_policy"
  role = aws_iam_role.bootstrap_role.id

  policy = <<EOF
{
  "Version" : "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::${var.bootstrap_s3bucket}"
    },
    {
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::${var.bootstrap_s3bucket}/*"
    }
  ]
}
EOF
}


////////////////////////
//// Bootstrap Profile
////////////////////////
//
//
//resource "aws_iam_instance_profile" "bootstrap_profile" {
//  name = "ngfw_bootstrap_profile"
//  role = "${aws_iam_role.bootstrap_role.name}"
//  path = "/"
//}


///////////////
// Spoke1 VPC
///////////////


module "spoke_vpc1" {
  source = "../../modules/vpc/spoke-vpc1"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name   = var.aws_key

  vpc_name = var.spoke-Vpc1-Name
  vpc_cidr = var.spoke-Vpc1-cidr

  lb_access_log_bucket = aws_s3_bucket.lb_access_log_bucket.bucket

  spoke1-web-a = var.spoke1-web-a
  spoke1-web-b = var.spoke1-web-b

  web1_private_ip = var.web1_private_ip
  web2_private_ip = var.web2_private_ip
}

resource "aws_route" "spoke1_tgw_route" {
  route_table_id         = module.spoke_vpc1.Spoke1_RT_id
  destination_cidr_block = "0.0.0.0/0"
  transit_gateway_id     = module.transit_gateway.tgw_id
}


///////////////
// Spoke2 VPC
///////////////


module "spoke_vpc2" {
  source = "../../modules/vpc/spoke-vpc2"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name   = var.aws_key

  vpc_name = var.spoke-Vpc2-Name
  vpc_cidr = var.spoke-Vpc2-cidr

  spoke2-db-a = var.spoke2-db-a
  spoke2-db-b = var.spoke2-db-b

  ssh1_private_ip = var.ssh1_private_ip
  ssh2_private_ip = var.ssh2_private_ip
}

resource "aws_route" "spoke2_tgw_route" {
  route_table_id         = module.spoke_vpc2.Spoke2_RT_id
  destination_cidr_block = "0.0.0.0/0"
  transit_gateway_id     = module.transit_gateway.tgw_id
}


////////////////////////
// Services VPC Module
////////////////////////


module "services_vpc" {
  source = "../../modules/vpc/services-vpc"

  aws_region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
  aws_key = var.aws_key

  vpc_name = var.services-Vpc-Name
  vpc_cidr = var.services-Vpc-cidr

  Services-a = var.Services-a
  Services-b = var.Services-b

  mgmtpanoramaip = var.mgmtpanoramaip
  panorama_instance_type = var.panorama_instance_type
  panorama_name = var.panorama_name
  panorama_license_type = var.panorama_license_type
  panorama_license_type_map = var.panorama_license_type_map
  panorama_version = var.panorama_version
}


///////////////////////////////
// Security Inbound VPC Module
///////////////////////////////


module "security_in_vpc" {
  source = "../../modules/vpc/security-in"

  access_key = var.access_key
  secret_key = var.secret_key
  aws_key    = var.aws_key
  aws_region = var.aws_region

  fw_instance_type = var.security-In-fw_instance_type
  fw_license_type_map = var.fw_license_type_map
  ngfw_license_type = var.security-In-ngfw_license_type
  ngfw_version = var.security-In-ngfw_version

  bootstrap_s3bucket_id   = aws_s3_bucket.bootstrap_bucket.id
  bootstrap_role_name     = aws_iam_role.bootstrap_role.name
  bootstrap_s3bucket_name = aws_s3_bucket.bootstrap_bucket.bucket

  vpc_name             = var.security-In-Vpc-Name
  vpc_cidr             = var.security-In-Vpc-cidr
  lb_access_log_bucket = aws_s3_bucket.lb_access_log_bucket.bucket

  security-In-Mgmt-a = var.security-In-Mgmt-a
  security-In-TGW-a  = var.security-In-TGW-a
  security-In-Pub-a  = var.security-In-Pub-a
  security-In-Priv-a = var.security-In-Priv-a

  security-In-Mgmt-b = var.security-In-Mgmt-b
  security-In-TGW-b  = var.security-In-TGW-b
  security-In-Pub-b  = var.security-In-Pub-b
  security-In-Priv-b = var.security-In-Priv-b

  fw1_name       = var.security-In-fw1_name
  fw1_mgmt_ip    = var.security-In-fw1_mgmt_ip
  fw1_untrust_ip = var.security-In-fw1_untrust_ip
  fw1_trust_ip   = var.security-In-fw1_trust_ip

  fw2_name       = var.security-In-fw2_name
  fw2_mgmt_ip    = var.security-In-fw2_mgmt_ip
  fw2_untrust_ip = var.security-In-fw2_untrust_ip
  fw2_trust_ip   = var.security-In-fw2_trust_ip
}


////////////////////////////////
// Security Outbound VPC Module
////////////////////////////////


module "security_out_vpc" {
  source = "../../modules/vpc/security-out"

  access_key = var.access_key
  secret_key = var.secret_key
  aws_key    = var.aws_key
  aws_region = var.aws_region

  fw_instance_type = var.security-Out-fw_instance_type
  fw_license_type_map = var.fw_license_type_map
  ngfw_license_type = var.security-Out-ngfw_license_type
  ngfw_version = var.security-Out-ngfw_version

  bootstrap_s3bucket_id   = aws_s3_bucket.bootstrap_bucket.id
  bootstrap_role_name     = aws_iam_role.bootstrap_role.name
  bootstrap_s3bucket_name = aws_s3_bucket.bootstrap_bucket.bucket

  vpc_name = var.security-Out-Vpc-Name
  vpc_cidr = var.security-Out-Vpc-cidr

  security-Out-Mgmt-a = var.security-Out-Mgmt-a
  security-Out-TGW-a  = var.security-Out-TGW-a
  security-Out-Pub-a  = var.security-Out-Pub-a
  security-Out-Mgmt-b = var.security-Out-Mgmt-b
  security-Out-TGW-b  = var.security-Out-TGW-b
  security-Out-Pub-b  = var.security-Out-Pub-b

  fw1_name       = var.security-Out-fw1_name
  fw1_mgmt_ip    = var.security-Out-fw1_mgmt_ip
  fw1_untrust_ip = var.security-Out-fw1_untrust_ip
  //  fw1_trust_ip = "${var.security-Out-fw1_trust_ip}"

  fw2_name       = var.security-Out-fw2_name
  fw2_mgmt_ip    = var.security-Out-fw2_mgmt_ip
  fw2_untrust_ip = var.security-Out-fw2_untrust_ip
  //  fw2_trust_ip = "${var.security-Out-fw2_trust_ip}"
}


/////////////////////////////////
// East-West Security VPC Module
/////////////////////////////////


module "security_east_west_vpc" {
  source = "../../modules/vpc/security-east-west"

  access_key = var.access_key
  secret_key = var.secret_key
  aws_key    = var.aws_key
  aws_region = var.aws_region

  fw_instance_type = var.security-East-West-fw_instance_type
  fw_license_type_map = var.fw_license_type_map
  ngfw_license_type = var.security-East-West-ngfw_license_type
  ngfw_version = var.security-East-West-ngfw_version

  bootstrap_s3bucket_id   = aws_s3_bucket.bootstrap_bucket.id
  bootstrap_role_name     = aws_iam_role.bootstrap_role.name
  bootstrap_s3bucket_name = aws_s3_bucket.bootstrap_bucket.bucket

  vpc_name = var.security-East-West-Vpc-Name
  vpc_cidr = var.security-East-West-Vpc-cidr

  security-East-West-Mgmt-a = var.security-East-West-Mgmt-a
  security-East-West-TGW-a  = var.security-East-West-TGW-a
  security-East-West-Pub-a  = var.security-East-West-Pub-a
  security-East-West-Mgmt-b = var.security-East-West-Mgmt-b
  security-East-West-TGW-b  = var.security-East-West-TGW-b
  security-East-West-Pub-b  = var.security-East-West-Pub-b

  fw1_name       = var.security-East-West-fw1_name
  fw1_mgmt_ip    = var.security-East-West-fw1_mgmt_ip
  fw1_untrust_ip = var.security-East-West-fw1_untrust_ip
  //  fw1_trust_ip = "${var.security-East-West-fw1_trust_ip}"

  fw2_name       = var.security-East-West-fw2_name
  fw2_mgmt_ip    = var.security-East-West-fw2_mgmt_ip
  fw2_untrust_ip = var.security-East-West-fw2_untrust_ip
  //  fw2_trust_ip = "${var.security-East-West-fw2_trust_ip}"
}


//////////////////////
// Customer Gateways
//////////////////////


// ToDo: Check if below code actually works!

// **** security-Out VPC FW1 CGW<->TGW VPN Attachment **** //

resource "aws_customer_gateway" "vmfw-sec-out-aza-1_cgw" {
  bgp_asn    = var.sec-out-asn
  ip_address = module.security_out_vpc.sec_out_fw1_vpn_ip
  type       = "ipsec.1"

  tags = {
    Name = "vmfw-sec-out-aza-1"
  }
}

resource "aws_vpn_connection" "sec_out_fw1_vpn_conn" {
  customer_gateway_id = aws_customer_gateway.vmfw-sec-out-aza-1_cgw.id
  transit_gateway_id  = module.transit_gateway.tgw_id
  type                = aws_customer_gateway.vmfw-sec-out-aza-1_cgw.type
}

data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_out_fw1_attach" {
  vpn_connection_id  = aws_vpn_connection.sec_out_fw1_vpn_conn.id
  transit_gateway_id = module.transit_gateway.tgw_id
}

resource "aws_ec2_transit_gateway_route_table_association" "sec_out_fw1_tgw_asso" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw1_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "sec_out_fw1_tgw_propo" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw1_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

// **** security-Out VPC FW2 CGW<->TGW VPN Attachment **** //

resource "aws_customer_gateway" "vmfw-sec-out-azb-1_cgw" {
  bgp_asn    = var.sec-out-asn
  ip_address = module.security_out_vpc.sec_out_fw2_vpn_ip
  type       = "ipsec.1"

  tags = {
    Name = "vmfw-sec-out-azb-1"
  }
}

resource "aws_vpn_connection" "sec_out_fw2_vpn_conn" {
  customer_gateway_id = aws_customer_gateway.vmfw-sec-out-azb-1_cgw.id
  transit_gateway_id  = module.transit_gateway.tgw_id
  type                = aws_customer_gateway.vmfw-sec-out-azb-1_cgw.type
}

data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_out_fw2_attach" {
  vpn_connection_id  = aws_vpn_connection.sec_out_fw2_vpn_conn.id
  transit_gateway_id = module.transit_gateway.tgw_id
}

resource "aws_ec2_transit_gateway_route_table_association" "sec_out_fw2_tgw_asso" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw2_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "sec_out_fw2_tgw_propo" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_out_fw2_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

// **** security-East-West VPC FW1 CGW<->TGW VPN Attachment **** //

resource "aws_customer_gateway" "vmfw-sec-east-west-aza-1_cgw" {
  bgp_asn    = var.sec-east-west-asn
  ip_address = module.security_east_west_vpc.sec_east_west_fw1_vpn_ip
  type       = "ipsec.1"

  tags = {
    Name = "vmfw-sec-east-west-aza-1"
  }
}

resource "aws_vpn_connection" "sec_east_west_fw1_vpn_conn" {
  customer_gateway_id = aws_customer_gateway.vmfw-sec-east-west-aza-1_cgw.id
  transit_gateway_id  = module.transit_gateway.tgw_id
  type                = aws_customer_gateway.vmfw-sec-east-west-aza-1_cgw.type
}

data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_east_west_fw1_attach" {
  vpn_connection_id  = aws_vpn_connection.sec_east_west_fw1_vpn_conn.id
  transit_gateway_id = module.transit_gateway.tgw_id
}

resource "aws_ec2_transit_gateway_route_table_association" "sec_east_west_fw1_tgw_asso" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw1_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "sec_east_west_fw1_tgw_propo" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw1_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

// **** security-East-West VPC FW2 CGW<->TGW VPN Attachment **** //

resource "aws_customer_gateway" "vmfw-sec-east-west-azb-1_cgw" {
  bgp_asn    = var.sec-east-west-asn
  ip_address = module.security_east_west_vpc.sec_east_west_fw2_vpn_ip
  type       = "ipsec.1"

  tags = {
    Name = "vmfw-sec-east-west-azb-1"
  }
}

resource "aws_vpn_connection" "sec_east_west_fw2_vpn_conn" {
  customer_gateway_id = aws_customer_gateway.vmfw-sec-east-west-azb-1_cgw.id
  transit_gateway_id  = module.transit_gateway.tgw_id
  type                = aws_customer_gateway.vmfw-sec-east-west-azb-1_cgw.type
}

data "aws_ec2_transit_gateway_vpn_attachment" "tgw_vpn_sec_east_west_fw2_attach" {
  vpn_connection_id  = aws_vpn_connection.sec_east_west_fw2_vpn_conn.id
  transit_gateway_id = module.transit_gateway.tgw_id
}

resource "aws_ec2_transit_gateway_route_table_association" "sec_east_west_fw2_tgw_asso" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw2_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "sec_east_west_fw2_tgw_propo" {
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpn_attachment.tgw_vpn_sec_east_west_fw2_attach.id
  transit_gateway_route_table_id = module.transit_gateway.TGW_Security_RT_id
}


///////////////////////////
// Transit Gateway Module
///////////////////////////


module "transit_gateway" {
  source = "../../modules/transit-gateway"

  tgw_name = var.tgw_name

  aws_region      = var.aws_region
  amazon_side_asn = var.amazon_side_asn

  security_in_vpc_id       = module.security_in_vpc.vpc_id
  sub_security-In-TGW-a_id = module.security_in_vpc.security-In-TGW-a_id
  sub_security-In-TGW-b_id = module.security_in_vpc.security-In-TGW-b_id

  security_out_vpc_id       = module.security_out_vpc.vpc_id
  sub_security-Out-TGW-a_id = module.security_out_vpc.security-Out-TGW-a_id
  sub_security-Out-TGW-b_id = module.security_out_vpc.security-Out-TGW-b_id

  security_east_west_vpc_id       = module.security_east_west_vpc.vpc_id
  sub_security-East-West-TGW-a_id = module.security_east_west_vpc.security-East-West-TGW-a_id
  sub_security-East-West-TGW-b_id = module.security_east_west_vpc.security-East-West-TGW-b_id

  services_vpc_id   = module.services_vpc.vpc_id
  sub_Services-a_id = module.services_vpc.Services-a_id
  sub_Services-b_id = module.services_vpc.Services-b_id

  vpc1_id             = module.spoke_vpc1.vpc_id
  sub_spoke1-web-a_id = module.spoke_vpc1.spoke1-web-a_id
  sub_spoke1-web-b_id = module.spoke_vpc1.spoke1-web-b_id

  vpc2_id             = module.spoke_vpc2.vpc_id
  sub_spoke2-web-a_id = module.spoke_vpc2.spoke2-web-a_id
  sub_spoke2-web-b_id = module.spoke_vpc2.spoke2-web-b_id
}
