from django.contrib import admin

from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto, Realineacion, Snr,  img_to_show

admin.site.register(Tipoimagenes)
admin.site.register(Tagsdicom)
admin.site.register(Campostagimg)
admin.site.register(Campos_defecto)
admin.site.register(Realineacion)
admin.site.register(Snr)
admin.site.register(img_to_show)
