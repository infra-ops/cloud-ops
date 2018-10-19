variable "region" {
  default = "us-east1"
}

variable "project-name" {
  default = "terra-test-219910"
}

variable "subnetwork-region" {
  default = "us-east1"
}

variable "zones" {
  default = {
    zone0 = "us-east1-b"
    zone1 = "us-east1-c"
  }
}

variable "network" {
  default = "my-network"
}

variable "vm_type" {
  default {
    "512gig" = "f1-micro"
  }
}

variable "os" {
  default = "debian-cloud/debian-9"
}

variable "instance-name" {
  default = "compute-instance"
}

variable "bastion-instance-name" {
  default = "bastion-instance"
}

variable "hostname" {
  default = {
    host0 = "host1"
    host1 = "host2"
    host2 = "bastionhost"
  }
}

variable "public-cidr" {
  default = "10.0.1.0/24"
}

variable "private-cidr" {
  default = "10.0.2.0/24"
}

variable "internet-lb-name" {
  default = "http-backend"
}
