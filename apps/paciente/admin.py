from django.contrib import admin

# Register your models here.
from apps.paciente.models import Candidato, Dprevio, Medico

admin.site.register(Candidato)
admin.site.register(Dprevio)
admin.site.register(Medico)

