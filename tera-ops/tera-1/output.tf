output "public_ip"  {
  value = "${aws_instance.linuxapp.public_ip}"
}


output "id"  {
  value = "${aws_instance.linuxapp.id}"
}
