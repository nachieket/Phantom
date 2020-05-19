output "TGW_Security_RT_id" {
  value = "${aws_ec2_transit_gateway_route_table.Security.id}"
}

output "TGW_Spokes_RT_id" {
  value = "${aws_ec2_transit_gateway_route_table.Spokes.id}"
}

output "tgw_id" {
  value = "${aws_ec2_transit_gateway.transit_gateway.id}"
}
