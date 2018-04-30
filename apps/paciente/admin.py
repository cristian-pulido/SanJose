from django.contrib import admin

# Register your models here.
from apps.paciente.models import Candidato, Dprevio, Medico, Apatologicos, Ingreso, Radiologia, Uci

admin.site.register(Candidato)
admin.site.register(Ingreso)
admin.site.register(Radiologia)
admin.site.register(Uci)
admin.site.register(Dprevio)
admin.site.register(Apatologicos)
admin.site.register(Medico)

