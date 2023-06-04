#!/bin/bash
source /home/www/code/realworker/env/bin/activate
exec gunicorn -c "/home/www/code/realworker/gunicorn_config.py" realworker.wsgi

