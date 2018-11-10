
variable "ssh_key_name" {
  description = "The aws ssh key name."
  default = "vpn42"
}

variable "ssh_key_file" {
  description = "The ssh public key for using with the cloud provider."
  default = "/root/.ssh/id_rsa.pub"
}

variable "region" {
  default = "us-east-1"
}

variable "az" {
  type = "list"
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
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
  type    = "list"
  default = ["10.10.30.0/24", "10.10.40.0/24", "10.10.50.0/24"]
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
    "serv_in_private_count" = 3
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
  default = "tera-2"
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

variable "load_balancer_name" {
  default = "test"
}
variable "load_balancer_is_internal" {
  default = "false"
}
variable "security_groups" {
  default = "sg-0d22aaf761da3705a"
}

variable "subnets" {
  default = ["subnet-0f5694d5a7818dc9d"]
}

# variable "vpc_id" {
#   default = "vpc-03041f4905dc36795"
# }

variable "idle_timeout" {
  description = "The time in seconds that the connection is allowed to be idle"
  default     = 60
}

variable "enable_cross_zone_load_balancing" {
  description = "Enable cross-zone load balancing"
  default     = true
}

variable "enable_deletion_protection" {
  description = "Enable deletion protection for the load balancer"
  default = false
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
  type        = "map"
  default     = {}
}

variable "log_bucket_name" {
  description = "An access logs block"
  default     = "tera-2"
}

variable "log_location_prefix" {
  description = "Log location prefix"
  default = "tera-2"
}

variable "load_balancer_create_timeout" {
  description = "LB create timeout"
  default = "200s"
}

variable "load_balancer_update_timeout" {
  description = "LB update timeout"
  default = "120s"
}

variable "load_balancer_delete_timeout" {
  description = "LB delete timeout"
  default = "120s"
}

variable "logging_enabled" {
  description = "If set to true, a load balancer will be created with logging enabled"
  default = true
}


variable "target_groups" {
  description = "target group placeholder variables"
  type = "list"

  default = [{
    name = "backend1"
    backend_port = "8080"
    backend_protocol = "HTTP"
    deregistration_delay = 300
    target_type = "ip"
    health_check_interval = "20"
    health_check_path = "/"
    health_check_port = "80"
    health_check_healthy_threshold = "3"
    health_check_unhealthy_threshold = "3"
    health_check_timeout = "7"
    healthcheck_protocol = "HTTP"
    health_check_matcher = "200-299"
  }]
}

variable "target_groups_defaults" {
  description = "target group placeholder variables"
  type = "map"

  default = {
    name = "backend1"
    backend_port = "8080"
    backend_protocol = "HTTP"
    deregistration_delay = 300
    target_type = "ip"
    health_check_interval = "20"
    health_check_path = "/"
    health_check_port = "80"
    health_check_healthy_threshold = "3"
    health_check_unhealthy_threshold = "3"
    health_check_timeout = "7"
    healthcheck_protocol = "HTTP"
    health_check_matcher = "200-299"
  }
}

variable "http_tcp_listeners" {
  description = "placeholder variable for http tcp listeners"
  type = "list"

  default = [{
    port = "80"
    protocol = "HTTP"
  }]
}
