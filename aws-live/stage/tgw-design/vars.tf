
/////////////////
// GENERIC MAPS
/////////////////


variable "panorama_license_type_map" {
	default = {
		"byol" = "eclz7j04vu9lf8ont8ta3n17o",
	}
}

variable "fw_license_type_map" {			
	default = {
		"byol"  = "6njl1pau431dv1qxipg63mvah"
		"payg1" = "6kxdw3bbmdeda3o6i1ggqt4km"
		"payg2" = "806j2of0qy5osgjjixq9gqc6g"
	}
}


/////////////
// Provider
/////////////


variable "access_key" {
	default = "AKIAVFK6UURB6VTP6LOJ"
}

variable "secret_key" {
	default = "Zo3u7dchqBg6hoZg2jRp0JmeilFvWlbBCc5HVCQN"
}

variable "aws_region" {
	default = "eu-west-2"
}


variable "aws_key" {
	default = "pyty"
}


//////////////
// S3 BUCKET
//////////////


variable "s3_bucket" {
	default = "aws-transit-gateway-s3-bucket-nj-241219"
}


/////////////////
// Services VPC
/////////////////


variable "services-Vpc-Name" {
	default = "Services"
}

variable "services-Vpc-cidr" {
	default = "10.3.0.0/16"
}

variable "Services-a" {
	default = "10.3.1.0/24"
}

variable "Services-b" {
	default = "10.3.2.0/24"
}

variable "js_services_private_ip" {
	default = "10.3.1.110"
}

variable "ubuntu_aws_key" {
	default = "pyty"
}


/////////////
// Panorama
///////////// 


variable "panorama_version" {
	default = "9.0.3"
}

variable "panorama_license_type" {
	default = "byol"
}

variable "panorama_instance_type" {
	default = "m4.2xlarge"
}

variable "mgmtpanoramaip" {
	default = "10.3.1.100"
}

variable "panorama_name" {
	default = "PANW-Panorama"
}

variable "panorama_aws_key" {
	default = "pyty"
}

