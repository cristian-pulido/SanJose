from django.urls import path

from .views import graphs_dash,	graphs_demografico, graphs_clinica, graphs_uci, graphs_neuropsicologia, graphs_neurologia

urlpatterns = [

    path('dashboard', graphs_dash.as_view(),name='graph_dash'),
    path('demografico', graphs_demografico.as_view(),name='graph_demografico'),
    path('clinica', graphs_clinica.as_view(),name='graph_clinica'),
    path('uci', graphs_uci.as_view(),name='graph_uci'),
    path('neuropsicologia', graphs_neuropsicologia.as_view(),name='graph_neuropsicologia'),
    path('neurologia', graphs_neurologia.as_view(),name='graph_neurologia'),
    
]
