from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from apps.validacion.forms import Campos_defectoForm, gruposForm, pipelinesForm
from apps.validacion.models import Campos_defecto, Campostagimg, Taskgroup, Pipeline
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


class TaskgroupCreate(CreateView):
    model = Taskgroup
    form_class = gruposForm
    template_name = 'validacion/grupos_form.html'


    def get_success_url(self):
        log.info("--------------------- Creacion Grupo de Tareas" + str(self.object.nombre) + "---------------------")
        return reverse_lazy('login')

class TaskgroupUpdate(UpdateView):
    model = Taskgroup
    form_class = gruposForm
    template_name = 'validacion/grupos_form.html'

    def get_success_url(self):
        log.info("--------------------- Editar Grupo de Tareas" + str(self.object.nombre) + "---------------------")
        return reverse_lazy('login')

class TaskgroupDelete(DeleteView):
    model = Taskgroup
    # a donde va dirigido
    template_name = 'validacion/grupos_eliminar.html'
    def get_success_url(self):
        log.info("--------------------- Eliminar Grupo de Tareas" + str(
            self.object.nombre) + "---------------------")
        return reverse_lazy('login')

class PipelinesCreate(CreateView):
    model = Pipeline
    form_class = pipelinesForm
    template_name = 'validacion/pipeline_form.html'


    def get_success_url(self):
        log.info("--------------------- Creacion Pipeline " + str(self.object.nombre) + "---------------------")

        return reverse_lazy('login')

class PipelinesUpdate(UpdateView):
    model = Pipeline
    form_class = pipelinesForm
    template_name = 'validacion/pipeline_form.html'

    def get_success_url(self):
        log.info("--------------------- Editar Pipeline " + str(self.object.nombre) + "---------------------")
        return reverse_lazy('login')

class PipelinesDelete(DeleteView):
    model = Pipeline
    # a donde va dirigido
    template_name = 'validacion/pipeline_eliminar.html'
    def get_success_url(self):
        log.info("--------------------- Eliminar Pipeline " + str(self.object.nombre) + "---------------------")
        return reverse_lazy('login')

class PipelinesList(ListView):
    model = Pipeline
    template_name = 'validacion/pipeline_listar.html'
    log.info("Vista pipelines")




