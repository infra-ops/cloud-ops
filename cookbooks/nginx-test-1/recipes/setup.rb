#
# Cookbook Name:: nik
# Recipe:: setup
#
# Copyright 2016, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

cookbook_file '/usr/local/src/deployer.sh' do
  source 'deployer.sh'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

execute 'Run deployer' do
  command '/bin/sh /usr/local/src/deployer.sh'
end
