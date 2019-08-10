from django.urls import path

from .views import graphs_dash,	graphs_demografico

urlpatterns = [

    path('dashboard', graphs_dash.as_view(),name='graph_dash'),
    path('demografico', graphs_demografico.as_view(),name='graph_demografico'),
    
]