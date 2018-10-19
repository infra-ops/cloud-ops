resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.ecs_cluster_name}"
}

#resource "aws_launch_configuration" "ecs" {
#  name = "ecs"
#  image_id = "${var.amis["server_ami"]}"
#  instance_type = "${var.instance_types["serv_in_private"]}"
#  key_name = "${aws_key_pair.ssh_key_pair.key_name}"
#  security_groups = ["${aws_security_group.private-subnet-serv.id}"]
#}

