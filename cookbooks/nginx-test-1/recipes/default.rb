#
# Cookbook Name:: nginx
# Recipe:: default
#
# Copyright 2016, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
package 'nginx' do
  action :install
end

directory '/usr/local/stack-2' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/usr/local/stack-2/Dockerfile' do
  source 'Dockerfile'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

execute 'Build Dockerfile' do
  command 'docker build -f /usr/local/stack-2/Dockerfile /usr/local/stack-2/'
end

cookbook_file "/usr/share/nginx/html/p4.jpg" do
  source "p4.jpg"
  owner 'root'
  group 'root'
  mode '0755'
 action :create
end

cookbook_file "/usr/share/nginx/html/index.html" do
  source "index.html"
  owner 'root'
  group 'root'
  mode '0755'
 action :create
end

service 'nginx' do
  action [ :enable, :start ]
end

