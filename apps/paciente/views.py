from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.paciente.forms import PacienteForm
from apps.paciente.models import Candidato


class PacienteCreate(CreateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'Sujeto/sujeto_form.html'
    success_url = reverse_lazy('upload-new')

class PacienteUpdate(UpdateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'Sujeto/sujeto_form.html'
    # a donde va dirigido
    success_url = reverse_lazy('upload-new')