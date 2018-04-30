
from django import forms
from apps.paciente.models import Candidato, Dprevio, Medico, Ingreso, Radiologia, Uci
from django.forms.widgets import CheckboxSelectMultiple

class MedicoForm(forms.ModelForm):

    class Meta:
        model = Medico
        fields = ['nombre',]
        labels = {'nombre': "Nombre",}
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Nombre')}),}


class PacienteForm(forms.ModelForm):


    class Meta:
        model = Candidato

        fields = [
            'nombres',
            'apellidos',
            'edad',
            'cc',
            'sexo',
            'sujeto_numero',
            'fecha_de_registro',
            'HC',
            'cama_numero',
            'fecha_evento_principal',
            'hora_evento_principal',
            'fecha_ingreso',
            'hora_ingreso',
            'G_diagnostico',
            'D_neuro_logico_psiquiatrico_previo',
            'D_especificos',
            'ci',
            'ci3',
            'ci4',
            'ce1',
            'ce2',
            'ce3',
            'ce4',
            'medico_responsable',


        ]

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'cc': 'C.C',
            'sexo': 'Sexo',
            'sujeto_numero' : "Sujeto #",
            'fecha_de_registro' : "Fecha de Registro",
            'HC': "Historia Clinica",
            'cama_numero': 'Cama UCI',
            'fecha_evento_principal': "Fecha de evento principal",
            'hora_evento_principal': "Hora de evento principal",
            'fecha_ingreso': "Fecha de ingreso UCI",
            'hora_ingreso': "Hora de ingreso UCI",
            'G_diagnostico': 'Grupo diagnóstico',
            'D_neuro_logico_psiquiatrico_previo': "Diagnósticos neurológicos/psiquiátricos previos al evento",
            'D_especificos': 'Especifique diagnóstico',
            'medico_responsable': "Profesional Responsable",
             }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Nombres')}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Apellidos')}),
            'edad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Edad')}),
            'cc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Cédula de Ciudadanía')}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'sujeto_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_de_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'HC':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Historia clínica número')}),
            'cama_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Ingrese número entero')}),
            'fecha_evento_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_evento_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Formato 24 horas')}),
            'fecha_ingreso': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_ingreso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Formato 24 horas')}),
            'G_diagnostico': forms.Select(attrs={'class': 'form-control'}),
            'D_neuro_logico_psiquiatrico_previo': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'D_especificos': forms.Textarea(attrs={'class': 'form-control'}),
            'ci': forms.RadioSelect(),
            'ci3': forms.CheckboxInput(),
            'ci4': forms.CheckboxInput(),
            'ce1': forms.CheckboxInput(),
            'ce2': forms.CheckboxInput(),
            'ce3': forms.CheckboxInput(),
            'ce4': forms.CheckboxInput(),
            'medico_responsable': forms.Select(attrs={'class': 'form-control'}),


        }

class IngresoForm(forms.ModelForm):


    class Meta:
        model = Ingreso

        fields = [
            'fecha_form',
            'lugar_nacimiento',
            'lugar_residencia',
            'direccion',
            'nombre_acompanante',
            'tel1',
            'tel2',
            'peso',
            'estatura',
            'n_educativo',
            'lateralidad',
            'conciencia',
            'sedado',
            'a_patologicos',
            'a_patologicos_cual',
            'quirurgicos',
            'fecha_craneotomia',
            'causa_quirurgicos',
            'a_toxico_alergenicos',
            'a_farmaco1',
            'a_farmaco1_dosis',
            'a_farmaco2',
            'a_farmaco2_dosis',
            'a_familiares',
            'firma_consentimiento',
            'firma_causa',


        ]

        labels = {
            'fecha_form':"Fecha",
            'lugar_nacimiento':"Lugar de nacimiento",
            'lugar_residencia': "Lugar de residencia",
            'direccion':"Dirección",
            'nombre_acompanante':"Nombre Acompañante",
            'tel1': "Teléfono de contacto 1",
            'tel2': "Teléfono de contacto 2",
            'peso': "Peso",
            'estatura':"Estatura",
            'n_educativo':"Nivel Educativo",
            'lateralidad':"Lateralidad",
            'conciencia':"Estado de Conciencia",
            'sedado': "Sedado por neuroprotección",
            'a_patologicos':"Antecedentes Patológicos",
            'a_patologicos_cual': "Si escoge otro especifique cual",
            'quirurgicos':"Antecedentes quirúrgicos",
            'causa_quirurgicos':"Especifique causa",
            'a_toxico_alergenicos':"Antecedentes Tóxico alérgicos",
            'a_farmaco1': "Antecedentes Farmacológicos 1",
            'a_farmaco1_dosis':"Dosis total/día",
            'a_farmaco2': "Antecedentes Farmacológicos 2",
            'a_farmaco2_dosis':"Dosis total/día",
            'a_familiares':"Antecedentes Familiares relevantes",
            'firma_consentimiento':"Firma de consentimiento informado",
            'firma_causa':"Causa",
             }
        widgets = {
            'fecha_form': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Fecha cuando se llena este formulario')}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Escriba la dirección de residencia')}),
            'nombre_acompanante': forms.TextInput(attrs={'class': 'form-control'}),
            'tel1': forms.TextInput(attrs={'class': 'form-control'}),
            'tel2': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Peso en Kilogramos')}),
            'estatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Estatura en centimetros')}),
            'n_educativo': forms.Select(attrs={'class': 'form-control'}),
            'lateralidad': forms.Select(attrs={'class': 'form-control'}),
            'conciencia': forms.Select(attrs={'class': 'form-control'}),
            'sedado': forms.CheckboxInput(),
            'a_patologicos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'a_patologicos_cual': forms.TextInput(attrs={'class': 'form-control'}),
            'quirurgicos': forms.Select(attrs={'class': 'form-control'}),
            'fecha_craneotomia':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Si se escoge craneotomía')}),
            'causa_quirurgicos': forms.TextInput(attrs={'class': 'form-control'}),
            'a_toxico_alergenicos': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco1': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco1_dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco2': forms.TextInput(attrs={'class': 'form-control'}),
            'a_farmaco2_dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'a_familiares': forms.TextInput(attrs={'class': 'form-control'}),
            'firma_consentimiento': forms.CheckboxInput(),
            'firma_causa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Si no se firma')}),
        }

class RadiologiaForm(forms.ModelForm):


    class Meta:
        model = Radiologia

        fields = [
            'fecha_procedimiento',
            'hora_inicio',
            'ur_pulsoximetro_sv',
            'ur_frecuencia_cardiaca_sv',
            'ur_frecuencia_respiratoria_sv',
            'ur_visoscopio_sv',
            'ur_tension_sv',
            'pic',
            'ppc',
            'me_cual',
            'me_dosis',
            'sedacion',
            'sedacion_dt',
            'sedacion_sv',
            'analgesia',
            'analgesia_dt',
            'analgesia_sv',
            'relajacion',
            'relajacion_dt',
            'relajacion_sv',
            'otra_medicacion',
            'otra_medicacion_dt',
            'otra_medicacion_cual',
            'ru_pulsoximetro_sv',
            'ru_frecuencia_cardiaca_sv',
            'ru_frecuencia_respiratoria_sv',
            'ru_visoscopio_sv',
            'ru_tension_sv',
            'tiempo_sesonacia',
            'hora_llegada',
            'complicaciones_cuales',
            'transportable',
            'jefe_enfermeria',
            'aux_enfermeria',
            'medico_uci',
            'anestesiologo',
            'terapeuta_respiratorio',
            'vmi',
            'vasopresor',
            'ionotropico',
            'ur_pulsoximetro',
            'ur_frecuencia_cardiaca',
            'ur_frecuencia_respiratoria',
            'ur_visoscopio',
            'ur_tension',
            'medicamentos_emergencia',
            'ru_pulsoximetro',
            'ru_frecuencia_cardiaca',
            'ru_frecuencia_respiratoria',
            'ru_visoscopio',
            'ru_tension',
            'complicaciones',
        ]

        labels = {
            'fecha_procedimiento':'Fecha de procedimiento',
            'hora_inicio':"Hora inicio",
            'pic':"#PIC",
            'ppc':'#PPC',
            'me_cual':"Cuál",
            'me_dosis':"Dosis Total",
            'sedacion_dt':"Dosis Total",
            'analgesia_dt':"Dosis Total",
            'relajacion_dt': "Dosis Total",
            'otra_medicacion_dt':"Dosis Total",
            'otra_medicacion_cual':"Cuál",
            'tiempo_sesonacia': "Tiempo de resonancia",
            'hora_llegada' :"Hora de llegada a UCI",
            'complicaciones_cuales':"Cuales",


             }
        widgets = {
            'fecha_procedimiento':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Fecha de procedimiento')}),
            'hora_inicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Formato 24 horas')}),
            'ur_pulsoximetro_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ur_frecuencia_cardiaca_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ur_frecuencia_respiratoria_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ur_visoscopio_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ur_tension_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'pic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ppc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'me_cual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Solo si se selecciona SI')}),
            'me_dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),

            'sedacion_dt':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'sedacion_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'analgesia_dt':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'analgesia_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'relajacion_dt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'relajacion_sv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'otra_medicacion_dt':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'otra_medicacion_cual':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Solo si se selecciona SI')}),
            'ru_pulsoximetro_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ru_frecuencia_cardiaca_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ru_frecuencia_respiratoria_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ru_visoscopio_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'ru_tension_sv':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'tiempo_sesonacia':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'hora_llegada':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Formato 24 horas')}),
            'complicaciones_cuales':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Solo si se selecciona Si')}),

            'transportable':forms.RadioSelect(),
            'jefe_enfermeria': forms.RadioSelect(),
            'aux_enfermeria': forms.RadioSelect(),
            'medico_uci': forms.RadioSelect(),
            'anestesiologo':forms.RadioSelect(),
            'terapeuta_respiratorio':forms.RadioSelect(),
            'vmi':forms.RadioSelect(),
            'vasopresor':forms.RadioSelect(),
            'ionotropico':forms.RadioSelect(),
            'ur_pulsoximetro':forms.RadioSelect(),
            'ur_frecuencia_cardiaca':forms.RadioSelect(),
            'ur_frecuencia_respiratoria':forms.RadioSelect(),
            'ur_visoscopio':forms.RadioSelect(),
            'ur_tension':forms.RadioSelect(),
            'medicamentos_emergencia':forms.RadioSelect(),
            'sedacion':forms.RadioSelect(),
            'analgesia':forms.RadioSelect(),
            'relajacion':forms.RadioSelect(),
            'otra_medicacion':forms.RadioSelect(),
            'ru_pulsoximetro':forms.RadioSelect(),
            'ru_frecuencia_cardiaca':forms.RadioSelect(),
            'ru_frecuencia_respiratoria':forms.RadioSelect(),
            'ru_visoscopio':forms.RadioSelect(),
            'ru_tension':forms.RadioSelect(),
            'complicaciones':forms.RadioSelect(),

        }

class UciForm(forms.ModelForm):

    class Meta:
        model = Uci

        fields = [
            'fechauci',
            'horauci',
            'apertura_ocular',
            'respuesta_motora',
            'respuesta_verbal',
            'glasgowtotal',
        ]

        labels = {
            'fechauci': "Fecha",
            'horauci':"Hora",
            'apertura_ocular':"Apertura ocular",
            'respuesta_motora':"Respuesta motora",
            'respuesta_verbal':"Respuesta verbal",
            'glasgowtotal':"Glasgow total",

        }
        widgets = {
            'fechauci': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),
            'horauci': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Formato 24 horas')}),
            'apertura_ocular' :forms.RadioSelect(),
            'respuesta_motora':forms.RadioSelect(),
            'respuesta_verbal':forms.RadioSelect(),
            'glasgowtotal':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('')}),

        }