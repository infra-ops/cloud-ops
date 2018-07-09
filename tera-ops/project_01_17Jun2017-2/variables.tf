variable "access_key" {
  description = "AWS Access Key - Pass via command line"
}

variable "secret_key" {
  description = "AWS Secret Key - Pass via command line"
}

variable "ssh_key_name" {
  description = "The aws ssh key name."
  default = ""
}

variable "ssh_key_file" {
  description = "The ssh public key for using with the cloud provider."
  default = "Testing_keypair.pub"
}

variable "region" {
  default = "us-west-2"
}

variable "az_1" {
  default = "us-west-2a"
}

variable "az_2" {
  default = "us-west-2b"
}

variable "environment_name" {
  default = "tera"
}

variable "vpc_cidr_block" {
  default = "10.10.0.0/16"
  description = "CIDR for the VPC"
}
variable "public_subnet_cidr" {
  default = "10.10.35.0/24"
  description = "CIDR for Public Subnet"
}
variable "private_subnet_cidr" {
  default = "10.10.30.0/24"
  description = "CIDR for Private Subnet"
}
variable "other_private_subnet_cidr" {
  default = "10.10.31.0/24"
  description = "CIDR for Other Private Subnet"
}

variable "amis" {
  description = "default AMIs"
  type = "map"
  default = {
    server_ami = "ami-7180e511"  #globality-ecs-optimized-2017-05-11_05-44-20
    bastion = "ami-7180e511"  #globality-ecs-optimized-2017-05-11_05-44-20
  }
}

variable "instance_counts" {
  type = "map"
  description = "Instance count in different subnet"
  default = {
    "serv_in_private_count" = 2
    "serv_in_private1_count" = 1
    "serv_in_public_count" = 1
    "bastion" = 1
  }
}

variable "instance_types" {
  type = "map"
  description = "Instance types"
  default = {
    serv_in_private = "t2.micro"
    serv_in_public = "t2.micro"
    nat = "t2.micro"
    bastion = "t2.micro"
  }
}

variable "ecs_cluster_name" {
  default = "tera-ecs-cluster"
  description = "The Name of the ECS cluster"
}

variable "app_user_data" {
  default = "priv_user-data.sh"
}

variable "s3_bucket_name" {
  description = "The name of the s3 bucket to store the registry data in"
  default = "s3-ecs-docker-registry"
}

variable "registry_username" {
  description = "The username to use when connecting to the registry."
  default = "Registry"
}

variable "registry_docker_image" {
  description = "The docker image to use when provisioning the registry."
  default     = "allingeek/registry:2-s3"
}
