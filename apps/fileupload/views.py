# encoding: utf-8
import json
from fileinput import filename

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from apps.sujeto.models import Sujeto
from programa.creacionarchivo import newtext
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize


class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        ## Crear archivo
        #t = newtext()
        #t.test()
        ## Crear objeto vacio y añadirle la imagen subida
        s = Sujeto.objects.create(inscrito=True,imagen=self.object)
        s.save()

        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'fileupload.delete_picture'
    model = Picture
    template_name = 'fileupload/eliminar.html'
    # a donde va dirigido
    success_url = reverse_lazy('upload-new')
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
