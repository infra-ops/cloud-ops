update-alternatives --install /usr/bin/java java /opt/AIC-CLOUDS/jdk1.7.0/bin/java 2
update-alternatives --install /usr/bin/jar jar /opt/AIC-CLOUDS/jdk1.7.0/bin/jar 2
update-alternatives --install /usr/bin/javac javac /opt/AIC-CLOUDS/jdk1.7.0/bin/javac 2
update-alternatives --set jar /opt/AIC-CLOUDS/jdk1.7.0/bin/jar
update-alternatives --set javac /opt/AIC-CLOUDS/jdk1.7.0/bin/javac

java -version

sed -i -e '$a\JAVA_HOME=/opt/AIC-CLOUDS/jdk1.7.0/' /etc/profile
sed -i -e '$a\export JAVA_HOME' /etc/profile
sed -i -e '$a\PATH=$JAVA_HOME/bin:$PATH' /etc/profile
sed -i -e '$a\export PATH' /etc/profile

export JRE_HOME=/opt/jdk1.8.0_144/jre
export JRE_PATH=$PATH:$JRE_HOME/bin
export JAVA_HOME=/opt/jdk1.8.0_144/
export JAVA_PATH=$JAVA_HOME
