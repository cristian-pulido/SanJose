from django.db import models

# Create your models here.
from django.forms import ModelForm

from apps.fileupload.models import Picture


class Sujeto(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=70, null=True)
    edad = models.PositiveIntegerField(null=True)
    cc = models.PositiveIntegerField(null=True)
    #######sexo
    hombre = 'Hombre'
    mujer = 'Mujer'
    Sexo_choices = ((hombre, u'Hombre'), (mujer, u'Mujer'))
    sexo = models.CharField(max_length=9, choices=Sexo_choices, null=True)
    imagen = models.OneToOneField(Picture, null=True, on_delete=models.CASCADE)
    estado = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return '{}'.format(self.pk)

    def delete(self, using=None, keep_parents=False):

        self.imagen.delete()