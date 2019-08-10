from django.http import HttpResponse
from django.views.generic import TemplateView
from . import plots

class graphs_dash(TemplateView):
    template_name = 'graphs/plot.html'
    def get_context_data(self, **kwargs):
        context = super(graphs_dash, self).get_context_data(**kwargs)
        context['num_sujetos']=plots.num_sujetos()
        context['time_line_sujetos']=plots.time_line_sujetos()
        context['motivo_exclusion']=plots.motivo_exclusion()

        

        
        
        return context


class graphs_demografico(TemplateView):
    template_name = 'graphs/demografico.html'
    def get_context_data(self, **kwargs):
        context = super(graphs_demografico, self).get_context_data(**kwargs)
        context['demografico_continuo']=plots.demografico_continuo()
        context['demografico_categorical']=plots.demografico_categorical()        
        context['demografico_map']=plots.demografico_map()
        context['demografico_multi_scatter']=plots.demografico_multi_scatter()
        context['demografico_multi_categorical']=plots.demografico_multi_categorical()

        return context





        