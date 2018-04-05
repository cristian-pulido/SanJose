from django.db import models

# Create your models here.
from django.forms import ModelForm

from apps.fileupload.models import Picture


class Sujeto(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField(null=True)
    #imagen = models.ForeignKey(Picture, null=True, on_delete=models.CASCADE)
    imagen = models.OneToOneField(Picture, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

