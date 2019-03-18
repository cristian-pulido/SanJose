from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from apps.validacion.forms import Campos_defectoForm
from apps.validacion.models import Campos_defecto, Campostagimg
from apps.validacion.templatetags.scripts_validacion import campos_a_mostrar

import logging

log=logging.getLogger('django')

class Campos_defectoCreate(CreateView):
    model = Campos_defecto
    form_class = Campos_defectoForm
    template_name = 'validacion/filtro_form.html'


    def get_success_url(self):
        o = self.object
        if o.precision == None:
            o.precision = 0
        if o.v_esperado == None:
            o.v_esperado = ""
        if o.medidas == None:
            o.medidas = ""
        o.save()
        campos_a_mostrar()
        log.info("--------------------- Creacion Campos Defecto" + str(o)+"---------------------")
        return reverse_lazy('filtro_listar')


class Campos_defectoUpdate(UpdateView):
    model = Campos_defecto
    form_class = Campos_defectoForm
    template_name = 'validacion/filtro_form.html'
    # a donde va dirigido
    def get_success_url(self):
        o = self.object
        if o.precision == None:
            o.precision = 0
        if o.v_esperado == None:
            o.v_esperado = ""
        if o.medidas == None:
            o.medidas = ""
        o.save()
        campos_a_mostrar()
        log.info("--------------------- Editar Campos Defecto" + str(o) + "---------------------")
        return reverse_lazy('filtro_listar')


class Campos_defectoList(ListView):
    model = Campos_defecto
    template_name = 'validacion/filtros.html'

class Campos_defectoDelete(DeleteView):
    model = Campos_defecto
    # a donde va dirigido
    def get_success_url(self):
        campo = Campostagimg.objects.filter(tag=self.object.tag, imagen=self.object.imagen)
        for c in campo:
            c.visible = False
            c.save()
            c.medidas = ""
            c.save()
            c.precision = 0
            c.save()
            c.v_esperado = ""
            c.save()
        log.info("--------------------- Eliminar Campos Defecto" + str(c) + "---------------------")
        return reverse_lazy('filtro_listar')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)






