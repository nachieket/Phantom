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


output "spoke2-web-a_id" {
  value = "${aws_subnet.spoke2-db-b.id}"
}

output "spoke2-web-b_id" {
  value = "${aws_subnet.spoke2-db-b.id}"
}


////////////////
// ROUTE TABLE
////////////////

output "Spoke2_RT_id" {
  value = "${aws_route_table.Spoke2_RT.id}"
}
