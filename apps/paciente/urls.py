from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from apps.paciente.views import PacienteCreate, PacienteUpdate

urlpatterns = [

    path('nuevo', PacienteCreate.as_view(), name='paciente_crear'),
    path('editar/<int:pk>/', PacienteUpdate.as_view(), name='paciente_editar'),

]
