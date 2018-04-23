
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from apps.fileupload.models import Picture
from apps.paciente.models import Candidato
from apps.sujeto.forms import SujetoForm
from apps.sujeto.models import Sujeto


class SujetoCreate(CreateView):
    model = Sujeto
    form_class = SujetoForm
    template_name = 'Sujeto/sujeto_form.html'
    success_url = reverse_lazy('upload-new')

class SujetoUpdate(UpdateView):
    model = Sujeto
    form_class = SujetoForm
    template_name = 'Sujeto/sujeto_form.html'
    def get_success_url(self):
        s = self.object
        if s.estado < 2 :
            s.estado=2
            s.save()
        try:
            if s.inscrito==True:
                img=s.imagen
                c=Candidato.objects.create(imagen=img)
            else:
                c = Candidato.objects.create(sujeto=s, ci3=False, ci4=False)
            return reverse_lazy('paciente_editar', args=[c.pk])
        except:
            print("")

class SujetoDelete(DeleteView):
    model = Sujeto
    template_name = 'Sujeto/sujeto_eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('paciente_listar')


class SujetoList(DetailView):
    model = Sujeto
    template_name = 'Sujeto/formularios.html'


