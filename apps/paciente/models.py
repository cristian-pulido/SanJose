
import datetime
import shutil

from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone

from apps.fileupload.models import Picture
from programas import definitions


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
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


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
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Medico(models.Model):
    nombre = models.CharField(max_length=70)

    def get_pacientes(self):
        return self.candidato_set.all()
    def __str__(self):
        return '{}'.format(self.nombre)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
class Candidato(models.Model):
    sujeto_numero = models.PositiveIntegerField(null=True, unique=True)
    fecha_de_registro= models.DateField(null=True, default=timezone.now)
    cc = models.PositiveIntegerField(null=True, unique=True)
    nombres = models.CharField(null=True, max_length=50, default="")
    apellidos = models.CharField(null=True, max_length=50, default="")
    fecha_nacimiento = models.DateField(null=True)
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
    hora_evento_principal = models.TimeField(blank=True, null=True)
    fecha_hora_ingreso = models.DateTimeField(null=True)

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
        ('Paciente con episodio de parada cardíaca con reanimación exitosa', 'Paciente con episodio de parada cardíaca con reanimación exitosa'),
        ('Paciente con Dx de lesión cerebral aguda de origen traumático', 'Paciente con Dx de lesión cerebral aguda de origen traumático'),
        ('Paciente con Dx de lesión cerebral aguda por evento cerebrovascular', 'Paciente con Dx de lesión cerebral aguda por evento cerebrovascular'),

    )
    ci = models.CharField(choices=criterios_CHOICES, max_length=128, null=True, default='Paciente con episodio de parada cardíaca con reanimación exitosa',blank=True)
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
    imagen = models.FileField(null=True, upload_to="img",blank=True)
    estado = models.PositiveIntegerField(null=True, default=0)
    inscrito = models.NullBooleanField(default=False)
    archivo = models.FileField(null=True, upload_to="img", blank=True)

    def __str__(self):
        return '{}'.format(self.sujeto_numero)

    def get_seguimiento(self):
        return self.seguimiento_set.all().order_by('fechaseguimiento')
    def get_radio(self):
        return self.cambioradiologia_set.all()
    def get_neuro(self):
        return self.neurologia_set.all().order_by('fechaneuro')
    def get_img(self):
        i=Picture.objects.get(slug=self.sujeto_numero)
        return i

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        c = self
        n=c.sujeto_numero
        shutil.rmtree(settings.MEDIA_ROOT+"/img/sujeto"+str(n), ignore_errors=True)
        super(Candidato, self).delete(*args, **kwargs)
        try:
            i=Picture.objects.get(slug=str(n))
            i.delete()
        except:
            ""

    class Meta:
        permissions = (
            ("can_descargar_candidato", u"puede descargar candidato"),
        )

    class ReportBuilder:
        exclude = ('nombres','apellidos','cc','imagen','id', 'archivo', )  # Lists or tuple of excluded fields


class Ingreso(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fecha_form = models.DateField(null=True)
    lugar_nacimiento = models.CharField(max_length=80, null=True, default="")
    lugar_residencia = models.CharField(max_length=80, null=True, default="")
    direccion = models.CharField(max_length=60, null=True, blank=True)
    nombre_acompanante = models.CharField(max_length=50,null=True, default="")
    tel1 = models.PositiveIntegerField(null=True)
    tel2 = models.PositiveIntegerField(null=True, blank=True)
    peso =models.PositiveIntegerField(null=True, blank=True)
    estatura = models.PositiveIntegerField(null=True, blank=True)
    ####### nivel educativo
    Analfabeta = 'Analfabeta'
    primaria = 'Primaria'
    bachillerato = 'Bachillerato'
    tecnico = 'Técnico'
    profesional = 'Profesional'
    educativo_choices = ((Analfabeta, u'Analfabeta'),(primaria, u'Primaria'), (bachillerato, u'Bachillerato'), (tecnico, u'Técnico'), (profesional, u'Profesional'))
    n_educativo = models.CharField(max_length=20, choices=educativo_choices, null=True)
    ######
    ####### lateralidad
    diestro = 'Diestro'
    zurdo = 'Zurdo'
    ambidiestro = 'Ambidiestro'
    lateralidad_choices = ((diestro, u'Diestro'), (zurdo, u'Zurdo'), (ambidiestro, u'Ambidiestro'))
    lateralidad = models.CharField(max_length=20, choices=lateralidad_choices, null=True)
    ######
    ####### conciencia
    coma = 'Coma'
    svsr = 'SVSR'
    emc = 'EMC'
    conciencia_choices = ((coma, u'Coma'), (svsr, u'SVSR'), (emc, u'EMC'))
    conciencia = models.CharField(max_length=20, choices=conciencia_choices, null=True)
    ######
    sedado=models.NullBooleanField("Sedado por neuroprotección")
    a_patologicos = models.ManyToManyField(Apatologicos, blank=True)
    a_patologicos_cual= models.CharField(max_length=50, null=True,blank=True)


    fecha_craneotomia=models.DateField(blank=True, null=True)
    causa_quirurgicos = models.CharField(max_length=100, null=True, blank=True)

    a_toxico_alergenicos= models.CharField(max_length=50, null=True, blank=True)
    a_farmaco1=models.CharField(max_length=50, null=True, blank=True)
    a_farmaco1_dosis=models.CharField(max_length=30, null=True, blank=True)
    a_farmaco2 = models.CharField(max_length=50, null=True, blank=True)
    a_farmaco2_dosis = models.CharField(max_length=30, null=True, blank=True)
    a_familiares=models.CharField(max_length=50, null=True, blank=True)
    firma_consentimiento=models.BooleanField(default=True)
    firma_causa=models.CharField(max_length=50, null=True,blank=True)
    fechafirma=models.DateField(null=True, blank=True)
    archivo = models.FileField(null=True, upload_to="img", blank=True)
    archivofirma = models.FileField(null=True, upload_to="img", blank=True)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.archivo.delete(False)
        super(Ingreso, self).delete(*args, **kwargs)
    class Meta:
        permissions = (
            ("can_ver_ingreso", u"puede ver ingreso"),
        )
    class ReportBuilder:
        exclude = ('id','archivo','archivofirma','direccion' )  # Lists or tuple of excluded fields


class Radiologia(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fecha_procedimiento = models.DateField(null=True)
    radiologo=models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    transportable = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True,default='SI')
    hora_inicio = models.TimeField(null=True)
    jefe_enfermeria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    aux_enfermeria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    medico_uci = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    anestesiologo = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    terapeuta_respiratorio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    vmi = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    vasopresor= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ionotropico= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_pulsoximetro= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_pulsoximetro_sv=models.CharField(max_length=2, null=True,blank=True)
    ur_frecuencia_cardiaca= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_frecuencia_cardiaca_sv = models.CharField(max_length=3, null=True, blank=True)
    ur_frecuencia_respiratoria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_frecuencia_respiratoria_sv = models.CharField(max_length=2, null=True, blank=True)
    ur_visoscopio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_visoscopio_sv = models.CharField(max_length=25, null=True, blank=True)
    ur_tension= models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ur_tension_sv = models.CharField(max_length=7, null=True, blank=True)
    monitoreo=models.CharField(max_length=50, null=True, choices=seleccion_CHOICES)
    pic=models.CharField(max_length=10, null=True, blank=True)
    ppc = models.CharField(max_length=10, null=True, blank=True)
    medicamentos_emergencia = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    me_cual = models.CharField(max_length=15, null=True,blank=True)
    me_dosis= models.CharField(max_length=15, null=True,blank=True)
    sedacion=models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    sedacion_dt=models.CharField(max_length=25, null=True, blank=True)
    sedacion_sv = models.CharField(max_length=2, null=True, blank=True)
    analgesia = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    analgesia_dt = models.CharField(max_length=25, null=True, blank=True)
    analgesia_sv = models.CharField(max_length=3, null=True, blank=True)
    relajacion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    relajacion_dt = models.CharField(max_length=25, null=True, blank=True)
    relajacion_sv = models.CharField(max_length=3, null=True, blank=True)
    svadicional1 = models.CharField(max_length=25, null=True, blank=True)
    svadicional2 = models.CharField(max_length=7, null=True, blank=True)
    otra_medicacion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    otra_medicacion_dt = models.CharField(max_length=25, null=True, blank=True)
    otra_medicacion_cual = models.CharField(max_length=25, null=True, blank=True)
    ru_pulsoximetro = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_pulsoximetro_sv = models.CharField(max_length=2, null=True, blank=True)
    ru_frecuencia_cardiaca = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_frecuencia_cardiaca_sv = models.CharField(max_length=3, null=True, blank=True)
    ru_frecuencia_respiratoria = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_frecuencia_respiratoria_sv = models.CharField(max_length=3, null=True, blank=True)
    ru_visoscopio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_visoscopio_sv = models.CharField(max_length=25, null=True, blank=True)
    ru_tension = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ru_tension_sv = models.CharField(max_length=7, null=True, blank=True)
    tiempo_sesonacia=models.CharField(max_length=50, null=True)
    hora_llegada = models.TimeField(null=True)
    complicaciones = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    complicaciones_cuales = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_radiologia", u"puede ver radiologia"),
        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Uci(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fechauci = models.DateField(null=True)
    horauci = models.TimeField(null=True)
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
    fallaorganica = models.CharField(choices=seleccion_CHOICES,max_length=12,null=True)
    fallaorganica_cual = models.CharField(max_length=50,null=True,blank=True,default="")
    sepsis = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    presion_intracraneana = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    monitoria_pic = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    ventilacionmecanica = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    soportevasopresor = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    noradrenalina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, blank=True)
    vasopresina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, blank=True)
    adrenalina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, blank=True)
    midazolan = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    midazolan_dt = models.CharField(max_length=50, null=True, blank=True)
    tiopental = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    tiopental_dt = models.CharField(max_length=50, null=True, blank=True)
    dexmedetomidina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    dexmedetomidina_dt = models.CharField(max_length=50, null=True, blank=True)
    morfina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    morfina_dt = models.CharField(max_length=50, null=True, blank=True)
    hidromorfona = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    hidromorfona_dt = models.CharField(max_length=50, null=True, blank=True)
    fentanyl = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    fentanyl_dt = models.CharField(max_length=50, null=True, blank=True)
    fenitoina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    fenitoina_dt = models.CharField(max_length=50, null=True, blank=True)
    topiramato = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    topiramato_dt = models.CharField(max_length=50, null=True, blank=True)
    acido_valproico = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    acido_valproico_dt = models.CharField(max_length=50, null=True, blank=True)
    levetiracetam = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    levetiracetam_dt = models.CharField(max_length=50, null=True, blank=True)
    lacosamida = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    lacosamida_dt = models.CharField(max_length=50, null=True, blank=True)
    clozapina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    clozapina_dt = models.CharField(max_length=50, null=True, blank=True)
    haloperidol = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    haloperidol_dt = models.CharField(max_length=50, null=True, blank=True)
    ketiapina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    ketiapina_dt = models.CharField(max_length=50, null=True, blank=True)
    carbamacepina = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    carbamacepina_dt = models.CharField(max_length=50, null=True, blank=True)
    carbonato_litio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default="NO")
    carbonato_litio_dt = models.CharField(max_length=50, null=True, blank=True)
    valorable_neuro = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    valorable_neuro_causa = models.CharField(max_length=50, null=True, blank=True)
    continua_studio = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True)
    fechaegreso = models.DateField(null=True, blank=True)
    horaegreso = models.TimeField(null=True, blank=True)
    condicion_CHOICES = (
        ('Vivo', 'Vivo'),
        ('Remitido', 'Remitido'),
        ('Fallecido', 'Fallecido'),
    )
    condicion_egreso=models.CharField(max_length=100, choices=condicion_CHOICES, null=True,blank=True)
    dx_egreso=models.CharField(max_length=230,null=True,blank=True,default="")
    causa_mortalidad=models.CharField(max_length=200,null=True,blank=True)
    fechamortalidad=models.DateField(null=True, blank=True)
    horamortalidad = models.TimeField(null=True, blank=True)
    apertura_ocular_e = models.CharField(choices=numero_CHOICES, max_length=5, null=True, blank=True)
    respuesta_motora_e = models.CharField(choices=numero_CHOICES, max_length=5, null=True,blank=True)
    respuesta_verbal_e = models.CharField(choices=numero_CHOICES, max_length=5, null=True,blank=True)
    glasgowtotal_e = models.CharField(max_length=5, null=True, default=0,blank=True)


    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_uci", u"puede ver uci"),
        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Neurologia(models.Model):
    numero_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )
    conciencia_CHOICES = (
        ('Coma', 'Coma'),
        ('Vigilia sin respuesta', 'Vigilia sin respuesta'),
        ('Mínima conciencia', 'Mínima conciencia'),
    )
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    fechaneuro = models.DateField(null=True)
    neurologo = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    auditiva = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    motora = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    comunicacion = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    visual = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    verbal = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    alerta = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    total1 = models.CharField(max_length=20,null=True,default=0)
    aperturaocular = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    respuestamotora = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    reflejos = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    respiracion = models.CharField(max_length=100, choices=numero_CHOICES, null=True)
    total2=models.CharField(max_length=20,null=True,default=0)
    estadoconciencia=models.CharField(choices=conciencia_CHOICES,max_length=30,null=True)
    epileptico=models.CharField(max_length=20, choices=seleccion_CHOICES, null=True)
    fechaeeg=models.DateField(null=True,blank=True)
    resultadoeeg=models.CharField(max_length=50, null=True,blank=True,default="")
    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_neurologia", u"puede ver neurologia"),
        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Bold(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fechaimg=models.DateField(null=True)
    axt2prop=models.BooleanField(default=False)
    axt2prop1=models.BooleanField(default=False)
    axt2prop2 = models.BooleanField(default=False)
    axt2prop3 = models.BooleanField(default=False)
    axt2prop4 = models.BooleanField(default=False)
    axt2prop5 = models.BooleanField(default=False)
    difussion = models.BooleanField(default=False)
    difussion1 = models.BooleanField(default=False)
    difussion2 = models.BooleanField(default=False)
    difussion3 = models.BooleanField(default=False)
    difussion4 = models.BooleanField(default=False)
    difussion5 = models.BooleanField(default=False)
    difussion6 = models.BooleanField(default=False)
    difussion7 = models.BooleanField(default=False)
    resting = models.BooleanField(default=False)
    resting1 = models.BooleanField(default=False)
    resting2 = models.BooleanField(default=False)
    resting3 = models.BooleanField(default=False)
    resting4 = models.BooleanField(default=False)
    resting5 = models.BooleanField(default=False)
    resting6 = models.BooleanField(default=False)
    resting7 = models.BooleanField(default=False)
    resting8 = models.BooleanField(default=False)
    obl = models.BooleanField(default=False)
    obl1 = models.BooleanField(default=False)
    obl2 = models.BooleanField(default=False)
    obl3 = models.BooleanField(default=False)
    obl4 = models.BooleanField(default=False)
    obl5 = models.BooleanField(default=False)
    obl6 = models.BooleanField(default=False)
    flair = models.BooleanField(default=False)
    flair1 = models.BooleanField(default=False)
    flair2 = models.BooleanField(default=False)
    flair3 = models.BooleanField(default=False)
    flair4 = models.BooleanField(default=False)
    flair5 = models.BooleanField(default=False)
    flair6 = models.BooleanField(default=False)
    flair7 = models.BooleanField(default=False)
    cal = models.BooleanField(default=False)
    cal1 = models.BooleanField(default=False)
    cal2 = models.BooleanField(default=False)
    cal3 = models.BooleanField(default=False)
    cal4 = models.BooleanField(default=False)
    cal5 = models.BooleanField(default=False)
    swi = models.BooleanField(default=False)
    swi1 = models.BooleanField(default=False)
    swi2 = models.BooleanField(default=False)
    swi3 = models.BooleanField(default=False)
    swi4 = models.BooleanField(default=False)
    swi5 = models.BooleanField(default=False)
    swi6 = models.BooleanField(default=False)
    swi7 = models.BooleanField(default=False)
    swi8 = models.BooleanField(default=False)
    tensor = models.BooleanField(default=False)
    tensor1 = models.BooleanField(default=False)
    tensor2 = models.BooleanField(default=False)
    tensor3 = models.BooleanField(default=False)
    tensor4 = models.BooleanField(default=False)
    tensor5 = models.BooleanField(default=False)
    tensor6 = models.BooleanField(default=False)
    tensor7 = models.BooleanField(default=False)
    tensor8 = models.BooleanField(default=False)
    t1A=models.BooleanField(default=False)
    t1G=models.BooleanField(default=False)
    t1M=models.BooleanField(default=False)
    t2A=models.BooleanField(default=False)
    t2M=models.BooleanField(default=False)
    flairA=models.BooleanField(default=False)
    flairM=models.BooleanField(default=False)
    tensorA=models.BooleanField(default=False)
    tensord=models.BooleanField(default=False)
    tensorG=models.BooleanField(default=False)
    tensorM=models.BooleanField(default=False)
    difussionA=models.BooleanField(default=False)
    difussionM=models.BooleanField(default=False)
    restingA=models.BooleanField(default=False)
    restingV=models.BooleanField(default=False)
    restingG=models.BooleanField(default=False)
    restingT=models.BooleanField(default=False)
    restingM=models.BooleanField(default=False)
    cd=models.BooleanField(default=False)
    responsable=models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_bold", u"puede ver bold"),
        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Mayor(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fechaentrevista = models.DateField(null=True)
    neuropsicologa = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    informante = models.CharField(max_length=200, null=True,default="")
    parentezco= models.CharField(max_length=100, null=True,default="")
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    confiable = models.CharField(choices=seleccion_CHOICES, null=True,max_length=50)
    numero_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    cambio1 = models.CharField(max_length=30,choices=numero_CHOICES,null=True)
    cambio2 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio3 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio4 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio5 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio6 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio7 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio8 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio9 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio10 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio11 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio12 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio13 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio14 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio15 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio16 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio17 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio18 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio19 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio20 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio21 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio22 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio23 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio24 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio25 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    cambio26 = models.CharField(max_length=30, choices=numero_CHOICES, null=True)
    total = models.CharField(max_length=30,null=True,default=0)
    resultado = models.CharField(max_length=100,null=True, default= "Mejoría")
    gds_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    )
    severidadgds=models.CharField(max_length=20,null=True,choices=gds_CHOICES)
    dxdemencia=models.CharField(max_length=20,null=True,choices=seleccion_CHOICES)
    tiempo=models.CharField(max_length=35,null=True)


    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class ReportBuilder:
        exclude = ('id', 'informante' )  # Lists or tuple of excluded fields

class Informante(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fechaentrevista = models.DateField(null=True)
    neuropsicologa = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    informante = models.CharField(max_length=200, null=True, default="")
    parentezco = models.CharField(max_length=100, null=True, default="")
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    confiable = models.CharField(choices=seleccion_CHOICES, null=True, max_length=50)
    numero_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    telefono = models.CharField(choices=numero_CHOICES,null=True,max_length=50)
    compras = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    comida = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    casa = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    ropa = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    transporte = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    medicacion = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    finanzas = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    totalindependencia=models.CharField(max_length=30,null=True,default=0)
    memoria1 = models.CharField(choices=numero_CHOICES,null=True,max_length=50)
    memoria2 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria3 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria4 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria5 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria6 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria7 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria8 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria9 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria10 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria11 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria12 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria13 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria14 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    memoria15 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    totalmemoria = models.CharField(max_length=30,null=True,default=0)
    frontal1= models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal2= models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal3 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal4 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal5 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal6 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal7 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal8 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal9 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal10 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal11 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal12 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal13 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal14 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal15 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal16 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal17 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal18 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal19 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal20 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal21 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal22 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal23 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal24 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal25 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal26 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal27 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal28 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal29 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal30 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal31 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal32 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal33 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal34 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal35 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal36 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal37 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal38 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal39 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal40 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal41 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal42 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal43 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal44 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal45 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    frontal46 = models.CharField(choices=numero_CHOICES, null=True, max_length=50)
    totalapatia= models.CharField(max_length=30,null=True,default=0)
    totaldes= models.CharField(max_length=30,null=True,default=0)
    totalfunciones = models.CharField(max_length=30, null=True, default=0)

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_informante", u"puede ver informante"),
        )
    class ReportBuilder:
        exclude = ('id','informante' )  # Lists or tuple of excluded fields

class Seguimiento(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    fechaseguimiento = models.DateField(null=True, default=timezone.now)
    medico_responsable = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
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
    fallaorganica = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    fallaorganica_cual = models.CharField(max_length=70, null=True, blank=True, default="")
    infeccion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    infeccion_foco = models.CharField(max_length=70, null=True, blank=True, default="")
    parada = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    parada_tiempo = models.CharField(max_length=12, null=True,blank=True,default="")
    pic = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    pic_numero = models.CharField(max_length=12, null=True, blank=True, default="")
    ventilacion = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    soporte = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    soporte_cual = models.CharField(max_length=200, null=True, blank=True, default="")
    neuroimagen = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    imgobservacion = models.CharField(max_length=200,null=True,default="",blank=True)
    neurologia = models.CharField(choices=seleccion_CHOICES, max_length=12, null=True, default='NO')
    midazolam = models.CharField(max_length=12, null=True, default=0)
    dexmedeto = models.CharField(max_length=12, null=True, default=0)
    fentanyl = models.CharField(max_length=12, null=True, default=0)
    tiopental = models.CharField(max_length=12, null=True, default=0)
    vecuronio = models.CharField(max_length=12, null=True, default=0)
    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)
    class Meta:
        permissions = (
            ("can_ver_seguimiento", u"puede ver seguimiento"),
        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Moca(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    fecha=models.DateField(null=True)
    funcion_visoespacial=models.CharField(max_length=1,null=True)
    identificacion = models.CharField(max_length=1, null=True)
    atencion_numero = models.CharField(max_length=1, null=True)
    atencion_letras = models.CharField(max_length=1, null=True)
    atencion_resta = models.CharField(max_length=1, null=True)
    lenguaje_repite = models.CharField(max_length=1, null=True)
    lenguaje_fluidez = models.CharField(max_length=1, null=True)
    abstraccion = models.CharField(max_length=1, null=True)
    recuerdo = models.CharField(max_length=1, null=True)
    orientacion = models.CharField(max_length=1, null=True)
    total= models.CharField(max_length=2, null=True)


    class Meta:
        ordering = ['fecha']
        permissions = (
            ("can_ver_moca", u"puede ver moca"),

        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields





    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)


class Control(models.Model):
    numero = models.PositiveIntegerField(null=True, unique=True)
    imagen = models.FileField(null=True, upload_to="controles", blank=True)
    fecha_nacimiento = models.DateField(null=True)
    fecha = models.DateField(null=True)
    edad=models.PositiveIntegerField(null=True)
    #######sexo
    hombre = 'Hombre'
    mujer = 'Mujer'
    Sexo_choices = ((hombre, u'Hombre'), (mujer, u'Mujer'))
    sexo = models.CharField(max_length=9, choices=Sexo_choices, null=True)
    funcion_visoespacial=models.CharField(max_length=1,null=True)
    identificacion = models.CharField(max_length=1, null=True)
    atencion_numero = models.CharField(max_length=1, null=True)
    atencion_letras = models.CharField(max_length=1, null=True)
    atencion_resta = models.CharField(max_length=1, null=True)
    lenguaje_repite = models.CharField(max_length=1, null=True)
    lenguaje_fluidez = models.CharField(max_length=1, null=True)
    abstraccion = models.CharField(max_length=1, null=True)
    recuerdo = models.CharField(max_length=1, null=True)
    orientacion = models.CharField(max_length=1, null=True)
    total= models.CharField(max_length=2, null=True)
    ####### nivel educativo
    Analfabeta = 'Analfabeta'
    primaria = 'Primaria'
    bachillerato = 'Bachillerato'
    tecnico = 'Técnico'
    profesional = 'Profesional'
    educativo_choices = (
        (Analfabeta, u'Analfabeta'),(primaria, u'Primaria'), (bachillerato, u'Bachillerato'), (tecnico, u'Técnico'), (profesional, u'Profesional'))
    n_educativo = models.CharField(max_length=20, choices=educativo_choices, null=True)

    class Meta:
        ordering = ["numero"]
        permissions = (
            ("can_descargar_control", u"puede descargar control"),

        )
    class ReportBuilder:
        exclude = ('id', 'imagen')  # Lists or tuple of excluded fields




    def __str__(self):
        return '{}'.format(self.numero)
    def get_img(self):
        i=Picture.objects.get(slug="c"+str(self.numero))
        return i

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        c = self
        n=c.numero
        shutil.rmtree(settings.MEDIA_ROOT+"/controles/control"+str(n), ignore_errors=True)
        super(Control, self).delete(*args, **kwargs)
        try:
            i=Picture.objects.get(slug="c"+str(n))
            i.delete()
        except:
            ""


class Cambioradiologia(models.Model):

    sujeto=models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    fecha=models.DateTimeField(null=True)
    razon=models.CharField(max_length=20,null=True)

    def __str__(self):
        return '{}'.format(self.sujeto.sujeto_numero)

class Valorablenps(models.Model):

    sujeto=models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    valorable=models.NullBooleanField()
    respuestas = (
        ('Fallecido','Fallecido'),
        ('No localizable','No localizable'),
        ('No colabora','No colabora'),
        ('EMC', 'EMC'),
        ('SVSR', 'SVSR'),

    )
    razon=models.CharField(max_length=100, choices=respuestas, null=True)
    fecha = models.DateTimeField(null=True,blank=True)
    fechafallecido = models.DateField(null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.sujeto.sujeto_numero)

class Neuropsi(models.Model):
    seleccion_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    evaluacion_CHOICES = (
        ('Normal Alto', 'Normal Alto'),
        ('Normal', 'Normal'),
        ('Moderado', 'Moderado'),
        ('Severo', 'Severo'),
    )
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True)
    medicado = models.CharField(max_length=12, choices=seleccion_CHOICES, null=True, default="NO")
    medicado_cual = models.CharField(max_length=180, null=True, blank=True)
    medicado_dt = models.CharField(max_length=180, null=True, blank=True)
    imagen = models.TextField(null=True, blank=True)
    orientacion_tiempo=models.CharField(max_length=1,null=True)
    orientacion_espacio = models.CharField(max_length=1, null=True)
    orientacion_persona = models.CharField(max_length=1, null=True)
    orientacion=models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    atencion_digitos = models.CharField(max_length=1, null=True)
    atencion_visual = models.CharField(max_length=2, null=True)
    atencion_20_3 = models.CharField(max_length=1, null=True)
    atencion = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    codificacion_palabras = models.CharField(max_length=1, null=True)
    codificacion_figura = models.CharField(max_length=4, null=True)
    codificacion = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    evocacion_figura = models.CharField(max_length=4, null=True)
    evocacion_espontanea = models.CharField(max_length=1, null=True)
    evocacion_claves = models.CharField(max_length=1, null=True)
    evocacion_reconocimiento = models.CharField(max_length=1, null=True)
    evocacion = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    lenguaje_denominacion = models.CharField(max_length=1, null=True)
    lenguaje_repeticion = models.CharField(max_length=1, null=True)
    lenguaje_comprension = models.CharField(max_length=1, null=True)
    lenguaje_semantica = models.CharField(max_length=2, null=True)
    lenguaje_fonologica = models.CharField(max_length=2, null=True)
    lenguaje = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    lectura_lectura = models.CharField(max_length=1, null=True)
    lectura_dictado = models.CharField(max_length=1, null=True)
    lectura_copiado = models.CharField(max_length=1, null=True)
    lectura = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    conceptual_semejanzas = models.CharField(max_length=1, null=True)
    conceptual_calculo = models.CharField(max_length=1, null=True)
    conceptual_secuenciacion = models.CharField(max_length=1, null=True)
    conceptual = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    motora_mano_der = models.CharField(max_length=1, null=True)
    motora_mano_izq = models.CharField(max_length=1, null=True)
    motora_alternos = models.CharField(max_length=1, null=True)
    motora_reacciones = models.CharField(max_length=1, null=True)
    motora = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)
    resultado = models.CharField(max_length=15, choices=evaluacion_CHOICES, null=True)

    class ReportBuilder:
        exclude = ('id',)  # Lists or tuple of excluded fields

    def __str__(self):
        return '{}'.format(self.candidato.sujeto_numero)


class Parametrosmotioncorrect(models.Model):
    sujeto = models.OneToOneField(Candidato, on_delete=models.CASCADE, null=True, blank=True)
    control = models.OneToOneField(Control, on_delete=models.CASCADE, null=True, blank=True)
    absolute_func = models.CharField(max_length=50, null=True)
    relative_func = models.CharField(max_length=50, null=True)
    graphic_desplazamiento_func = models.CharField(max_length=300,null=True,blank=True)
    graphic_rotacion_func= models.CharField(max_length=300,null=True,blank=True)
    graphic_traslacion_func= models.CharField(max_length=300,null=True,blank=True)
    aceptado_func = models.NullBooleanField()

    absolute_dwi = models.CharField(max_length=50, null=True)
    relative_dwi = models.CharField(max_length=50, null=True)
    graphic_desplazamiento_dwi = models.CharField(max_length=300, null=True, blank=True)
    graphic_rotacion_dwi = models.CharField(max_length=300, null=True, blank=True)
    graphic_traslacion_dwi = models.CharField(max_length=300, null=True, blank=True)
    aceptado_dwi = models.NullBooleanField()



