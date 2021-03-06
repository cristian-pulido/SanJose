import datetime
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from SanJose.settings import MEDIA_ROOT
from apps.fileupload.models import Picture
from apps.paciente.models import Ingreso, Candidato, Radiologia, Uci, Neurologia, Bold, Mayor, Informante, Seguimiento, \
    Control, Cambioradiologia, Moca, Valorablenps, Neuropsi, Parametrosmotioncorrect, Lectura_resonancia
from apps.validacion.models import Tipoimagenes
from programas import anonimizador
from programas.dcm2niix import T1_path, rest_path, DWI_path
from programas.realineacion import transformaciones
from apps.procesamiento.models import Task, Taskgroup, Pipeline, task_celery
from django.contrib.auth.models import Group, Permission, User
from apps.procesamiento.templatetags.scripts_procesamiento import crear_tarea


import logging

log=logging.getLogger('django')

def error(request):
    return render(request, 'registration/login-error.html')


def crearingreso(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'ingreso'):
            log.info("--------------------- Editar Ingreso Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/ingreso/editar/" + str(c.ingreso.pk))
        else:
            i=Ingreso.objects.create(candidato=c)
            log.info("--------------------- Crear Ingreso Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/ingreso/editar/"+str(i.pk))


def crearradiologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'radiologia'):
            log.info("--------------------- Editar Radiologia Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/radiologia/editar/" + str(c.radiologia.pk))
        else:
            i=Radiologia.objects.create(candidato=c)
            log.info("--------------------- Crear Radiologia Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/radiologia/editar/"+str(i.pk))

def crearuci(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'uci'):
            log.info("--------------------- Editar Uci Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/uci/editar/" + str(c.uci.pk))
        else:
            u=Uci.objects.create(candidato=c)
            log.info("--------------------- Crear Uci Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/uci/editar/"+str(u.pk))



def crearneurologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        neuro=c.neurologia_set.all()
        if len(neuro) == 0:
            n = Neurologia.objects.create(candidato=c)
            log.info("--------------------- Crear Neurologia Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/neurologia/editar/" + str(n.pk))
        else:
            n=c.neurologia_set.all().last()
            if n.fechaneuro == None:
                log.info("--------------------- Editar Neurologia Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/neurologia/editar/" + str(n.pk))
            else:
                hoy=datetime.date.today()
                if hoy != n.fechaneuro:
                    n=Neurologia.objects.create(candidato=c)
                    log.info("--------------------- Crear Neurologia Sujeto " + str(
                        c.sujeto_numero) + "---------------------")
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
            log.info("--------------------- Editar Bold Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/bold/editar/" + str(c.bold.pk))
        else:
            b=Bold.objects.create(candidato=c)
            log.info("--------------------- Crear Bold Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/bold/editar/"+str(b.pk))



def crearinformante(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        edad=c.edad
        if edad>59:
            if hasattr(c, 'mayor'):
                log.info(
                    "--------------------- Editar Mayor Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/mayor/editar/" + str(c.mayor.pk))
            else:
                m = Mayor.objects.create(candidato=c)
                i = Informante.objects.create(candidato=c)
                log.info(
                    "--------------------- Crear Mayor Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/mayor/editar/" + str(m.pk))
        else:
            if hasattr(c, 'informante'):
                log.info(
                    "--------------------- Editar Informante Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/informante/editar/" + str(c.informante.pk))
            else:
                i = Informante.objects.create(candidato=c)
                log.info(
                    "--------------------- Crear Informante Sujeto " + str(c.sujeto_numero) + "---------------------")
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
            log.info("--------------------- Crear Seguimiento Sujeto " + str(c.sujeto_numero) + "---------------------")
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
        log.info("--------------------- Crear cambio fecha readiologia Sujeto " + str(c.sujeto_numero) + "---------------------")
        return redirect("/paciente/formularios/" + str(c.pk))

def crearnps(request, pk, razon, fecha):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        r=int(razon)
        choice=""
        if r == 1:
            choice="Fallecido"
        elif r == 2:
            choice="No localizable"
        elif r == 3:
            choice="No colabora"
        elif r == 4:
            choice="EMC"
        else:
            choice="SVSR"
        if fecha != "None":
            n = Valorablenps.objects.create(sujeto=c,valorable=False,fecha=datetime.datetime.now(),razon=choice,fechafallecido=fecha)
        else:
            n = Valorablenps.objects.create(sujeto=c, valorable=False, fecha=datetime.datetime.now(), razon=choice)
        from django.contrib import messages
        messages.add_message(request, messages.INFO, 'Sujeto #'+str(c.sujeto_numero)+" no valorable por Neuropsicología, causa: "+choice)
        log.info("--------------------- Crear nps Sujeto " + str(c.sujeto_numero) + "---------------------")
        return redirect("/paciente/formularios/" + str(c.pk))

def crearmoca(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        n = len(c.moca_set.all())
        if n != 0:
            m = c.moca_set.all()
            if m.last().fecha == None:
                log.info(
                    "--------------------- Crear Moca Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/moca/editar/" + str(m.last().pk))
            else:
                nps = Moca.objects.create(candidato=c)
                log.info(
                    "--------------------- Crear Moca Sujeto " + str(c.sujeto_numero) + "---------------------")
                return redirect("/paciente/moca/editar/" + str(nps.pk))
        else:
            nps = Moca.objects.create(candidato=c)
            log.info("--------------------- Crear Moca Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/moca/editar/" + str(nps.pk))

def crearneuropsi(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'neuropsi'):
            log.info("--------------------- Editar Nuropsi Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/neuropsi/editar/" + str(c.neuropsi.pk))
        else:
            n = Neuropsi.objects.create(candidato=c)
            log.info("--------------------- Crear Neropsi Sujeto " + str(c.sujeto_numero) + "---------------------")
            return redirect("/paciente/neuropsi/editar/" + str(n.pk))

def crearlectura(request, pk, tipo):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if tipo == 'candidato':
            c = Candidato.objects.get(pk=pk)
        else:
            c = Control.objects.get(pk=pk)
        if hasattr(c, 'lectura_resonancia'):
            log.info("--------------------- Editar Lectura ---------------------")
            return redirect("/paciente/lectura/editar/" + str(c.lectura_resonancia.pk))
        else:
            l=Lectura_resonancia.objects.create()
            setattr(l, tipo, c)
            l.save()
            log.info("--------------------- Editar Lectura ---------------------")
            return redirect("/paciente/lectura/editar/"+str(l.pk))


def visionimagen(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        i = Tipoimagenes.objects.get(pk=pk)
        if i.mostrar == True:
            i.mostrar = False
        else:
            i.mostrar = True
        i.save()
        return redirect("login")


def validarmovimiento(request, tipo,pk,v1,v2):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        if tipo == "sujeto":
            C=Candidato.objects.get(sujeto_numero=pk)
            parametros = Parametrosmotioncorrect.objects.get(sujeto=C)
        else:
            C = Control.objects.get(numero=pk)
            parametros = Parametrosmotioncorrect.objects.get(control=C)

        if v1 == '1':
            parametros.aceptado_func = True
        else:
            parametros.aceptado_func = False

        if v2 == '1':
            parametros.aceptado_dwi = True
        else:
            parametros.aceptado_dwi = False

        parametros.save()
        log.info("--------------------- Validar Movimiento"+str(C)+" ---------------------")
        return redirect("login")


def alinear(request,tipo,pk,img,der,frente,arriba,x,y,z,tx,ty,tz,save):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        der=-float(der.replace('_','.'))
        frente = float(frente.replace('_','.'))
        arriba = float(arriba.replace('_','.'))
        x = float(x.replace('_','.'))
        y = float(y.replace('_','.'))
        z = float(z.replace('_','.'))
        tx = float(tx.replace('_','.'))
        ty = float(ty.replace('_','.'))
        tz = float(tz.replace('_','.'))
        save = int(save)
        if tipo == "sujeto":
            C=Candidato.objects.get(pk=pk)
        else:
            C = Control.objects.get(pk=pk)
        R=C.get_realineacion()
        folder_nii=settings.MEDIA_ROOT+os.path.dirname(os.path.dirname(R.structural.name))
        log.info("--------------------- Alinear imagenes ---------------------")

        if img == "structural":
            img_path=T1_path(folder_nii)
            out_path=settings.MEDIA_ROOT+R.structural.name
            t=transformaciones(img_path, out_path,img_path, der, frente, arriba, x, y, z, tx, ty, tz,save)
            R.structural=R.structural.name
            R.structural_cambio = bool(save)
            R.save()

            return redirect(R.structural.url)

        if img == "funcional":
            img_path=rest_path(folder_nii)
            out_path=settings.MEDIA_ROOT+R.funcional.name
            t=transformaciones(img_path, out_path,img_path, der, frente, arriba, x, y, z, tx, ty, tz,save)
            R.funcional=R.funcional.name
            R.funcional_cambio = bool(save)
            R.save()

            return redirect(R.funcional.url)

        if img == "tensor":
            img_path=DWI_path(folder_nii, False)
            out_path=settings.MEDIA_ROOT+R.tensor.name
            t=transformaciones(img_path, out_path,img_path, der, frente, arriba, x, y, z, tx, ty, tz,save)
            R.tensor=R.tensor.name
            R.tensor_cambio = bool(save)
            R.save()

            return redirect(R.tensor.url)



def reportes(request):
    return render(request,'base/reportes.html')


def run_pipeline(request,user_pk,img_pk,pipeline_pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user=User.objects.get(pk=user_pk)
        picture=Picture.objects.get(pk=img_pk)
        pipeline=Pipeline.objects.get(pk=pipeline_pk)
        
        
        t_celery=task_celery.objects.create(user=user,imagen=picture,pipeline=pipeline,
                                            estado="iniciado")
        
        tarea=crear_tarea.delay(t_celery.pk)
        
        t_celery.id_task=tarea.task_id
        t_celery.save()
        
        return redirect("login")












