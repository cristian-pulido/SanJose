
from django.urls import path

from apps.paciente.views import PacienteCreate, PacienteUpdate, MedicoCreate, MedicoList, MedicoUpdate, MedicoDelete, \
    PacienteList, PacienteView, PacienteDelete, IngresoUpdate, RadiologiaUpdate, UciUpdate, NeurologiaUpdate, BoldUpdate

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
    path('ingreso/editar/<int:pk>/', IngresoUpdate.as_view(), name='ingreso_editar'),
    path('radiologia/editar/<int:pk>/', RadiologiaUpdate.as_view(), name='radiologia_editar'),
    path('uci/editar/<int:pk>/', UciUpdate.as_view(), name='uci_editar'),
    path('neurologia/editar/<int:pk>/', NeurologiaUpdate.as_view(), name='neurologia_editar'),
    path('bold/editar/<int:pk>/', BoldUpdate.as_view(), name='bold_editar'),
]
