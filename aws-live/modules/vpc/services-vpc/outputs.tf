////////
// VPC
////////


output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "vpc_cidr_block" {
  value = var.vpc_cidr
}


/////////////
// SUBNETS
/////////////


output "Services-a_id" {
  value = aws_subnet.Services-a.id
}

output "Services-b_id" {
  value = aws_subnet.Services-b.id
}


////////////////
// ROUTE TABLE
////////////////


output "Services_RT_id" {
  value = aws_route_table.Services_RT.id
}


///////////////
// Ubuntu EIP
///////////////


output "services_ubuntu_ip" {
  value = aws_eip.mgmt_eip
}
