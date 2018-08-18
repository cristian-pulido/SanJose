import os, shutil
import programas.definitions as defi


## conversor
from SanJose import settings
from apps.fileupload.models import Picture
from apps.paciente.models import Candidato, Control


def convertir_dcm_2_nii(folder_dicom, folder_nii):
    ## ubicacion ejecutable dcm2niix
    print("Convirtiendo Dicom a Nifty ...")
    ejecutable = defi.path_dcm2niix
    options = '-b y -z y -f %f_%p -o'  # Json, zipped, name folder_process
    if len(os.listdir(folder_nii)) == 0:
        os.system(ejecutable + " " + options + " " + folder_nii + " " + folder_dicom)
    print("Finalizado")


# identifica la direccion de la T1
def T1_path(folder):
    lista = os.listdir(folder)
    path = ""
    for l in lista:
        if "T1" in l and os.path.splitext(l)[1] == ".gz":
            path = os.path.join(folder, l)
            break
    return path


# identifica la direccion de la Tensor / DWI
def DWI_path(folder):
    lista = os.listdir(folder)
    path = []
    for l in lista:
        if "TENSOR" in l and os.path.splitext(l)[1] != ".json":
            path.append(os.path.join(folder, l))
    return path


# identifica la direccion de la funcioal resting
def rest_path(folder):
    lista = os.listdir(folder)
    path = ""
    for l in lista:
        if "RESTING" in l and os.path.splitext(l)[1] == ".gz":
            path = os.path.join(folder, l)
            break
    return path


## copia
def copytodata(sujeto_numero, folder_data, folder_nii, tipo):
    print("Copiando Archivos")
    if tipo == "control":
        folder = os.path.join(folder_data, defi.folder_data_types[0])+"/"+tipo+str(sujeto_numero)
    else:
        folder = os.path.join(folder_data, defi.folder_data_types[1]) + "/"+tipo + str(sujeto_numero)
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    subfolders = defi.subfolders
    files = [[T1_path(folder_nii)], DWI_path(folder_nii), [rest_path(folder_nii)]]
    for i in range(len(subfolders)):
        path_subfolder = os.path.join(folder, subfolders[i])
        os.mkdir(path_subfolder)
        path_4d= os.path.join(path_subfolder, "nii")
        path_3d = os.path.join(path_subfolder, "hdr_img")
        os.mkdir(path_3d)
        os.mkdir(path_4d)
        for j in files[i]:
            if i == 1:
                ext = os.path.splitext(j)[1]
                if ext == '.gz':
                    shutil.copy(j, os.path.join(path_4d,"dwi.nii.gz"))
                    shutil.copy(j,os.path.join(path_3d,"dwi.nii.gz"))
                else:
                    shutil.copy(j, os.path.join(path_4d,"dwi"+ext))
                    shutil.copy(j,os.path.join(path_3d,"dwi"+ext))
            elif i == 0:
                shutil.copy(j, os.path.join(path_4d,"mprage_anonymized.nii.gz"))
                shutil.copy(j,os.path.join(path_3d,"mprage_anonymized.nii.gz"))
            else:
                shutil.copy(j, os.path.join(path_4d,"rest.nii.gz"))
                shutil.copy(j,os.path.join(path_3d,"rest.nii.gz"))
            lista = os.listdir(path_3d)
            try:
                file = ""
                for l in lista:
                    if os.path.splitext(l)[1] == ".gz" or os.path.splitext(l)[1] == ".nii":
                        file = path_3d+"/"+l
                os.system("dcm2nii -4 n -n n -m n -s n "+file)
                os.remove(file)
            except:
                print("")

    print("Finalizado")


## arreglo sujetos ya cargados
def do_change(sujeto_numero):
    sn=str(sujeto_numero)
    base_dir = settings.MEDIA_ROOT+"/img/sujeto" + sn
    if len(os.listdir(base_dir)) > 2:
        os.rename(os.path.join(base_dir,sn+".zip"),os.path.join(base_dir,"sujeto"+sn+"_dicom.zip"))
        folder_dicom = os.path.join(base_dir,"imagenes")
        folder_nii = os.path.join(base_dir,"nifty")
        os.mkdir(folder_nii)
        convertir_dcm_2_nii(base_dir,folder_nii)
        shutil.rmtree(folder_dicom)
        zip_name = base_dir + "/sujeto" +sn
        carpeta = folder_nii
        shutil.make_archive(zip_name, 'zip', carpeta)
        i = Picture.objects.get(slug=sn)
        i.file = "/img/sujeto" + sn + "/sujeto" + sn + ".zip"
        i.save()
        c=Candidato.objects.get(sujeto_numero=sn)
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Conversion Dicom a Nifty\n")
        f.close()
        folder_data = defi.folder_data
        copytodata(sn,folder_data,folder_nii,"sujeto")
    return "Completo"

## arreglo controles
def do_change_control(sujeto_numero):
    sn = str(sujeto_numero)
    base_dir = settings.MEDIA_ROOT+"/controles/" + sn
    if len(sn) == 1:
        os.rename(base_dir,base_dir[:-1]+"control"+base_dir[-1])
    else:
        os.rename(base_dir,base_dir[:-2]+"control"+base_dir[-2:])
    base_dir = settings.MEDIA_ROOT+"/controles/control"+sn
    if len(os.listdir(base_dir)) > 2:
        os.rename(os.path.join(base_dir,sn+".zip"),os.path.join(base_dir,"control"+sn+"_dicom.zip"))
        folder_dicom=os.path.join(base_dir,"imagenes")
        folder_nii=os.path.join(base_dir,"nifty")
        os.mkdir(folder_nii)
        convertir_dcm_2_nii(base_dir,folder_nii)
        shutil.rmtree(folder_dicom)
        zip_name = base_dir + "/control" + sn
        carpeta = folder_nii
        shutil.make_archive(zip_name, 'zip', carpeta)
        i = Picture.objects.get(slug="c"+sn)
        i.file = "/controles/control" + sn + "/control" + sn + ".zip"
        i.save()
        c = Control.objects.get(numero=sn)
        c.imagen="/controles/control"+sn+"/"+sn+".txt"
        c.save()
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Conversion Dicom a Nifty\n")
        f.close()
        folder_data=defi.folder_data
        copytodata(sn,folder_data,folder_nii,"control")
    return "Completo"

## arreglo todos
def modificar():
    totalsujetos=Candidato.objects.all()
    for sujeto in totalsujetos:
        try:
            do_change(sujeto.sujeto_numero)
        except:
            pass
        print("Sujeto "+str(sujeto.sujeto_numero)+ " Listo")
    totalcontroles = Control.objects.all()
    for control in totalcontroles:
        try:
            do_change_control(control.numero)
        except:
            pass
        print("Control " + str(control.numero) + " Listo")
