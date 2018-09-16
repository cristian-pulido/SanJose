import os, shutil
import programas.definitions as defi


## conversor
from SanJose import settings
from apps.fileupload.models import Picture
from apps.paciente.models import Candidato, Control, Parametrosmotioncorrect
from apps.validacion.templatetags.scripts_validacion import pass_tags_to_db, campos_a_mostrar
from programas import definitions
from programas.anonimizador import get_tags_dicom
from programas.motion_correct_fmri import func_motion_correct


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


# identifica la direccion de la Tensor / DWI si b es False devuelve unicamente la direccion de la imagen nifty
def DWI_path(folder, b=True):
    lista = os.listdir(folder)
    path = []
    for l in lista:
        if "TENSOR" in l and os.path.splitext(l)[1] != ".json":
            path.append(os.path.join(folder, l))
    if b == True:
        return path
    else:
        img = ""
        for item in path:
            if os.path.splitext(item)[1] != ".bvec" and os.path.splitext(item)[1] != ".bval":
                img = item
        return img


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
def do_change(sujeto_numero,tipe):
    n = str(sujeto_numero)
    if tipe == 'control':

        base_dir = settings.MEDIA_ROOT + "/controles/control" + n
        c = Control.objects.get(numero=n)
        archive = os.path.join(base_dir, "control" + n + "_dicom.zip")


    else:

        base_dir = settings.MEDIA_ROOT + "/img/sujeto" + n
        c = Candidato.objects.get(sujeto_numero=n)
        archive = os.path.join(base_dir, "sujeto" + n + "_dicom.zip")






    if len(os.listdir(base_dir)) > 2:
        shutil.rmtree(base_dir+"/nifty")
        os.remove(base_dir+"/"+n+".txt")

        import zipfile
        a = zipfile.ZipFile(archive)
        a.extractall(base_dir)

        lista=os.listdir(base_dir)
        for i in lista:
            if os.path.isdir(os.path.join(base_dir,i)) and not "__" in i and not i.startswith('.'):
                folder_dicom=os.path.join(base_dir,i)




        series = get_tags_dicom(folder_dicom)
        if tipe == "control":
            sn="c"+n
        else:
            sn=n
        pass_tags_to_db(sn, series)
        campos_a_mostrar()
        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Anonimizado\n")
        f.write("-Verificación Parametros\n")
        f.close()

        folder_nii = os.path.join(base_dir, "nifty")
        os.mkdir(folder_nii)
        convertir_dcm_2_nii(base_dir, folder_nii)
        shutil.rmtree(folder_dicom)


        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Conversion Dicom a Nifty\n")
        f.close()

        func_result = os.path.join(folder_nii, "func_result")
        absolute_func, relative_func, paths_html_func = func_motion_correct(rest_path(folder_nii), func_result, n, tipe,
                                                                            "func")
        os.remove(rest_path(folder_nii))
        shutil.move(rest_path(func_result), folder_nii)

        dir_dwi = os.path.join(folder_nii, "dwi_mc")
        os.mkdir(dir_dwi)
        shutil.move(DWI_path(folder_nii, False), dir_dwi)
        os.system("fslsplit " + os.path.join(dir_dwi, os.listdir(dir_dwi)[0]) + " " + dir_dwi + "/vol")
        os.remove(DWI_path(dir_dwi, False))
        b0 = os.path.join(dir_dwi, "b0.nii.gz")
        shutil.move(os.path.join(dir_dwi, "vol0000.nii.gz"), b0)
        dwi_image_no_b0 = os.path.join(dir_dwi, "TENSOR")
        os.system("fslmerge -t " + dwi_image_no_b0 + " " + dir_dwi + "/vol* ")
        volumenes = os.listdir(dir_dwi)
        for volumen in volumenes:
            if "vol" in volumen:
                os.remove(os.path.join(dir_dwi, volumen))
        dwi_result = os.path.join(folder_nii, "dwi_result")
        absolute_dwi, relative_dwi, paths_html_dwi = func_motion_correct(DWI_path(dir_dwi, False),
                                                                         dwi_result,
                                                                         n, tipe, "dwi")
        os.system("fslmerge -t " + folder_nii + "/TENSOR" + " " + b0 + " " + DWI_path(dwi_result, False))
        os.remove(DWI_path(dwi_result, False))
        shutil.rmtree(dir_dwi)

        P = Parametrosmotioncorrect.objects.create(absolute_func=absolute_func,
                                                   relative_func=relative_func,
                                                   graphic_desplazamiento_func=paths_html_func["desplazamiento"],
                                                   graphic_rotacion_func=paths_html_func["rotaciones"],
                                                   graphic_traslacion_func=paths_html_func["traslaciones"],
                                                   absolute_dwi=absolute_dwi,
                                                   relative_dwi=relative_dwi,
                                                   graphic_desplazamiento_dwi=paths_html_dwi["desplazamiento"],
                                                   graphic_rotacion_dwi=paths_html_dwi["rotaciones"],
                                                   graphic_traslacion_dwi=paths_html_dwi["traslaciones"]
                                                   )
        setattr(P, tipe, c)
        P.save()

        f = open(settings.MEDIA_ROOT[:-6] + c.imagen.url, "a")
        f.write("-Correccion movimiento\n")
        f.close()

        folder_data = definitions.folder_data
        copytodata(n, folder_data, folder_nii, tipe)

    return "Completo"


## arreglo todos
def modificar():
    totalsujetos=Candidato.objects.all()
    for sujeto in totalsujetos:
        try:
            do_change(sujeto.sujeto_numero,"sujeto")
        except:
            pass
        print("Sujeto "+str(sujeto.sujeto_numero)+ " Listo")
    totalcontroles = Control.objects.all()
    for control in totalcontroles:
        try:
            do_change(control.numero,"control")
        except:
            pass
        print("Control " + str(control.numero) + " Listo")
