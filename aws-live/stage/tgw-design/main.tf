
/////////////
// PROVIDER
/////////////


provider "aws" {
	region     = var.aws_region
	access_key = var.access_key
	secret_key = var.secret_key
}


////////////
// BACKEND
////////////


terraform {
	backend "s3" {
		bucket     = "aws-transit-gateway-s3-bucket-nj-241219"
		key        = "stage/transit-gateway/terraform.tfstate"
		region     = "eu-west-2"
		encrypt    = true
		access_key = "AKIAVFK6UURB6VTP6LOJ"
		secret_key = "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"
	}
}


/////////////
// IAM Role
/////////////


resource "aws_iam_role" "bootstrap_role" {
	name = "ngfw_bootstrap_role"

	assume_role_policy = <<EOF
{
	"Version": "2012-10-17",
	"Statement": [
	{
		"Effect": "Allow",
		"Principal": {
		"Service": "ec2.amazonaws.com"
	},
		"Action": "sts:AssumeRole"
	}
	]
}
EOF
}

resource "aws_iam_role_policy" "bootstrap_policy" {
	name = "ngfw_bootstrap_policy"
	role = aws_iam_role.bootstrap_role.id

	policy = <<EOF
{
	"Version" : "2012-10-17",
	"Statement": [
	{
		"Effect": "Allow",
		"Action": "s3:ListBucket",
		"Resource": "arn:aws:s3:::${var.s3_bucket}"
	},
	{
	"Effect": "Allow",
	"Action": "s3:GetObject",
	"Resource": "arn:aws:s3:::${var.s3_bucket}/*"
	}
	]
}
EOF
}


/////////////////
// SERVICES VPC
/////////////////


module "services_vpc" {
	source = "../../modules/vpc/services-vpc"

	aws_region = var.aws_region
	access_key = var.access_key
	secret_key = var.secret_key
	ubuntu_aws_key = var.ubuntu_aws_key

	vpc_name = var.services-Vpc-Name
	vpc_cidr = var.services-Vpc-cidr

	Services-a = var.Services-a
	Services-b = var.Services-b

	ssh_private_ip = var.js_services_private_ip
}


/////////////
// PANORAMA
/////////////


module "panorama" {
	source = "../../modules/panorama"

	aws_region = var.aws_region
	access_key = var.access_key
	secret_key = var.secret_key
	panorama_aws_key = var.panorama_aws_key

	panorama_mgmt_subnet_id = module.services_vpc.Services-a_id
	mgmtpanoramaip = var.mgmtpanoramaip
	panorama_instance_type = var.panorama_instance_type
	panorama_name = var.panorama_name
	panorama_license_type = var.panorama_license_type
	panorama_license_type_map = var.panorama_license_type_map
	panorama_version = var.panorama_version

	services-Vpc-Name = var.services-Vpc-Name
	services_vpc_id = module.services_vpc.vpc_id
}

