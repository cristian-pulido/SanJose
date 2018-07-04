#!/bin/bash

source /home/colciencias/.virtualenvs/trabajo/bin/activate

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
cd /home/colciencias/SanJose
celery worker -A SanJose --loglevel=INFO
