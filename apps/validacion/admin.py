from django.contrib import admin

from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto, Realineacion, Snr, Task, \
    Taskgroup, Pipeline

admin.site.register(Tipoimagenes)
admin.site.register(Tagsdicom)
admin.site.register(Campostagimg)
admin.site.register(Campos_defecto)
admin.site.register(Realineacion)
admin.site.register(Snr)
admin.site.register(Task)
admin.site.register(Taskgroup)
admin.site.register(Pipeline)
