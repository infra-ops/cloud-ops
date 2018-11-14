This is a freelancing project

Thie project does the following stuffs:
1. Create vpc, routing tables, internet gateway
2. Create public subnet and private subnet
3. Create security groups for instances. Please modify the security group rules accordingly in security_groups.tf file
4. create jumpbox, instance and NAT gateway in public subnet. Assigns EIP to these instances
5. Create 2 instances in Private subnet. (Used ecs optimized AMIs)
6. Create ELB and add the 2 instances in private subnet to the ELB
7. create ecs cluster.

Tasks to be done:
1. Please create a keypair and add the public key in aws_key_pair resource as i have done in instances.tf. With this you wil be able to login to the servers
2. Update the access and secret key in terraform.tfvars file. make sure the account has full access to use all the resources in AWS

I have used ECS optimized AMI for the instances and also have created ecs cluster. Please create Docker images and use it accordingly to use it in ECS cluster. and accordingly modify the terraform code.