output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "internet_gateway" {
  value = "${aws_internet_gateway.internet_gateway.id}"
}

output "private_subnet" {
  value = "${aws_subnet.private_subnet.id}"
}

output "private_route_table" {
  value = "${aws_route_table.private-routing.id}"
}

output "public_subnet" {
  value = "${aws_subnet.public_subnet.id}"
}

output "public_route_table" {
  value = "${aws_route_table.public-routing.id}"
}

output "bastion" {
  value = {
    "Instance_id" = "${aws_instance.bastion.id}",
    "Public_IP" = "${aws_instance.bastion.public_ip}",
    "Public_DNS" = "${aws_instance.bastion.public_dns}"
  }
}

output "private_serv" {
  value = {
    "Instance_id" = ["${join(",", aws_instance.private_subnet_serv.*.id)}"],
    "Private_IPs" = ["${join(",", aws_instance.private_subnet_serv.*.private_ip)}"]
  }
}

/*
output "public_serv" {
  value = {
    "Instance_id" = ["${join(",", aws_instance.ecs-pub.*.id)}"],
    "Private_IPs" = ["${join(",", aws_instance.ecs-pub.*.private_ip)}"]
    "Public_IPs" =  ["${aws_eip.ecs-pub_eip.public_ip}"]
  }
}
*/

output "ecs_cluster" {
  value = "${aws_ecs_cluster}"
}
