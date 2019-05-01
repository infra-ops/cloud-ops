FROM ubuntu:16.04
MAINTAINER nik

ENV DEBIAN_FRONTEND=noninteractive LANG=C LC_ALL=C

# prep
RUN \
    apt-get -yq update && \
    apt-get install -y software-properties-common && \
    apt-get install -yq python-software-properties && \
    apt-get install -yq python-pip && \
    apt-add-repository ppa:git-core/ppa -y && \
    apt-get -yq update && \
    apt-get dist-upgrade -yq && \
    apt-get install -yqq sudo wget aptitude htop vim vim-puppet git traceroute dnsutils \
      curl ssh sudo psmisc gcc make build-essential libfreetype6 libfontconfig openjdk-8-jdk-headless \
      augeas-tools tree tcpdump && \
    echo "jenkins ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/jenkins && \
    chmod 0440 /etc/sudoers.d/jenkins && \
    echo "set modeline" > /etc/vim/vimrc.local && \
    echo "export TERM=vt100\nexport LANG=C\nexport LC_ALL=C" > /etc/profile.d/dockenv.sh && \
    sed -i 's/^#\( alias l\)/\1/' /root/.bashrc && \
    echo "export TERM=vt100" >> /root/.bashrc && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# From Official jenkins docker image - https://github.com/jenkinsci/docker
ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT 50000

ARG user=jenkins
ARG group=jenkins
ARG uid=1001
ARG gid=1001

RUN groupadd -g ${gid} ${group} \
    && useradd -d "$JENKINS_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}


RUN wget -qO - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add - && \
    echo 'deb http://pkg.jenkins-ci.org/debian binary/' \
      | tee /etc/apt/sources.list.d/jenkins.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y jenkins && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    update-rc.d -f jenkins disable



EXPOSE 8080 50000

#CMD ["/usr/bin/java", "-jar", "/usr/share/jenkins/jenkins.war"]




CMD ["/usr/bin/java", "-Djenkins.install.runSetupWizard=false", "-jar","/usr/share/jenkins/jenkins.war"]
