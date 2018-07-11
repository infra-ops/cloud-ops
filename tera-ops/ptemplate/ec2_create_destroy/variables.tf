variable "key_name" {
    description = "Name of the SSH keypair to use in AWS."
    default = "test_key"
}

variable "key_path" {
    description = "Path to the private portion of the SSH key specified."
    default = "/home/prithvi/projects/aws_terraform/test_private.pem"
}

variable "aws_region" {
    description = "AWS region to launch servers."
    default = "us-west-2"
}

variable "aws_access_key" {
  default = "AKIAJNKCE4Y3PWMAS6GQ"
}
variable "aws_secret_key" {
   default = "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"
}

variable "subnet_id" {
    description = "Subnet ID to use in VPC"
    default = "subnet-398bc84f"
}

variable "instance_type" {
    description = "Instance type"
    default = "t1.micro"
}

variable "instance_name" {
    description = "Instance Name"
}

variable "aws_amis" {
  default = {
    eu-west-1 = "ami-b1cf19c6"
    us-east-1 = "ami-de7ab6b6"
    us-west-1 = "ami-3f75767a"
    us-west-2 = "ami-21f78e11"
  }
}
