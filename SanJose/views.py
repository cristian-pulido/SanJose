from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.paciente.models import Candidato
from apps.sujeto.models import Sujeto


def error(request):
    return render(request, 'registration/login-error.html')

def crearcandidato(request, pk):
    s = Sujeto.objects.get(pk=pk)
    if s.estado==1:
        s.estado=2
        s.save()
        Candidato.objects.create(imagen=s.imagen)
        c = Candidato.objects.get(imagen=s.imagen)
        return HttpResponseRedirect('/paciente/editar/'+str(c.pk))
    else:
        return HttpResponseRedirect('/carga/new')