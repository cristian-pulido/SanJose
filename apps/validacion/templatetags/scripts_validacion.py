from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto
from django import template

register = template.Library()

def pass_tags_to_db(sn,series):
    for serie in series:
        TipoImg=Tipoimagenes.objects.get_or_create(nombre=serie)[0]
        for tag in series[serie]:
            num_tag=series[serie][tag]["num_tag"]
            name_tag=tag
            key_tag=series[serie][tag]["name_tag"]
            Tag=Tagsdicom.objects.get_or_create(num_tag=num_tag,name_tag=name_tag,key_tag=key_tag)[0]
            CampoTag=Campostagimg.objects.create(tag=Tag,
                                                valor=series[serie][tag]["v_tag"],
                                                visible=False,
                                                imagen=TipoImg,
                                                sujeto=sn
                                               )

@register.simple_tag
def get_images_names_sujeto(sn):
    sn=str(sn)
    C=Campostagimg.objects.filter(sujeto=sn)
    result=[]
    nombres=[]
    for c in C:
        if c.imagen.nombre in nombres:
            continue
        else:
            nombres.append(c.imagen.nombre)
            if c.imagen.nombre_aux == None:
                c.imagen.nombre_aux = ""
            result.append(tuple((c.imagen.nombre,c.imagen.nombre_aux,c.imagen.mostrar,c.imagen.pk)))
    return  sorted(result, key=lambda m: m[2],reverse=True)
@register.simple_tag
def get_images_names_control(sn):
    sn="c"+str(sn)
    C=Campostagimg.objects.filter(sujeto=sn)
    result = []
    nombres = []
    for c in C:
        if c.imagen.nombre in nombres:
            continue
        else:
            nombres.append(c.imagen.nombre)
            if c.imagen.nombre_aux == None:
                c.imagen.nombre_aux = ""
            result.append(tuple((c.imagen.nombre, c.imagen.nombre_aux, c.imagen.mostrar, c.imagen.pk)))
    return sorted(result, key=lambda m: m[2], reverse=True)
@register.simple_tag
def get_campos_from_image_sujeto(sn,nombre_img):
    sn=str(sn)
    imagen=Tipoimagenes.objects.get(nombre=nombre_img)
    campos = Campostagimg.objects.filter(imagen=imagen, sujeto=sn, visible=True)
    return campos

@register.simple_tag
def get_campos_from_image_control(sn,nombre_img):
    sn = "c" + str(sn)
    imagen=Tipoimagenes.objects.get(nombre=nombre_img)
    campos = Campostagimg.objects.filter(imagen=imagen, sujeto=sn, visible=True)
    return campos

def campos_a_mostrar():
    default=Campos_defecto.objects.all()
    for d in default:
        campo=Campostagimg.objects.filter(tag=d.tag,imagen=d.imagen)
        for c in campo:
            c.visible=True
            c.save()
            c.medidas=d.medidas
            c.save()
            c.precision=d.precision
            c.save()
            c.v_esperado=d.v_esperado
            c.save()
            if c.v_esperado == "" or c.v_esperado == None:
                continue
            else:
                sup=float(c.v_esperado)*(1+float(c.precision)/100)
                inf = float(c.v_esperado) * (1 - float(c.precision) / 100)
                if float(c.v_esperado) >= inf and float(c.v_esperado) <= sup:
                    c.cumple = True
                else:
                    c.cumple = False
                c.save()

    return ""

@register.simple_tag
def get_name_images():
    I=Tipoimagenes.objects.filter(mostrar=True)
    return I

@register.simple_tag
def get_tags_images(nombre):
    I = Tipoimagenes.objects.get(nombre=nombre)
    C = Campos_defecto.objects.filter(imagen=I)
    return C