# encoding: utf-8
import mimetypes
import re

from django.urls import reverse

from apps.sujeto.models import Sujeto



def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)

    return name

def veri(estado):
    if estado==0:
        return "Registro Incompleto"
    elif estado==1:
        return "Información basica cargada"
    elif estado==2:
        return "Información basica cargada"
    elif estado==3:
        return "Formulario de inclución cargado"

def color(e):
    if e==0:
        return "color:red;"
    else:
        return "color:black;"

def direccion(s):
    if s.estado==0:
        return "/sujeto/editar/"+str(s.pk)
    else:
        return "/sujeto/formularios/"+str(s.pk)

def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.
    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField
    """
    obj = getattr(instance, file_attr)




    n = ""
    u=""
    e=0
    etiqueta =order_name(obj.name)
    try:
        S=instance.sujeto
        n = S.nombres
        u=direccion(S)
        e=S.estado
    except:
        print("")

    else:
        print("")
    try:
        P=instance.candidato
        etiqueta="Sujeto #"+str(P.sujeto_numero)
    except:
        print("")

    else:
        print("")



    return {
        'pk':instance.pk,
        'url': u,
        'name': etiqueta,
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
        'sujeto': n,
        'verificacion': veri(e),
        'color': color(e),
    }


