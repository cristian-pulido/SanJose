#!/bin/bash

source /home/colciencias/Envs/trabajo/bin/activate

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
cd /home/colciencias/SanJose
celery worker -A SanJose --without-mingle --loglevel=INFO --concurrency=3 -n sj@%h -f=/home/colciencias/media/celery.log

# --broker=amqp://col1:col1@localhost:5672/sanjose
