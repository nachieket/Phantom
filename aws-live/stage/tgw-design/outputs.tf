
output "services_ubuntu_public_ip" {
	value = module.services_vpc.services_ubuntu_ip.public_ip
}

output "panorama_mgmt_public_ip" {
	value = module.panorama.panorama_mgmt_eip.public_ip
}
