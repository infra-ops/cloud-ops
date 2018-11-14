#ELB
resource "aws_elb" "private_elb" {
  name = "private-elb"
  subnets = ["${aws_subnet.private_subnet.id}"]
  security_groups = ["${aws_security_group.elb.id}"]

  connection_draining = true

  "listener" {
    instance_port     = 8000
    instance_protocol = "http"
    lb_port           = 443
    lb_protocol       = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    target              = "tcp:22"
    interval            = 10
  }

  instances = ["${aws_instance.private_subnet_serv.*.id}"]

  tags {
    Name        = "${var.environment_name}-private-elb"
    Environment = "${var.environment_name}"
  }
}