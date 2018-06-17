#!/bin/bash

source /home/ubuntu/.virtualenvs/ambiente/bin/activate

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
cd /home/ubuntu/SanJose
celery worker -A SanJose --loglevel=INFO
