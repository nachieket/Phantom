////////////
// PROVIDER
////////////


provider "panos" {}

provider "aws" {
  region = "eu-west-2"
  access_key = var.access_key
  secret_key = var.secret_key
}


////////////////
// DATA SOURCES
////////////////


data "aws_ami" "ngfw" {
  most_recent = true
  owners = ["aws-marketplace"]
  
  filter {
    name   = "owner-alias"
    values = ["aws-marketplace"]
  }

  filter {
    name   = "product-code"
    values = [
      var.fw_license_type_map[var.ngfw_license_type]]
  }

  filter {
    name   = "name"
    values = ["PA-VM-AWS-${var.ngfw_version}*"]
  }
}

data "aws_region" "region" {
  name = var.aws_region
}


//////////////////
// FW INTERFACES
//////////////////


resource "aws_network_interface" "mgmt_eni" {
  subnet_id         = var.mgmt_subnet_id
  private_ips       = [
    var.mgmtfwip]
  security_groups   = [
    var.mgmt_security_group_id]
  source_dest_check = true

  tags = {
    Name = "${var.fw_name}_mgmt_eni"
  }
}

//resource "aws_network_interface" "trust_eni" {
//  subnet_id         = "${var.trust_subnet_id}"
//  private_ips       = ["${var.trustfwip}"]
//  security_groups   = ["${var.trust_security_group_id}"]
//  source_dest_check = false
//
//  tags = {
//    Name = "${var.fw_name}_trust_eni"
//  }
//}

resource "aws_network_interface" "untrust_eni" {
  subnet_id         = var.untrust_subnet_id
  private_ips       = [
    var.untrustfwip]
  security_groups   = [
    var.untrust_security_group_id]
  source_dest_check = false

  tags = {
    Name = "${var.fw_name}_untrust_eni"
  }
}


////////
// EIP
////////


resource "aws_eip" "mgmt_eip" {
  vpc               = true
  network_interface = aws_network_interface.mgmt_eni.id

  tags = {
    Name = "${var.fw_name}_mgmt_eip"
  }
}

resource "aws_eip" "untrust_eip" {
  vpc               = true
  network_interface = aws_network_interface.untrust_eni.id

  tags = {
    Name = "${var.fw_name}_untrust_eip"
  }
}


////////////////
// FW INSTANCE
////////////////


resource "aws_instance" "ngfw_instance" {
  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "stop"
  iam_instance_profile                 = module.bootstrap.bootstrap_profile_id
  user_data                            = base64encode(join("", list("vmseries-bootstrap-aws-s3bucket=", var.bootstrap_s3bucket_name)))

  ebs_optimized = true
  ami           = data.aws_ami.ngfw.image_id
  instance_type = var.fw_instance_type
  key_name      = var.aws_key

  monitoring = false

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.untrust_eni.id
  }

  network_interface {
    device_index         = 1
    network_interface_id = aws_network_interface.mgmt_eni.id
  }

//  network_interface {
//    device_index         = 2
//    network_interface_id = "${aws_network_interface.trust_eni.id}"
//  }

  tags = {
    Name = var.fw_name
  }
}


//////////////
// Bootstrap
//////////////


module "bootstrap" {
  source = "./bootstrap/"

  bootstrap_s3bucket_id = var.bootstrap_s3bucket_id
  bootstrap_role_name = var.bootstrap_role_name

  fw_name = var.fw_name

  xml_key = var.xml_key
  xml_source = var.xml_source

  init_cfg_key = var.init_cfg_key
  init_cfg_source = var.init_cfg_source

  license_key = var.license_key

  software_key = var.software_key

  content_key = var.content_key
  license_source = var.license_source
}
