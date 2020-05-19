////////////
// PROVIDER
////////////


provider "panos" {}

provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


/////////////////////////
// PANORAMA DATA SOURCE
/////////////////////////


data "aws_ami" "panorama" {
  most_recent = true
  owners = ["aws-marketplace"]

  filter {
    name   = "product-code"
    values = [
      var.panorama_license_type_map[var.panorama_license_type]]
  }

  filter {
    name   = "name"
    values = ["Panorama-AWS-${var.panorama_version}*"]
  }
}


///////////////////////////
// DATA SOURCE DEFINITIONS
///////////////////////////


data "aws_availability_zones" "available" {
  state = "available"
}


///////////////////
// SECURITY GROUP
///////////////////


//// Panorama Management SG ////


resource "aws_security_group" "panorama_management" {
	name = "${var.services-Vpc-Name}_panorama_mgmt_sg"
	vpc_id = var.services_vpc_id

	tags = {
		Name = "${var.services-Vpc-Name}_panorama_mgmt_sg"
	}
}

resource "aws_security_group_rule" "panorama_management_3978" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 3978
	to_port = 3978
	protocol = "tcp"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_28443" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 28443
	to_port = 28443
	protocol = "tcp"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_123" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 123
	to_port = 123
	protocol = "tcp"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_22" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 22
	to_port = 22
	protocol = "tcp"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_443" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 443
	to_port = 443
	protocol = "-1"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_icmp" {
	type = "ingress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = -1
	to_port = -1
	protocol = "icmp"
	cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "panorama_management_outbound" {
	type = "egress"
	security_group_id = aws_security_group.panorama_management.id

	from_port = 0
	to_port = 65535
	protocol = "-1"
	cidr_blocks = ["0.0.0.0/0"]
}


////////////////////////
// PANORAMA INTERFACES
////////////////////////


resource "aws_network_interface" "mgmt_eni" {
  subnet_id         = var.panorama_mgmt_subnet_id
  private_ips       = [var.mgmtpanoramaip]
  security_groups   = [aws_security_group.panorama_management.id]
  source_dest_check = true

  tags = {
    Name = "${var.panorama_name}_mgmt_eni"
  }
}


//////////////////////
// PANORAMA INSTANCE
//////////////////////


resource "aws_instance" "panorama_instance" {
  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "stop"

  availability_zone = data.aws_availability_zones.available.names[0]

  ebs_optimized = true
  ami           = data.aws_ami.panorama.image_id
  instance_type = var.panorama_instance_type
  key_name      = var.panorama_aws_key

  monitoring = false

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.mgmt_eni.id
  }

  tags = {
    Name = var.panorama_name
  }
}


////////
// EIP
////////


resource "aws_eip" "mgmt_eip" {
	vpc               = true
	network_interface = aws_network_interface.mgmt_eni.id

	tags = {
		Name = "panorama_mgmt_eip"
	}
}