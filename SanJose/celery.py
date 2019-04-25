import os
from celery import Celery
from celery._state import _set_current_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SanJose.settings')

app = Celery('SanJose',broker='amqp://col1:col1@localhost:5672/sanjose')
app.config_from_object('django.conf:settings', namespace='SanJose')
_set_current_app(app)
app.autodiscover_tasks()
