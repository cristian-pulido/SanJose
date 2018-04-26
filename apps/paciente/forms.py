
from django import forms
from apps.paciente.models import Candidato, Dprevio, Medico, Ingreso
from django.forms.widgets import CheckboxSelectMultiple

class MedicoForm(forms.ModelForm):

    class Meta:
        model = Medico
        fields = ['nombre',]
        labels = {'nombre': "Nombre",}
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': ('Nombre')}),}


class PacienteForm(forms.ModelForm):


    class Meta:
        model = Candidato

        fields = [
            'nombres',
            'apellidos',
            'edad',
            'cc',
            'sexo',
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
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'cc': 'C.C',
            'sexo': 'Sexo',
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
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Este campo es requerido')}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'cc': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'sujeto_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_de_registro': forms.TextInput(attrs={'class': 'form-control'}),
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
            'medico_responsable': forms.Select(attrs={'class': 'form-control'}),


        }

class IngresoForm(forms.ModelForm):


    class Meta:
        model = Ingreso

        fields = [
            'fecha_form',
            'lugar_nacimiento',
            'lugar_residencia',
            'direccion',
            'nombre_acompanante',
            'tel1',
            'tel2',
            'peso',
            'estatura',
            'n_educativo',
            'lateralidad',
            'conciencia',
            'sedado',
            'a_patologicos',
            'a_patologicos_cual',
            'quirurgicos',
            'fecha_craneotomia',
            'causa_quirurgicos',
            'a_toxico_alergenicos',
            'a_farmaco1',
            'a_farmaco1_dosis',
            'a_farmaco2',
            'a_farmaco2_dosis',
            'a_familiares',
            'firma_consentimiento',
            'firma_causa',


        ]

        labels = {
            'fecha_form':"Fecha",
            'lugar_nacimiento':"Lugar de nacimiento",
            'lugar_residencia': "Lugar de residencia",
            'direccion':"Dirección",
            'nombre_acompanante':"Nombre Acompañante",
            'tel1': "Teléfono de contacto 1",
            'tel2': "Teléfono de contacto 2",
            'peso': "Peso",
            'estatura':"Estatura",
            'n_educativo':"Nivel Educativo",
            'lateralidad':"Lateralidad",
            'conciencia':"Estado de Conciencia",
            'sedado': "Sedado por neuroprotección",
            'a_patologicos':"Antecedentes Patológicos",
            'quirurgicos':"Antecedentes quirúrgicos",
            'causa_quirurgicos':"Especifique causa:",
            'a_toxico_alergenicos':"Antecedentes Tóxico alérgicos",
            'a_farmaco1_dosis':"Dosis total/día",
            'a_farmaco2_dosis':"Dosis total/día",
            'a_familiares':"Antecedentes Familiares relevantes",
            'firma_consentimiento':"Firma de consentimiento informado",
            'firma_causa':"Causa",
             }
        widgets = {
            'fecha_form': forms.SelectDateWidget(years=range(2017, 2020)),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_acompanante': forms.TextInput(attrs={'class': 'form-control'}),
            'tel1': forms.TextInput(attrs={'class': 'form-control'}),
            'tel2': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Peso en Kilogramos')}),
            'estatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Estatura en centimetros')}),
            'n_educativo': forms.Select(attrs={'class': 'form-control'}),
            'lateralidad': forms.Select(attrs={'class': 'form-control'}),
            'conciencia': forms.Select(attrs={'class': 'form-control'}),
            'sedado': forms.CheckboxInput(),
            'a_patologicos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'a_patologicos_cual': forms.TextInput(attrs={'class': 'form-control'}),
            'quirurgicos': forms.Select(attrs={'class': 'form-control'}),
            'fecha_craneotomia':forms.SelectDateWidget(),
            'causa_quirurgicos': forms.TextInput(attrs={'class': 'form-control'}),
            'a_toxico_alergenicos': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco1': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco1_dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco2': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco2_dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'a_familiares': forms.TextInput(attrs={'class': 'form-control'}),
            'firma_consentimiento': forms.CheckboxInput(),
            'firma_causa': forms.TextInput(attrs={'class': 'form-control'}),
        }
