from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

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
    # a donde va dirigido
    success_url = reverse_lazy('upload-new')

