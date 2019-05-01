require 'spec_helper'

#describe command('hostname  -I | cut -d " " -f1') do
#  its(:stdout) { should match ENV['TARGET_IPV4'] }
#end

#describe command('uptime') do
#  puts("up=#{command('uptime').stdout}")
#end

#describe command('uname -n'), :if => 'ac-1' == 'ac-1' do
#  its(:stdout) { should match ENV['TARGET_HOST'] }
#end



describe nil do
  puts("addr=#{ENV['TARGET_IPV4']}")
  puts("hosts=#{ENV['TARGET_HOST']}")
end


describe command('ls -ld /opt/data') do
  its(:stdout) { should match '/opt/data' }
end

describe command('ls -ld  /opt/apps/solr/server/logs') do
  its(:stdout) { should match '/opt/apps/solr/server/logs' }
end


describe command('ls -ld  /opt/apps/zookeeper/logs') do
  its(:stdout) { should match '/opt/apps/zookeeper/logs' }
end

describe command('cat /opt/apps/solr/bin/solr.in.sh | grep -i SOLR_LOGS_DIR=') do
  its(:stdout) { should match '/opt/data/solr/logs' }
end


describe command('cat /opt/apps/zookeeper/conf/zookeeper-env.sh  | grep -i ZOO_LOG_DIR=') do
  its(:stdout) { should match '/opt/data/zookeeper/logs' }
end


describe command('cat /opt/apps/solr/server/resources/log4j.properties | grep -i solr.log') do
  its(:stdout) { should match '/opt/data/solr/logs' }
end

