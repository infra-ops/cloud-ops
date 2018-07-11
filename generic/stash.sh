#mkdir /opt/stash
#mkdir /opt/stash/install
#mkdir /opt/stash/home
#cd	/opt/stash/install ;wget http://www.atlassian.com/software/stash/downloads/binary/atlassian-stash-2.11.4.tar.gz ; tar zxf atlassian-stash-2.11.4.tar.gz
#/usr/sbin/useradd --create-home --home-dir /usr/local/stash --shell /bin/bash stash
#/usr/local/stash --shell /bin/bash stash

#vim /opt/stash/home/atlassian-stash-2.11.4/bin/setenv.sh

#chown -R stash /opt/stash
#/var/stash/install/atlassian-stash-2.11.4/bin/start-stash.sh


cd /opt/store ; wget https://www.atlassian.com/software/stash/downloads/binary/atlassian-stash-3.11.1-x64.bin ; chmod 777 atlassian-stash-3.11.1-x64.bin

