provider "aws" {
  region     = "eu-west-2"
  access_key = "AKIAVFK6UURB6VTP6LOJ"
  secret_key = "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"
}

module "check" {
  source = "./source"

  some = "../bootstrap_files/east-west/fw1/bootstrap.xml"
}
