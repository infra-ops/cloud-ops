/opt/terraform apply -target=aws_instance.bastion
/opt/terraform apply -target=aws_instance.ecs-master
/opt/terraform apply -target=aws_instance.private_subnet_serv
/opt/terraform apply -target=aws_instance.private_subnet_serv1

terraform destroy -target=aws_lb_target_group.main
terraform destroy -target=aws_instance.private_subnet_serv
terraform destroy --auto-approve

