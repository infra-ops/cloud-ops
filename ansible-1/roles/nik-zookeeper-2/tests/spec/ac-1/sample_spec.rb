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
describe file('/opt/app/zookeeper/conf/zoo.cfg') do
  it { should be_file }
   it { should contain('server.1').before(/^=zookeeper1:2888:3888/) }
end
#describe service('zookeeper') do
#  it { should be_running }
#end
describe port(2181) do
  it { should be_listening }
end
