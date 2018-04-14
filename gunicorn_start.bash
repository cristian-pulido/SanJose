#!/bin/bash

NAME="SanJose"                                   # Name of the application
DJANGODIR=/home/ubuntu/SanJose               # Django project directory
SOCKFILE=/home/ubuntu/django_env/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                         # the user to run as
GROUP=ubuntu                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=SanJose.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=SanJose.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

source /home/ubuntu/.virtualenvs/ambiente1/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn --bind 0.0.0.0:8000 SanJose.wsgi



