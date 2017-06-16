#!/bin/bash
#
# install.sh - install carbon-http files
#

cp carbon-http-graphite.conf /etc/apache/sites-available/
mkdir /usr/share/carbon-http
cp carbon-http.wsgi /usr/share/carbon-http/
service apache2 restart

