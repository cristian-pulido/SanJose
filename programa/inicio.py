from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

def grupos():
    group = Group(name='cargador')
    group.save()
