
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

class Realineacion(models.Model):
    sujeto = models.CharField(max_length=15, null=True, blank=True)
    structural = models.FileField(upload_to="Archivos",null=True,blank=True)
    structural_cambio=models.BooleanField(default=False)
    funcional = models.FileField(upload_to="Archivos",null=True,blank=True)
    funcional_cambio = models.BooleanField(default=False)
    tensor = models.FileField(upload_to="Archivos",null=True,blank=True)
    tensor_cambio = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.sujeto)
    class Meta:
        permissions = (
            ("can_ver_alineacion", u"puede ver alineacion"),

        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Snr(models.Model):

    sujeto = models.CharField(max_length=15, null=True, blank=True)
    structural=models.CharField(max_length=30, null=True)
    funcional=models.CharField(max_length=30, null=True)
    funcional_plot=models.CharField(max_length=300,null=True,blank=True)
    tensor=models.CharField(max_length=30, null=True)
    tensor_plot = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.sujeto)
    class Meta:
        permissions = (
            ("can_ver_snr", u"puede ver snr"),

        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Task(models.Model):
    nombre = models.CharField(max_length=100)
    pathscript = models.CharField(max_length=150)
    dependencia = models.ForeignKey('self', on_delete=None, null=True, default=None, blank=True)
    habilitado = models.BooleanField(default=True)
    tipo_imagen = models.ForeignKey(Tipoimagenes, on_delete=None)

    def __str__(self):
        return '{}'.format(self.nombre)

class Taskgroup(models.Model):

    nombre=models.CharField(max_length=100)
    tasks=models.ManyToManyField(Task)
    tipo_imagen = models.ForeignKey(Tipoimagenes, on_delete=None)
    dependencia = models.ForeignKey('self',on_delete=None,null=True,default=None,blank=True)
    def __str__(self):
        return '{}'.format(self.nombre)

    def get_task(self):
        tasks = self.tasks.all()
        tareas = []
        for tar in tasks:
            if tar.dependencia == None or tar.dependencia not in tasks:
                tareas.append(tar)
                break
        contador = 0
        while len(tareas) != len(tasks):
            for tar in tasks:
                if tar in tareas:
                    continue
                else:
                    if tar.dependencia == tareas[contador]:
                        tareas.append(tar)
                        contador += 1

        return tareas



class Pipeline(models.Model):

    nombre=models.CharField(max_length=100)
    tipo_imagen=models.ForeignKey(Tipoimagenes,on_delete=None)
    pathout = models.CharField(max_length=150,null=True)
    dependencia=models.ForeignKey('self',on_delete=None,null=True,default=None,blank=True)

    grupos = models.ManyToManyField(Taskgroup)

    def __str__(self):
        return '{}'.format(self.nombre)


