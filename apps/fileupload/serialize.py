# encoding: utf-8
import mimetypes
import re

from django.urls import reverse




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
        return "Formulario de inclusión cargado"
    elif estado==2:
        return "Formulario de ingreso cargado"

def color(e):
    if e==0:
        return "color:red;"
    else:
        return "color:black;"
def eti(S,anterior):
    if S.estado!=0:
        return "Sujeto #" + str(S.sujeto_numero)
    else:
        return anterior


def direccion(s):
    if s.estado==0:
        return "/paciente/editar/"+str(s.pk)
    else:
        return "/paciente/formularios/"+str(s.pk)

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
        S=instance.candidato
        n = S.nombres
        u=direccion(S)
        e=S.estado
        etiqueta = eti(S, etiqueta)
    except:
        print("")

    else:
        print("")



    return {
        'pk': instance.pk,
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


