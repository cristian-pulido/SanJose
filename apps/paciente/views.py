
# Create your views here.
import os
import shutil
from collections import Counter
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView


from apps.paciente.forms import PacienteForm, MedicoForm, IngresoForm, RadiologiaForm, UciForm, NeurologiaForm, \
    BoldForm, MayorForm, InformanteForm, SeguimientoForm, ControlForm, MocaForm, NeuropsiForm, LecturaresonanciaForm
from apps.paciente.models import Candidato, Medico, Ingreso, Radiologia, Uci, Neurologia, Bold, Mayor, Informante, \
    Seguimiento, Control, Moca, Valorablenps, Neuropsi, Lectura_resonancia


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
        if u.glasgowtotal_e == '0' and u.fechaegreso != None:
            u.fechaegreso = ""
            u.horaegreso = ""
            u.save()
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

class LecturaUpdate(UpdateView):
    model = Lectura_resonancia
    form_class = LecturaresonanciaForm
    template_name = 'paciente/lectura_form.html'
    # a donde va dirigido

    def get_success_url(self):
        l=self.object
        if l.candidato != None:
            p=l.candidato
            return reverse_lazy('paciente', args=[p.pk])
        if l.control != None:
            p=l.control
            return reverse_lazy('control', args=[p.pk])

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
        hoy = datetime.today().strftime('%Y-%m-%d')
        messages.add_message(self.request, messages.INFO,"Se ha añadido el seguiento del sujeto " + str(p.sujeto_numero).zfill(4) + " para la fecha "+ s.fechaseguimiento.strftime('%d/%m/%Y'))
        if str(s.fechaseguimiento) == hoy:
            return reverse_lazy('paciente', args=[p.pk])
        else:
            return reverse_lazy('crear_seguimiento', args=[p.pk])


class MocaUpdate(UpdateView):
    model = Moca
    form_class = MocaForm
    template_name = 'paciente/moca_form.html'
    # a donde va dirigido

    def get_success_url(self):
        b=self.object
        p=b.candidato
        n = Valorablenps.objects.get_or_create(sujeto=p)[0]
        n.valorable=True
        n.save()
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


class ControlCreate(CreateView):
    model = Control
    form_class = ControlForm
    template_name = 'paciente/control_form.html'


    def get_success_url(self):
        c=self.object
        cantidad=len(Control.objects.all())
        if cantidad == 1:
            c.numero=1
            c.save()
            try:
                os.mkdir(settings.MEDIA_ROOT + "/controles")
            except:
                ""
            os.mkdir(settings.MEDIA_ROOT + "/controles/control1")
        else:
            flag = False
            i = 2
            while flag == False:
                try:
                    c.numero=i
                    c.save()
                    flag = True
                except:
                    ""
                i = i + 1
            os.mkdir(settings.MEDIA_ROOT + "/controles/control" + str(c.numero))
        nacimiento = c.fecha_nacimiento
        hoy = datetime.now().date()
        dt = hoy - nacimiento
        c.edad = int(dt.days / 365)
        c.save()
        messages.add_message(self.request, messages.INFO,"Se ha añadido el registro del control " + str(c.numero).zfill(4) + ".")
        return reverse_lazy('controles_listar')

class ControlUpdate(UpdateView):
    model = Control
    form_class = ControlForm
    template_name = 'paciente/control_form.html'
    success_url = reverse_lazy('controles_listar')

class NeuropsiUpdate(UpdateView):
    model = Neuropsi
    form_class = NeuropsiForm
    template_name = 'paciente/neuropsi_form.html'

    def get_success_url(self):
        n=self.object
        p=n.candidato

        ## escolaridad 0-Analfabeta  1-4-Primaria  5-9 bachillerato  10-24  tecnico-profesional
        escolaridad=p.ingreso.n_educativo
        edad=p.edad

        #resultado
        resultado=[]
        ## orientacion
        orientacion=[]
        #tiempo
        tiempo=int(n.orientacion_tiempo)
        if tiempo == 3:
            orientacion.append("Normal")
        elif tiempo == 2:
            if edad >= 66 :
                orientacion.append("Normal")
            elif edad >= 31 and edad <=50:
                if escolaridad == 'Técnico' or escolaridad == 'Profesional' or escolaridad == 'Bachillerato':
                    orientacion.append("Severo")
                else:
                    orientacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    orientacion.append("Normal")
        elif tiempo == 1:
            if edad >= 31 and edad <=50:
                orientacion.append("Severo")
            elif edad >= 66 :
                if escolaridad == 'Técnico' or escolaridad == 'Profesional':
                    orientacion.append("Moderado")
                elif escolaridad == 'Analfabeta':
                    orientacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    orientacion.append("Severo")
        else:
            orientacion.append("Severo")

        #lugar
        lugar=int(n.orientacion_espacio)
        if lugar == 2:
            orientacion.append("Normal")
        elif lugar == 1:
            if edad >= 66 :
                if escolaridad == 'Técnico' or escolaridad == 'Profesional' or escolaridad == 'Analfabeta':
                    orientacion.append("Moderado")
                else:
                    orientacion.append("Severo")
            elif edad >= 31 and edad <=50:
                if escolaridad == 'Técnico' or escolaridad == 'Profesional':
                    orientacion.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    orientacion.append("Normal")
                else:
                    orientacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    orientacion.append("Moderado")
        else:
            orientacion.append("Severo")


        # persona
        persona = int(n.orientacion_persona)
        if lugar == 1:
            orientacion.append("Normal")
        else:
            if edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    orientacion.append("Moderado")
            else:
                orientacion.append("Severo")

        n.orientacion=Counter(orientacion).most_common(1)[0][0]
        resultado.append(n.orientacion)

        ## Atencion y concentracion
        atencion=[]
        #digitos
        digitos=int(n.atencion_digitos)
        if digitos >= 5:
            if edad >= 31 and edad <=50 and digitos == 5:
                if escolaridad == 'Técnico' or escolaridad == 'Profesional' or escolaridad == 'Bachillerato':
                    atencion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    orientacion.append("Normal Alto")
            else:
                atencion.append("Normal Alto")
        elif digitos == 4 or digitos == 3:
            if digitos == 4 and escolaridad == 'Primaria' and not (edad >= 31 and edad <= 50):
                atencion.append("Normal Alto")
            else:
                atencion.append("Normal")
        elif digitos == 2:
            if escolaridad == 'Profesional':
                atencion.append("Moderado")
            elif escolaridad == 'Técnico':
                if edad >= 66 and edad <= 85:
                    atencion.append("Moderado")
            else:
                atencion.append("Normal")
        else:
            if edad >= 66 and edad <= 85 and escolaridad == 'Bachillerato':
                atencion.append("Moderado")
            elif edad >= 31 and edad <=50 and escolaridad == 'Analfabeta':
                atencion.append("Moderado")
            else:
                atencion.append("Severo")
        # deteccion visual
        visual = int(n.atencion_visual)
        if visual == 16 :
            if edad >= 66 and edad <= 85:
                atencion.append("Normal Alto")
            elif edad >= 31 and edad <=50:
                if escolaridad == 'Primaria':
                    atencion.append("Normal Alto")
                else:
                    atencion.append("Normal")
            elif edad >= 51 and edad <=65:
                if escolaridad == 'Primaria':
                    atencion.append("Normal Alto")
        elif visual >= 13 and visual <=15:
            if edad >= 31 and edad <= 50:
                atencion.append("Normal")
            elif edad >= 51 and edad <=65:
                if escolaridad == 'Primaria':
                    atencion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Bachillerato':
                    if visual == 15:
                        atencion.append("Normal Alto")
                    else:
                        atencion.append("Normal")
                else:
                    atencion.append("Normal")
        elif visual >= 7 and visual <=12:
            if edad >= 66 and edad <= 85:
                atencion.append("Normal")
            elif edad >= 51 and edad <=65:
                if escolaridad == 'Primaria':
                    atencion.append("Normal")
            elif edad >= 31 and edad <=50:
                if escolaridad == 'Analfabeta':
                    atencion.append("Normal")
                elif escolaridad == 'Primaria':
                    if visual > 8:
                        atencion.append("Normal")
                    else:
                        atencion.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if visual > 8:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                elif escolaridad == 'Bachillerato' or escolaridad == 'Profesional':
                    if visual > 10:
                        atencion.append("Normal")
                    else:
                        atencion.append("Moderado")
        else:
            if edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    atencion.append("Severo")
                elif escolaridad == 'Bachillerato':
                    if visual > 3:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                elif escolaridad == 'Primaria':
                    if visual > 1:
                        atencion.append("Normal")
                    elif visual == 1:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                else:
                    atencion.append("Normal")
            elif edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if visual == 7:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                elif escolaridad == 'Bachillerato':
                    atencion.append("Severo")
                elif escolaridad == 'Primaria':
                    if visual > 4:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                else:
                    if visual == 6:
                        atencion.append("Normal")
                    elif visual < 6 and visual > 2:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if visual > 5:
                        atencion.append("Normal")
                    elif visual == 4 and visual ==5:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
                else:
                    if visual == 6:
                        atencion.append("Normal")
                    elif visual < 6 and visual > 2:
                        atencion.append("Moderado")
                    else:
                        atencion.append("Severo")
        # 20-3
        a_20_3 = int(n.atencion_20_3)
        if a_20_3 == 4 or a_20_3 == 5:
            if edad >= 31 and edad <= 50:
                atencion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    atencion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if a_20_3 == 4 and escolaridad == 'Bachillerato':
                    atencion.append("Moderado")
                else:
                    atencion.append("Normal")
        elif a_20_3 == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    atencion.append("Moderado")
                else:
                    atencion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    atencion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    atencion.append("Normal")
                elif escolaridad == 'Bachillerato':
                    atencion.append("Severo")
                else:
                    atencion.append("Moderado")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    atencion.append("Severo")
                elif a_20_3 == 2 and ( escolaridad == 'Analfabeta' or escolaridad == 'Primaria'):
                    atencion.append("Normal")
                else:
                    atencion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if a_20_3 == 0:
                        atencion.append("Severo")
                    else:
                        atencion.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    atencion.append("Normal")
                elif escolaridad == 'Bachillerato' or escolaridad == 'Primaria':
                    atencion.append("Severo")
                else:
                    if a_20_3 == 0:
                        atencion.append("Severo")
                    else:
                        atencion.append("Moderado")

        n.atencion = Counter(atencion).most_common(1)[0][0]
        resultado.append(n.atencion)

        ## Memoria

        ## codificacion
        codificacion=[]
        #palabras
        palabras=int(n.codificacion_palabras)
        if palabras == 6:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    codificacion.append("Normal")
                else:
                    codificacion.append("Normal Alto")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal Alto")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    codificacion.append("Normal")
                else:
                    codificacion.append("Normal Alto")
        elif palabras == 5 or palabras == 4:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' and palabras == 4:
                    codificacion.append("Moderado")
                else:
                    codificacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    codificacion.append("Normal")
                else:
                    if palabras == 5:
                        codificacion.append("Normal Alto")
                    else:
                        codificacion.append("Normal")
        elif palabras == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' :
                    codificacion.append("Severo")
                else:
                    codificacion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Bachillerato' or escolaridad == 'Primaria':
                    codificacion.append("Moderado")
                else:
                    codificacion.append("Normal")
        else:
            if edad >= 31 and edad <= 50:
                codificacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Severo")
            elif edad >= 66 and edad <= 85:
                if palabras == 2:
                    if escolaridad == 'Analfabeta':
                        codificacion.append("Normal")
                    elif escolaridad == 'Profesional' or escolaridad == 'Técnico':
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Severo")
                else:
                    codificacion.append("Severo")

                if escolaridad == 'Bachillerato' or escolaridad == 'Primaria':
                    codificacion.append("Severo")
                else:
                    codificacion.append("Normal")
        # codificacion figura
        cfigura = int(n.codificacion_figura)
        if cfigura >= 11 and cfigura <= 12: 
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta':
                    codificacion.append("Normal Alto")
                else:
                    codificacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    codificacion.append("Normal")
                elif escolaridad == 'Primaria':
                    if cfigura == 12:
                        codificacion.append("Normal Alto")
                    else:
                        codificacion.append("Normal")
                else:
                    codificacion.append("Normal Alto")
        elif cfigura >= 10 and cfigura < 11:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if cfigura > 10:
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Severo")
                else:
                    codificacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    codificacion.append("Normal Alto")
                else:
                    codificacion.append("Normal")
        elif cfigura >= 8 and cfigura < 10:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                    codificacion.append("Normal")
                elif escolaridad == 'Bachillerato':
                    if cfigura == 8:
                        codificacion.append("Severo")
                    else:
                        codificacion.append("Moderado")
                else:
                    codificacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Bachillerato':
                    if cfigura < 9:
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Normal")
                else:
                    codificacion.append("Normal")
        elif cfigura >= 6 and cfigura < 8:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    codificacion.append("Severo")
                elif escolaridad == 'Primaria':
                    if cfigura < 7:
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Normal")
                else:
                    codificacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    codificacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if cfigura == 6:
                        codificacion.append("Severo")
                    else:
                        codificacion.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    codificacion.append("Moderado")
                else:
                    codificacion.append("Normal")
        elif cfigura >= 3 and cfigura < 6:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    codificacion.append("Severo")
                elif escolaridad == 'Primaria':
                    codificacion.append("Moderado")
                else:
                    if cfigura > 5 :
                        codificacion.append("Normal")
                    else:
                        codificacion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if cfigura >= 5:
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    codificacion.append("Severo")
                elif escolaridad == 'Primaria':
                    if cfigura < 4:
                        codificacion.append("Severo")
                    else:
                        codificacion.append("Moderado")
                else:
                    if cfigura == 3:
                        codificacion.append("Moderado")
                    else:
                        codificacion.append("Normal")
        else:
            codificacion.append("Severo")
            
        n.codificacion = Counter(codificacion).most_common(1)[0][0]
        resultado.append(n.codificacion)

        ## evocacion
        evocacion = []
        # espontanea
        espontanea = int(n.evocacion_espontanea)
        if espontanea >= 4 and espontanea <= 6:
            if edad >= 31 and edad <= 50:
                evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Primaria' or escolaridad == 'Analfabeta':
                    if espontanea == 6:
                        evocacion.append("Normal Alto")
                    else:
                        evocacion.append("Normal")
                else:
                    evocacion.append("Normal")
        
        elif espontanea == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    evocacion.append("Moderado")
                else:
                    evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                evocacion.append("Normal")
                
        elif espontanea == 2:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    evocacion.append("Moderado")
                else:
                    evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                evocacion.append("Normal")
                
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    evocacion.append("Severo")
                elif escolaridad == 'Primaria':
                    if espontanea == 1:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")
                else:
                    evocacion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if espontanea == 1:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Primaria' or escolaridad == 'Analfabeta':
                    evocacion.append("Normal")
                elif escolaridad == 'Bachillerato':
                    if espontanea == 1:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")
                else:
                    if espontanea == 1:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")

        # claves
        claves = int(n.evocacion_claves)
        if claves >= 4 and claves <= 6:
            if edad >= 31 and edad <= 50:
                evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Primaria':
                    if claves == 6 or claves == 5:
                        evocacion.append("Normal Alto")
                    else:
                        evocacion.append("Normal")
                else:
                    evocacion.append("Normal")

        elif claves == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta':
                    evocacion.append("Normal")
                else:
                    evocacion.append("Moderado")
            elif edad >= 66 and edad <= 85:
                evocacion.append("Normal")

        elif claves == 2:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Analfabeta':
                    evocacion.append("Moderado")
                else:
                    evocacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                evocacion.append("Normal")

        else:
            if edad >= 31 and edad <= 50:
                evocacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if claves == 2:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    evocacion.append("Moderado")
                else:
                    if claves == 1:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")

        # reconocimiento
        reconocimiento = int(n.evocacion_reconocimiento)
        if reconocimiento >= 4 and reconocimiento <= 6:
            if edad >= 31 and edad <= 50:
                if reconocimiento == 5 or reconocimiento == 6:
                    evocacion.append("Normal")
                elif reconocimiento == 4:
                    if escolaridad == 'Primaria':
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if reconocimiento == 4:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' and reconocimiento == 4:
                    evocacion.append("Moderado")
                else:
                    evocacion.append("Normal")
                    
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if reconocimiento == 0:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
                else:
                    evocacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if reconocimiento == 3:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    if reconocimiento < 2:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
                elif escolaridad == 'Primaria':
                    if reconocimiento == 3:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")
                else:
                    evocacion.append("Severo")

        # evocacion figura
        efigura = int(n.evocacion_figura)
        if efigura >= 10 and efigura <= 12:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta':
                    evocacion.append("Normal Alto")
                elif escolaridad == 'Primaria':
                    if efigura == 12:
                        evocacion.append("Normal Alto")
                    else:
                        evocacion.append("Normal")
                else:
                    evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if efigura >= 10.5:
                        evocacion.append("Normal Alto")
                    else:
                        evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    evocacion.append("Normal")
                elif escolaridad == 'Bachillerato':
                    if efigura == 12:
                        evocacion.append("Normal Alto")
                    else:
                        evocacion.append("Normal")
                elif escolaridad == 'Primaria':
                    if efigura == 10:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Normal Alto")
                else:
                    evocacion.append("Normal Alto")
        elif efigura >= 6 and efigura < 10:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if efigura > 8:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if efigura > 7:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Severo")
                else:
                    evocacion.append("Normal")
            elif edad >= 66 and edad <= 85:
                evocacion.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    evocacion.append("Normal")
        elif efigura >= 3 and efigura < 6:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    evocacion.append("Severo")
                elif escolaridad == 'Primaria':
                    if efigura < 5:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Normal")
                else:
                    if efigura > 4:
                        evocacion.append("Normal")
                    elif efigura == 3:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if efigura > 4:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Bachillerato':
                    if efigura > 4:
                        evocacion.append("Normal")
                    else:
                        evocacion.append("Moderado")
                else:
                    evocacion.append("Normal")
        else:
            if edad >= 31 and edad <= 50:
                evocacion.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if efigura > 2:
                        evocacion.append("Moderado")
                    else:
                        evocacion.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if efigura < 2:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if efigura == 0:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
                elif escolaridad == 'Primaria':
                    if efigura > 1:
                        evocacion.append("Normal")
                    elif efigura < 1:
                        evocacion.append("Severo")
                    else:
                        evocacion.append("Moderado")
                else:
                    evocacion.append("Moderado")

        n.evocacion = Counter(evocacion).most_common(1)[0][0]
        resultado.append(n.evocacion)
        
        ## Lenguaje
        lenguaje = []
        # denominacion
        denominacion=int(n.lenguaje_denominacion)
        if denominacion == 8 or denominacion == 7:
            if edad >= 31 and edad <= 50:
                if denominacion == 8:
                    lenguaje.append("Normal")
                else:
                    if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 66 and edad <= 85:
                lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal")
        elif denominacion == 6:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta':
                    lenguaje.append("Moderado")
                else:
                    lenguaje.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Bachillerato':
                    lenguaje.append("Moderado")
                elif escolaridad == 'Primaria':
                    lenguaje.append("Normal")
                else:
                    lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Severo")
        else:
            if edad >= 31 and edad <= 50:
                lenguaje.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lenguaje.append("Severo")
                elif escolaridad == 'Bachillerato':
                    if denominacion < 4:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                else:
                    if denominacion == 5:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Severo")

        # repeticion
        repeticion = int(n.lenguaje_repeticion)
        if repeticion == 4:
            lenguaje.append("Normal")
        elif repeticion == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal")
                else:
                    lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    lenguaje.append("Moderado")
                else:
                    lenguaje.append("Severo")
        else:
            lenguaje.append("Severo")

        # comprension
        comprension = int(n.lenguaje_comprension)
        if comprension == 6:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta':
                    lenguaje.append("Normal Alto")
                else:
                    lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal Alto")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                    lenguaje.append("Normal Alto")
                else:
                    lenguaje.append("Normal")
        elif comprension == 5:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                    lenguaje.append("Normal")
                elif escolaridad == 'Bachillerato':
                    lenguaje.append("Moderado")
                else:
                    lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    lenguaje.append("Normal Alto")
                elif escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lenguaje.append("Severo")
                else:
                    lenguaje.append("Normal")
        elif comprension == 4 or comprension == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    lenguaje.append("Severo")
                elif escolaridad == 'Primaria':
                    if comprension == 4:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
                else:
                    lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    lenguaje.append("Normal")
                elif escolaridad == 'Bachillerato' or escolaridad == 'Primaria':
                    if comprension == 4:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
                else:
                    lenguaje.append("Severo")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad != 'Analfabeta':
                    lenguaje.append("Severo")
                else:
                    if comprension == 2:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if comprension == 2:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad != 'Analfabeta':
                    lenguaje.append("Severo")
                else:
                    if comprension == 2:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")

        # semantica
        semantica = int(n.lenguaje_semantica)
        if semantica >= 30:
            lenguaje.append("Normal Alto")
        elif semantica >= 25 and semantica < 30:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                    lenguaje.append("Normal Alto")
                else:
                    lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal Alto")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if semantica < 27:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Normal Alto")
                else:
                    lenguaje.append("Normal Alto")
        elif semantica >= 15 or semantica < 25:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    lenguaje.append("Normal")
                elif escolaridad == 'Primaria':
                    if semantica > 20:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                else:
                    if semantica > 18:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if semantica > 22:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    if semantica > 17:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                else:
                    lenguaje.append("Normal")
                    
        elif semantica >= 10 or semantica < 15:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lenguaje.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if semantica > 11:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
                else:
                    lenguaje.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if semantica > 10:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta' or escolaridad == 'Primaria':
                    lenguaje.append("Normal")
                else:
                    if semantica > 11:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if semantica > 7:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
                elif escolaridad == 'Bachillerato':
                    lenguaje.append("Severo")
                elif escolaridad == 'Primaria':
                    if semantica > 6:
                        lenguaje.append("Normal")
                    elif semantica < 4:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                else:
                    if semantica > 4:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if semantica > 3:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if semantica > 5:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
                elif escolaridad == 'Bachillerato':
                    if semantica > 3:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
                elif escolaridad == 'Primaria':
                    if semantica > 8:
                        lenguaje.append("Normal")
                    elif semantica < 4:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                else:
                    if semantica > 3:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")

        # fonologica
        fonologica = int(n.lenguaje_fonologica)
        if fonologica > 20:
            if escolaridad != 'Analfabeta':
                lenguaje.append("Normal Alto")
        elif fonologica >= 9 and fonologica <= 20:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lenguaje.append("Normal")
                elif escolaridad == 'Bachillerato':
                    if fonologica > 18:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                elif escolaridad == 'Primaria':
                    if fonologica > 11:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                else:
                    print("")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if fonologica > 15:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lenguaje.append("Normal")
                elif escolaridad == 'Bachillerato':
                    if fonologica > 16:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                elif escolaridad == 'Primaria':
                    if fonologica > 12:
                        lenguaje.append("Normal Alto")
                    else:
                        lenguaje.append("Normal")
                else:
                    print("")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if fonologica > 3:
                        lenguaje.append("Moderado")
                    else:
                        lenguaje.append("Severo")
                elif escolaridad == 'Bachillerato':
                    if fonologica > 3:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Severo")
                elif escolaridad == 'Primaria':
                    if fonologica > 0:
                        lenguaje.append("Normal")
                    else:
                        lenguaje.append("Moderado")
                else:
                    print("")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    lenguaje.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if fonologica > 6:
                        lenguaje.append("Normal")
                    elif fonologica < 2:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if fonologica > 4:
                        lenguaje.append("Normal")
                    elif fonologica < 1:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                elif escolaridad == 'Primaria':
                    if fonologica > 1:
                        lenguaje.append("Normal")
                    elif fonologica < 1:
                        lenguaje.append("Severo")
                    else:
                        lenguaje.append("Moderado")
                else:
                    print("")
                        
                        
        n.lenguaje=Counter(lenguaje).most_common(1)[0][0]
        resultado.append(n.lenguaje)

        ## Lectura y Escritura
        lye=[]
        # lectura
        lectura=int(n.lectura_lectura)
        if lectura == 3:
            lye.append("Normal")
        elif lectura == 2:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lye.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    lye.append("Normal")
                else:
                    print("")
            elif edad >= 66 and edad <= 85:
                lye.append("Normal")
        elif lectura == 1:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lye.append("Severo")
                elif escolaridad == 'Bachillerato':
                    lye.append("Normal")
                else:
                    print("")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lye.append("Normal")
                elif escolaridad == 'Bachillerato':
                    lye.append("Moderado")
                else:
                    print("")
        elif lectura == 0:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    lye.append("Severo")
                elif escolaridad == 'Bachillerato':
                    lye.append("Moderado")
                else:
                    print("")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    lye.append("Severo")
                else:
                    print("")
        # dictado
        dictado = int(n.lectura_dictado)
        if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
            if dictado == 1:
                lye.append("Normal")
            else:
                lye.append("Severo")

        # copiado
        copiado = int(n.lectura_copiado)
        if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
            if copiado == 1:
                lye.append("Normal")
            else:
                lye.append("Severo")
                

        try:
            n.lectura=Counter(lye).most_common(1)[0][0]
            resultado.append(n.lectura)
        except:
            print("")
        

        ## Funciones Ejecutivas
        
        #Conceptual
        conceptual=[]
        #semejanzas
        semejanzas=int(n.conceptual_semejanzas)
        if semejanzas == 6 or semejanzas == 5:
            if edad >= 31 and edad <= 50:
                conceptual.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    conceptual.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Analfabeta':
                    conceptual.append("Normal Alto")
                else:
                    conceptual.append("Normal")
        elif semejanzas == 4 or semejanzas == 3:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato':
                    if semejanzas == 4:
                        conceptual.append("Normal")
                    else:
                        conceptual.append("Moderado")
                elif escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    conceptual.append("Moderado")
                else:
                    conceptual.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    conceptual.append("Normal")
            elif edad >= 66 and edad <= 85:
                conceptual.append("Normal")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    conceptual.append("Severo")
                elif escolaridad == 'Primaria':
                    if semejanzas == 2:
                        conceptual.append("Normal")
                    else:
                        conceptual.append("Moderado")
                else:
                    conceptual.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if semejanzas == 0:
                        conceptual.append("Moderado")
                    else:
                        conceptual.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    if semejanzas == 0:
                        conceptual.append("Severo")
                    else:
                        conceptual.append("Moderado")
                elif escolaridad == 'Bachillerato':
                    if semejanzas == 2:
                        conceptual.append("Moderado")
                    else:
                        conceptual.append("Severo")
                else:
                    conceptual.append("Normal")

        # calculo
        calculo = int(n.conceptual_calculo)
        if calculo == 3 or calculo == 2:
            if escolaridad != 'Analfabeta':
                conceptual.append("Normal")
        elif calculo == 1:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    conceptual.append("Moderado")
                elif escolaridad == 'Primaria':
                    conceptual.append("Normal")
                else:
                    print("")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    conceptual.append("Normal")
            elif edad >= 66 and edad <= 85:
                if escolaridad != 'Analfabeta':
                    conceptual.append("Normal")
        else:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    conceptual.append("Severo")
                elif escolaridad == 'Primaria':
                    conceptual.append("Normal")
                else:
                    print("")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    conceptual.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    conceptual.append("Severo")
                elif escolaridad == 'Primaria':
                    conceptual.append("Moderado")
                else:
                    print("")

        # secuenciacion
        secuenciacion = int(n.conceptual_secuenciacion)
        if escolaridad == 'Técnico' or escolaridad == 'Profesional':
            if secuenciacion == 1:
                conceptual.append("Normal")
            else:
                conceptual.append("Severo")
        elif escolaridad == 'Bachillerato':
            if secuenciacion == 1:
                conceptual.append("Normal")
            else:
                conceptual.append("Moderado")
        else:
            print("")
            
        n.conceptual= Counter(resultado).most_common(1)[0][0]
        resultado.append(n.conceptual)
        
        ## Motoras
        motora=[]
        ## mano derecha
        mder=int(n.motora_mano_der)
        
        if mder == 0:
            if edad >= 31 and edad <= 50:
                motora.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    motora.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Primaria' or escolaridad == "Analfabeta":
                    motora.append("Moderado")
                else:
                    motora.append("Severo")
        else:
            motora.append("Normal")
    
        ## mano izquierda
        mizq = int(n.motora_mano_izq)
    
        if mizq == 0:
            if edad >= 31 and edad <= 50:
                motora.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    motora.append("Moderado")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Bachillerato' or escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    motora.append("Severo")
                elif escolaridad == 'Primaria':
                    motora.append("Normal")
                else:
                    motora.append("Moderado")
        else:
            motora.append("Normal")

        ## movimientos alternos
        alternos = int(n.motora_alternos)

        if alternos == 2:
            motora.append("Normal")
        elif alternos == 1:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                    motora.append("Moderado")
                else:
                    motora.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    motora.append("Normal")
            elif edad >= 66 and edad <= 85:
                motora.append("Normal")
        else:
            if escolaridad == 'Profesional' or escolaridad == 'Técnico':
                motora.append("Severo")
            elif escolaridad == "Analfabeta":
                motora.append("Normal")
            elif escolaridad == 'Bachillerato':
                if edad >= 31 and edad <= 50:
                    motora.append("Moderado")
                elif edad >= 66 and edad <= 85:
                    motora.append("Severo")
            else:
                if edad >= 31 and edad <= 50:
                    motora.append("Moderado")
                elif edad >= 66 and edad <= 85:
                    motora.append("Normal")
                elif edad >= 51 and edad <= 65:
                    motora.append("Moderado")

        ## Reacciones opuestas
        opuestas=int(n.motora_reacciones)

        if opuestas == 2 or opuestas == 1:
            if edad >= 31 and edad <= 50:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Primaria':
                    if opuestas == 2:
                        motora.append("Normal")
                    else:
                        motora.append("Moderado")
                else:
                    motora.append("Normal")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    if opuestas == 1:
                        motora.append("Moderado")
                    else:
                        motora.append("Normal")
            elif edad >= 66 and edad <= 85:
                motora.append("Normal")
        else:
            if edad >= 31 and edad <= 50:
                motora.append("Severo")
            elif edad >= 66 and edad <= 85:
                if escolaridad == 'Profesional' or escolaridad == 'Técnico' or escolaridad == 'Bachillerato':
                    motora.append("Severo")
                else:
                    motora.append("Moderado")
            elif edad >= 51 and edad <= 65:
                if escolaridad == 'Primaria':
                    motora.append("Severo")


        n.motora= Counter(motora).most_common(1)[0][0]
        resultado.append(n.motora)

        n.resultado= Counter(resultado).most_common(1)[0][0]
        n.save()




        return reverse_lazy('paciente', args=[p.pk])


