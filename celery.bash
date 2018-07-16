#!/bin/bash

source /home/colciencias/Envs/trabajo/bin/activate

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
cd /home/colciencias/SanJose
celery worker -A SanJose --loglevel=INFO
