///////////////////////
// PROVIDER DEFINITION
///////////////////////


provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


///////////////////////////
// DATA SOURCE DEFINITIONS
///////////////////////////


data "aws_availability_zones" "available" {
  state = "available"
}


////////////////////
// VPC DEFINITIONS
////////////////////


resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = var.vpc_name
  }
}


//////////////////////
// SUBNET DEFINITIONS
//////////////////////

// Availability Zone - A //

resource "aws_subnet" "security-Out-Mgmt-a" {
  cidr_block = var.security-Out-Mgmt-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-Out-Mgmt-a"
  }
}

resource "aws_subnet" "security-Out-TGW-a" {
  cidr_block = var.security-Out-TGW-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-Out-TGW-a"
  }
}

resource "aws_subnet" "security-Out-Pub-a" {
  cidr_block = var.security-Out-Pub-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-Out-Pub-a"
  }
}

// Availability Zone - B //

resource "aws_subnet" "security-Out-Mgmt-b" {
  cidr_block = var.security-Out-Mgmt-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-Out-Mgmt-b"
  }
}

resource "aws_subnet" "security-Out-TGW-b" {
  cidr_block = var.security-Out-TGW-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-Out-TGW-b"
  }
}

resource "aws_subnet" "security-Out-Pub-b" {
  cidr_block = var.security-Out-Pub-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-Out-Pub-b"
  }
}

////////
// IGW
////////


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_igw"
  }
}


//////////////////////////////
// SECURITY GROUP DEFINITIONS
//////////////////////////////

////// Allow All SG //////

resource "aws_security_group" "allow_all" {
  name = "${var.vpc_name}_allow_all_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_allow_all"
  }
}

resource "aws_security_group_rule" "allow_all_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.allow_all.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_all_outbound" {
  type = "egress"
  security_group_id = aws_security_group.allow_all.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

////// Management SG //////

resource "aws_security_group" "management" {
  name = "${var.vpc_name}_mgmt_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_management"
  }
}

resource "aws_security_group_rule" "management_3978" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = 3978
  to_port = 3978
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "management_28443" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = 28443
  to_port = 28443
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "management_123" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = 123
  to_port = 123
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "management_22" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["10.0.0.0/8", "172.16.0.0/16"]
}

resource "aws_security_group_rule" "management_443" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = 443
  to_port = 443
  protocol = "-1"
  cidr_blocks = ["10.0.0.0/8", "172.16.0.0/16"]
}

resource "aws_security_group_rule" "management_icmp" {
  type = "ingress"
  security_group_id = aws_security_group.management.id

  from_port = -1
  to_port = -1
  protocol = "icmp"
  cidr_blocks = ["10.0.0.0/8"]
}

resource "aws_security_group_rule" "management_outbound" {
  type = "egress"
  security_group_id = aws_security_group.management.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["10.0.0.0/8"]
}


////////////////
// ROUTE TABLE
////////////////

////// Security-Out-IGW //////

resource "aws_route_table" "Security-Out-IGW_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-Out-IGW"
  }
}

resource "aws_route_table_association" "security-Out-Pub-a_rt_asso" {
  route_table_id = aws_route_table.Security-Out-IGW_RT.id
  subnet_id = aws_subnet.security-Out-Pub-a.id
}

resource "aws_route_table_association" "security-Out-Pub-b_rt_asso" {
  route_table_id = aws_route_table.Security-Out-IGW_RT.id
  subnet_id = aws_subnet.security-Out-Pub-b.id
}

resource "aws_route" "Security-In-IGW_Default" {
  route_table_id = aws_route_table.Security-Out-IGW_RT.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}

////// Security-Out-TGW //////

resource "aws_route_table" "Security-Out-TGW_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-Out-TGW"
  }
}

resource "aws_route_table_association" "security-Out-TGW-a_rt_asso" {
  route_table_id = aws_route_table.Security-Out-TGW_RT.id
  subnet_id = aws_subnet.security-Out-TGW-a.id
}

resource "aws_route_table_association" "security-Out-TGW-b_rt_asso" {
  route_table_id = aws_route_table.Security-Out-TGW_RT.id
  subnet_id = aws_subnet.security-Out-TGW-b.id
}

////// Security-Out-Mgmt //////

resource "aws_route_table" "Security-Out-Mgmt_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-Out-Mgmt"
  }
}

resource "aws_route_table_association" "security-Out-Mgmt-a_rt_asso" {
  route_table_id = aws_route_table.Security-Out-Mgmt_RT.id
  subnet_id = aws_subnet.security-Out-Mgmt-a.id
}

resource "aws_route_table_association" "security-Out-Mgmt-b_rt_asso" {
  route_table_id = aws_route_table.Security-Out-Mgmt_RT.id
  subnet_id = aws_subnet.security-Out-Mgmt-b.id
}


/////////////
// FIREWALL
/////////////

// **** FW - Zone-A **** //

module "FW1_Out" {
  source = "../../firewall/"

  access_key = var.aws_key
  secret_key = var.secret_key

  fw_name = var.fw1_name
  aws_key = var.aws_key
  aws_region = var.aws_region
  fw_instance_type = var.fw_instance_type

  fw_license_type_map = var.fw_license_type_map
  ngfw_license_type = var.ngfw_license_type
  ngfw_version = var.ngfw_version

  mgmt_subnet_id = aws_subnet.security-Out-Mgmt-a.id
  mgmt_security_group_id = aws_security_group.management.id
  mgmtfwip = var.fw1_mgmt_ip

  untrust_subnet_id = aws_subnet.security-Out-Pub-a.id
  untrust_security_group_id = aws_security_group.allow_all.id
  untrustfwip = var.fw1_untrust_ip

//  trust_subnet_id = "${aws_subnet.security-Out-TGW-a.id}"         // Internal Subnet Interface
//  trust_security_group_id = "${aws_security_group.allow_all.id}"
//  trustfwip = "${var.fw1_trust_ip}"

  bootstrap_s3bucket_id = var.bootstrap_s3bucket_id
  bootstrap_role_name = var.bootstrap_role_name
  bootstrap_s3bucket_name = var.bootstrap_s3bucket_name

  xml_key = "security-out/fw1/config/bootstrap.xml"
  xml_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw1/config/bootstrap.xml"

  init_cfg_key = "security-out/fw1/config/init-cfg.txt"
  init_cfg_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw1/config/init-cfg.txt"

  license_key = "security-out/fw1/license/"
  license_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw1/license/authcodes"

  software_key = "security-out/fw1/software/"
  content_key = "security-out/fw1/content/"
}

// **** FW - Zone-B **** //

module "FW2_Out" {
  source = "../../firewall/"

  access_key = var.aws_key
  secret_key = var.secret_key

  fw_name = var.fw2_name
  aws_key = var.aws_key
  aws_region = var.aws_region
  fw_instance_type = var.fw_instance_type

  fw_license_type_map = var.fw_license_type_map
  ngfw_license_type = var.ngfw_license_type
  ngfw_version = var.ngfw_version

  mgmt_subnet_id = aws_subnet.security-Out-Mgmt-b.id
  mgmt_security_group_id = aws_security_group.management.id
  mgmtfwip = var.fw2_mgmt_ip

  untrust_subnet_id = aws_subnet.security-Out-Pub-b.id
  untrust_security_group_id = aws_security_group.allow_all.id
  untrustfwip = var.fw2_untrust_ip

//  trust_subnet_id = "${aws_subnet.security-Out-TGW-b.id}"         // Internal Subnet Interface
//  trust_security_group_id = "${aws_security_group.allow_all.id}"
//  trustfwip = "${var.fw2_trust_ip}"

  bootstrap_s3bucket_id = var.bootstrap_s3bucket_id
  bootstrap_role_name = var.bootstrap_role_name
  bootstrap_s3bucket_name = var.bootstrap_s3bucket_name

  xml_key = "security-out/fw2/config/bootstrap.xml"
  xml_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw2/config/bootstrap.xml"

  init_cfg_key = "security-out/fw2/config/init-cfg.txt"
  init_cfg_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw2/config/init-cfg.txt"

  license_key = "security-out/fw2/license/"
  license_source = "../../modules/firewall/bootstrap/bootstrap_files/security-out/fw2/license/init-cfg.txt"

  software_key = "security-out/fw2/software/"
  content_key = "security-out/fw2/content/"
}
