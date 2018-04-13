# encoding: utf-8
import mimetypes
import re

from django.http import request, HttpRequest
from django.urls import reverse, reverse_lazy

from apps.sujeto.models import Sujeto

def suj(name):
    suj = -1
    c = Sujeto.objects.all()
    for i in range(len(c)):
        if c[i].imagen.slug == name:
            suj = c[i].pk
            break
    return suj


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)

    return name

def veri(n):
    if n=="":
        return "Registro Incompleto"
    else:
        return "Registro Completo"

def color(n):
    if n=="":
        return "color:red;"
    else:
        return "color:black;"

def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField
    #"http://127.0.0.1:8000/sujeto/editar/"+str(instance.pk)
    """


    obj = getattr(instance, file_attr)
    n = ""
    u=""
    try:
        s = Sujeto.objects.get(pk=suj(order_name(obj.name)))
        n = s.nombre
        u="/sujeto/editar/"+str(s.pk)
    except:
        print("")

    else:
        print("")



    return {
        'url': u,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
        'sujeto': n,
        'verificacion':veri(n),
        'color': color(n),
    }


