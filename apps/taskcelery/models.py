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
        if self.sujeto:
            return 'sujeto %s - proceso %s' % (self.sujeto.sujeto_numero,self.proceso.nombre)
        elif self.control:
            return 'control %s - proceso %s' % (self.control.numero,self.proceso.nombre)
        else:
            return 'algo {}'.format(self.estado)

    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
