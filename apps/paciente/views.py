
# Create your views here.
import os
import shutil

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView


from apps.paciente.forms import PacienteForm, MedicoForm, IngresoForm, RadiologiaForm, UciForm, NeurologiaForm, \
    BoldForm, MayorForm, InformanteForm, SeguimientoForm
from apps.paciente.models import Candidato, Medico, Ingreso, Radiologia, Uci, Neurologia, Bold, Mayor, Informante, \
    Seguimiento, Control


class PacienteCreate(CreateView):
    model = Candidato
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'


    def get_success_url(self):
        p=self.object
        cantidad=len(Candidato.objects.all())
        if cantidad == 1:
            p.sujeto_numero=1
            p.save()



            try:
                os.mkdir(settings.MEDIA_ROOT+"/img")
            except:
                ""
        else:
            C=Candidato.objects.order_by("sujeto_numero").last()
            p.sujeto_numero=C.sujeto_numero+1
            p.save()
        p.ci=""
        p.save()
        Diagnosticos=len(p.D_neuro_logico_psiquiatrico_previo.all())
        if Diagnosticos > 0:
            p.estado=1
            p.save()

        try:
            os.mkdir(settings.MEDIA_ROOT+"/img/sujeto" + str(p.sujeto_numero))
        except:
            ""
        try:
            shutil.move(settings.MEDIA_ROOT+'/' + str(p.archivo), settings.MEDIA_ROOT+'/img/sujeto' + str(p.sujeto_numero))
            p.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(p.archivo)[4:]
            p.save()
        except:
            ""
        messages.add_message(self.request, messages.INFO, "Se ha añadido el registro del sujeto "+str(p.sujeto_numero).zfill(4)+".")


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
            criterios_inclusion = p.ci3 * 1 + p.ci4 * 1
            criterios_exclusion = p.ce1 * 1 + p.ce2 * 1 + p.ce3 * 1 + p.ce4 * 1
            if criterios_inclusion == 2 and criterios_exclusion == 0:
                p.inscrito = True
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
        try:
            shutil.move(settings.MEDIA_ROOT+'/' + str(i.archivo), settings.MEDIA_ROOT+'/img/sujeto' + str(p.sujeto_numero))
            i.archivo = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(i.archivo)[4:]
            i.save()
        except:
            ""
        try:
            if i.archivofirma != None:
                shutil.move(settings.MEDIA_ROOT+'/' + str(i.archivofirma), settings.MEDIA_ROOT+'/img/sujeto' + str(p.sujeto_numero))
                i.archivofirma = '/img/sujeto' + str(p.sujeto_numero) + "/" + str(i.archivofirma)[4:]
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
        if u.continua_studio == 'NO':
            p.inscrito=False
            p.save()
            messages.add_message(self.request, messages.INFO,"Sujeto " + str(p.sujeto_numero).zfill(4) + " excluido.")
        if u.glasgowtotal_e != '0' and p.imagen == "":
            p.inscrito=False
            p.save()
            messages.add_message(self.request, messages.INFO,"Sujeto " + str(p.sujeto_numero).zfill(4) + " excluido por realizar evaluación de egreso sin tener archivos de imagen.")
        return reverse_lazy('paciente', args=[p.pk])

class NeurologiaUpdate(UpdateView):
    model = Neurologia
    form_class = NeurologiaForm
    template_name = 'paciente/neurologia_form.html'
    # a donde va dirigido

    def get_success_url(self):
        n=self.object
        p=n.candidato
        return reverse_lazy('paciente', args=[p.pk])

class RadiologiaUpdate(UpdateView):
    model = Radiologia
    form_class = RadiologiaForm
    template_name = 'paciente/radiologia_form.html'
    # a donde va dirigido

    def get_success_url(self):
        r=self.object
        p=r.candidato
        return reverse_lazy('paciente', args=[p.pk])

class BoldUpdate(UpdateView):
    model = Bold
    form_class = BoldForm
    template_name = 'paciente/bold_form.html'
    # a donde va dirigido

    def get_success_url(self):
        b=self.object
        p=b.candidato
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
        return reverse_lazy('paciente', args=[p.pk])

class SeguimientoUpdate(UpdateView):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = 'paciente/seguimiento_form.html'
    # a donde va dirigido

    def get_success_url(self):
        s=self.object
        p=s.candidato
        return reverse_lazy('paciente', args=[p.pk])




class PacienteView(DetailView):
    model = Candidato
    template_name = 'paciente/formularios.html'

class ControlView(DetailView):
    model = Control
    template_name = 'paciente/controles.html'

class PacienteList(ListView):
    model = Candidato
    template_name = 'paciente/paciente_listar.html'

class ControlList(ListView):
    model = Control
    template_name = 'paciente/controles_listar.html'

class PacienteDelete(DeleteView):
    model = Candidato
    template_name = 'paciente/paciente_eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('paciente_listar')

class ControlDelete(DeleteView):
    model = Control
    template_name = 'paciente/control_eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('controles_listar')


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


