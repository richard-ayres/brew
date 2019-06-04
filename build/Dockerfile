FROM ubuntu:18.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-flask python3-flask-sqlalchemy python3-sqlalchemy-utils
RUN apt-get -y install ipython3 python3-pip
RUN pip3 install jupyter
RUN apt-get -y install python3-mysqldb
RUN pip3 install pymysql

ENTRYPOINT ["/usr/local/bin/jupyter", "notebook", "--allow-root", "--ip=0.0.0.0"]
#ENTRYPOINT ["/bin/sleep", "infinity"]
