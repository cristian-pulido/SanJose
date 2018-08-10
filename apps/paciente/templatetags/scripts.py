import os
import shutil
from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from celery import shared_task
from apps.fileupload.models import Picture
from apps.paciente.models import Dprevio, Apatologicos, Candidato, Control
from django import template

from programas import anonimizador, definitions
from programas.dcm2niix import convertir_dcm_2_nii, copytodata

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
        #hoy=datetime.now().date()
        for s in c:
            nacimiento=s.fecha_nacimiento
            registro = s.fecha_de_registro
            dt=registro-nacimiento
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
def tiempoeventoprincipal(c):
    entrada=c.fecha_evento_principal
    minimo=entrada+timedelta(days=90)
    maximo = entrada + timedelta(days=180)
    ahora = datetime.now().date()
    if ahora > minimo and ahora < maximo:
        return True
    else:
        return False


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
    admin.permissions.add(p1, m1, m2, m3, c1, c2, c3, b1, b2, b3, i1, i2, i3, u2, u3, n1, n2, n3, r1, r2, r3, inf1, inf2, inf3, seg3, mo1, mo2, mo3)
    residente.permissions.add(s1, s2, u1, u3, seg1, seg3)
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
        # shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, settings.MEDIA_ROOT+'/controles/' + sn[1:] + "/imagenes")
        # anonimizador.dicom_anonymizer(settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/imagenes")
        # zip_name = settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/" + sn[1:]
        # carpeta = settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/imagenes"
        # shutil.make_archive(zip_name, 'zip', carpeta)
        # i.file = "/controles/" + sn[1:] + "/" + sn[1:] + ".zip"
        # i.anonimo = 1
        # i.save()
        # c = Control.objects.get(numero=sn[1:])
        # f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        # f.write("-Anonimizado\n")
        # f.close()


        n = str(sn[1:])
        base_dir = settings.MEDIA_ROOT + "/controles/control" + n
        folder_dicom = os.path.join(base_dir, "imagenes")

        shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, folder_dicom)
        anonimizador.dicom_anonymizer(folder_dicom)
        c = Control.objects.get(numero=n)
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Anonimizado\n")
        f.close()
        i.anonimo = 1
        i.save()

        folder_nii = os.path.join(base_dir, "nifty")
        os.mkdir(folder_nii)
        convertir_dcm_2_nii(base_dir, folder_nii)
        zip_name = base_dir + "/control" + n + "_dicom"
        carpeta = folder_dicom
        shutil.make_archive(zip_name, 'zip', carpeta)
        shutil.rmtree(folder_dicom)

        zip_name = base_dir + "/control" + n
        carpeta = folder_nii
        shutil.make_archive(zip_name, 'zip', carpeta)

        i.file = "/controles/control" + n + "/control" + n + ".zip"
        i.save()
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Conversion Dicom a Nifty\n")
        f.close()
        folder_data = definitions.folder_data
        copytodata(n, folder_data, folder_nii, "control")

    else:
        # shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, settings.MEDIA_ROOT+'/img/sujeto' + str(sn) + "/imagenes")
        # anonimizador.dicom_anonymizer(settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/imagenes")
        # zip_name = settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/" + str(sn)
        # carpeta = settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/imagenes"
        # shutil.make_archive(zip_name, 'zip', carpeta)
        # i.file = "/img/sujeto" + str(sn) + "/" + str(sn) + ".zip"
        # i.anonimo = 1
        # i.save()
        # c=Candidato.objects.get(sujeto_numero=sn)
        # f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        # f.write("-Anonimizado\n")
        # f.close()

        sn = str(sn)
        base_dir = settings.MEDIA_ROOT + "/img/sujeto" + sn
        folder_dicom = os.path.join(base_dir, "imagenes")

        shutil.move(settings.MEDIA_ROOT[:-6] + i.file.url, folder_dicom)
        anonimizador.dicom_anonymizer(folder_dicom)


        c = Candidato.objects.get(sujeto_numero=sn)
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Anonimizado\n")
        f.close()
        i.anonimo = 1
        i.save()

        folder_nii = os.path.join(base_dir, "nifty")
        os.mkdir(folder_nii)
        convertir_dcm_2_nii(base_dir, folder_nii)
        zip_name = base_dir + "/sujeto" + sn + "_dicom"
        carpeta = folder_dicom
        shutil.make_archive(zip_name, 'zip', carpeta)
        shutil.rmtree(folder_dicom)

        zip_name = base_dir + "/sujeto" + sn
        carpeta = folder_nii
        shutil.make_archive(zip_name, 'zip', carpeta)

        i.file = "/img/sujeto" + sn + "/sujeto" + sn + ".zip"
        i.save()

        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Conversion Dicom a Nifty\n")
        f.close()
        folder_data = definitions.folder_data
        copytodata(sn, folder_data, folder_nii,"sujeto")

    return "Completo"

@register.simple_tag
def checkseguimiento(o):
    if hasattr(o, 'uci') and o.uci.fechauci != None:
        if o.uci.fechaegreso == None:
            hoy = datetime.today().strftime('%Y-%m-%d')
            if str(o.uci.fechauci) == hoy:
                return "Formulario Ingreso UCI cargado"
            else:
                s=o.get_seguimiento()
                if len(s) > 0:
                    if str(s.last().fechaseguimiento) == hoy and s.last().glasgowtotal != '0':
                        return "si"
                    else:
                        return "no"
                else:
                    return "no"
        else:
            return "Paciente dado de alta"
    else:
        return "Formulario Ingreso UCI aún no cargado"

@register.simple_tag
def totalincluidos():
    t=len(Candidato.objects.filter(inscrito=True))
    c=len(Candidato.objects.all())
    return ""+str(t)+"/"+str(c)

@register.simple_tag
def totalexcluidos():
    t=len(Candidato.objects.filter(inscrito=False))
    c = len(Candidato.objects.all())
    return "" + str(t) + "/" + str(c)

@register.simple_tag
def mexclusion(c):
    a=len(c.D_neuro_logico_psiquiatrico_previo.all())
    ci=c.ci3*1+c.ci4*1;
    ce=c.ce1*1+c.ce2*1+c.ce3*1+c.ce4*1

    if a > 0 :
        return "Antecedentes neurologicos o neuropsiquiátricos"
    elif ci < 2:
        return "No cumple los criterios de inclusión"
    elif ce > 0:
        return "Cumple criterios de exclusión"
    elif hasattr(c, 'uci') and c.uci.continua_studio == "NO":
        return "No pudo continuar en el estudio"
    elif hasattr(c, 'uci') and c.uci.glasgowtotal_e != "0" and c.imagen == "":
        return "Imagenes dañadas o muerte anterior a la toma de estas"
    else:
        return 0
