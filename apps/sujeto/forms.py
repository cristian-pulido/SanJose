from django import forms

from apps.sujeto.models import Sujeto


class SujetoForm(forms.ModelForm):

    class Meta:
        model = Sujeto

        fields = [
            'nombres',
            'apellidos',
            'edad',
            'cc',
            'sexo',

        ]

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'cc': 'C.C',
            'sexo':'Sexo',
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control','placeholder': ('Este campo es requerido')}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'cc': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo':forms.Select(attrs={'class': 'form-control'}),
        }
