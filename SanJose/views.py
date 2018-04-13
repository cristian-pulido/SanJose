from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')

def error(request):
    return render(request, 'registration/login-error.html')