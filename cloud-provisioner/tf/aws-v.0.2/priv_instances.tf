data "template_file" "userdata" {
  template = "${file("priv_user-data.sh.tpl")}"

  vars {
    ecs_cluster_name = "${var.ecs_cluster_name}"
  }
}

#Instances in Private subnet
resource "aws_instance" "private_subnet_serv" {
  count = "${var.instance_counts["serv_in_private_count"]}"

  ami           = "${var.amis["server_ami"]}"
  instance_type = "${var.instance_types["serv_in_private"]}"

  key_name = "${var.ssh_key_name}"
 # key_name = "${aws_key_pair.ssh_key_pair.key_name}"
  vpc_security_group_ids = ["${aws_security_group.private-subnet-serv.id}"]
  subnet_id              = "${aws_subnet.private_subnet.*.id[count.index]}"

  iam_instance_profile = "${aws_iam_instance_profile.ECSRoleToEC2.id}"
  user_data            = "${data.template_file.userdata.rendered}"

  associate_public_ip_address = false

  tags {
    Name        = "ecs-node-${count.index}"
    Environment = "${var.environment_name}"
  }
}

resource "aws_instance" "private_subnet_serv1" {
  count = "${var.instance_counts["serv_in_private1_count"]}"

  ami           = "${var.amis["server_ami"]}"
  instance_type = "${var.instance_types["serv_in_private"]}"

  key_name = "${var.ssh_key_name}"
 # key_name = "${aws_key_pair.ssh_key_pair.key_name}"
  vpc_security_group_ids = ["${aws_security_group.private-subnet-serv.id}"]
  subnet_id              = "${aws_subnet.private_subnet.*.id[count.index]}"

  iam_instance_profile = "${aws_iam_instance_profile.ECSRoleToEC2.id}"
  user_data            = "${data.template_file.userdata.rendered}"

  associate_public_ip_address = false

  tags {
    Name        = "ecs-master-${count.index}"
    Environment = "${var.environment_name}"
  }
}
