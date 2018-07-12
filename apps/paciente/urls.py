
from django.urls import path

from apps.paciente.views import PacienteCreate, PacienteUpdate, MedicoCreate, MedicoList, MedicoUpdate, MedicoDelete, \
    PacienteList, PacienteView, PacienteDelete, IngresoUpdate, RadiologiaUpdate, UciUpdate, NeurologiaUpdate, \
    BoldUpdate, MayorUpdate, InformanteUpdate, SeguimientoUpdate, ControlView, ControlList, ControlDelete, \
    ControlCreate, ControlUpdate, MocaUpdate

urlpatterns = [

    path('nuevo', PacienteCreate.as_view(), name='paciente_crear'),
    path('control', ControlCreate.as_view(), name='control_crear'),
    path('editar/<int:pk>/', PacienteUpdate.as_view(), name='paciente_editar'),
    path('control/editar/<int:pk>/', ControlUpdate.as_view(), name='control_editar'),
    path('formularios/<slug:pk>', PacienteView.as_view(), name='paciente'),
    path('controles/<slug:pk>', ControlView.as_view(), name='control'),
    path('listar/', PacienteList.as_view(), name='paciente_listar'),
    path('controles/', ControlList.as_view(), name='controles_listar'),
    path('eliminar/<int:pk>/', PacienteDelete.as_view(), name='paciente_eliminar'),
    path('controles/eliminar/<int:pk>/', ControlDelete.as_view(), name='control_eliminar'),
    path('medico/nuevo', MedicoCreate.as_view(), name='medico_crear'),
    path('medico/listar', MedicoList.as_view(), name='medico_listar'),
    path('medico/editar/<int:pk>/', MedicoUpdate.as_view(), name='medico_editar'),
    path('medico/eliminar/<int:pk>/', MedicoDelete.as_view(), name='medico_eliminar'),
    path('ingreso/editar/<int:pk>/', IngresoUpdate.as_view(), name='ingreso_editar'),
    path('radiologia/editar/<int:pk>/', RadiologiaUpdate.as_view(), name='radiologia_editar'),
    path('uci/editar/<int:pk>/', UciUpdate.as_view(), name='uci_editar'),
    path('neurologia/editar/<int:pk>/', NeurologiaUpdate.as_view(), name='neurologia_editar'),
    path('bold/editar/<int:pk>/', BoldUpdate.as_view(), name='bold_editar'),
    path('mayor/editar/<int:pk>/', MayorUpdate.as_view(), name='mayor_editar'),
    path('informante/editar/<int:pk>/', InformanteUpdate.as_view(), name='informante_editar'),
    path('seguimiento/editar/<int:pk>/', SeguimientoUpdate.as_view(), name='seguimiento_editar'),
    path('moca/editar/<int:pk>/', MocaUpdate.as_view(), name='moca_editar'),


]
