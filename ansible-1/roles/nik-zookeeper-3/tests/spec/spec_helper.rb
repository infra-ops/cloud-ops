require 'serverspec'
require 'net/ssh'
require 'yaml'




set :backend, :ssh


properties = YAML.load_file('properties.yml')

if ENV['ASK_SUDO_PASSWORD']
  begin
    require 'highline/import'
  rescue LoadError
    fail "highline is not available. Try installing it."
  end
  set :sudo_password, ask("Enter sudo password: ") { |q| q.echo = false }
else
  set :sudo_password, ENV['SUDO_PASSWORD']
end

host = ENV['TARGET_IPV4']

options = Net::SSH::Config.for(host)

options[:user] = 'root'

set :host,        options[:host_name] || host
set :ssh_options, options

#if os[:family] == 'ubuntu16.04'
#end


# Disable sudo
# set :disable_sudo, true


# Set environment variables
# set :env, :LANG => 'C', :LC_MESSAGES => 'C'

# Set PATH
# set :path, '/sbin:/usr/local/sbin:$PATH'
