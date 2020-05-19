////////////////////
// Bootstrap Bucket
////////////////////

provider "aws" {
  region     = "eu-west-2"
  access_key = "AKIAVFK6UURB6VTP6LOJ"
  secret_key = "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"
}

variable "some" {}

resource "aws_s3_bucket" "bootstrap_bucket" {
  bucket        = "adwwdwdqdqdwqwd-sfsasd203ed320-23e32ea-asdas"
  acl           = "private"
  force_destroy = true

  tags = {
    Name = "bootstrap_bucket"
  }
}

///////////////////////
// Bootstraps Folders
///////////////////////


resource "aws_s3_bucket_object" "bootstrap_xml" {
  bucket = "${aws_s3_bucket.bootstrap_bucket.id}"
  acl    = "private"
  key    = "config/bootstrap.xml"
  source = "${var.some}"
}
