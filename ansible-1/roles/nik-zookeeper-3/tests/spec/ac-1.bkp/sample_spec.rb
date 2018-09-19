require 'spec_helper'


if os[:family] == 'ubuntu'
  pip_package = 'python-pip'
end



describe package('oracle-java8-installer') do
  it { should be_installed }
end
describe package('ruby2.5') do
  it { should be_installed }
end
describe package('ruby2.5-dev') do
  it { should be_installed }
end
describe file('/opt/apps/zookeeper/conf/zookeeper-env.sh') do
  it { should be_file }
   it { should contain('ZOO_LOG_DIR').before(/^=/opt/data/zookeeper/logs) }
end
#describe service('zookeeper') do
#  it { should be_running }
#end
#describe port(2181) do
#  it { should be_listening }
#end
