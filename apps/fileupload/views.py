# encoding: utf-8
import json
from fileinput import filename

from django.http import HttpResponse
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
        t = newtext()
        t.test()
        ## Crear objeto vacio y añadirle la imagen subida
        s = Sujeto.objects.create()
        s.save()
        s.imagen=self.object
        s.save()
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture


    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
