resource "aws_iam_role" "ecs" {
  name = "ecs_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "RegistryFullAccessRoleattach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
  roles = ["${aws_iam_role.ecs.name}"]
  name = "RegistryFullAccessRoleattach"
}

resource "aws_iam_policy_attachment" "ECSserviceFullAccessRoleattach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerServiceFullAccess"
  roles = ["${aws_iam_role.ecs.name}"]
  name = "ECSserviceFullAccessRoleattach"
}

resource "aws_iam_policy_attachment" "ServiceforEC2Roleattach" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
  roles = ["${aws_iam_role.ecs.name}"]
  name = "ServiceforEC2Roleattach"
}

resource "aws_iam_instance_profile" "ECSRoleToEC2" {
  name = "ECSRoleToEC2"
  role = "${aws_iam_role.ecs.name}"
}
