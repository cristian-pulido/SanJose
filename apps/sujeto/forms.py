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
            'imagen',
        ]

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'cc': 'C.C',
            'sexo':'Sexo',
            'imagen': 'Imagen',
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'cc': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo':forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.Select(attrs={'class': 'form-control'}),
        }
