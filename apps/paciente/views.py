
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from apps.paciente.forms import PacienteForm, MedicoForm, IngresoForm, RadiologiaForm, UciForm, NeurologiaForm
from apps.paciente.models import Candidato, Medico, Ingreso, Radiologia, Uci, Neurologia


class PacienteCreate(CreateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'
    success_url = reverse_lazy('paciente_listar')


class PacienteUpdate(UpdateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'
    # a donde va dirigido

    def get_success_url(self):
        p=self.object
        if p.estado==0:
            p.estado=1
            p.save()
        return reverse_lazy('paciente', args=[p.pk])

class IngresoUpdate(UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'paciente/ingreso_form.html'
    # a donde va dirigido

    def get_success_url(self):
        i=self.object
        p=i.candidato
        if p.estado==1:
            p.estado=2
            p.save()
        return reverse_lazy('paciente', args=[p.pk])


class UciUpdate(UpdateView):
    model = Uci
    form_class = UciForm
    template_name = 'paciente/uci_form.html'
    # a donde va dirigido

    def get_success_url(self):
        u=self.object
        p=u.candidato
        if p.estado==2:
            p.estado=3
            p.save()
        return reverse_lazy('paciente', args=[p.pk])

class NeurologiaUpdate(UpdateView):
    model = Neurologia
    form_class = NeurologiaForm
    template_name = 'paciente/neurologia_form.html'
    # a donde va dirigido

    def get_success_url(self):
        n=self.object
        p=n.candidato
        if p.estado==3:
            p.estado=4
            p.save()
        return reverse_lazy('paciente', args=[p.pk])

class RadiologiaUpdate(UpdateView):
    model = Radiologia
    form_class = RadiologiaForm
    template_name = 'paciente/radiologia_form.html'
    # a donde va dirigido

    def get_success_url(self):
        r=self.object
        p=r.candidato
        if p.estado==4:
            p.estado=5
            p.save()
        return reverse_lazy('paciente', args=[p.pk])



class PacienteView(DetailView):
    model = Candidato
    template_name = 'paciente/formularios.html'

class PacienteList(ListView):
    model = Candidato
    template_name = 'paciente/paciente_listar.html'

class PacienteDelete(DeleteView):
    model = Candidato
    template_name = 'paciente/paciente_eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('paciente_listar')

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


