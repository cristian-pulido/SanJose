"""SanJose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.contrib.auth import views
from .views import home

urlpatterns = [
    path('', lambda x: HttpResponseRedirect('/login')),
    #path('admin/', admin.site.urls),
    path('carga/', include('apps.fileupload.urls')),
    path('sujeto/', include('apps.sujeto.urls')),
    path('paciente/', include('apps.paciente.urls')),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, { 'template_name': 'registration/logout.html'},name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^home$', home, name='home'),
]
