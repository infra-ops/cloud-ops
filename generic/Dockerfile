FROM ubuntu:14.04

RUN  mkdir /var/run/sshd
RUN  apt-get update && apt-get upgrade -y
RUN  apt-get install  vim gcc curl git git-core libc6-i386 openssh-server telnet  net-tools elinks -y
RUN  apt-get install -y software-properties-common python-software-properties
RUN  apt-get install -y build-essential libcurl4-openssl-dev libssl-dev zlib1g-dev
RUN  apt-get install -y dnsutils
#RUN  apt-get install -y openjdk-7-jdk

RUN  apt-get update
RUN  export LC_ALL=C
RUN  mkdir -p /opt/store/

########GIT INSTALLATION
#RUN apt-get install   git  git-core -y


####JENKINS INSTALLATION
RUN wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
RUN echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list
RUN apt-get update
RUN apt-get install -y jenkins
######RUNDECK INSTALLATION
COPY  rundeck.sh /opt/store

#####MAVEN INSTALLATION
ADD maven  /opt/maven

#####JIRA INSTALLATION

COPY jira.sh   /opt/store

####STASH INSTALLATION
#http://chilion.nl/stash-on-ubuntu-14-04/

COPY  stash.sh 	/opt/store

#########################
COPY java.sh   	/opt/store
COPY java-env.sh   /opt/store
################################
RUN useradd -p docker123 -m  nik
RUN echo 'root:global123' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22
EXPOSE 8050
EXPOSE 7990
EXPOSE 4440

#CMD ["/usr/sbin/sshd", "-D"]
#ab -n 100 -c 10 http://blog.iceland.com/


