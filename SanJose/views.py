from django.shortcuts import render



def error(request):
    return render(request, 'registration/login-error.html')