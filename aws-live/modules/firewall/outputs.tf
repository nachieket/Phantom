/////////
// NGFW
/////////


output "ngfw_instance_id" {
  value = "${aws_instance.ngfw_instance.id}"
}

output "untrust_eni_id" {
  value = "${aws_network_interface.untrust_eni.id}"
}


////////
// EIP
////////


output "untrust_vpn_ip" {
  value = "${aws_eip.untrust_eip.public_ip}"
}

output "mgmt_public_ip" {
  value = "${aws_eip.mgmt_eip.public_ip}"
}
