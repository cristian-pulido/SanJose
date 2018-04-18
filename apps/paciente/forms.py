
from django import forms

from apps.paciente.models import Candidato
from django.contrib.admin import widgets

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
            'G_diagnostico',
            'D_neuro_logico_psiquiatrico_previo',
            'D_especificos',

        ]

        labels = {
            'sujeto_numero' : "Sujeto #",
            'fecha_de_registro' : "Fecha de Registro",
            'HC': "Historia Clinica",
            'cama_numero': 'Cama UCI',
            'fecha_evento_principal': "Fecha de evento principal",
            'hora_evento_principal': "Hora de evento principal",
            'G_diagnostico': 'Grupo diagnóstico',
            'D_neuro_logico_psiquiatrico_previo': "Diagnósticos neurológicos/psiquiátricos previos al evento",
            'D_especificos': 'Especifique diagnóstico',
        }
        widgets = {
            'sujeto_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_de_registro': forms.DateInput(attrs={'class': 'form-control'}),
            'HC':forms.TextInput(attrs={'class': 'form-control'}),
            'cama_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_evento_principal': forms.DateInput(attrs={'class': 'form-control'}),
            'hora_evento_principal': forms.TimeInput(attrs={'class': 'form-control'}),
            'G_diagnostico': forms.Select(attrs={'class': 'form-control'}),
            'D_especificosD_neuro_logico_psiquiatrico_previo': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'D_especificos': forms.Textarea(attrs={'class': 'form-control'}),
        }