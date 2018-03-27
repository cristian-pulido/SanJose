from django.db import models

# Create your models here.
from apps.fileupload.models import Picture

class Dprevio(models.Model):
    Traumaticos = "Traumáticos"
    Degenerativos = "Degenerativos"
    Neoplasticos = "Neoplásticos"
    Vasculares = "Vasculares"
    Infecciosos = "Infecciosos"
    Metabolicos = "Metabólicos"
    Tx_Neurodesarrollo = "Tx Neurodesarrollo"
    Tx_Psicótico = "TX Psicótico"
    Tx_Afectivo = "Tx Afectivo"
    Deficit = "Deficit cognitivo"
    Abuso = "Abuso de sustancias"
    Otro = "Otro"
    D_neuro_logico_psiquiatrico_previo_choices = (
    (Traumaticos, u"Traumáticos"), (Degenerativos, u"Degenerativos"), (Neoplasticos, u"Neoplásticos"),
    (Vasculares, u"Vasculares"), (Infecciosos, u"Infecciosos"), (Metabolicos, u"Metabólicos"),
    (Tx_Neurodesarrollo, u"Tx Neurodesarrollo"), (Tx_Psicótico, u"TX Psicótico"),
    (Tx_Afectivo, u"Tx Afectivo"), (Deficit, u"Deficit cognitivo"), (Abuso, u"Abuso de sustancias"),
    (Otro, u"Otro"))
    nombre=models.CharField(max_length=50,choices=D_neuro_logico_psiquiatrico_previo_choices)

    def __str__(self):
        return '{}'.format(self.nombre)


class Candidato(models.Model):
    sujeto_numero = models.PositiveIntegerField()
    fecha_de_registro= models.DateField()
    HC = models.PositiveIntegerField()
    CC = models.PositiveIntegerField()
    cama_numero =models.PositiveIntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=70)
    edad = models.PositiveIntegerField()
    #######sexo
    hombre = 'Hombre'
    mujer = 'Mujer'
    Sexo_choices = ((hombre, u'Hombre'), (mujer, u'Mujer'))
    sexo = models.CharField(max_length=9, choices=Sexo_choices)
    #########
    fecha_evento_principal = models.DateField()
    hora_evento_principal = models.TimeField(blank=True)
    ######## Grupo diagnostico
    TCE='TCE'
    H_A='Hipoxia/Anoxia'
    ACV='ACV'
    G_diagnostico_choices=((TCE, u'TCE'),(H_A, u'Hipoxia/Anoxia'),(ACV, u'ACV'))
    G_diagnostico=models.CharField(max_length=20,choices=G_diagnostico_choices)
    ######## Diagnosticos neuro / psiquiatricos previos
    D_neuro_logico_psiquiatrico_previo=models.ManyToManyField(Dprevio,blank=True)
    ###### Especificacion diagnosticos
    D_especificos = models.TextField(blank=True)
    ######## criterios de inclusion
    ci1=models.BooleanField("Paciente con episodio de parada cadíaca con reanimación exitosa")
    ci2=models.BooleanField("Paciente con Dx de lesión cerebral aguda de origen traumático o evento cerebrovascular")
    ci3=models.BooleanField("Puntaje en escala Glasgow igual o menor a 8 después del evento inicial")
    ci4=models.BooleanField("Paciente transportable a un resonador")

    ####### Criterios de exclusion
    ce1=models.BooleanField("Diagnóstico de muerte cerebral en las primeras 48 horas del ingreso a UCI")
    ce2=models.BooleanField("Destruccion masiva del parénquima cerebral no rescatable por neurocirugía")
    ce3=models.BooleanField("Decisión de la familia de no participar en estudios de investigación")

    #######resultado
    resultado=models.BooleanField("PACIENTE APTO PARA INGRESO AL ESTUDIO")

    medico_responsable=models.CharField(max_length=80)


    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)