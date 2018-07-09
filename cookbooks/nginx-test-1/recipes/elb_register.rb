#
# Cookbook Name:: nik
# Recipe:: elb_register
#
# Copyright 2016, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

execute 'Regster to the CDS Load Balancers' do
  command "aws elbv2 register-targets --target-group-arn #{node['public-cds-demo']} --targets Id=`curl http://169.254.169.254/latest/meta-data/instance-id` --region us-east-1"
end

execute 'Regster to the LAP Load Balancers' do
  command "aws elbv2 register-targets --target-group-arn #{node['public-lap-demo']} --targets Id=`curl http://169.254.169.254/latest/meta-data/instance-id` --region us-east-1"
end

execute 'Regster to the LEC Load Balancers' do
  command "aws elbv2 register-targets --target-group-arn #{node['public-lec-demo']} --targets Id=`curl http://169.254.169.254/latest/meta-data/instance-id` --region us-east-1"
end

execute 'Regster to the LED Load Balancers' do
  command "aws elbv2 register-targets --target-group-arn #{node['public-led-demo']} --targets Id=`curl http://169.254.169.254/latest/meta-data/instance-id` --region us-east-1"
end

execute 'Regster to the LMS Load Balancers' do
  command "aws elbv2 register-targets --target-group-arn #{node['public-lms-demo']} --targets Id=`curl http://169.254.169.254/latest/meta-data/instance-id` --region us-east-1"
end
