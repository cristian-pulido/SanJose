from django.contrib import admin

from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto

admin.site.register(Tipoimagenes)
admin.site.register(Tagsdicom)
admin.site.register(Campostagimg)
admin.site.register(Campos_defecto)
