#!/usr/bin/env bash

cd /var/www/thedatalab_staging/thedatalab

. /etc/profile.d/thedatalab_staging.sh && exec ../../venv/bin/gunicorn frontend.wsgi -c ../deploy/gunicorn-thedatalab_staging.conf.py
