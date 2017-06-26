# Version: 0.1.0
FROM centos
MAINTAINER Vladimir Gerasimenko <vladworldss@yandex.ru>
LABEL name="vladworldss/omniorb" \
      vendor="CentOS" \
      license="GPLv2" \
      build-date="20170626"

ADD . /tmp/

ENV omniORB_path=/root/corba/omniORB

RUN yum -y update && \
    yum -y install gcc gcc-c++ && \
    yum -y install git wget curl nano mc && \
    yum install -y epel-release pandoc && \
    yum -y install tar make bzip2 openssl openssl-devel && \
    
    # Установка pyenv
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile && \
      
    /bin/bash -c "source ~/.bash_profile && \
      	pyenv install 3.6.0 && \
        pyenv rehash && \
        pyenv virtualenv 3.6.0 omniORB && \
		    
        # Установка omniORB
        mkdir -p ${omniORB_path} && \
        cd ${omniORB_path} && \
        
        pyenv local omniORB && \
        pip install -r /tmp/requirements.txt && \

        mv /tmp/omni* . && \
        tar xvfj omniORB-4.2.2.tar.bz2 && rm omniORB-4.2.2.tar.bz2 && \
        tar xvfj omniORBpy-4.2.2.tar.bz2 && rm omniORBpy-4.2.2.tar.bz2 && \
        mkdir omniORB_install && \

    		cd omniORB-4.2.2 && mkdir build && cd build && \
    		../configure --prefix=${omniORB_path}/omniORB_install/ PYTHON=/root/.pyenv/versions/omniORB/bin/python && \
    		make && make install && \

		    cd ../../omniORBpy-4.2.2 && mkdir build && cd build && \
		    ../configure --prefix=${omniORB_path}/omniORB_install/ PYTHON=/root/.pyenv/versions/omniORB/bin/python --with-omniorb=${omniORB_path}/omniORB_install/ && \
		    make && make install && \

        cp ${omniORB_path}/omniorb.pth /root/.pyenv/versions/3.6.0/lib/python3.6/site-packages && \
        mv ${omniORB_path}/omniorb.pth /root/.pyenv/versions/omniORB/lib/python3.6/site-packages && \
    
        cd ${omniORB_path} && \
        mv /tmp/idl* . && \
        tar xvfj idl.tar.bz2 && rm idl.tar.bz2" && \
    
    /bin/bash -c "source ~/.bash_profile" && \

    yum clean packages && \
    rm -rf /tmp/* /var/tmp/*

RUN echo 'export LD_LIBRARY_PATH="${omniORB_path}/omniORB_install/lib"' >> ~/.bash_profile && \
    echo 'export PATH="${omniORB_path}/omniORB_install/bin:$PATH"' >> ~/.bash_profile && \
    /bin/bash -c "source ~/.bash_profile"

ENTRYPOINT /bin/bash
