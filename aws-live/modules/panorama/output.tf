output "panorama_mgmt_eni_id" {
  value = aws_network_interface.mgmt_eni.id
}

output "panorama_mgmt_eip" {
  value = aws_eip.mgmt_eip
}
