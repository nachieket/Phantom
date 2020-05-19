////////
// VPC
////////

output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "vpc_cidr_block" {
  value = "${var.vpc_cidr}"
}

///////////
// SUBNETS
///////////

output "security-In-TGW-a_id" {
  value = "${aws_subnet.security-In-TGW-a.id}"
}

output "security-In-TGW-b_id" {
  value = "${aws_subnet.security-In-TGW-b.id}"
}

////////////////
// ROUTE TABLE
////////////////

output "Security-In-Priv_RT_id" {
  value = "${aws_route_table.Security-In-Priv_RT.id}"
}

output "Security-In-Mgmt_RT_id" {
  value = "${aws_route_table.Security-In-Mgmt_RT.id}"
}
