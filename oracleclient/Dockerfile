# Version: 0.0.1
FROM centos:7
MAINTAINER Vladimir Gerasimenko <vladworldss@yandex.ru>
LABEL name="vladworld/pyoracli" \
      vendor="CentOS" \
      license="GPLv2" \
      build-date="20170512"

ADD . /tmp/

RUN yum update && \
    yum install -y gcc && \
    yum -y localinstall /tmp/oracle-instantclient12.2/oracle* --nogpgcheck && \
    mkdir /usr/lib/oracle/12.2/client/network/admin -p && \
    cp /tmp/tnsnames.ora /usr/lib/oracle/12.2/client/network/admin/tnsnames.ora

ENV ORACLE_HOME=/usr/lib/oracle/12.2/client64
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV TNS_ADMIN=$ORACLE_HOME/network/admin

RUN yum -y install git wget curl && \
    yum install -y epel-release pandoc && \
    yum -y install tar gcc make bzip2 openssl openssl-devel && \
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile && \

    /bin/bash -c "source ~/.bash_profile && \
    	pyenv install 2.7.13 && \
        pyenv install 3.6.1 && \
        pyenv rehash && \
	    mkdir ~/ioss && \
	    pyenv virtualenv 2.7.13 core && \
	    cp -r /tmp/core ~/ioss && \
	    cd ~/ioss/core && \
	    pyenv local core && \
      	pip install -r requirements.txt" && \
    
    source ~/.bash_profile && \
    yum clean packages && \
    rm -rf /tmp/* /var/tmp/*

ENTRYPOINT /bin/bash
