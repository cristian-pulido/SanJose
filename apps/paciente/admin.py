from django.contrib import admin

# Register your models here.
from apps.paciente.models import Candidato,Dprevio

admin.site.register(Candidato)
admin.site.register(Dprevio)

