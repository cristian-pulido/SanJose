from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from apps.paciente.views import PacienteCreate, PacienteUpdate, MedicoCreate, MedicoList, MedicoUpdate, MedicoDelete, \
    PacienteList

urlpatterns = [

    path('nuevo', PacienteCreate.as_view(), name='paciente_crear'),
    path('editar/<int:pk>/', PacienteUpdate.as_view(), name='paciente_editar'),
    path('listar/', PacienteList.as_view(), name='paciente_listar'),
    path('medico/nuevo', MedicoCreate.as_view(), name='medico_crear'),
    path('medico/listar', MedicoList.as_view(), name='medico_listar'),
    path('medico/editar/<int:pk>/', MedicoUpdate.as_view(), name='medico_editar'),
    path('medico/eliminar/<int:pk>/', MedicoDelete.as_view(), name='medico_eliminar'),
]
