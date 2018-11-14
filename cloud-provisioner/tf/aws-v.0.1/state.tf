terraform {
  backend "s3" {
    bucket = "dev-nik-1"
    region = "us-east-1"
    key    = "tfstate-2/terraform.tfstate"
  }
}
