from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from apps.sujeto.views import SujetoCreate, SujetoUpdate

urlpatterns = [

    path('nuevo', SujetoCreate.as_view(), name='sujeto_crear'),
    path('editar/<int:pk>/', SujetoUpdate.as_view(), name='sujeto_editar'),

]
