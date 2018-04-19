
from django import forms
from apps.paciente.models import Candidato, Dprevio
from django.forms.widgets import CheckboxSelectMultiple


class PacienteForm(forms.ModelForm):



    class Meta:
        model = Candidato

        fields = [
            'sujeto_numero',
            'fecha_de_registro',
            'HC',
            'cama_numero',
            'fecha_evento_principal',
            'hora_evento_principal',
            'fecha_ingreso',
            'hora_ingreso',
            'G_diagnostico',
            'D_neuro_logico_psiquiatrico_previo',
            'D_especificos',
            'ci',
            'ci3',
            'ci4',
            'ce1',
            'ce2',
            'ce3',
            'ce4',
            'medico_responsable',


        ]

        labels = {
            'sujeto_numero' : "Sujeto #",
            'fecha_de_registro' : "Fecha de Registro",
            'HC': "Historia Clinica",
            'cama_numero': 'Cama UCI',
            'fecha_evento_principal': "Fecha de evento principal",
            'hora_evento_principal': "Hora de evento principal",
            'fecha_ingreso': "Fecha de ingreso UCI",
            'hora_ingreso': "Hora de ingreso UCI",
            'G_diagnostico': 'Grupo diagnóstico',
            'D_neuro_logico_psiquiatrico_previo': "Diagnósticos neurológicos/psiquiátricos previos al evento",
            'D_especificos': 'Especifique diagnóstico',
            'medico_responsable': "Medico Responsable",
             }
        widgets = {
            'sujeto_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_de_registro': forms.SelectDateWidget(years=range(2017, 2020)),
            'HC':forms.TextInput(attrs={'class': 'form-control'}),
            'cama_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_evento_principal': forms.SelectDateWidget(years=range(2017, 2020)),
            'hora_evento_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.SelectDateWidget(years=range(2017, 2020)),
            'hora_ingreso': forms.TextInput(attrs={'class': 'form-control'}),
            'G_diagnostico': forms.Select(attrs={'class': 'form-control'}),
            'D_neuro_logico_psiquiatrico_previo': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'D_especificos': forms.Textarea(attrs={'class': 'form-control'}),
            'ci': forms.RadioSelect(),
            'ci3': forms.CheckboxInput(),
            'ci4': forms.CheckboxInput(),
            'ce1': forms.CheckboxInput(),
            'ce2': forms.CheckboxInput(),
            'ce3': forms.CheckboxInput(),
            'ce4': forms.CheckboxInput(),
            'medico_responsable': forms.TextInput(attrs={'class': 'form-control'}),


        }
