resource "aws_instance" "linuxapp" {
  ami           = "${lookup(var.AmiLinux, var.region)}"
  instance_type = "t2.micro"
  associate_public_ip_address = "true"
  subnet_id = "${aws_subnet.PublicAZA.id}"
  vpc_security_group_ids = ["${aws_security_group.FrontEnd.id}"]
  key_name = "${var.key_name}"
  tags {
        Name = "linux-top"
  }


user_data = <<HEREDOC
  #!/bin/bash
  apt-get update -y
  apt-get install -y vim gcc curl wget git
  git clone https://github.com/nik786/etl.git /tmp/et-2/   
HEREDOC
}
