/////////////
// PROVIDER
/////////////


provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


///////////////////
// TRANSIT GATEWAY
///////////////////


resource "aws_ec2_transit_gateway" "transit_gateway" {
  description = "AWS Transit Gateway"

  amazon_side_asn = var.amazon_side_asn
  auto_accept_shared_attachments = "enable"
  default_route_table_association = "disable"
  default_route_table_propagation = "disable"
  dns_support = "enable"
  vpn_ecmp_support = "enable"

  tags = {
    Name = var.tgw_name
  }
}


////////////////////
// VPC Attachments
////////////////////


resource "aws_ec2_transit_gateway_vpc_attachment" "spoke_vpc1_attach" {
  subnet_ids         = [var.sub_spoke1-web-a_id, var.sub_spoke1-web-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.vpc1_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Spoke_VPC1_Attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "spoke_vpc2_attach" {
  subnet_ids         = [var.sub_spoke2-web-a_id, var.sub_spoke2-web-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.vpc2_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Spoke_VPC2_Attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "security_in_attach" {
  subnet_ids = [var.sub_security-In-TGW-a_id, var.sub_security-In-TGW-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.security_in_vpc_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Security_In_Attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "security_out_attach" {
  subnet_ids = [var.sub_security-Out-TGW-a_id, var.sub_security-Out-TGW-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.security_out_vpc_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Security_Out_Attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "security_east_west_attach" {
  subnet_ids = [var.sub_security-East-West-TGW-a_id, var.sub_security-East-West-TGW-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.security_east_west_vpc_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Security_East_West_Attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "services_attach" {
  subnet_ids = [var.sub_Services-a_id, var.sub_Services-b_id]
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
  vpc_id             = var.services_vpc_id
  transit_gateway_default_route_table_association = "false"
  transit_gateway_default_route_table_propagation = "false"

  tags = {
    Name = "Services_Attachment"
  }
}


////////////////////
// TGW Route Table
////////////////////


resource "aws_ec2_transit_gateway_route_table" "Security" {
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id

  tags = {
    Name = "TGW_Security_RT"
  }
}

resource "aws_ec2_transit_gateway_route_table" "Spokes" {
  transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id

  tags = {
    Name = "TGW_Spokes_RT"
  }
}

////// ROUTE TABLE ASSOCIATIONS //////

resource "aws_ec2_transit_gateway_route_table_association" "spoke_vpc1_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.spoke_vpc1_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Spokes.id
}

resource "aws_ec2_transit_gateway_route_table_association" "spoke_vpc2_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.spoke_vpc2_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Spokes.id
}

resource "aws_ec2_transit_gateway_route_table_association" "security_in_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.security_in_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}

resource "aws_ec2_transit_gateway_route_table_association" "security_out_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.security_out_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}

resource "aws_ec2_transit_gateway_route_table_association" "security_east_west_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.security_east_west_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}

resource "aws_ec2_transit_gateway_route_table_association" "services_asso" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.services_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}

////// ROUTE TABLE PROPOGATIONS //////

resource "aws_ec2_transit_gateway_route_table_propagation" "security_in_propo" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.security_in_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Spokes.id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "spoke_vpc1_propo" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.spoke_vpc1_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}

resource "aws_ec2_transit_gateway_route_table_propagation" "spoke_vpc2_propo" {
  transit_gateway_attachment_id = aws_ec2_transit_gateway_vpc_attachment.spoke_vpc2_attach.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.Security.id
}


///////////////
// TGW Routes
///////////////


//resource "aws_ec2_transit_gateway_route" "spoke_vpc1_route1" {
//  destination_cidr_block         = "${var.vpc1_cidr}"
//  transit_gateway_attachment_id  = "${aws_ec2_transit_gateway_vpc_attachment.spoke_vpc1_attach.id}"
//  transit_gateway_route_table_id = "${aws_ec2_transit_gateway_route_table.outbound_rt.id}"
//}
//
//resource "aws_ec2_transit_gateway_route" "spoke_vpc2_route1" {
//  destination_cidr_block         = "${var.vpc2_cidr}"
//  transit_gateway_attachment_id  = "${aws_ec2_transit_gateway_vpc_attachment.spoke_vpc2_attach.id}"
//  transit_gateway_route_table_id = "${aws_ec2_transit_gateway_route_table.outbound_rt.id}"
//}



///////////////////////
//// Spoke VPC1 Module
///////////////////////
//
//
//module "spoke_vpc1" {
//  source = "..\/architecture\/vpc\/spoke-vpc1"
//
//  vpc_name = "Spoke1"
//  vpc_cidr = "10.1.0.0/16"
//
//  spoke1-web-a = "10.1.1.0/24"
//  spoke1-web-b = "10.1.2.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "vpc1_tgw_route" {
//  route_table_id = "${module.spoke_vpc1.Spoke1_RT_id}"
//  destination_cidr_block = "0.0.0.0/0"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//
///////////////////////
//// Spoke VPC2 Module
///////////////////////
//
//
//module "spoke_vpc2" {
//  source = "../architecture/vpc/spoke-vpc2"
//
//  vpc_name = "Spoke2"
//  vpc_cidr = "10.2.0.0/16"
//
//  spoke2-db-a = "10.2.1.0/24"
//  spoke2-db-b = "10.2.2.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "vpc2_tgw_route" {
//  route_table_id = "${module.spoke_vpc2.Spoke2_RT_id}"
//  destination_cidr_block = "0.0.0.0/0"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//
/////////////////////////
//// Services VPC Module
/////////////////////////
//
//
//module "services" {
//  source = "../architecture/vpc/services-vpc"
//
//  vpc_name = "Services"
//  vpc_cidr = "10.3.0.0/16"
//
//  Services-a = "10.3.1.0/24"
//  Services-b = "10.3.2.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "services_tgw_route" {
//  route_table_id = "${module.services.Services_RT_id}"
//  destination_cidr_block = "10.0.0.0/8"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//
/////////////////////////////////
//// Security Inbound VPC Module
/////////////////////////////////
//
//
//module "security_in" {
//  source = "../architecture/vpc/security-in"
//
//  vpc_name = "Security-In"
//  vpc_cidr = "10.255.0.0/16"
//
//  security-In-Mgmt-a = "10.255.110.0/24"
//  security-In-TGW-a = "10.255.1.0/24"
//  security-In-Pub-a = "10.255.100.0/24"
//  security-In-Priv-a = "10.255.11.0/24"
//  security-In-Mgmt-b = "10.255.120.0/24"
//  security-In-TGW-b = "10.255.2.0/24"
//  security-In-Pub-b = "10.255.200.0/24"
//  security-In-Priv-b = "10.255.12.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "sec_in_route_10.0.0.0" {
//  route_table_id = "${module.security_in.Security-In-Priv_RT_id}"
//  destination_cidr_block = "10.0.0.0/8"                                   // TODO: Change Static Value
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//resource "aws_route" "sec_in_route_0.0.0.0" {
//  route_table_id = "${module.security_in.Security-In-Mgmt_RT_id}"
//  destination_cidr_block = "0.0.0.0/0"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//
//////////////////////////////////
//// Security Outbound VPC Module
//////////////////////////////////
//
//
//module "security_out" {
//  source = "../architecture/vpc/security-out"
//
//  vpc_name = "Security-Out"
//  vpc_cidr = "10.254.0.0/16"
//
//  security-Out-Mgmt-a = "10.254.110.0/24"
//  security-Out-TGW-a = "10.254.1.0/24"
//  security-Out-Pub-a = "10.254.100.0/24"
//  security-Out-Mgmt-b = "10.254.120.0/24"
//  security-Out-TGW-b = "10.254.2.0/24"
//  security-Out-Pub-b = "10.254.200.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "sec_out_route_0.0.0.0" {
//  route_table_id = "${module.security_out.Security-Out-Mgmt_RT_id}"
//  destination_cidr_block = "0.0.0.0/0"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}
//
//
///////////////////////////////////
//// East-West Security VPC Module
///////////////////////////////////
//
//
//module "security_east_west" {
//  source = "../architecture/vpc/security-east-west"
//
//  vpc_name = "Security-East-West"
//  vpc_cidr = "10.253.0.0/16"
//
//  security-East-West-Mgmt-a = "10.253.110.0/24"
//  security-East-West-TGW-a = "10.253.1.0/24"
//  security-East-West-Pub-a = "10.253.100.0/24"
//  security-East-West-Mgmt-b = "10.253.120.0/24"
//  security-East-West-TGW-b = "10.253.2.0/24"
//  security-East-West-Pub-b = "10.253.200.0/24"
//}
//
//////// ROUTES //////
//
//resource "aws_route" "east_west_route_0.0.0.0" {
//  route_table_id = "${module.security_east_west.Security-East-West-Mgmt_RT_id}"
//  destination_cidr_block = "0.0.0.0/0"
//  transit_gateway_id = "${aws_ec2_transit_gateway.transit_gateway.id}"
//}