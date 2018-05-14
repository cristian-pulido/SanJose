from django.shortcuts import render, redirect
from apps.paciente.models import Ingreso, Candidato, Radiologia, Uci, Neurologia, Bold


def error(request):
    return render(request, 'registration/login-error.html')


def crearingreso(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'ingreso'):
            return redirect("/paciente/ingreso/editar/" + str(c.ingreso.pk))
        else:
            i=Ingreso.objects.create(candidato=c)
            return redirect("/paciente/ingreso/editar/"+str(i.pk))


def crearradiologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'radiologia'):
            return redirect("/paciente/radiologia/editar/" + str(c.radiologia.pk))
        else:
            i=Radiologia.objects.create(candidato=c)
            return redirect("/paciente/radiologia/editar/"+str(i.pk))

def crearuci(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'uci'):
            return redirect("/paciente/uci/editar/" + str(c.uci.pk))
        else:
            u=Uci.objects.create(candidato=c)
            return redirect("/paciente/uci/editar/"+str(u.pk))

def crearneurologia(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'neurologia'):
            return redirect("/paciente/neurologia/editar/" + str(c.neurologia.pk))
        else:
            n=Neurologia.objects.create(candidato=c)
            return redirect("/paciente/neurologia/editar/"+str(n.pk))

def crearbold(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        c = Candidato.objects.get(pk=pk)
        if hasattr(c, 'bold'):
            return redirect("/paciente/bold/editar/" + str(c.bold.pk))
        else:
            b=Bold.objects.create(candidato=c)
            return redirect("/paciente/bold/editar/"+str(b.pk))


