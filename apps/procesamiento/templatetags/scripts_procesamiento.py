from django import template
from programas.dcm2niix import T1_path,DWI_path,rest_path
from apps.procesamiento.models import Task, Taskgroup, Pipeline, task_celery
from apps.validacion.models import Tipoimagenes
from django.conf import settings
register = template.Library()
from apps.validacion.models import img_to_show
import os
import shutil
from programas.definitions import results as result_path
from programas.workflows import run_pipeline
from celery import shared_task
from apps.procesamiento.models import default_result
from apps.procesamiento.models import results
from programas.motion_correct_fmri import grafics_plot
import numpy as np


@register.filter(name='zip')
def zip_lists(a, b):
      return zip(a, b)




@register.simple_tag
def get_task_for_images(img):
    return img.task_set.all()

@register.simple_tag
def get_groups_for_images(img):
    return img.taskgroup_set.all()



@register.simple_tag
def get_img_with_tasks():
    T=Task.objects.all()
    imgs=[]
    for t in T:
        if t.tipo_imagen in imgs:
            continue
        else:
            imgs.append(t.tipo_imagen)
            
    return imgs

@register.simple_tag
def get_taskgroups():
    
    return Taskgroup.objects.all()

@register.simple_tag
def get_pipelines():
    
    return Pipeline.objects.all()

@register.simple_tag
def get_estado_pipeline(pipeline,img):
        
    return task_celery.objects.filter(imagen=img,pipeline=pipeline)

@register.simple_tag
def get_result_type(task,t):
    return task.results_set.filter(tipo=t)

@register.simple_tag
def tareas_defecto():
    
    DWI=Tipoimagenes.objects.get_or_create(nombre="TENSOR  AXI")[0]
    
    P=Pipeline.objects.filter(nombre="Pipeline Difusion",tipo_imagen=DWI)
    folder_tareas=os.path.join(settings.BASE_DIR,"tareas")
    
    if len(P) == 0 :
                
        eddy=Task.objects.get_or_create(nombre="eddy correction",
                                        pathscript=os.path.join(folder_tareas,"eddy_correction.py"),
                                        tipo_imagen=DWI)[0]
        nlm=Task.objects.get_or_create(nombre="Non Local Mean",
                                       pathscript=os.path.join(folder_tareas,"nonLocalMean.py"),
                                       tipo_imagen=DWI)[0]
        reslicing=Task.objects.get_or_create(nombre="Reslicing",
                                             pathscript=os.path.join(folder_tareas,"reslicing.py"),
                                             tipo_imagen=DWI)[0]
        bet_dwi=Task.objects.get_or_create(nombre="Bet DWI",
                                           pathscript=os.path.join(folder_tareas,"betDWI.py"),
                                           tipo_imagen=DWI)[0]
        dwi_2_mni=Task.objects.get_or_create(nombre="To register dwi to MNI",
                                             pathscript=os.path.join(folder_tareas,"to_register_dwi_to_mni.py"),
                                             tipo_imagen=DWI,
                                             dependencia=bet_dwi)[0]
        estimate_dti=Task.objects.get_or_create(nombre="To estimate dti",
                                                pathscript=os.path.join(folder_tareas,"to_estimate_dti.py"),
                                                tipo_imagen=DWI,
                                                dependencia=bet_dwi)[0]
        estimate_dti_maps=Task.objects.get_or_create(nombre="To estimate dti maps",
                                                     pathscript=os.path.join(folder_tareas,"to_estimate_dti_maps.py"),
                                                     tipo_imagen=DWI,
                                                     dependencia=estimate_dti)[0]
        generate_bundles=Task.objects.get_or_create(nombre="To Generate Bunddle",
                                                    pathscript=os.path.join(folder_tareas,"to_generate_bunddle.py"),
                                                    tipo_imagen=DWI,
                                                    dependencia=dwi_2_mni)[0]
        generate_tracto=Task.objects.get_or_create(nombre="To Generate Tractography",
                                                   pathscript=os.path.join(folder_tareas,"to_generate_tractography.py"),
                                                   tipo_imagen=DWI,
                                                   dependencia=bet_dwi)[0]
        pre_DWI=Taskgroup.objects.get_or_create(nombre="Preprocesamiento DWI",tipo_imagen=DWI,eliminable=False)[0]
        task_pre_dwi=[eddy,nlm,reslicing,bet_dwi,dwi_2_mni]
        orden=""
        for t in task_pre_dwi:
            pre_DWI.task.add(t)
            orden+=str(t.pk)+"_"
        pre_DWI.orden=orden
        pre_DWI.save()
        
        post_DWI=Taskgroup.objects.get_or_create(nombre="Postprocesamiento DWI",tipo_imagen=DWI,dependencia=pre_DWI,
                                                 eliminable=False)[0]
        task_post_dwi=[estimate_dti,estimate_dti_maps,generate_bundles,generate_tracto]
        orden=""
        for t in task_post_dwi:
            post_DWI.task.add(t)
            orden+=str(t.pk)+"_"
        post_DWI.orden=orden
        post_DWI.save()
        
        P_DWI=Pipeline.objects.get_or_create(nombre="Pipeline Difusion",
                                             tipo_imagen=DWI,eliminable=False)[0]
        groups_P=[pre_DWI,post_DWI]
        orden=""
        for t in groups_P:
            P_DWI.grupos.add(t)
            orden+=str(t.pk)+"_"
        P_DWI.orden=orden
        P_DWI.save()
        
    REST=Tipoimagenes.objects.get_or_create(nombre="RESTING")[0]
    
    P_rest=Pipeline.objects.filter(nombre="Pipeline Resting",tipo_imagen=REST)
    
    
    if len(P_rest) == 0 :
        
                     
        rest_task=Task.objects.get_or_create(nombre="Resting Task",
                                        pathscript=os.path.join(folder_tareas,"rest_process.py"),
                                        tipo_imagen=REST)[0]
        rest_Group=Taskgroup.objects.get_or_create(nombre="Resting Group",tipo_imagen=REST,eliminable=False)[0]
        task_rest_group=[rest_task]
        orden=""
        for t in task_rest_group:
            rest_Group.task.add(t)
            orden+=str(t.pk)+"_"
        rest_Group.orden=orden
        rest_Group.save()
        
                
        rest_PIPE=Pipeline.objects.get_or_create(nombre="Pipeline Resting",
                                                 tipo_imagen=REST,eliminable=False)[0]
        groups_PIPE=[rest_Group]
        orden=""
        for t in groups_PIPE:
            rest_PIPE.grupos.add(t)
            orden+=str(t.pk)+"_"
        rest_PIPE.orden=orden
        rest_PIPE.save()
        
    ## resultados defecto 
    bet_DWI=Task.objects.get_or_create(nombre="Bet DWI")[0]
    default_result.objects.get_or_create(nombre="b0 masked",task=bet_DWI,
                                         word_key="b0_masked.nii.gz",
                                         tipo="Archivo nii")
    
    default_result.objects.get_or_create(nombre="b0 mask",task=bet_DWI,
                                         word_key="b0_masked_mask.nii.gz",
                                         tipo="Archivo nii")
    
    default_result.objects.get_or_create(nombre="dwi masked",task=bet_DWI,
                                         word_key="dwi_masked.nii.gz",
                                         tipo="Archivo nii")
    
    eddy=Task.objects.get_or_create(nombre="eddy correction")[0]
    default_result.objects.get_or_create(nombre="Eddy Correct",task=eddy,
                                         word_key="EddyCorrect.nii.gz",
                                         tipo="Archivo nii")
    
    nlm=Task.objects.get_or_create(nombre="Non Local Mean")[0]
    default_result.objects.get_or_create(nombre="Non Local Mean",task=nlm,
                                         word_key="NonLocalMean.nii.gz",
                                         tipo="Archivo nii")
    
    estimate_dti=Task.objects.get_or_create(nombre="To estimate dti")[0]
    default_result.objects.get_or_create(nombre="DTI Evecs",task=estimate_dti,
                                         word_key="DTIEvecs.nii.gz",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="DTI Evals",task=estimate_dti,
                                         word_key="DTIEvals.nii.gz",
                                         tipo="Archivo nii")
    
    estimate_dti_maps=Task.objects.get_or_create(nombre="To estimate dti maps")[0]
    default_result.objects.get_or_create(nombre="FA map",task=estimate_dti_maps,
                                         word_key="FA.nii.gz",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="AD map",task=estimate_dti_maps,
                                         word_key="AD.nii.gz",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="FA RGB map",task=estimate_dti_maps,
                                         word_key="FA_RGB.nii.gz",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="MD map",task=estimate_dti_maps,
                                         word_key="MD.nii.gz",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="RD map",task=estimate_dti_maps,
                                         word_key="RD.nii.gz",
                                         tipo="Archivo nii")
    
    default_result.objects.get_or_create(nombre="Tracto EuDx",task=estimate_dti_maps,
                                         word_key="EuDx.trk",
                                         tipo="Archivo trk")
    
    
    generate_tracto=Task.objects.get_or_create(nombre="To Generate Tractography")[0]
    default_result.objects.get_or_create(nombre="tractography",task=generate_tracto,
                                         word_key="_tractography_CsaOdf",
                                         tipo="Archivo trk")
    
    
    
    generate_b=Task.objects.get_or_create(nombre="To Generate Bunddle")[0]
    default_result.objects.get_or_create(nombre="bundle rules",task=generate_b,
                                         word_key="bundle_rule_",
                                         tipo="Archivo trk")
    default_result.objects.get_or_create(nombre="features",task=generate_b,
                                         word_key="feature",
                                         tipo="Texto")
    
    resting_task=Task.objects.get_or_create(nombre="Resting Task")[0]
    default_result.objects.get_or_create(nombre="ica",task=resting_task,
                                         word_key="ica_",
                                         tipo="Ica Component")
    default_result.objects.get_or_create(nombre="time series ica",task=resting_task,
                                         word_key="time_series_ica",
                                         tipo="Archivo csv")
    default_result.objects.get_or_create(nombre="ev without gs",task=resting_task,
                                         word_key="without",
                                         tipo="Archivo csv")
    default_result.objects.get_or_create(nombre="ev with gs",task=resting_task,
                                         word_key="with_gs",
                                         tipo="Archivo csv")
    default_result.objects.get_or_create(nombre="time series",task=resting_task,
                                         word_key="time_series.csv",
                                         tipo="Archivo csv")
    default_result.objects.get_or_create(nombre="matrix",task=resting_task,
                                         word_key="matrix",
                                         tipo="Imagen")
    default_result.objects.get_or_create(nombre="wt1 pve 0",task=resting_task,
                                         word_key="pve_0.nii",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="wt1 pve 2",task=resting_task,
                                         word_key="pve_2.nii",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="wt1 n4bias",task=resting_task,
                                         word_key="n4bias.nii",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="swfmri",task=resting_task,
                                         word_key="swfmri",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="Ica Components",task=resting_task,
                                         word_key="canica",
                                         tipo="Archivo nii")
    default_result.objects.get_or_create(nombre="Descomposition Dict",task=resting_task,
                                         word_key="dict",
                                         tipo="Archivo nii")
        
    return ""


def validar_orden(tareas):
    flag = True
    for t in range(len(tareas)):
        if tareas[t].dependencia:
            if tareas[t].dependencia not in tareas[:t]:
                flag=False
                
    return flag

def get_task_list(pipeline):
    tareas=[]
    for g in pipeline.get_groups():
        for t in g.get_tasks():
            if t not in tareas:
                tareas.append(t)
            
    return tareas

def organizar(tareas):
    while(validar_orden(tareas) == False):
        for t in tareas:
            if t.dependencia:
                if t.dependencia in tareas[tareas.index(t):]:
                    tareas.remove(t.dependencia)
                    break
                elif t.dependencia not in tareas:
                    tareas.insert(tareas.index(t),t.dependencia)
                    break
                else:
                    continue

def generate_plots_ica(archive,task_c):
    media=settings.MEDIA_ROOT
    folder=os.path.dirname(archive)
    folder_js=os.path.join(folder,"series_js")
    os.mkdir(folder_js)
                    
    data=np.genfromtxt(archive,delimiter=",")
    data=data.T
    
    for i in range(len(data)):
        path=os.path.join(folder_js,"ts_ica_"+str(i+1)+".js")
        grafics_plot(arrays=[data[i]],
                     direccion=path,
                     legends=["Actividad"],
                     labelaxes= ["Tiempo","Actividad"],
                     Title="Actividad Cerebral ica "+str(i+1),
                     myDiv="div_ts_"+str(i+1),
                     autosize=False)
        results.objects.create(task_celery=task_c,nombre="ts ica "+str(i+1),
                               path=path[len(os.path.dirname(media)):],
                               tipo="Ica Graph")                    

@shared_task
def crear_tarea(pk):
    
    t_celery = task_celery.objects.get(pk=pk)
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        
    folder_sujetos= os.path.join(result_path,"Sujetos")
    
    if not os.path.exists(folder_sujetos):
        os.mkdir(folder_sujetos)
        
    folder_controles= os.path.join(result_path,"Controles")
    
    if not os.path.exists(folder_controles):
        os.mkdir(folder_controles)
        
    folder_img=""    
        
    picture=t_celery.imagen
    
    if picture.slug[0] == 'c':
        folder_img= os.path.join(folder_controles,"Control_"+str(picture.slug[1:]))
    else:
        folder_img= os.path.join(folder_sujetos,"Sujeto_"+str(picture.slug))
       
        
        
    if not os.path.exists(folder_img):
        os.mkdir(folder_img)
        
    folder_pipeline = os.path.join(folder_img,str(t_celery.pipeline.nombre.replace(" ","_")))
    
    if not os.path.exists(folder_pipeline):
        os.mkdir(folder_pipeline)
        
    tareas=get_task_list(t_celery.pipeline)
    organizar(tareas)
    
    media=settings.MEDIA_ROOT
    
    folder_nii=os.path.join(os.path.dirname(media+t_celery.imagen.file.name),"nifty")
    
    archives=[T1_path(folder_nii)]+DWI_path(folder_nii)+[rest_path(folder_nii)]
    
    for file in archives:
        shutil.copy(file,folder_pipeline)
        
    img=img_to_show.objects.get(sujeto=t_celery.imagen,imagen=t_celery.pipeline.tipo_imagen)
    
    path_in=os.path.join(folder_pipeline,os.path.basename(img.path))
    
    dic_tareas={}
    for i in range(len(tareas)):
            dic_tareas[i]=[str(tareas[i].nombre.replace(" ","_")),tareas[i].pathscript,[path_in]]
    path_in=run_pipeline("g",dic_tareas,folder_pipeline)
    
    if path_in == "error":
        t_celery.estado="Finalizado con Error"
        t_celery.save()
        
    else:
        t_celery.estado="Finalizado"
        t_celery.save()
        
    
        if not os.path.isdir(path_in):
            path_in = os.path.dirname(path_in)

        

        archivos=os.listdir(path_in)
        
        if "time_series_ica.csv" in archivos:
            generate_plots_ica(os.path.join(path_in,"time_series_ica.csv"),
                               t_celery)
        
        full_list = [os.path.join(path_in,i) for i in archivos]
        time_sorted_list = sorted(full_list, key=os.path.getmtime)

        for tarea in tareas:
            for def_res in tarea.default_result_set.all():
                for a in time_sorted_list:
                    name=os.path.basename(a)
                    if def_res.word_key in a:
                        nombre=name.split('.')[0]
                        results.objects.create(task_celery=t_celery,nombre=nombre,
                                               path=a[len(os.path.dirname(media)):],
                                               tipo=def_res.tipo)
    

    
    return ""
        