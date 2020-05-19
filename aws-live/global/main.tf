provider "aws" {
    region = var.aws_region
    access_key = var.access_key
    secret_key = var.secret_key
}

resource "aws_s3_bucket" "s3_state" {
    bucket = var.s3_bucket

    versioning {
        enabled = true
    }

    lifecycle {
        prevent_destroy = true
    }
}

terraform {
    backend "s3" {
        bucket  = "aws-transit-gateway-s3-phantom-bucket"
        region  = "eu-west-2"
        key     = "global/s3/terraform.tfstate"
        encrypt = true
        access_key = "AKIAVFK6UURB6VTP6LOJ"
        secret_key = "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"
    }
}
