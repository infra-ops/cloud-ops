#Security Groups
#resource "aws_security_group" "nat" {
#  name = "${var.environment_name}-nat-sg"
#  description = "Security group for NAT instance"
#  vpc_id = "${aws_vpc.vpc.id}"
#
#  tags {
#    Name = "${var.environment_name}-nat-sg"
#    Environment = "${var.environment_name}"
#  }
#
#  ingress {
#    from_port = 80
#    protocol = "tcp"
#    to_port = 80
#    cidr_blocks = ["${var.vpc_cidr_block}"]
#  }
#  ingress {
#    from_port = 443
#    protocol = "tcp"
#    to_port = 443
#    cidr_blocks = ["${var.vpc_cidr_block}"]
#  }
#  ingress {
#    from_port = 22
#    protocol = "ssh"
#    to_port = 22
#    cidr_blocks = ["${aws_security_group.bastion.id}"]
#  }
#  #Everything, Everywhere
#  egress {
#    from_port = 0
#    protocol = "-1"
#    to_port = 0
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#}
/*
resource "aws_security_group" "nat" {
  name   = "${var.environment_name}-nat-sg"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name        = "${var.environment_name}-nat-sg"
    Environment = "${var.environment_name}"
  }

  # HTTP from elb
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  # SSH from bastion
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = ["${aws_security_group.bastion.id}"]
  }

  # Allow pings in
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #  #Everything, Everywhere
  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
*/

resource "aws_security_group" "bastion" {
  name        = "${var.environment_name}-bastion-sg"
  description = "Allows ssh from the world. This is our bastion. Google it."
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    Name        = "${var.environment_name}-jump-sg"
    Environment = "${var.environment_name}"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Everything, everywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#resource "aws_security_group" "private-subnet-serv" {
#  name   = "${var.environment_name}-priv-subnet-sg"
#  vpc_id = "${aws_vpc.vpc.id}"

 # tags {
 #   Name        = "${var.environment_name}-priv-subnet-sg"
 #   Environment = "${var.environment_name}"
 # }

 # ingress {
 #   from_port   = 8000
 #   to_port     = 8000
 #   protocol    = "tcp"
 #   cidr_blocks = ["${var.vpc_cidr_block}"]
 # }

# ingress {
 #   from_port       = 22
 #   to_port         = 22
 #   protocol        = "tcp"
 #   security_groups = ["${aws_security_group.bastion.id}"]
 # }

  # Allow pings in
  #ingress {
  #  from_port   = -1
  #  to_port     = -1
  #  protocol    = "icmp"
  #  cidr_blocks = ["${var.vpc_cidr_block}"]
  #}

  #egress {
  #  from_port   = 80
  #  to_port     = 80
  #  protocol    = "tcp"
  #  cidr_blocks = ["${aws_security_group.bastion.id}"]
  #}

  #egress {
  #  from_port   = 443
  #  to_port     = 443
  #  protocol    = "tcp"
  #  cidr_blocks = ["${aws_security_group.bastion.id}}"]
  #}

  # DB security rules(PostgreSQL)
  #egress {
  #  from_port   = 5432
  #  to_port     = 5432
  #  protocol    = "tcp"
  #  cidr_blocks = ["${var.vpc_cidr}"]
  #}
#}


resource "aws_security_group" "private-subnet-serv" {
  name   = "${var.environment_name}-private-sg"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name        = "${var.environment_name}-private-sg"
    Environment = "${var.environment_name}"
  }

  # HTTP from elb
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  # SSH from bastion
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = ["${aws_security_group.bastion.id}"]
  }

  # Allow pings in
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "elb" {
  name   = "${var.environment_name}-elb-sg"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name        = "${var.environment_name}-elb-sg"
    Environment = "${var.environment_name}"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow pings in
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  # API
  egress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  # Web
  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }
}

resource "aws_security_group" "public-subnet-serv" {
  name   = "${var.environment_name}-web-sg"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name        = "${var.environment_name}-web-sg"
    Environment = "${var.environment_name}"
  }

  # HTTP from elb
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  # SSH from bastion
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = ["${aws_security_group.bastion.id}"]
  }

  # Allow pings in
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["${var.vpc_cidr_block}"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}