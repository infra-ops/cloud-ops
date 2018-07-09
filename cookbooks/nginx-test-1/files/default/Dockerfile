FROM ubuntu:14.04

RUN  mkdir /var/run/sshd
RUN  apt-get update
RUN  apt-get install  vim gcc curl git libc6-i386 openssh-server telnet  net-tools elinks -y
RUN  apt-get install -y software-properties-common python-software-properties
RUN  apt-get install -y build-essential libcurl4-openssl-dev libssl-dev zlib1g-dev
RUN  apt-get update
RUN  apt-get install -y openjdk-7-jdk

RUN  apt-get update
RUN  export LC_ALL=C
RUN  apt-get install apache2 -y

RUN useradd -p docker123 -m  nik
RUN echo 'root:global123' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd


EXPOSE 22
EXPOSE 8080
#CMD ["/usr/sbin/sshd", "-D"]
