////////////////////////
// PROVIDER DEFINITION
////////////////////////


provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


////////////////////////
// SSH-Server Instance
// TODO: Change AMI ID to dynamic vriable in future if possible
////////////////////////


resource "aws_instance" "web_instance" {
  ami = "ami-b2b55cd5"
  instance_type = "t2.micro"

  availability_zone = var.ssh_availability_zone
  key_name = var.ubuntu_aws_key

  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.eth0.id
  }

  root_block_device {
    volume_type = "standard"
    volume_size = 10
  }

  tags = {
    Name = "${var.vpc_name}_ubuntu"
  }
}

// **** NETWORK INTERFACES **** //

resource "aws_network_interface" "eth0" {
  subnet_id       = var.vpc_subnet_id
  private_ips     = [var.ssh_private_ip]
  security_groups = [var.vpc_security_group_id]

  tags = {
    Name = "${var.vpc_name}_web_eth0"
  }
}

// Enable below if second interface is needed

//resource "aws_network_interface" "eth1" {
//  subnet_id       = "${aws_subnet.public_subnet.id}"
//  private_ips     = ["${var.ubuntu_private_ip2}"]
//  security_groups = ["${aws_security_group.allow_all_sg.id}"]
//
//  attachment {
//    instance     = "${aws_instance.vpc_instance.id}"
//    device_index = 1
//  }
//
//  tags = {
//    Name = "${var.vpc_name}_ubuntu_eth1"
//  }
//}