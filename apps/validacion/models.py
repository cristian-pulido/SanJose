
from django.db import models

class Tipoimagenes(models.Model):
    nombre = models.CharField(max_length=75)
    nombre_aux = models.CharField(max_length=75,null=True,blank=True,default="")
    mostrar = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.nombre)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Tagsdicom(models.Model):
    num_tag = models.CharField(max_length=75)
    name_tag = models.CharField(max_length=200)
    key_tag = models.CharField(max_length=200,blank=True,null=True  )

    def __str__(self):
        return '{}'.format(self.name_tag)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Campostagimg(models.Model):
    tag = models.ForeignKey(Tagsdicom, on_delete=models.CASCADE)
    valor = models.CharField(max_length=200,null=True,blank=True,default="")
    medidas = models.CharField(max_length=50,null=True,blank=True,default="")
    visible = models.BooleanField(default=True)
    imagen = models.ForeignKey(Tipoimagenes,on_delete=models.CASCADE)
    sujeto = models.CharField(max_length=15,null=True,blank=True)
    precision = models.PositiveIntegerField(null=True,blank=True)
    v_esperado = models.CharField(max_length=150,null=True,blank=True,default="")
    cumple = models.NullBooleanField(default=None)

    def __str__(self):
        return '{}'.format(self.sujeto)
    class Meta:
        permissions = (
            ("can_ver_parametrosimg", u"puede ver parametrosimg"),

        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Campos_defecto(models.Model):
    imagen = models.ForeignKey(Tipoimagenes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tagsdicom, on_delete=models.CASCADE)
    precision = models.PositiveIntegerField(null=True, blank=True)
    v_esperado = models.CharField(max_length=150, null=True, blank=True, default="")
    medidas = models.CharField(max_length=50, null=True, blank=True, default="")

    def __str__(self):
        return '{}'.format(self.tag.name_tag)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
