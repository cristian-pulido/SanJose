import os
import matplotlib
matplotlib.use('Agg')
import nilearn.plotting as plt
import nibabel
import numpy as np
import math
import programas.tools as tools
from programas import definitions


def alineacion_manual(img_path, A,out_path,save_path,save):

    template = definitions.templete_T1
    img = nibabel.load(img_path)
    affine = np.dot(np.array(img.affine), np.array(A))
    header=img.header
    data = img.get_data()
    if len(data.shape) == 4:
        new_image = nibabel.nifti1.Nifti1Image(data[:,:,:,0], affine,header)
    else:
        new_image = nibabel.nifti1.Nifti1Image(data, affine,header)
    display = plt.plot_anat(template, cut_coords=(0, 0, 0),figure=None)
    display.add_contours(new_image)
    display.savefig(out_path)
    display.close()
    if save:
        new_image = nibabel.nifti1.Nifti1Image(data, affine, header)
        nibabel.save(new_image, save_path)


def traslacion(der=0, frente=0, arriba=0):
    A = np.eye(4)
    A[0][3] = der
    A[1][3] = frente
    A[2][3] = arriba
    return A


def escala(y=1, x=1, z=1):
    A = np.eye(4)
    A[0][0] = y
    A[1][1] = x
    A[2][2] = z
    return A


def rotarx(theta=0):
    A = np.eye(4)
    A[1][1] = math.cos(theta)
    A[1][2] = -math.sin(theta)
    A[2][1] = math.sin(theta)
    A[2][2] = math.cos(theta)
    return A


def rotary(theta=0):
    A = np.eye(4)
    A[0][0] = math.cos(theta)
    A[0][2] = -math.sin(theta)
    A[2][0] = math.sin(theta)
    A[2][2] = math.cos(theta)
    return A


def rotarz(theta=0):
    A = np.eye(4)
    A[0][0] = math.cos(theta)
    A[0][1] = -math.sin(theta)
    A[1][0] = math.sin(theta)
    A[1][1] = math.cos(theta)
    return A


def transformaciones(img_path, out_path,save_path,der=0, frente=0, arriba=0, x=1, y=1, z=1, tx=0, ty=0, tz=0,save=0):
    T = traslacion(der=der, frente=frente, arriba=arriba)
    E = escala(x=x, y=y, z=z)
    Rx = rotarx(tx)
    Ry = rotary(ty)
    Rz = rotarz(tz)
    transformaciones = [T, Rz, Ry, Rx, E]
    A = np.eye(4)
    for i in transformaciones:
        A = np.dot(A, i)
    alineacion_manual(img_path, A,out_path,save_path,bool(save))


def registro(path_in,path_out,path_plot):
    MNI_T1 = nibabel.load(definitions.templete_T1)
    MNI_T1_data = MNI_T1.get_data()
    MNI_T1_affine = MNI_T1.affine
    img = nibabel.load(path_in)
    data = img.get_data()
    print(data.shape)
    affineStructural = img.affine
    affine, starting_affine = tools.affine_registration(data, MNI_T1_data, moving_grid2world=affineStructural,
                                                        static_grid2world=MNI_T1_affine)
    new_image = nibabel.nifti1.Nifti1Image(affine, affine=MNI_T1_affine,header=img.header)
    nibabel.save(new_image, path_out)
    transformaciones(path_out,path_plot,path_out,der=0,frente=0,arriba=0,x=1,y=1,z=1,tx=0,ty=0,tz=0,save=1)