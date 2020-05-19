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


/////////////
// SUBNETS
/////////////


// Availability Zone - A //

resource "aws_subnet" "spoke1-web-a" {
  cidr_block = var.spoke1-web-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_spoke1-web-a"
  }
}

// Availability Zone - B //

resource "aws_subnet" "spoke1-web-b" {
  cidr_block = var.spoke1-web-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_spoke1-web-b"
  }
}


//////////////////
// ROUTE TABLE
//////////////////


resource "aws_route_table" "Spoke1_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Spoke1"
  }
}

resource "aws_route_table_association" "spoke1-web-a_rt_asso" {
  route_table_id = aws_route_table.Spoke1_RT.id
  subnet_id = aws_subnet.spoke1-web-a.id
}

resource "aws_route_table_association" "spoke1-web-b_rt_asso" {
  route_table_id = aws_route_table.Spoke1_RT.id
  subnet_id = aws_subnet.spoke1-web-b.id
}


///////////////////
// SECURITY GROUPS
///////////////////


// ****** Web Server SG ******

resource "aws_security_group" "web_server_sg" {
  name = "${var.vpc_name}_web_server_sg"
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.vpc_name}_web_server_sg"
  }
}

resource "aws_security_group_rule" "web_server_80" {
  type = "ingress"
  security_group_id = aws_security_group.web_server_sg.id

  from_port = 80
  to_port = 80
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "web_server_443" {
  type = "ingress"
  security_group_id = aws_security_group.web_server_sg.id

  from_port = 443
  to_port = 443
  protocol = "tcp"
  cidr_blocks = ["10.0.0.0/8", "172.16.0.0/16"]
}

resource "aws_security_group_rule" "web_server_22" {
  type = "ingress"
  security_group_id = aws_security_group.web_server_sg.id

  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["10.0.0.0/8", "172.16.0.0/16"]
}

resource "aws_security_group_rule" "web_server_icmp" {
  type = "ingress"
  security_group_id = aws_security_group.web_server_sg.id

  from_port = -1
  to_port = -1
  protocol = "icmp"
  cidr_blocks = ["10.0.0.0/8"]
}

resource "aws_security_group_rule" "web_server_outbound" {
  type = "egress"
  security_group_id = aws_security_group.web_server_sg.id

  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["10.0.0.0/8"]
}


/////////////////
// Web Instances
/////////////////


module "web_server1" {
  source = "../../../modules/web-server"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name = var.key_name
  vpc_name = var.vpc_name

  spoke1_subnet_id = aws_subnet.spoke1-web-a.id
  spoke1_security_group_id = aws_security_group.web_server_sg.id

  web_availability_zone = data.aws_availability_zones.available.names[0]
  web_private_ip = var.web1_private_ip
}

module "web_server2" {
  source = "../../../modules/web-server"

  access_key = var.access_key
  secret_key = var.secret_key

  aws_region = var.aws_region
  key_name = var.key_name
  vpc_name = var.vpc_name

  spoke1_subnet_id = aws_subnet.spoke1-web-b.id
  spoke1_security_group_id = aws_security_group.web_server_sg.id

  web_availability_zone = data.aws_availability_zones.available.names[1]
  web_private_ip = var.web2_private_ip
}


///////////////////////////////
// Application Load Balancer
///////////////////////////////


module "app_lb" {
  source = "../../../modules/load-balancer/application"

  aws_region = var.aws_region
  vpc_id = aws_vpc.vpc.id
  vpc_name = var.vpc_name

  lb_internal = "true"
  lb_access_log_bucket = var.lb_access_log_bucket

  security_group_id = aws_security_group.web_server_sg.id
  subnet_a_id = aws_subnet.spoke1-web-a.id
  subnet_b_id = aws_subnet.spoke1-web-b.id

  instance1_ip = var.web1_private_ip
  instance2_ip = var.web2_private_ip
}


////////
// IGW - NN
////////


//resource "aws_internet_gateway" "igw" {
//  vpc_id = "${aws_vpc.vpc.id}"
//
//  tags = {
//    Name = "${var.vpc_name}_igw"
//  }
//}


////////
// EIP
////////


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
