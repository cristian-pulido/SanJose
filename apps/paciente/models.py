
import datetime
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
    nombre=models.CharField(max_length=50, choices=D_neuro_logico_psiquiatrico_previo_choices)

    def __str__(self):
        return '{}'.format(self.nombre)

class Apatologicos(models.Model):
    hta='HTA'
    diabetes='Diabetes'
    iam='IAM'
    hipotiroidismo='Hipotiroidismo'
    dislipidemia= 'Dislipidemia'
    otro='Otro'

    Apatologicos_choices= ((hta,u"HTA"),(diabetes,u"Diabetes"),(iam,u"IAM"),(hipotiroidismo,u"Hipotiroidismo"),(dislipidemia,u"Dislipidemia"),(otro,u"Otro"))
    nombre=models.CharField(max_length=50, choices=Apatologicos_choices)

    def __str__(self):
        return '{}'.format(self.nombre)


class Medico(models.Model):
    nombre = models.CharField(max_length=70)

    def get_pacientes(self):
        return self.candidato_set.all()
    def __str__(self):
        return '{}'.format(self.nombre)
class Candidato(models.Model):
    sujeto_numero = models.CharField(max_length=20, null=True, unique=True)
    fecha_de_registro= models.DateField(null=True)
    cc = models.PositiveIntegerField(null=True,unique=True)
    nombres = models.CharField(null=True, max_length=70)
    apellidos = models.CharField(null=True, max_length=70)
    edad = models.PositiveIntegerField(null=True)
    #######sexo
    hombre = 'Hombre'
    mujer = 'Mujer'
    Sexo_choices = ((hombre, u'Hombre'), (mujer, u'Mujer'))
    sexo = models.CharField(max_length=9, choices=Sexo_choices, null=True)
    ######
    HC = models.PositiveIntegerField(null=True, unique=True)
    cama_numero =models.PositiveIntegerField(null=True)
    fecha_evento_principal = models.DateField(null=True)
    hora_evento_principal = models.TimeField(blank=True, null=True, default=datetime.time(00, 00))
    fecha_ingreso = models.DateField(null=True)
    hora_ingreso = models.TimeField(blank=True, null=True, default=datetime.time(00, 00))
    ######## Grupo diagnostico
    TCE='TCE'
    H_A='Hipoxia/Anoxia'
    ACV='ACV'
    G_diagnostico_choices=((TCE, u'TCE'),(H_A, u'Hipoxia/Anoxia'),(ACV, u'ACV'))
    G_diagnostico=models.CharField(max_length=20, choices=G_diagnostico_choices, null=True)
    ######## Diagnosticos neuro / psiquiatricos previos
    D_neuro_logico_psiquiatrico_previo=models.ManyToManyField(Dprevio, blank=True)
    ###### Especificacion diagnosticos
    D_especificos = models.TextField(blank=True, null=True)
    ######## criterios de inclusion
    criterios_CHOICES = (
        ('ci1', 'Paciente con episodio de parada cadíaca con reanimación exitosa'),
        ('ci2', 'Paciente con Dx de lesión cerebral aguda de origen traumático o evento cerebrovascular'),
    )
    ci = models.CharField(choices=criterios_CHOICES, max_length=128, null=True, default='ci1')
    ci3 = models.NullBooleanField('Puntaje en escala Glasgow igual o menor a 8 después del evento inicial')
    ci4=models.NullBooleanField("Paciente transportable a un resonador")

    ####### Criterios de exclusion
    ce1=models.NullBooleanField("Diagnóstico de muerte cerebral en las primeras 48 horas del ingreso a UCI")
    ce2=models.NullBooleanField("Destruccion masiva del parénquima cerebral no rescatable por neurocirugía")
    ce3=models.NullBooleanField("Disfunción neurológica y/o neuropsiquiátrica previa")
    ce4=models.NullBooleanField("Decisión de la familia de no participar en estudios de investigación")
    #######
    #######resultado


    medico_responsable=models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    imagen = models.OneToOneField(Picture, blank=True, null=True, on_delete=models.CASCADE)
    estado = models.PositiveIntegerField(null=True, default=1)
    inscrito = models.NullBooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.sujeto_numero)

    class Meta:
        ordering = ('sujeto_numero',)

class Ingreso(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fecha_form = models.DateField(null=True)
    lugar_nacimiento = models.CharField(max_length=80,null=True, blank=True)
    lugar_residencia = models.CharField(max_length=80,null=True,blank=True)
    direccion = models.CharField(max_length=100,null=True,blank=True)
    nombre_acompanante = models.CharField(max_length=70,null=True,blank=True)
    tel1 = models.PositiveIntegerField(null=True,blank=True)
    tel2 = models.PositiveIntegerField(null=True,blank=True)
    peso =models.PositiveIntegerField(null=True,blank=True)
    estatura = models.PositiveIntegerField(null=True,blank=True)
    ####### nivel educativo
    primaria = 'Primaria'
    bachillerato = 'Bachillerato'
    tecnico = 'Técnico'
    profesional = 'Profesional'
    educativo_choices = ((primaria, u'Primaria'), (bachillerato, u'Bachillerato'), (tecnico, u'Técnico'),(profesional, u'Profesional'))
    n_educativo = models.CharField(max_length=20, choices=educativo_choices, null=True,blank=True)
    ######
    ####### lateralidad
    diestro = 'Diestro'
    zurdo = 'Zurdo'
    ambidiestro = 'Ambidiestro'
    lateralidad_choices = ((diestro, u'Diestro'), (zurdo, u'Zurdo'), (ambidiestro, u'Ambidiestro'))
    lateralidad = models.CharField(max_length=20, choices=lateralidad_choices, null=True,blank=True)
    ######
    ####### conciencia
    coma = 'Coma'
    svsr = 'SVSR'
    emc = 'EMC'
    conciencia_choices = ((coma, u'Coma'), (svsr, u'SVSR'), (emc, u'EMC'))
    conciencia = models.CharField(max_length=20, choices=conciencia_choices, null=True,blank=True)
    ######
    sedado=models.NullBooleanField("Sedado por neuroprotección")
    a_patologicos = models.ManyToManyField(Apatologicos, blank=True)
    a_patologicos_cual= models.CharField(max_length=50, null=True)
    ######## antecedentes quirurgicos
    quirurgicos_CHOICES = (
        ('craneotomia', 'Craneotomía'),
        ('otro', 'Otro'),
    )
    quirurgicos = models.CharField(choices=quirurgicos_CHOICES, max_length=128, null=True,blank=True)
    fecha_craneotomia=models.DateField(blank=True, null=True)
    causa_quirurgicos = models.CharField(max_length=100,null=True, blank=True)
    a_toxico_alergenicos= models.CharField(max_length=180,null=True, blank=True)
    a_farmaco1=models.CharField(max_length=180,null=True, blank=True)
    a_farmaco1_dosis=models.CharField(max_length=30,null=True, blank=True)
    a_farmaco2 = models.CharField(max_length=180, null=True, blank=True)
    a_farmaco2_dosis = models.CharField(max_length=30, null=True, blank=True)
    a_familiares=models.CharField(max_length=180,null=True, blank=True)
    firma_consentimiento=models.BooleanField(default=True)
    firma_causa=models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)

class Radiologia(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fecha_procedimiento = models.DateField(null=True)
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    transportable = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    hora_inicio = models.TimeField(null=True, default=datetime.time(00, 00))
    jefe_enfermeria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    aux_enfermeria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    medico_uci = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    anestesiologo = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    terapeuta_respiratorio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    vmi = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    vasopresor= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ionotropico= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_pulsoximetro= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_pulsoximetro_sv=models.CharField(max_length=50, null=True,blank=True)
    ur_frecuencia_cardiaca= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_frecuencia_cardiaca_sv = models.CharField(max_length=50, null=True, blank=True)
    ur_frecuencia_respiratoria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_frecuencia_respiratoria_sv = models.CharField(max_length=50, null=True, blank=True)
    ur_visoscopio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_visoscopio_sv = models.CharField(max_length=50, null=True, blank=True)
    ur_tension= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_tension_sv = models.CharField(max_length=50, null=True, blank=True)
    pic=models.CharField(max_length=25,null=True,blank=True)
    ppc = models.CharField(max_length=25, null=True, blank=True)
    medicamentos_emergencia = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    me_cual = models.CharField(max_length=25,null=True,blank=True)
    me_dosis= models.CharField(max_length=25,null=True,blank=True)
    sedacion=models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    sedacion_dt=models.CharField(max_length=25, null=True, blank=True)
    sedacion_sv = models.CharField(max_length=25, null=True, blank=True)
    analgesia = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    analgesia_dt = models.CharField(max_length=25, null=True, blank=True)
    analgesia_sv = models.CharField(max_length=25, null=True, blank=True)
    relajacion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    relajacion_dt = models.CharField(max_length=25, null=True, blank=True)
    relajacion_sv = models.CharField(max_length=25, null=True, blank=True)
    otra_medicacion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    otra_medicacion_dt = models.CharField(max_length=25, null=True, blank=True)
    otra_medicacion_cual = models.CharField(max_length=25, null=True, blank=True)
    ru_pulsoximetro = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_pulsoximetro_sv = models.CharField(max_length=50, null=True, blank=True)
    ru_frecuencia_cardiaca = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_frecuencia_cardiaca_sv = models.CharField(max_length=50, null=True, blank=True)
    ru_frecuencia_respiratoria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_frecuencia_respiratoria_sv = models.CharField(max_length=50, null=True, blank=True)
    ru_visoscopio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_visoscopio_sv = models.CharField(max_length=50, null=True, blank=True)
    ru_tension = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_tension_sv = models.CharField(max_length=50, null=True, blank=True)
    tiempo_sesonacia=models.CharField(max_length=50,null=True)
    hora_llegada = models.TimeField(null=True, default=datetime.time(00, 00), blank=True)
    complicaciones = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    complicaciones_cuales = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)


class Uci(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fechauci = models.DateField(null=True)
    horauci = models.TimeField(null=True, default=datetime.time(00, 00))
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    numero_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )
    apertura_ocular = models.CharField(choices=numero_CHOICES, max_length=5, null=True)
    respuesta_motora = models.CharField(choices=numero_CHOICES, max_length=5, null=True)
    respuesta_verbal = models.CharField(choices=numero_CHOICES, max_length=5, null=True)
    glasgowtotal = models.CharField(max_length=5,null=True,default=0)


    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)