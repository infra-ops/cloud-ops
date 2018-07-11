directory '/opt/router-package' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

directory '/opt/AIC-CLOUD' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

directory '/opt/AIC-CLOUD/tomcat' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end






cookbook_file '/opt/router-package/apache-tomcat-7.0.47.tar.gz' do
  source 'apache-tomcat-7.0.47.tar.gz'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end


#execute 'extract_wp' do
  # cwd "#{node[:path]}/setup"
#  command <<-EOF
#    tar xzf #{node[:path]}/setup/apache-tomcat-7.0.47.tar.gz -C #{node[:path]}/#{node[:site]}
#  EOF
#  not_if { File.exists?("#{node[:path]}/#{node[:site]}/wp-config.php") }
#end


execute 'extract_tomcat' do
 
  command <<-EOF
    tar xzf /opt/router-package/apache-tomcat-7.0.47.tar.gz -C /opt/router-package
  EOF

end


execute 'rename_the_directory' do
  command  'mv /opt/router-package/apache-tomcat-7.0.47/*  /opt/AIC-CLOUD/tomcat'
end


bash 'print_helloworld' do
  code <<-EOF
    bash /vagrant/hello.sh
  EOF
end




template  "/opt/AIC-CLOUD/tomcat/conf/server.xml"  do
           source "server.xml.erb"
           variables({
           	   :shutdown_port => "#{node[:shutdown_port]}",
                   :port => "#{node[:port]}" 
           })

end



























