#!/usr/bin/env bash

cd /var/www/thedatalab/thedatalab/thedatalab

. /etc/profile.d/thedatalab.sh && ../../venv/bin/gunicorn thedatalab.wsgi -c ../deploy/gunicorn-thedatalab.conf.py
