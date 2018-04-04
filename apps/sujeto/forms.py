from django import forms

from apps.sujeto.models import Sujeto


class SujetoForm(forms.ModelForm):

    class Meta:
        model = Sujeto

        fields = [
            'nombre',
            'edad',
            'imagen',
        ]

        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
            'imagen': 'Imagen',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control'}),
        }
