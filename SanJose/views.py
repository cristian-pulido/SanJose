from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from apps.paciente.models import Candidato


def error(request):
    return render(request, 'registration/login-error.html')


def crearsujeto(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        s=Candidato.objects.create(inscrito=False, estado=0, ci3=False,ci4=False)
        return HttpResponseRedirect('/paciente/editar/' + str(s.pk))