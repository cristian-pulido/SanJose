from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from apps.paciente.models import Candidato
from apps.sujeto.models import Sujeto


def error(request):
    return render(request, 'registration/login-error.html')


def crearsujeto(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        s=Sujeto.objects.create(inscrito=False, estado=1)
        return HttpResponseRedirect('/sujeto/editar/' + str(s.pk))