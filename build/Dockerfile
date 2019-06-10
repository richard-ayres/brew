FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3 python3-flask python3-flask-sqlalchemy python3-sqlalchemy-utils \
                        python3-mysqldb python3-yaml python3-arrow ipython3 python3-pip
RUN pip3 install pymysql
RUN pip3 install jupyter
RUN pip3 install inotify

RUN apt-get -y install apache2 libapache2-mod-wsgi-py3

COPY brew.conf /etc/apache2/sites-available
RUN a2enmod wsgi && a2ensite brew

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
