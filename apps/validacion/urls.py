
from django.urls import path

from apps.validacion.views import Campos_defectoCreate, Campos_defectoUpdate, Campos_defectoList, Campos_defectoDelete, \
    TaskgroupCreate, TaskgroupUpdate, TaskgroupDelete, PipelinesCreate, PipelinesUpdate, PipelinesDelete, PipelinesList

urlpatterns = [


    path('nuevo', Campos_defectoCreate.as_view(), name='filtro_crear'),
    path('editar/<int:pk>/', Campos_defectoUpdate.as_view(), name='filtro_editar'),
    path('filtros/', Campos_defectoList.as_view(), name='filtro_listar'),
    path('eliminar/<int:pk>/', Campos_defectoDelete.as_view(), name='filtro_eliminar'),

    path('grupos/crear', TaskgroupCreate.as_view(), name='grupo_crear'),
    path('grupos/editar/<int:pk>/', TaskgroupUpdate.as_view(), name='grupo_editar'),
    path('grupos/eliminar/<int:pk>/', TaskgroupDelete.as_view(), name='grupo_eliminar'),

    path('pipelines/crear', PipelinesCreate.as_view(), name='pipelines_crear'),
    path('pipelines/editar/<int:pk>/', PipelinesUpdate.as_view(), name='pipelines_editar'),
    path('pipelines/eliminar/<int:pk>/', PipelinesDelete.as_view(), name='pipelines_eliminar'),

    path('pipelines/listar/', PipelinesList.as_view(), name='pipelines_listar'),


]
