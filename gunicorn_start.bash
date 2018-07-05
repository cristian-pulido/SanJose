#!/bin/bash

NAME="SanJose"                                   # Name of the application
DJANGODIR=/home/colciencias/SanJose               # Django project directory
SOCKFILE=/home/colciencias/django_env/run/gunicorn.sock  # we will communicte using this unix socket
USER=colciencias                                         # the user to run as
GROUP=colciencias                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=SanJose.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=SanJose.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

source /home/colciencias/.virtualenvs/trabajo/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
cd /home/colciencias/SanJose
#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000
./manage.py runserver 0.0.0.0:8000

