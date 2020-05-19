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


output "security-Out-TGW-a_id" {
  value = "${aws_subnet.security-Out-TGW-a.id}"
}

output "security-Out-TGW-b_id" {
  value = "${aws_subnet.security-Out-TGW-b.id}"
}


////////////////
// ROUTE TABLE
////////////////


output "Security-Out-Mgmt_RT_id" {
  value = "${aws_route_table.Security-Out-Mgmt_RT.id}"
}


////////
// EIP
////////


output "sec_out_fw1_vpn_ip" {
  value = "${module.FW1_Out.untrust_vpn_ip}"
}

output "sec_out_fw2_vpn_ip" {
  value = "${module.FW2_Out.untrust_vpn_ip}"
}
