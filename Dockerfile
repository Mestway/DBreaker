FROM ubuntu:16.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y git

RUN apt-get update \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update \
    && apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
    && python3.6 -m pip install pip --upgrade \
    && python3.6 -m pip install wheel \
    && ln -s /usr/bin/python3.6 python

RUN apt-get update && \
  apt-get install -y --no-install-recommends locales && \
  locale-gen en_US.UTF-8 && \
  apt-get dist-upgrade -y && \
  apt-get --purge remove openjdk* && \
  echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections && \
  echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" > /etc/apt/sources.list.d/webupd8team-java-trusty.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886 && \
  apt-get update && \
  apt-get install -y --no-install-recommends oracle-java8-installer oracle-java8-set-default && \
  apt-get clean all

RUN apt-get update && \
    apt-get install -y maven

RUN export DEBIAN_FRONTEND=noninteractive
ENV MYSQL_ROOT_PASS root
RUN echo "mysql-server mysql-server/root_password password ${MYSQL_ROOT_PASS}" | debconf-set-selections  && \
    echo "mysql-server mysql-server/root_password_again password ${MYSQL_ROOT_PASS}" | debconf-set-selections && \
    apt-get -q -y install mysql-server

RUN find /var/lib/mysql/mysql -exec touch -c -a {} + && service mysql start

RUN git clone --recursive https://github.com/Mestway/dbreaker.git
WORKDIR dbreaker
