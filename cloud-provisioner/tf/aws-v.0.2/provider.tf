provider "aws" {
  region = "${var.region}"
  shared_credentials_file = "/root/.aws/credentials"
  #version = "1.2.0"
}
