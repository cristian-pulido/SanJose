import self
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.paciente.forms import PacienteForm
from apps.paciente.models import Candidato
from apps.sujeto.models import Sujeto


class PacienteCreate(CreateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'
    success_url = reverse_lazy('upload-new')

class PacienteUpdate(UpdateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'
    # a donde va dirigido

    def get_success_url(self):
        img=self.object.imagen
        s=Sujeto.objects.get(imagen=img)
        s.estado=3
        s.save()
        return reverse_lazy('sujeto', args=[s.pk])


