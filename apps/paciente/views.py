
# Create your views here.
import os
import shutil

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from apps.paciente.forms import PacienteForm, MedicoForm, IngresoForm, RadiologiaForm, UciForm, NeurologiaForm, \
    BoldForm, MayorForm, InformanteForm
from apps.paciente.models import Candidato, Medico, Ingreso, Radiologia, Uci, Neurologia, Bold, Mayor, Informante


class PacienteCreate(CreateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'

    def get_success_url(self):
        p=self.object
        criterios_inclusion=p.ci3*1+p.ci4*1
        criterios_exclusion = p.ce1 * 1 + p.ce2 * 1 + p.ce3 * 1 + p.ce4 * 1
        if criterios_inclusion == 2 and criterios_exclusion == 0:
            p.inscrito = True
            p.save()

        try:
            os.mkdir("/home/ubuntu/media/img/sujeto" + str(p.sujeto_numero))
        except:
            ""
        try:
            shutil.move('/home/ubuntu/media/' + str(p.archivo), '/home/ubuntu/media/img/sujeto' + str(p.sujeto_numero))
            p.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(p.archivo)[11:]
            p.save()
        except:
            ""

        return reverse_lazy('paciente_listar')


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
        try:
            if hasattr(p, 'picture'):
                shutil.move('/home/ubuntu/media/' + str(p.archivo), '/home/ubuntu/media/img/sujeto' + str(p.sujeto_numero))
                p.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(p.archivo)[11:]
                p.save()

            else:
                try:
                    os.mkdir("/home/ubuntu/media/img/sujeto" + str(p.sujeto_numero))
                except:
                    ""
                shutil.move('/home/ubuntu/media/' + str(p.archivo), '/home/ubuntu/media/img/sujeto' + str(p.sujeto_numero))
                p.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(p.archivo)[11:]
                p.save()

        except:
            ""

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
        try:
            shutil.move('/home/ubuntu/media/' + str(i.archivo), '/home/ubuntu/media/img/sujeto' + str(p.sujeto_numero))
            i.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(i.archivo)[11:]
            i.save()
        except:
            ""
        try:
            if i.archivofirma != None:
                shutil.move('/home/ubuntu/media/' + str(i.archivofirma), '/home/ubuntu/media/img/sujeto' + str(p.sujeto_numero))
                i.archivofirma = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(i.archivofirma)[11:]
                i.save()

        except:
            ""
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

class BoldUpdate(UpdateView):
    model = Bold
    form_class = BoldForm
    template_name = 'paciente/bold_form.html'
    # a donde va dirigido

    def get_success_url(self):
        b=self.object
        p=b.candidato
        if p.estado==5:
            p.estado=6
            p.save()
        return reverse_lazy('paciente', args=[p.pk])

class MayorUpdate(UpdateView):
    model = Mayor
    form_class = MayorForm
    template_name = 'paciente/mayor_form.html'
    # a donde va dirigido

    def get_success_url(self):
        m=self.object
        p=m.candidato
        i=p.informante
        i.fechaentrevista = p.mayor.fechaentrevista
        i.neuropsicologa = p.mayor.neuropsicologa
        i.informante = p.mayor.informante
        i.parentezco = p.mayor.parentezco
        i.confiable = p.mayor.confiable
        i.save()
        return reverse_lazy('informante_editar', args=[i.pk])

class InformanteUpdate(UpdateView):
    model = Informante
    form_class = InformanteForm
    template_name = 'paciente/informante_form.html'
    # a donde va dirigido

    def get_success_url(self):
        i=self.object
        p=i.candidato
        if p.estado==6:
            p.estado=7
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
    success_url = reverse_lazy('paciente_listar')

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


