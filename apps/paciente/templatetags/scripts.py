from django.contrib.auth.models import Group, Permission, User

from apps.fileupload.models import Picture
from apps.paciente.models import Dprevio, Apatologicos, Candidato
from django import template

from programas import anonimizador

register = template.Library()

@register.simple_tag
def numexcluido():
    if len(Candidato.objects.all())==0:
        return "P1"
    else:
        a=len(Candidato.objects.all())
        return "P"+str(int(a)+1)



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
def creargrupos():

    try:
        #permisos
        p1 = Permission.objects.get(name="Can Add picture")
        p2 = Permission.objects.get(name="Can Change picture")
        p3 = Permission.objects.get(name="Can Delete picture")
        p4 = Permission.objects.get(name="Can Add candidato")
        p5 = Permission.objects.get(name="Can Change candidato")
        p6 = Permission.objects.get(name="Can Delete candidato")
        p7 = Permission.objects.get(name="Can Add medico")
        p8 = Permission.objects.get(name="Can Change medico")
        p9 = Permission.objects.get(name="Can Delete medico")
        p10 = Permission.objects.get(name="Can Add candidato")
        p11 = Permission.objects.get(name="Can Change candidato")
        p12 = Permission.objects.get(name="Can Delete candidato")

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


@register.simple_tag
def anonimizar():

    try:
        imagenes=Picture.objects.all()
        for img in imagenes:
            if img.anonimo == 1:
                img.anonimo = 2
                img.save()

            if img.anonimo == 0:
                img.anonimo = 1
                img.save()


        for img in imagenes:
            if img.anonimo == 1:
                n = img.candidato.sujeto_numero
                ### anonimizador
                anonimizador.dicom_anonymizer("/home/ubuntu/media/img/sujeto" + str(n))
                img.anonimo = 3
                img.save()

    except:
        print("")

    return ""





