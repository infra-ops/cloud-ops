#VPC
resource "aws_vpc" "vpc" {
  cidr_block = "${var.vpc_cidr_block}"
  enable_dns_hostnames = true
  enable_dns_support = true
  instance_tenancy = "default"

  tags {
    Name = "${var.environment_name}-vpc"
    Environment = "${var.environment_name}"
  }
}

#internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name = "${var.environment_name}-gateway"
    Environment = "${var.environment_name}"
  }
}

#Public subnet
resource "aws_subnet" "public_subnet" {
  cidr_block = "${var.public_subnet_cidr}"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name = "${var.environment_name}-public-subnet"
    Environment = "${var.environment_name}"
  }
}

resource "aws_route_table" "public-routing" {
  vpc_id = "${aws_vpc.vpc.id}"

  #Route everything through Internet Gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.internet_gateway.id}"
  }

  tags {
    Name = "${var.environment_name}-public-subnet-route"
    Environment = "${var.environment_name}"
  }
}

resource "aws_route_table_association" "public-routing-association" {
  route_table_id = "${aws_route_table.public-routing.id}"
  subnet_id = "${aws_subnet.public_subnet.id}"
}

#Private Subnet
resource "aws_subnet" "private_subnet" {
  cidr_block = "${var.private_subnet_cidr}"
  vpc_id = "${aws_vpc.vpc.id}"
  availability_zone = "${var.az_1}"

  tags {
    Name = "${var.environment_name}-private-subnet"
    Environment = "${var.environment_name}"
  }
}

resource "aws_route_table" "private-routing" {
  vpc_id = "${aws_vpc.vpc.id}"

  #Route everything through NAT instance
  route {
    cidr_block = "0.0.0.0/0"
    #instance_id = "${aws_instance.nat.id}"
    nat_gateway_id = "${aws_nat_gateway.nat.id}"
  }

  tags {
    Name = "${var.environment_name}-private-subnet-route"
    Environment = "${var.environment_name}"
  }
}

resource "aws_route_table_association" "private-routing-association" {
  route_table_id = "${aws_route_table.private-routing.id}"
  subnet_id = "${aws_subnet.private_subnet.id}"
}

#NAT Gateway
resource "aws_eip" "nat_eip" {
  vpc = true
}

resource "aws_nat_gateway" "nat" {
  allocation_id = "${aws_eip.nat_eip.id}"
  subnet_id = "${aws_subnet.public_subnet.id}"
}

