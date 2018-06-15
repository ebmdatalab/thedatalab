#!/usr/bin/env bash

cd /var/www/thedatalab_staging/thedatalab/thedatalab

. /etc/profile.d/thedatalab_staging.sh && exec ../../venv/bin/gunicorn thedatalab.wsgi -c ../deploy/gunicorn-thedatalab_staging.conf.py
