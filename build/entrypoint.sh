#!/usr/bin/env bash
set -e

/usr/sbin/apachectl -k start
/usr/local/bin/jupyter notebook --allow-root --ip=0.0.0.0 &
#(cd /var/www/brew; env LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_APP=brew.py flask run --host=0.0.0.0) &

sleep infinity
