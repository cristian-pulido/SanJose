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
        context['D_previo_hist']=plots.D_previo_hist()
        context['D_especifico']=plots.D_especifico()
              

        
        
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

class graphs_clinica(TemplateView):
    template_name = 'graphs/clinica.html'
    def get_context_data(self, **kwargs):
        context = super(graphs_clinica, self).get_context_data(**kwargs)
        context['clinica_grupod']=plots.clinica_grupod()
        context['clinica_conciencia']=plots.clinica_conciencia()
        context['clinica_uci_g']=plots.clinica_uci_g()
        context['clinica_uci_egreso']=plots.clinica_uci_egreso()
        context['clinica_formularios']=plots.clinica_formularios()   
        context['clinica_a_patologicos']=plots.clinica_a_patologicos()   
        context['clinica_a_patologicos_cual'],context['a_toxico_alergenicos'],context['a_familiares']=plots.clinica_antecedentes()   
        
        
        

        return context

class graphs_uci(TemplateView):
    template_name = 'graphs/uci.html'
    def get_context_data(self, **kwargs):
        context = super(graphs_uci, self).get_context_data(**kwargs)
        context['uci_glasgow_ingreso']=plots.uci_glasgow_ingreso()   
        context['uci_variables_vs_egreso']=plots.uci_variables_vs_egreso() 
        context['uci_falla_organica']=plots.uci_falla_organica() 
        context['uci_glasgow_egreso']=plots.uci_glasgow_egreso() 
        context['uci_causa_mortalidad']=plots.uci_causa_mortalidad() 
        context['uci_dx_egreso']=plots.uci_dx_egreso()     
        
        return context

class graphs_neuropsicologia(TemplateView):
    template_name = 'graphs/neuropsicologia.html'
    def get_context_data(self, **kwargs):
        context = super(graphs_neuropsicologia, self).get_context_data(**kwargs)
        context['neuropsi_vs_G_diagnostico']=plots.neuropsi_vs_G_diagnostico()      
        context['neuropsi_vs_G_diagnostico_2']=plots.neuropsi_vs_G_diagnostico_2()      
        

        return context







        