# Version: 0.1.0
FROM vladworldss/omniorb
MAINTAINER Vladimir Gerasimenko <vladworldss@yandex.ru>
LABEL name="vladworldss/omniorb" \
      vendor="CentOS" \
      license="GPLv2" \
      build-date="20170628"

ADD . /tmp/
ENV LANG en_US.UTF-8

ENV base_dir=/root/corba/omniORB
RUN /bin/bash -c "source ~/.bash_profile && \
                cp -avr /tmp/* ${base_dir} && \
                cd ${base_dir}/U2000 && \
                python idl.py" && \
    yum clean packages && \
    rm -rf /tmp/* /var/tmp/*

ENTRYPOINT /bin/bash
