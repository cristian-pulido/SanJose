from django.contrib import admin

# Register your models here.
from apps.paciente.models import Candidato, Dprevio, Medico, Apatologicos, Ingreso, Radiologia, Uci, Neurologia, Bold, \
    Mayor, Informante, Seguimiento, Control, Cambioradiologia, Moca, Valorablenps, Neuropsi, Parametrosmotioncorrect, \
    Lectura_resonancia

admin.site.register(Candidato)
admin.site.register(Cambioradiologia)
admin.site.register(Control)
admin.site.register(Ingreso)
admin.site.register(Radiologia)
admin.site.register(Uci)
admin.site.register(Seguimiento)
admin.site.register(Neurologia)
admin.site.register(Bold)
admin.site.register(Mayor)
admin.site.register(Informante)
admin.site.register(Dprevio)
admin.site.register(Apatologicos)
admin.site.register(Moca)
admin.site.register(Valorablenps)
admin.site.register(Medico)
admin.site.register(Neuropsi)
admin.site.register(Parametrosmotioncorrect)
admin.site.register(Lectura_resonancia)


