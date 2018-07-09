#Instances in Public subnet
resource "aws_key_pair" "ssh_key_pair" {
  public_key = "${file(var.ssh_key_file)}"
  key_name = "Testing_keypair"
  #key_name = "ravi"
}

resource "aws_eip" "bastion" {
  instance = "${aws_instance.bastion.id}"
  vpc      = true
}

resource "aws_instance" "bastion" {
  ami = "${var.amis["bastion"]}"
  instance_type = "${var.instance_types["bastion"]}"

  subnet_id = "${aws_subnet.public_subnet.id}"
  associate_public_ip_address = true
  vpc_security_group_ids = ["${aws_security_group.bastion.id}"]
 # key_name = "${var.ssh_key_name}"
  key_name = "${aws_key_pair.ssh_key_pair.key_name}"

  tags {
    Name = "${var.environment_name}-bastion"
    Environment = "${var.environment_name}"
  }
}

/*
  resource "aws_eip" "ecs-pub_eip" {
  instance = "${aws_instance.ecs-pub.id}"
  vpc = true
}




resource "aws_instance" "ecs-master" {
  count = "${var.instance_counts["serv_in_public_count"]}"

  ami           = "${var.amis["server_ami"]}"
  instance_type = "${var.instance_types["serv_in_public"]}"

 # key_name = "${var.ssh_key_name}"
  key_name = "${aws_key_pair.ssh_key_pair.key_name}"
  vpc_security_group_ids = ["${aws_security_group.public-subnet-serv.id}"]
  subnet_id              = "${aws_subnet.public_subnet.id}"

#  iam_instance_profile = "${var.codedeploy_instance_profile_id}"
#  user_data            = "${var.app_user_data}"

  associate_public_ip_address = true

  tags {
    Name        = "ecs-pub"
    Environment = "${var.environment_name}"
  }
}
*/





#resource "aws_instance" "nat" {
#  ami           = "${var.amis["nat_ami"]}"
#  instance_type = "${var.instance_types["nat"]}"
#
#  # key_name               = "${var.ssh_key_name}"
#  key_name = "${aws_key_pair.ssh_key_pair.key_name}"
#  vpc_security_group_ids = ["${aws_security_group.nat.id}"]
#
#  subnet_id                   = "${aws_subnet.public_subnet.id}"
#  associate_public_ip_address = true
#  source_dest_check           = false
#  #user_data                   = "${var.inf_user_data}"
#
#  tags {
#    Name        = "${var.environment_name}-nat"
#    Environment = "${var.environment_name}"
#    Service     = "${var.environment_name} NAT"
#  }
#}

