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


////// Availability Zone - A //////

resource "aws_subnet" "security-In-Mgmt-a" {
  cidr_block = var.security-In-Mgmt-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-In-Mgmt-a"
  }
}

resource "aws_subnet" "security-In-TGW-a" {
  cidr_block = var.security-In-TGW-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-In-TGW-a"
  }
}

resource "aws_subnet" "security-In-Pub-a" {
  cidr_block = var.security-In-Pub-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-In-Pub-a"
  }
}

resource "aws_subnet" "security-In-Priv-a" {
  cidr_block = var.security-In-Priv-a
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.vpc_name}_security-In-Priv-a"
  }
}

////// Availability Zone - B //////

resource "aws_subnet" "security-In-Mgmt-b" {
  cidr_block = var.security-In-Mgmt-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-In-Mgmt-b"
  }
}

resource "aws_subnet" "security-In-TGW-b" {
  cidr_block = var.security-In-TGW-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-In-TGW-b"
  }
}

resource "aws_subnet" "security-In-Pub-b" {
  cidr_block = var.security-In-Pub-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-In-Pub-b"
  }
}

resource "aws_subnet" "security-In-Priv-b" {
  cidr_block = var.security-In-Priv-b
  vpc_id = aws_vpc.vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.vpc_name}_security-In-Priv-b"
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

////// Security-In-IGW //////

resource "aws_route_table" "Security-In-IGW_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-In-IGW"
  }
}

resource "aws_route_table_association" "security-In-Pub-a_rt_asso" {
  route_table_id = aws_route_table.Security-In-IGW_RT.id
  subnet_id = aws_subnet.security-In-Pub-a.id
}

resource "aws_route_table_association" "security-In-Pub-b_rt_asso" {
  route_table_id = aws_route_table.Security-In-IGW_RT.id
  subnet_id = aws_subnet.security-In-Pub-b.id
}

resource "aws_route" "Security-In-IGW_Default" {
  route_table_id = aws_route_table.Security-In-IGW_RT.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}

////// Security-In-TGW //////

resource "aws_route_table" "Security-In-TGW_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-In-TGW"
  }
}

resource "aws_route_table_association" "security-In-TGW-a_rt_asso" {
  route_table_id = aws_route_table.Security-In-TGW_RT.id
  subnet_id = aws_subnet.security-In-TGW-a.id
}

resource "aws_route_table_association" "security-In-TGW-b_rt_asso" {
  route_table_id = aws_route_table.Security-In-TGW_RT.id
  subnet_id = aws_subnet.security-In-TGW-b.id
}

////// Security-In-Priv //////

resource "aws_route_table" "Security-In-Priv_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-In-Priv"
  }
}

resource "aws_route_table_association" "security-In-Priv-a_rt_asso" {
  route_table_id = aws_route_table.Security-In-Priv_RT.id
  subnet_id = aws_subnet.security-In-Priv-a.id
}

resource "aws_route_table_association" "security-In-Priv-b_rt_asso" {
  route_table_id = aws_route_table.Security-In-Priv_RT.id
  subnet_id = aws_subnet.security-In-Priv-b.id
}

////// Security-In-Mgmt //////

resource "aws_route_table" "Security-In-Mgmt_RT" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "Security-In-Mgmt"
  }
}

resource "aws_route_table_association" "security-In-Mgmt-a_rt_asso" {
  route_table_id = aws_route_table.Security-In-Mgmt_RT.id
  subnet_id = aws_subnet.security-In-Mgmt-a.id
}

resource "aws_route_table_association" "security-In-Mgmt-b_rt_asso" {
  route_table_id = aws_route_table.Security-In-Mgmt_RT.id
  subnet_id = aws_subnet.security-In-Mgmt-b.id
}


/////////////
// FIREWALL
/////////////

// **** FW - Zone-A **** //

module "FW1_In" {
  source = "../../firewall/"

  access_key = var.access_key
  secret_key = var.secret_key

  fw_name = var.fw1_name
  aws_key = var.aws_key
  aws_region = var.aws_region
  fw_instance_type = var.fw_instance_type

  fw_license_type_map = var.fw_license_type_map

  ngfw_license_type = var.ngfw_license_type
  ngfw_version = var.ngfw_version

  mgmt_subnet_id = aws_subnet.security-In-Mgmt-a.id
  mgmt_security_group_id = aws_security_group.management.id
  mgmtfwip = var.fw1_mgmt_ip

  untrust_subnet_id = aws_subnet.security-In-Pub-a.id
  untrust_security_group_id = aws_security_group.allow_all.id
  untrustfwip = var.fw1_untrust_ip

//  trust_subnet_id = "${aws_subnet.security-In-Priv-a.id}"
//  trust_security_group_id = "${aws_security_group.allow_all.id}"
//  trustfwip = "${var.fw1_trust_ip}"

  bootstrap_s3bucket_id = var.bootstrap_s3bucket_id
  bootstrap_role_name = var.bootstrap_role_name
  bootstrap_s3bucket_name = var.bootstrap_s3bucket_name

  xml_key = "security-in/fw1/config/bootstrap.xml"
  xml_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw1/config/bootstrap.xml"

  init_cfg_key = "security-in/fw1/config/init-cfg.txt"
  init_cfg_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw1/config/init-cfg.txt"

  license_key = "security-in/fw1/license/"
  license_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw1/license/authcodes"

  software_key = "security-in/fw1/software/"
  content_key = "security-in/fw1/content/"
}

// **** Trust Interface for Security-In Firewall **** //

resource "aws_network_interface" "fw1_trust_eni" {
  subnet_id         = aws_subnet.security-In-Priv-a.id
  private_ips       = [
    var.fw1_trust_ip]
  security_groups   = [
    aws_security_group.allow_all.id]
  source_dest_check = false

  tags = {
    Name = "${var.fw1_name}_trust_eni"
  }
}

resource "aws_network_interface_attachment" "fw1_trust_attach" {
  device_index = 2
  instance_id = module.FW1_In.ngfw_instance_id
  network_interface_id = aws_network_interface.fw1_trust_eni.id
}

// **** FW - Zone-B **** //

module "FW2_In" {
  source = "../../firewall/"

  access_key = var.access_key
  secret_key = var.secret_key

  fw_name = var.fw2_name
  aws_key = var.aws_key
  aws_region = var.aws_region
  fw_instance_type = var.fw_instance_type

  ngfw_license_type = var.ngfw_license_type
  ngfw_version = var.ngfw_version
  fw_license_type_map = var.fw_license_type_map

  mgmt_subnet_id = aws_subnet.security-In-Mgmt-b.id
  mgmt_security_group_id = aws_security_group.management.id
  mgmtfwip = var.fw2_mgmt_ip

  untrust_subnet_id = aws_subnet.security-In-Pub-b.id
  untrust_security_group_id = aws_security_group.allow_all.id
  untrustfwip = var.fw2_untrust_ip

//  trust_subnet_id = "${aws_subnet.security-In-Priv-b.id}"
//  trust_security_group_id = "${aws_security_group.allow_all.id}"
//  trustfwip = "${var.fw2_trust_ip}"

  bootstrap_s3bucket_id = var.bootstrap_s3bucket_id
  bootstrap_role_name = var.bootstrap_role_name
  bootstrap_s3bucket_name = var.bootstrap_s3bucket_name

  xml_key = "security-in/fw2/config/fw2/bootstrap.xml"
  xml_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw2/bootstrap.xml"

  init_cfg_key = "security-in/fw2/config/fw2/init-cfg.txt"
  init_cfg_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw2/init-cfg.txt"

  license_key = "security-in/fw2/fw2/license/"
  license_source = "../../modules/firewall/bootstrap/bootstrap_files/security-in/fw2/license/authcodes"

  software_key = "security-in/fw2/software/"
  content_key = "security-in/fw2/content/"
}

// **** Trust Interface for Security-In Firewall **** //

resource "aws_network_interface" "fw2_trust_eni" {
  subnet_id         = aws_subnet.security-In-Priv-b.id
  private_ips       = [
    var.fw2_trust_ip]
  security_groups   = [
    aws_security_group.allow_all.id]
  source_dest_check = false

  tags = {
    Name = "${var.fw2_name}_trust_eni"
  }
}

resource "aws_network_interface_attachment" "fw2_trust_attach" {
  device_index = 2
  instance_id = module.FW2_In.ngfw_instance_id
  network_interface_id = aws_network_interface.fw2_trust_eni.id
}


//////////////////////////////
// Application Load Balancer
//////////////////////////////


module "app_lb" {
  source = "../../../modules/load-balancer/application"

  aws_region = var.aws_region
  vpc_id = aws_vpc.vpc.id
  vpc_name = var.vpc_name

  lb_internal = "false"
  lb_access_log_bucket = var.lb_access_log_bucket

  security_group_id = aws_security_group.allow_all.id
  subnet_a_id = aws_subnet.security-In-Pub-a.id
  subnet_b_id = aws_subnet.security-In-Pub-b.id

  instance1_ip = var.fw1_untrust_ip
  instance2_ip = var.fw2_untrust_ip
}


//depends_on = [
//    "aws_vpc.vpc",
//  ]



//////////////////////////////////
//// Application Load Balancer
//////////////////////////////////
//
//
//
//
//
//resource "aws_lb" "app_lb" {
//  name = "security-In-App-LB"
//
//  vpc_id = "${aws_vpc.vpc.id}"
//
//  internal = false
//  load_balancer_type = "application"
//  security_groups = ["${aws_security_group.allow_all.id}"]
//  subnets = ["${aws_subnet.security-In-Pub-a.id}", "${aws_subnet.security-In-Pub-b.id}"]
//
//  enable_deletion_protection = false
//  enable_cross_zone_load_balancing = true
//
//  access_logs {
//    bucket = "aws-s3-bucket-application-lb-281019172330"
//    prefix = "app-lb"
//    enabled = false
//  }
//
//  tags = {
//    Environment = "production"
//    Name = "security-In-App-LB"
//  }
//}
//
//resource "aws_lb_target_group" "http_tg" {
//  name        = "http-Target-Group"
//  port        = 80
//  protocol    = "HTTP"
//  target_type = "ip"
//  vpc_id      = "${aws_vpc.vpc.id}"
//
//  health_check {
//    port = "traffic-port"
//    healthy_threshold = "5"
//    unhealthy_threshold = "2"
//    timeout = "3"
//    interval = "5"
//    matcher = "200"
//  }
//}
//
//resource "aws_lb_target_group_attachment" "fw1_http_tg_attach" {
//  target_group_arn = "${aws_lb_target_group.http_tg.arn}"
//  target_id        = "${var.fw1_untrust_ip}"
//  port             = 80
//}
//
//resource "aws_lb_target_group_attachment" "fw2_http_tg_attach" {
//  target_group_arn = "${aws_lb_target_group.http_tg.arn}"
//  target_id        = "${var.fw2_untrust_ip}"
//  port             = 80
//}
//
//resource "aws_lb_listener" "http_listener" {
//  load_balancer_arn = "${aws_lb.app_lb.arn}"
//  port = 80
//  protocol = "HTTP"
//
//  default_action {
//    type = "forward"
//    target_group_arn = "${aws_lb_target_group.http_tg.arn}"
//  }
//}
//
//resource "aws_lb_listener_rule" "http_rule" {
//  listener_arn = "${aws_lb_listener.http_listener.arn}"
//  priority     = 100
//
//  action {
//    type             = "forward"
//    target_group_arn = "${aws_lb_target_group.http_tg.arn}"
//  }
//
//  condition {
//    field  = "path-pattern"
//    values = ["/"]
//  }
//}