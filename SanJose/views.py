from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.paciente.models import Ingreso, Candidato


def error(request):
    return render(request, 'registration/login-error.html')


def crearingreso(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c=Candidato.objects.get(pk=pk)
        i=Ingreso.objects.create(candidato=c)
        return redirect("/paciente/ingreso/editar/"+str(i.pk))