#!/usr/bin/env bash

cd /var/www/thedatalab/thedatalab

. /etc/profile.d/thedatalab.sh && exec ../../venv/bin/gunicorn frontend.wsgi -c ../deploy/gunicorn-thedatalab.conf.py
