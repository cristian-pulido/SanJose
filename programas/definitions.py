import os

path_dcm2niix = '/home/colciencias/programas/dcm2niix/dcm2niix'
subfolders = ["anat", "diffus", "func"]
typeimg = ["4D", "3D"]
folder_data = "/home/runlab/data/sanjose"
folder_data_types = ["controls", "patients"]
templete_T1='/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz'
# templete_T1=os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T1_2mm.nii.gz')
