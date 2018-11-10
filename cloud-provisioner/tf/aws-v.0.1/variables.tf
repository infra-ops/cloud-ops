
variable "ssh_key_name" {
  description = "The aws ssh key name."
  default = "vpn42"
}

variable "ssh_key_file" {
  description = "The ssh public key for using with the cloud provider."
  default = "Testing_keypair.pub"
}

variable "region" {
  default = "us-east-1"
}

variable "az_1" {
  default = "us-east-1a"
}

variable "az_2" {
  default = "us-east-1b"
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
    server_ami = "ami-0efacdc5af3268b6e"  #globality-ecs-optimized-2017-05-11_05-44-20
    bastion = "ami-0efacdc5af3268b6e"  #globality-ecs-optimized-2017-05-11_05-44-20
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




##alb variables

variable "name" {
  description = "The name of the ELB"
}

variable "security_groups" {
  description = "A list of security group IDs to assign to the ELB"
  type        = "list"
}

variable "subnets" {
  description = "A list of subnet IDs to attach to the ELB"
  type        = "list"
}

variable "internal" {
  description = "If true, ELB will be an internal ELB"
}

variable "cross_zone_load_balancing" {
  description = "Enable cross-zone load balancing"
  default     = true
}

variable "idle_timeout" {
  description = "The time in seconds that the connection is allowed to be idle"
  default     = 60
}

variable "connection_draining" {
  description = "Boolean to enable connection draining"
  default     = false
}

variable "connection_draining_timeout" {
  description = "The time in seconds to allow for connections to drain"
  default     = 300
}

variable "tags" {
  description = "A mapping of tags to assign to the resource"
  default     = {}
}

variable "listener" {
  description = "A list of listener blocks"
  type        = "list"
}

variable "access_logs" {
  description = "An access logs block"
  type        = "list"
  default     = []
}

variable "health_check" {
  description = "A health check block"
  type        = "list"
}

variable "number_of_instances" {
  description = "Number of instances to attach to ELB"
  default     = 0
}

variable "instances" {
  description = "List of instances ID to place in the ELB pool"
  type        = "list"
  default     = []
}








