## ALB

resource "aws_lb" "main" {
  load_balancer_type               = "application"
  name                             = "${var.load_balancer_name}"
  internal                         = "${var.load_balancer_is_internal}"
  security_groups                  = ["${aws_security_group.elb.id}"]
  subnets                          = ["${aws_subnet.private_subnet.*.id}"]
  idle_timeout                     = "${var.idle_timeout}"
  enable_cross_zone_load_balancing = "${var.enable_cross_zone_load_balancing}"
  enable_deletion_protection       = "${var.enable_deletion_protection}"
  tags                             = "${merge(var.tags, map("Name", var.load_balancer_name))}"

  access_logs {
    enabled = true
    bucket  = "${var.log_bucket_name}"
    prefix  = "${var.log_location_prefix}"
  }


  count = "${var.logging_enabled ? 1 : 0}"
}

resource "aws_lb_target_group" "main" {
  name                 = "${lookup(var.target_groups[count.index], "name")}"
  vpc_id               = "${aws_vpc.vpc.id}"
  port                 = "${lookup(var.target_groups[count.index], "backend_port")}"
  protocol             = "${upper(lookup(var.target_groups[count.index], "backend_protocol"))}"
  deregistration_delay = "${lookup(var.target_groups[count.index], "deregistration_delay", lookup(var.target_groups_defaults, "deregistration_delay"))}"
  target_type          = "${lookup(var.target_groups[count.index], "target_type", lookup(var.target_groups_defaults, "target_type"))}"



  health_check {
    interval            = "${lookup(var.target_groups[count.index], "health_check_interval", lookup(var.target_groups_defaults, "health_check_interval"))}"
    path                = "${lookup(var.target_groups[count.index], "health_check_path", lookup(var.target_groups_defaults, "health_check_path"))}"
    port                = "${lookup(var.target_groups[count.index], "health_check_port", lookup(var.target_groups_defaults, "health_check_port"))}"
    healthy_threshold   = "${lookup(var.target_groups[count.index], "health_check_healthy_threshold", lookup(var.target_groups_defaults, "health_check_healthy_threshold"))}"
    unhealthy_threshold = "${lookup(var.target_groups[count.index], "health_check_unhealthy_threshold", lookup(var.target_groups_defaults, "health_check_unhealthy_threshold"))}"
    timeout             = "${lookup(var.target_groups[count.index], "health_check_timeout", lookup(var.target_groups_defaults, "health_check_timeout"))}"
    protocol            = "${upper(lookup(var.target_groups[count.index], "healthcheck_protocol", lookup(var.target_groups[count.index], "healthcheck_protocol")))}"
    matcher             = "${lookup(var.target_groups[count.index], "health_check_matcher", lookup(var.target_groups_defaults, "health_check_matcher"))}"
  }

  tags       = "${merge(var.tags, map("Name", lookup(var.target_groups[count.index], "name")))}"
  count      = "${var.logging_enabled ? length(var.target_groups) : 0}"
  depends_on = ["aws_lb.main"]

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_lb_listener" "frontend_http_tcp" {
  load_balancer_arn = "${aws_lb.main.arn}"
  port              = "${lookup(var.http_tcp_listeners[count.index], "port")}"
  protocol          = "${lookup(var.http_tcp_listeners[count.index], "protocol")}"
  count             = "${var.logging_enabled ? length(var.http_tcp_listeners) : 0}"

  default_action {
    target_group_arn = "${aws_lb_target_group.main.*.id[count.index]}"
    type             = "forward"
  }
}

resource "aws_lb_target_group_attachment" "attachments" {
  count            = "${var.instance_counts["serv_in_private_count"] * length(var.target_groups)}"
  target_group_arn = "${aws_lb_target_group.main.*.arn[count.index/var.instance_counts["serv_in_private_count"]]}"
  target_id        = "${aws_instance.private_subnet_serv.*.private_ip[count.index % var.instance_counts["serv_in_private_count"]]}"
  port             = "${lookup(var.target_groups_defaults, "backend_port")}"
}
