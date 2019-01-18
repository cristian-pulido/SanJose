from django.db import models

# Create your models here.
from apps.paciente.models import Control, Candidato
from apps.validacion.models import Pipeline


class taskc(models.Model):

    numero=models.CharField(max_length=100)
    control = models.ForeignKey(Control,on_delete=models.CASCADE,null=True)
    sujeto = models.ForeignKey(Candidato, on_delete=models.CASCADE,null=True)
    proceso = models.ForeignKey(Pipeline,on_delete=models.CASCADE,null=True)
    estado = models.CharField(max_length=50,default="No Creado")

    def __str__(self):
        return '{}'.format(self.numero)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
