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


/////////////
// SUBNETS
/////////////


// Availability Zone - A //

resource "aws_subnet" "spoke2-db-a" {
  cidr_block = var.spoke2-db-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_spoke2-db-a"
  }
}

// Availability Zone - B //

resource "aws_subnet" "spoke2-db-b" {
  cidr_block = var.spoke2-db-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_spoke2-db-b"
  }
}


//////////////////
// ROUTE TABLE
//////////////////


resource "aws_route_table" "Spoke2_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Spoke2"
  }
}

resource "aws_route_table_association" "spoke2-web-a_rt_asso" {
  route_table_id = aws_route_table.Spoke2_RT.id
  subnet_id = aws_subnet.spoke2-db-a.id
}

resource "aws_route_table_association" "spoke2-web-b_rt_asso" {
  route_table_id = aws_route_table.Spoke2_RT.id
  subnet_id = aws_subnet.spoke2-db-b.id
}


///////////////////
// SECURITY GROUPS
///////////////////


resource "aws_security_group" "allow_all_sg" {
  name = "${var.vpc_name}_allow_all_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_allow_all"
  }
}

resource "aws_security_group_rule" "vpc_allow_all_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.allow_all_sg.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "vpc_allow_all_outbound" {
  type = "egress"
  security_group_id = aws_security_group.allow_all_sg.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}


///////////////////
// Ubuntu Server1
///////////////////


module "ssh_server1" {
  source = "../../ubuntu-ssh"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name = var.key_name
  vpc_name = var.vpc_name

  spoke2_subnet_id = aws_subnet.spoke2-db-a.id
  spoke2_security_group_id = aws_security_group.allow_all_sg.id

  ssh_availability_zone = data.aws_availability_zones.available.names[0]
  ssh_private_ip = var.ssh1_private_ip
}

module "ssh_server2" {
  source = "../../ubuntu-ssh"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name = var.key_name
  vpc_name = var.vpc_name

  spoke2_subnet_id = aws_subnet.spoke2-db-b.id
  spoke2_security_group_id = aws_security_group.allow_all_sg.id

  ssh_availability_zone = data.aws_availability_zones.available.names[1]
  ssh_private_ip = var.ssh2_private_ip
}


//////////
//// IGW - NN
//////////
//
//
//resource "aws_internet_gateway" "igw" {
//  vpc_id = "${aws_vpc.vpc.id}"
//
//  tags = {
//    Name = "${var.vpc_name}_igw"
//  }
//}
//
//
//////////
//// EIP
//////////
//
//
//resource "aws_eip" "eth0_eip" {
//  vpc = true
//
//  instance = "${aws_instance.vpc_instance.id}"
//  network_interface = "${aws_network_interface.eth0.id}"
//  associate_with_private_ip = "${var.ubuntu_private_ip1}"
//
//  tags = {
//    Name = "${var.vpc_name}_ubuntu_eth0_eip"
//  }
//}
