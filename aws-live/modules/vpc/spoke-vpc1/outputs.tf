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


output "spoke1-web-a_id" {
  value = "${aws_subnet.spoke1-web-a.id}"
}

output "spoke1-web-b_id" {
  value = "${aws_subnet.spoke1-web-b.id}"
}


////////////////
// ROUTE TABLE
////////////////


output "Spoke1_RT_id" {
  value = "${aws_route_table.Spoke1_RT.id}"
}
