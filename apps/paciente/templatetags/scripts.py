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
    # permisos

    # imagenes
    p1 = Permission.objects.get(name="Can add picture")
    p2 = Permission.objects.get(name="Can change picture")
    p3 = Permission.objects.get(name="Can delete picture")

    # candidato/sujeto
    s1 = Permission.objects.get(name="Can add candidato")
    s2 = Permission.objects.get(name="Can change candidato")
    s3 = Permission.objects.get(name="Can delete candidato")
    s4 = Permission.objects.get(name="puede descargar candidato")



    # medico
    m1 = Permission.objects.get(name="Can add medico")
    m2 = Permission.objects.get(name="Can change medico")
    m3 = Permission.objects.get(name="Can delete medico")

    # controles
    c1 = Permission.objects.get(name="Can add control")
    c2 = Permission.objects.get(name="Can change control")
    c3 = Permission.objects.get(name="Can delete control")
    c4 = Permission.objects.get(name="puede descargar control")


    # ingreso
    i1 = Permission.objects.get(name="Can add ingreso")
    i2 = Permission.objects.get(name="Can change ingreso")
    i3 = Permission.objects.get(name="puede ver ingreso")
    # uci
    u1 = Permission.objects.get(name="Can add uci")
    u2 = Permission.objects.get(name="Can change uci")
    u3 = Permission.objects.get(name="puede ver uci")
    # neurologia
    n1 = Permission.objects.get(name="Can add neurologia")
    n2 = Permission.objects.get(name="Can change neurologia")
    n3 = Permission.objects.get(name="puede ver neurologia")
    # radiologia
    r1 = Permission.objects.get(name="Can add radiologia")
    r2 = Permission.objects.get(name="Can change radiologia")
    r3 = Permission.objects.get(name="puede ver radiologia")
    #bold
    b1 = Permission.objects.get(name="Can add bold")
    b2 = Permission.objects.get(name="Can change bold")
    b3 = Permission.objects.get(name="puede ver bold")
    # informante
    inf1 = Permission.objects.get(name="Can add informante")
    inf2 = Permission.objects.get(name="Can change informante")
    inf3 = Permission.objects.get(name="puede ver informante")
    # seguimiento
    seg1 = Permission.objects.get(name="Can add seguimiento")
    seg2 = Permission.objects.get(name="Can change seguimiento")
    seg3 = Permission.objects.get(name="puede ver seguimiento")
    # moca
    mo1 = Permission.objects.get(name="Can add moca")
    mo2 = Permission.objects.get(name="Can change moca")
    mo3 = Permission.objects.get(name="puede ver moca")

    ## creacion grupos
    invitado = Group.objects.get_or_create(name='Invitado')[0]
    consultor = Group.objects.get_or_create(name='Consultor')[0]
    residente = Group.objects.get_or_create(name='Residente')[0]
    informante = Group.objects.get_or_create(name='Informante')[0]
    admin = Group.objects.get_or_create(name='Coordinador')[0]
    sadmin = Group.objects.get_or_create(name='SuperAdministrador')[0]

    sadmin.permissions.add(p1, p2, p3, s1, s2, s3, s4, m1, m2, m3, c1, c2, c3, c4, b1, b2, b3, i1, i2, i3, u1, u2, u3, n1, n2, n3, r1, r2, r3, inf1, inf2, inf3, seg1, seg2, seg3, mo1, mo2, mo3)
    admin.permissions.add(p1, m1, m2, m3, c1, c2, c3, b1, b2, b3, i1, i2, i3, u3, n1, n2, n3, r1, r2, r3, inf1, inf2, inf3, seg3, mo1, mo2, mo3)
    residente.permissions.add(s1, s2, u1, u2, u3, seg1, seg3)
    informante.permissions.add(p1, s1, s2, i1, i3, u1, u3, n1, n3, r1, r3, b1, b3, inf1, inf3, seg1, seg3, mo1, mo3)


    users = User.objects.all()
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

