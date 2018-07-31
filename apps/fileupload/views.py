# encoding: utf-8
import json
import os
from fileinput import filename

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import  redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from apps.paciente.models import Candidato, Control
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from apps.paciente.templatetags.scripts import anonimizar



class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        sn=str(self.object.slug)
        if sn[0]=='c':
            c=Control.objects.get(numero=int(sn[1:]))
            os.mkdir(settings.MEDIA_ROOT+'/controles/' + sn[1:] + "/imagenes")
            file = open(settings.MEDIA_ROOT+"/controles/" + sn[1:] + "/" + sn[1:] + ".txt", "w")
            file.write("" + sn[1:]+"\n")
            file.close()
            c.imagen = "/controles/" + sn[1:] + "/" + sn[1:] + ".txt"
            c.save()
            anonimizar.delay(sn)
        else:
            p=Candidato.objects.get(sujeto_numero=int(sn))
            if p.estado==1:
                os.mkdir(settings.MEDIA_ROOT+'/img/sujeto' + str(sn) + "/imagenes")
                p.estado=2
                file = open(settings.MEDIA_ROOT+"/img/sujeto" + str(sn) + "/" + str(sn) + ".txt", "w")
                file.write("" + str(sn)+"\n")
                file.close()
                p.imagen = "/img/sujeto" + str(sn) + "/" + str(sn) + ".txt"
                p.save()
                anonimizar.delay(sn)
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'fileupload.delete_picture'
    model = Picture
    template_name = 'fileupload/eliminar.html'
    # a donde va dirigido
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return redirect('upload-new')


class PictureListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'fileupload.add_picture'
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
