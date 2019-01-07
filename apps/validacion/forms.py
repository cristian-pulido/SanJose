
from django import forms

from apps.validacion.models import Campos_defecto, Taskgroup, Pipeline


class Campos_defectoForm(forms.ModelForm):
    class Meta:
        model = Campos_defecto


        fields = [
            'imagen',
            'tag',
            'precision',
            'v_esperado',
            'medidas',
        ]

        labels = {
            'imagen': "Tipo de imágen",
            'tag': "Nombre del tag (Dicom)",
            'precision':"Toleracia (%)",
            'v_esperado': "Valor Esperado",
            'medidas': "Unidades de medida",

        }
        widgets = {
            'imagen': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'precision': forms.TextInput(attrs={'class': 'form-control', 'maxlength':3,'autocomplete':"off", 'placeholder': ('Entre 0 y 100'),'oninput': "this.value = this.value.replace(/[^0-9]/, '')"}),
            'v_esperado': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'medidas':forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
        }

class gruposForm(forms.ModelForm):
    class Meta:
        model = Taskgroup


        fields = [
            'nombre',
            'tasks',
            'tipo_imagen',
            'dependencia',

        ]

        labels = {
            'nombre':"Nombre",
            'tasks':"Tareas",
            'tipo_imagen':"Tipo de Imagen",
            'dependencia':"Dependencia",


        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'tasks': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tipo_imagen': forms.Select(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
        }

class pipelinesForm(forms.ModelForm):
    class Meta:
        model = Pipeline




        fields = [
            'nombre',
            'tipo_imagen',
            'grupos',
            'dependencia',

        ]

        labels = {
            'nombre':"Nombre",
            'tipo_imagen':"Tipo de Imagen",
            'grupos': "Grupos",
            'dependencia':"Dependencia",


        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'tipo_imagen': forms.Select(attrs={'class': 'form-control'}),
            'grupos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
        }

