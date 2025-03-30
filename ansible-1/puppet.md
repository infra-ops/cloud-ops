
Create a puppet script hellopuppet.pp in the directory /var/save/puppet_hello.
The script when executed should write "hello puppet" without quotes to 
/var/save/puppet_hello/hellopuppet.txt


```
cat /var/save/puppet_hello/hellopuppet.pp

file { '/var/save/puppet_hello':
  ensure => directory,
  mode   => '0755',
}

file { '/var/save/puppet_hello/hellopuppet.txt':
  ensure  => file,
  content => "hello puppet\n",
  require => File['/var/save/puppet_hello'],
}


puppet apply /var/save/puppet_hello/hellopuppet.pp


cat /var/save/puppet_hello/hellopuppet.txt






```
