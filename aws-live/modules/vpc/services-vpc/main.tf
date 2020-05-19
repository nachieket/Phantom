///////////////////////
// PROVIDER DEFINITION
///////////////////////


provider "aws" {
  region = "eu-west-2"
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


//////////////////////////////
// SECURITY GROUP DEFINITIONS
//////////////////////////////


////// Allow All SG //////


resource "aws_security_group" "allow_all" {
  name = "${var.vpc_name}_allow_all_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_allow_all_sg"
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


////// Ubuntu Management SG //////


resource "aws_security_group" "ubuntu_management" {
  name = "${var.vpc_name}_mgmt_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_ssh_mgmt_sg"
  }
}

resource "aws_security_group_rule" "ubuntu_management_22" {
  type = "ingress"
  security_group_id = aws_security_group.ubuntu_management.id

  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "ubuntu_management_outbound" {
  type = "egress"
  security_group_id = aws_security_group.ubuntu_management.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}


//////////////////////
// SUBNET DEFINITIONS
//////////////////////


// Availability Zone - A //

resource "aws_subnet" "Services-a" {
  cidr_block = var.Services-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}-a"
  }
}

// Availability Zone - B //

resource "aws_subnet" "Services-b" {
  cidr_block = var.Services-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}-b"
  }
}


//////////////////
// IGW DEFINITION
//////////////////


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_igw"
  }
}


////////////////
// ROUTE TABLE
////////////////

////// Services //////

resource "aws_route_table" "Services_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Services"
  }
}

resource "aws_route_table_association" "services-Pub-a_rt_asso" {
  route_table_id = aws_route_table.Services_RT.id
  subnet_id = aws_subnet.Services-a.id
}

resource "aws_route_table_association" "services-Pub-b_rt_asso" {
  route_table_id = aws_route_table.Services_RT.id
  subnet_id = aws_subnet.Services-b.id
}

resource "aws_route" "Security-In-IGW_Default" {
  route_table_id = aws_route_table.Services_RT.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}


//////////////////
// UBUNTU MODULE
//////////////////


module "ubuntu-ssh" {
  source = "../../ubuntu-ssh"

  access_key = var.access_key
  secret_key = var.secret_key
  aws_region = var.aws_region
  ubuntu_aws_key = var.ubuntu_aws_key

  vpc_name = var.vpc_name

  vpc_security_group_id = aws_security_group.ubuntu_management.id
  vpc_subnet_id = aws_subnet.Services-a.id

  ssh_availability_zone = data.aws_availability_zones.available.names[0]
  ssh_private_ip = var.ssh_private_ip
}


////////
// EIP
////////


resource "aws_eip" "mgmt_eip" {
  vpc               = true
  network_interface = module.ubuntu-ssh.ubuntu_mgmt_int_id

  tags = {
    Name = "jump_station_mgmt_eip"
  }
}
