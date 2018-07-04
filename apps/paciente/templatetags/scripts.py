import os
import shutil
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from celery import shared_task
from apps.fileupload.models import Picture
from apps.paciente.models import Dprevio, Apatologicos, Candidato, Control
from django import template

from programas import anonimizador

register = template.Library()

@register.simple_tag
def num():
    if len(Candidato.objects.all())==0:
        return "1"
    else:
        a=len(Candidato.objects.all())
        return ""+str((int(a)+1)).zfill(4)

@register.simple_tag
def edad():
    if len(Candidato.objects.all())==0:
        return ""
    else:
        c=Candidato.objects.all()
        hoy=datetime.now().date()
        for s in c:
            nacimiento=s.fecha_nacimiento
            dt=hoy-nacimiento
            s.edad=int(dt.days/365)
            s.save()
        return ""
@register.simple_tag
def tiempo(c):
    entrada=c.fecha_hora_ingreso
    ahora = datetime.now(timezone.utc)
    resta=ahora-entrada
    horas=int(resta.total_seconds()/3600)
    return horas


@register.simple_tag
def crearDprevios():
    if len(Dprevio.objects.all()) == 12:
        return ""
    else:
        d=Dprevio.D_neuro_logico_psiquiatrico_previo_choices
        total=len(d)
        for i in range(total):
            Dprevio.objects.create(nombre=d[i][0])
        p = Apatologicos.Apatologicos_choices
        total = len(p)
        for i in range(total):
            Apatologicos.objects.create(nombre=p[i][0])
        return ""
@register.simple_tag
def crearmedia():
    try:
        os.mkdir(settings.MEDIA_ROOT)
    except:
        ""
    return ""


@register.simple_tag
def creargrupos():

    try:
        #permisos
        p1 = Permission.objects.get(name="Can add picture")
        p2 = Permission.objects.get(name="Can change picture")
        p3 = Permission.objects.get(name="Can delete picture")
        p4 = Permission.objects.get(name="Can add candidato")
        p5 = Permission.objects.get(name="Can change candidato")
        p6 = Permission.objects.get(name="Can delete candidato")
        p7 = Permission.objects.get(name="Can add medico")
        p8 = Permission.objects.get(name="Can change medico")
        p9 = Permission.objects.get(name="Can delete medico")
        p10 = Permission.objects.get(name="Can add candidato")
        p11 = Permission.objects.get(name="Can change candidato")
        p12 = Permission.objects.get(name="Can delete candidato")

        ## creacion grupos
        invitado = Group.objects.create(name='Invitado')
        consultor = Group.objects.create(name='Consultor')
        cargador = Group.objects.create(name='Cargador')
        cargador.permissions.add(p1, p2, p4, p5, p7, p8, p10, p11)
        admin=Group.objects.create(name='Administrador')
        admin.permissions.add(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12)
    except:
        print("")
    users = User.objects.all()
    invitado = Group.objects.get(name="Invitado")
    for i in users[1:]:
        if len(i.groups.all()) == 0:
            invitado.user_set.add(i)


    return ""

@shared_task
def anonimizar(sn):
    i = Picture.objects.get(slug=sn)
    if sn[0]=='c':
        shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, settings.MEDIA_ROOT+'/controles/' + sn[1:] + "/imagenes")
        anonimizador.dicom_anonymizer(settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/imagenes")
        zip_name = settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/" + sn[1:]
        carpeta = settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/imagenes"
        shutil.make_archive(zip_name, 'zip', carpeta)
        i.file = "/controles/" + sn[1:] + "/" + sn[1:] + ".zip"
        i.anonimo = 1
        i.save()
        c = Control.objects.get(numero=sn[1:])
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Anonimizado\n")
        f.close()
    else:
        shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, settings.MEDIA_ROOT+'/img/sujeto' + str(sn) + "/imagenes")
        anonimizador.dicom_anonymizer(settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/imagenes")
        zip_name = settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/" + str(sn)
        carpeta = settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/imagenes"
        shutil.make_archive(zip_name, 'zip', carpeta)
        i.file = "/img/sujeto" + str(sn) + "/" + str(sn) + ".zip"
        i.anonimo = 1
        i.save()
        c=Candidato.objects.get(sujeto_numero=sn)
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Anonimizado\n")
        f.close()
    return "Completo"

