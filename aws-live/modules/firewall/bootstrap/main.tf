///////////////////////
// Bootstraps Folders
///////////////////////


resource "aws_s3_bucket_object" "bootstrap_xml" {
  bucket = var.bootstrap_s3bucket_id
  acl    = "private"
  key    = var.xml_key
  source = var.xml_source
}

resource "aws_s3_bucket_object" "init-cft_txt" {
  bucket = var.bootstrap_s3bucket_id
  acl    = "private"
  key    = var.init_cfg_key
  source = var.init_cfg_source
}

resource "aws_s3_bucket_object" "software" {
  bucket = var.bootstrap_s3bucket_id
  acl    = "private"
  key    = var.software_key
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "license" {
  bucket = var.bootstrap_s3bucket_id
  acl    = "private"
  key    = var.license_key
  source = var.license_source
}

resource "aws_s3_bucket_object" "content" {
  bucket = var.bootstrap_s3bucket_id
  acl    = "private"
  key    = var.content_key
  source = "/dev/null"
}


//////////////////////
// Bootstrap Profile
//////////////////////


resource "aws_iam_instance_profile" "bootstrap_profile" {
  name = "${var.fw_name}_ngfw_bootstrap_profile"
  role = var.bootstrap_role_name
  path = "/"
}


////////////////////
// Bootstrap Bucket
////////////////////


//resource "aws_s3_bucket" "bootstrap_bucket" {
//  bucket        = "${var.bootstrap_s3bucket}"
//  acl           = "private"
//  force_destroy = true
//
//  tags = {
//    Name = "bootstrap_bucket"
//  }
//}


///////////////
//// IAM Role
///////////////
//
//
//resource "aws_iam_role" "bootstrap_role" {
//  name = "ngfw_bootstrap_role"
//
//  assume_role_policy = <<EOF
//{
//  "Version": "2012-10-17",
//  "Statement": [
//    {
//      "Effect": "Allow",
//      "Principal": {
//      "Service": "ec2.amazonaws.com"
//    },
//      "Action": "sts:AssumeRole"
//    }
//  ]
//}
//EOF
//}
//
//resource "aws_iam_role_policy" "bootstrap_policy" {
//  name = "ngfw_bootstrap_policy"
//  role = "${aws_iam_role.bootstrap_role.id}"
//
//  policy = <<EOF
//{
//  "Version" : "2012-10-17",
//  "Statement": [
//    {
//      "Effect": "Allow",
//      "Action": "s3:ListBucket",
//      "Resource": "arn:aws:s3:::${var.bootstrap_s3bucket}"
//    },
//    {
//    "Effect": "Allow",
//    "Action": "s3:GetObject",
//    "Resource": "arn:aws:s3:::${var.bootstrap_s3bucket}/*"
//    }
//  ]
//}
//EOF
//}
