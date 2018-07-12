import datetime
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.fileupload.models import Picture
from apps.paciente.models import Ingreso, Candidato, Radiologia, Uci, Neurologia, Bold, Mayor, Informante, Seguimiento, \
    Control, Cambioradiologia, Moca
from programas import anonimizador

def error(request):
    return render(request, 'registration/login-error.html')


def crearingreso(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'ingreso'):
            return redirect("/paciente/ingreso/editar/" + str(c.ingreso.pk))
        else:
            i=Ingreso.objects.create(candidato=c)
            return redirect("/paciente/ingreso/editar/"+str(i.pk))


def crearradiologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'radiologia'):
            return redirect("/paciente/radiologia/editar/" + str(c.radiologia.pk))
        else:
            i=Radiologia.objects.create(candidato=c)
            return redirect("/paciente/radiologia/editar/"+str(i.pk))

def crearuci(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'uci'):
            return redirect("/paciente/uci/editar/" + str(c.uci.pk))
        else:
            u=Uci.objects.create(candidato=c)
            return redirect("/paciente/uci/editar/"+str(u.pk))

        u=Uci.objects.create(candidato=c)
        return redirect("/paciente/uci/editar/"+str(u.pk))

def crearneurologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        neuro=c.neurologia_set.all()
        if len(neuro) == 0:
            n = Neurologia.objects.create(candidato=c)
            return redirect("/paciente/neurologia/editar/" + str(n.pk))
        else:
            n=c.neurologia_set.all().last()
            if n.fechaneuro == None:
                return redirect("/paciente/neurologia/editar/" + str(n.pk))
            else:
                hoy=datetime.date.today()
                if hoy != n.fechaneuro:
                    n=Neurologia.objects.create(candidato=c)
                    return redirect("/paciente/neurologia/editar/" + str(n.pk))
                else:
                    from django.contrib import messages
                    messages.add_message(request, messages.INFO, 'Ya existe una evaluacion neurologica para hoy de este sujeto.')
                    return redirect("/paciente/formularios/" + str(c.pk))



def crearbold(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'bold'):
            return redirect("/paciente/bold/editar/" + str(c.bold.pk))
        else:
            b=Bold.objects.create(candidato=c)
            return redirect("/paciente/bold/editar/"+str(b.pk))



def crearinformante(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        edad=c.edad
        if edad>59:
            if hasattr(c, 'mayor'):
                return redirect("/paciente/mayor/editar/" + str(c.mayor.pk))
            else:
                m = Mayor.objects.create(candidato=c)
                i = Informante.objects.create(candidato=c)
                return redirect("/paciente/mayor/editar/" + str(m.pk))
        else:
            if hasattr(c, 'informante'):
                return redirect("/paciente/informante/editar/" + str(c.informante.pk))
            else:
                i = Informante.objects.create(candidato=c)
                return redirect("/paciente/informante/editar/" + str(i.pk))

def crearseguimiento(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        S = c.seguimiento_set.all()
        n = len(S)
        hoy = datetime.date.today()
        flag = 0
        vacio = None
        if n == 0:
            if hoy == c.uci.fechauci:
                flag=1
        else:
            for seguimiento in S:
                if hoy == seguimiento.fechaseguimiento:
                    flag = 1
                    if seguimiento.glasgowtotal == '0':
                        flag = 2
                        vacio = seguimiento
                    break
        if flag == 0:
            s = Seguimiento.objects.create(candidato=c)
            return redirect("/paciente/seguimiento/editar/" + str(s.pk))
        elif flag == 1:
            from django.contrib import messages
            messages.add_message(request, messages.INFO, 'Ya existe un seguimiento para hoy de este sujeto.')
            return redirect("/paciente/formularios/"+str(c.pk))
        else:
            return redirect("/paciente/seguimiento/editar/" + str(vacio.pk))


def crearradiologiaf(request, pk, razon):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        e= ' '
        while '_' in razon:
            p=razon.find('_')
            razon=razon[:p]+e+razon[p+1:]
        Cambioradiologia.objects.create(sujeto=c, fecha=datetime.datetime.now(),razon=razon)
        return redirect("/paciente/formularios/" + str(c.pk))

def crearmoca(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c,'uci') and c.uci.condicion_egreso == 'Vivo':
            if hasattr(c, 'moca'):
                return redirect("/paciente/moca/editar/" + str(c.moca.pk))
            else:
                m = Moca.objects.create(candidato=c)
                return redirect("/paciente/moca/editar/" + str(m.pk))
        else:
            return redirect('login')










