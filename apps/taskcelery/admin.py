from django.contrib import admin




# Register your models here.
from apps.taskcelery.models import taskc

admin.site.register(taskc)
