
from django.urls import path

from apps.paciente.views import PacienteCreate, PacienteUpdate, MedicoCreate, MedicoList, MedicoUpdate, MedicoDelete, \
    PacienteList, PacienteView, PacienteDelete

urlpatterns = [

    path('nuevo', PacienteCreate.as_view(), name='paciente_crear'),
    path('editar/<int:pk>/', PacienteUpdate.as_view(), name='paciente_editar'),
    path('formularios/<slug:pk>', PacienteView.as_view(), name='paciente'),
    path('listar/', PacienteList.as_view(), name='paciente_listar'),
    path('eliminar/<int:pk>/', PacienteDelete.as_view(), name='paciente_eliminar'),
    path('medico/nuevo', MedicoCreate.as_view(), name='medico_crear'),
    path('medico/listar', MedicoList.as_view(), name='medico_listar'),
    path('medico/editar/<int:pk>/', MedicoUpdate.as_view(), name='medico_editar'),
    path('medico/eliminar/<int:pk>/', MedicoDelete.as_view(), name='medico_eliminar'),
]
