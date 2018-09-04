from plotly.offline import plot
from plotly.graph_objs import Scatter, Box, Figure, Layout
import os, shutil
import nibabel as nib
from numpy import prod
import numpy as np


def np2str(a):
    line = "["
    for e in a:
        line += " " + str(e) + ","
    line = line[:-1] + "]"
    return line


def grafics_plot(arrays, direccion, legends, Title, labelaxes, myDiv):
    file = direccion
    f = open(file, "w+")
    traces = []
    for i in range(len(arrays)):
        traces.append("traces" + str(i))
        f.write("var " + traces[i] + " = { \n")
        f.write("y: " + np2str(arrays[i]) + ",\n")
        f.write("name: '" + legends[i] + "', \n")
        f.write("type: 'scatter' \n };\n")
    f.write("var data = " + np2str(traces) + ";\n")
    f.write("var layout = { \n title: '" + Title + "',\n 'titlefont': { \n 'size': 36, \n }, \n xaxis: { \n title: '" +
            labelaxes[0] + "', \n  titlefont: { \n")
    f.write("family: 'Courier New, monospace', \n size: 18, \n color: '#7f7f7f' \n   } \n  }, \n ")
    f.write(" yaxis: { \n  title: '" + labelaxes[
        1] + "', \n  titlefont: { \n  family: 'Courier New, monospace', \n size: 18, \n color: '#7f7f7f' \n } \n } \n }; \n")
    f.write("Plotly.newPlot('" + myDiv + "', data, layout);")

    f.close()

def func_motion_correct(dir_func, dir_result, sn, tipo, tipoimg):
    if os.path.exists(dir_result):
        shutil.rmtree(dir_result)
    os.mkdir(dir_result)
    dir_file = os.path.join(dir_result, "desing.fsf")
    file = open(dir_file, "w")
    file.write("set fmri(version) 6.00 \n")
    file.write("set fmri(inmelodic) 0 \n")
    file.write("set fmri(level) 1 \n")
    file.write("set fmri(analysis) 1 \n")
    file.write("set fmri(relative_yn) 0 \n")
    file.write("set fmri(help_yn) 0 \n")
    file.write("set fmri(featwatcher_yn) 0 \n")
    file.write("set fmri(sscleanup_yn) 0 \n")
    file.write('set fmri(outputdir) "' + dir_result + '"\n')
    img = nib.load(dir_func)
    tr = img.header.get_zooms()[-1]
    file.write("set fmri(tr) " + str(tr) + "\n")
    volumes = img.get_data().shape[-1]
    file.write("set fmri(npts) " + str(volumes) + "\n")
    file.write("set fmri(ndelete) 0 \n")
    file.write("set fmri(tagfirst) 1 \n")
    file.write("set fmri(multiple) 1 \n")
    file.write("set fmri(inputtype) 2 \n")
    file.write("set fmri(filtering_yn) 1 \n")
    file.write("set fmri(brain_thresh) 10 \n")
    file.write("set fmri(critical_z) 5.3 \n")
    file.write("set fmri(noise) 0.66 \n")
    file.write("set fmri(noisear) 0.34 \n")
    file.write("set fmri(mc) 1 \n")
    file.write("set fmri(sh_yn) 0 \n")
    file.write("set fmri(regunwarp_yn) 0 \n")
    file.write('set fmri(gdc) "" \n')
    file.write("set fmri(dwell) 0.7 \n")
    file.write("set fmri(te) 35 \n")
    file.write("set fmri(signallossthresh) 10 \n")
    file.write("set fmri(unwarp_dir) y- \n")
    file.write("set fmri(st) 0 \n")
    file.write('set fmri(st_file) "" \n')
    file.write("set fmri(bet_yn) 0  \n")
    file.write("set fmri(smooth) 5  \n")
    file.write("set fmri(norm_yn) 0 \n")
    file.write("set fmri(perfsub_yn) 0  \n")
    file.write("set fmri(temphp_yn) 0  \n")
    file.write("set fmri(templp_yn) 0  \n")
    file.write("set fmri(melodic_yn) 0  \n")
    file.write("set fmri(stats_yn) 0  \n")
    file.write("set fmri(prewhiten_yn) 1 \n")
    file.write("set fmri(motionevs) 0 \n")
    file.write('set fmri(motionevsbeta) "" \n')
    file.write('set fmri(scriptevsbeta) "" \n')
    file.write("set fmri(robust_yn) 0 \n")
    file.write("set fmri(mixed_yn) 2 \n")
    file.write("set fmri(randomisePermutations) 5000 \n")
    file.write("set fmri(evs_orig) 1 \n")
    file.write("set fmri(evs_real) 2 \n")
    file.write("set fmri(evs_vox) 0 \n")
    file.write("set fmri(ncon_orig) 1 \n")
    file.write("set fmri(ncon_real) 1 \n")
    file.write("set fmri(nftests_orig) 0 \n")
    file.write("set fmri(nftests_real) 0 \n")
    file.write("set fmri(constcol) 0 \n")
    file.write("set fmri(poststats_yn) 0 \n")
    file.write('set fmri(threshmask) "" \n')
    file.write("set fmri(thresh) 3 \n")
    file.write("set fmri(prob_thresh) 0.05 \n")
    file.write("set fmri(z_thresh) 3.1 \n")
    file.write("set fmri(zdisplay) 0 \n")
    file.write("set fmri(zmin) 2 \n")
    file.write("set fmri(zmax) 8 \n")
    file.write("set fmri(rendertype) 1 \n")
    file.write("set fmri(bgimage) 1 \n")
    file.write("set fmri(tsplot_yn) 1 \n")
    file.write("set fmri(reginitial_highres_yn) 0 \n")
    file.write("set fmri(reginitial_highres_search) 90 \n")
    file.write("set fmri(reginitial_highres_dof) 3 \n")
    file.write("set fmri(reghighres_yn) 0 \n")
    file.write("set fmri(reghighres_search) 90 \n")
    file.write("set fmri(reghighres_dof) BBR \n")
    file.write("set fmri(regstandard_yn) 0 \n")
    file.write("set fmri(alternateReference_yn) 0 \n")
    file.write('set fmri(regstandard) "/usr/local/fsl/data/standard/MNI152_T1_2mm_brain" \n')
    file.write("set fmri(regstandard_search) 90 \n")
    file.write("set fmri(regstandard_dof) 12 \n")
    file.write("set fmri(regstandard_nonlinear_yn) 0 \n")
    file.write("set fmri(regstandard_nonlinear_warpres) 10  \n")
    file.write("set fmri(paradigm_hp) 100 \n")
    dim = img.get_data().shape
    product = prod(dim)
    file.write("set fmri(totalVoxels) " + str(product) + "\n")
    file.write("set fmri(ncopeinputs) 0 \n")
    file.write('set feat_files(1) "' + dir_func + '" \n')
    file.write("set fmri(confoundevs) 0 \n")
    file.write('set fmri(evtitle1) "" \n')
    file.write("set fmri(shape1) 0 \n")
    file.write("set fmri(convolve1) 2 \n")
    file.write("set fmri(convolve_phase1) 0 \n")
    file.write("set fmri(tempfilt_yn1) 1 \n")
    file.write("set fmri(deriv_yn1) 1 \n")
    file.write("set fmri(skip1) 0 \n")
    file.write("set fmri(off1) 30 \n")
    file.write("set fmri(on1) 30 \n")
    file.write("set fmri(phase1) 0 \n")
    file.write("set fmri(stop1) -1 \n")
    file.write("set fmri(gammasigma1) 3 \n")
    file.write("set fmri(gammadelay1) 6 \n")
    file.write("set fmri(ortho1.0) 0 \n")
    file.write("set fmri(ortho1.1) 0 \n")
    file.write("set fmri(con_mode_old) orig \n")
    file.write("set fmri(con_mode) orig \n")
    file.write("set fmri(conpic_real.1) 1 \n")
    file.write('set fmri(conname_real.1) "" \n')
    file.write("set fmri(con_real1.1) 1 \n")
    file.write("set fmri(con_real1.2) 0 \n")
    file.write("set fmri(conpic_orig.1) 1 \n")
    file.write('set fmri(conname_orig.1) "" \n')
    file.write("set fmri(con_orig1.1) 1 \n")
    file.write("set fmri(conmask_zerothresh_yn) 0 \n")
    file.write("set fmri(conmask1_1) 0 \n")
    file.write('set fmri(alternative_mask) "" \n')
    file.write('set fmri(init_initial_highres) "" \n')
    file.write('set fmri(init_highres) "" \n')
    file.write('set fmri(init_standard) "" \n')
    file.write("set fmri(overwrite_yn) 0 \n")
    file.close()
    os.system("feat " + dir_file)

    img_out = dir_result + ".feat/filtered_func_data.nii.gz"
    shutil.copy(img_out, os.path.join(dir_result, os.path.basename(dir_func)))
    abs_mean_file = dir_result + ".feat/mc/prefiltered_func_data_mcf_abs_mean.rms"
    file = open(abs_mean_file, "r")
    absolute = float(file.read()[:4])
    relative_mean_file = dir_result + ".feat/mc/prefiltered_func_data_mcf_rel_mean.rms"
    file = open(relative_mean_file, "r")
    relative = float(file.read()[:4])
    abs_values_file = dir_result + ".feat/mc/prefiltered_func_data_mcf_abs.rms"
    abs_values = []
    with open(abs_values_file) as f:
        for line in f:
            abs_values.append(float(line))
    relative_values_file = dir_result + ".feat/mc/prefiltered_func_data_mcf_rel.rms"
    relative_values = []
    with open(relative_values_file) as f:
        for line in f:
            relative_values.append(float(line))
    paths_html = {}
    paths_html["desplazamiento"] = dir_result + "/desplazamiento.js"
    grafics_plot([abs_values, relative_values],
                 paths_html["desplazamiento"],
                 ["Absoluto", "Relativo"],
                 "Desplazamiento Medio " + tipo + " " + "# " + sn,
                 ["Tiempo (volumenes)", "Distancia (mm)"],
                 "div_"+tipoimg+"_desplazamiento")

    rot_n_tra_path = dir_result + ".feat/mc/prefiltered_func_data_mcf.par"
    rot_n_tra = np.loadtxt(rot_n_tra_path)
    rot = rot_n_tra[:, :3]
    tra = rot_n_tra[:, 3:]
    paths_html["rotaciones"] = dir_result + "/rotacion.js"
    grafics_plot(arrays=[rot[:, 0], rot[:, 1], rot[:, 2]],
                 direccion=paths_html["rotaciones"],
                 legends=["x", "y", "z"],
                 Title="Rotaciones",
                 labelaxes=["Tiempo (Volumenes)", "Radianes"],
                 myDiv="div_" + tipoimg + "_rotaciones")
    paths_html["traslaciones"] = dir_result + "/traslacion.js"
    grafics_plot(arrays=[tra[:, 0], tra[:, 1], tra[:, 2]],
                 direccion=paths_html["traslaciones"],
                 legends=["x", "y", "z"],
                 Title="Traslaciones",
                 labelaxes=["Tiempo (Volumenes)", "mm"],
                 myDiv="div_" + tipoimg + "_traslaciones")

    shutil.rmtree(dir_result + ".feat")
    os.remove(dir_file)
    for path in paths_html:
        ind = paths_html[path].index("/media")
        paths_html[path]=paths_html[path][ind:]


    return absolute, relative, paths_html
