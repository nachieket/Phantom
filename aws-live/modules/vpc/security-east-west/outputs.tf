////////
// VPC
////////


output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "vpc_cidr_block" {
  value = "${var.vpc_cidr}"
}


////////////
// SUBNETS
////////////

output "security-East-West-TGW-a_id" {
  value = "${aws_subnet.security-East-West-TGW-a.id}"
}

output "security-East-West-TGW-b_id" {
  value = "${aws_subnet.security-East-West-TGW-b.id}"
}


////////////////
// ROUTE TABLE
////////////////


output "Security-East-West-Mgmt_RT_id" {
  value = "${aws_route_table.Security-East-West-Mgmt_RT.id}"
}


////////
// EIP
////////


output "sec_east_west_fw1_vpn_ip" {
  value = "${module.FW1_EW.untrust_vpn_ip}"
}

output "sec_east_west_fw2_vpn_ip" {
  value = "${module.FW2_EW.untrust_vpn_ip}"
}
