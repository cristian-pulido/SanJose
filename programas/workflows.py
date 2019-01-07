import os

from nipype import Workflow,Node,Function
import inspect
from programas.dcm2niix import DWI_path, T1_path, rest_path


# def tarea(t):
#     import importlib
#     pathscript=t.pathscript
#     module=importlib.import_module(pathscript)
#     task=getattr(module,t.nombre)
#     return task


def to_call_by_terminal(ruta, path_in,path_out,parameters_list):
    import os
    str_parametros = ""
    for parametros in parameters_list:
        str_parametros += parametros + ' '

    # out=os.system("python "+ruta+" "+str_parametros)
    out = os.popen("python "+ruta+" "+path_in+" "+path_out+" "+str_parametros).read()
    return str(out).splitlines()[-1]


def run_pipeline(p_name, tareas,results):
    wf = Workflow(p_name)
    wf_nodes=[]
    import os
    for i in range(len(tareas)):
        modulo = to_call_by_terminal
        nodo = Node(Function(input_names=["ruta","path_in","path_out","parameters_list"],
                             output_names=["path_out"],
                             function=modulo),
                    name=tareas[i][0])
        wf_nodes.append(nodo)
        wf.add_nodes([nodo])
        if i == 0:
            nodo.inputs.ruta=tareas[i][1]
            nodo.inputs.path_in=tareas[i][2][0]


            if not os.path.exists(results):
                os.mkdir(results)
            nodo.inputs.path_out = results
            try:
                nodo.inputs.parameters_list=tareas[i][2][2:]
            except:
                print("no parametros extra")
        else:
            nodo.inputs.ruta = tareas[i][1]
            nodo.inputs.path_out = results
            try:
                nodo.inputs.parameters_list = tareas[i][2][2:]
            except:
                print("no parametros extra")
            wf.connect(wf_nodes[i-1],'path_out',nodo,'path_in')

    eg = wf.run()

    return list(eg.nodes())[-1].result.outputs.path_out



# @shared_task
# def crear_tareas(pipeline):
#     path_in=""
#     folder="/home/cristian/Escritorio/sujeto14/nifty/"
#     if pipeline.tipo_imagen.nombre == 'TENSOR  AXI':
#         path_in=DWI_path(folder,False)
#     elif pipeline.tipo_imagen.nombre == '3D AX Obl T1 FSPGR':
#         path_in=T1_path(folder)
#     else:
#         path_in=rest_path(folder)
#
#     grupos=pipeline.grupos.all()
#     for grupo in grupos:
#         tareas=grupo.get_task()
#         dic_tareas={}
#         for i in range(len(tareas)):
#                 dic_tareas[i]=[tareas[i].nombre,tareas[i].pathscript,[path_in,tareas[i].pathout]]
#         # print(dic_tareas)
#         w=run_pipeline(grupo.nombre,dic_tareas)
#
#
#     return w