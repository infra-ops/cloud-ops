terraform {
  backend "s3" {
    bucket = "tera-2"
    region = "us-east-1"
    key    = "tfstate-2/terraform.tfstate"
  }
}
