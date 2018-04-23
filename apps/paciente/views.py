
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from apps.paciente.forms import PacienteForm, MedicoForm
from apps.paciente.models import Candidato, Medico
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
        if self.object.imagen != 'None':
            img = self.object.imagen
            s = Sujeto.objects.get(imagen=img)
            s.estado = 3
            s.save()
        else:
            s = self.objects.sujeto

        return reverse_lazy('sujeto', args=[s.pk])


class PacienteList(ListView):
    model = Candidato
    template_name = 'paciente/paciente_listar.html'

class MedicoCreate(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'paciente/medico_form.html'
    success_url = reverse_lazy('upload-new')

class MedicoList(ListView):
    model = Medico
    template_name = 'paciente/medico_listar.html'

class MedicoUpdate(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'paciente/medico_form.html'
    # a donde va dirigido
    success_url = reverse_lazy('medico_listar')

class MedicoDelete(DeleteView):
    model = Medico
    template_name = 'paciente/medico_eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('medico_listar')


