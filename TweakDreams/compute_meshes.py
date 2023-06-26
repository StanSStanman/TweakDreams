import os
import os.path as op
import subprocess


def compute_freesurfer(freesurfer_home, subjects_dir, 
                       subject_name, mri_fname, n_jobs):
    """This function allows to launch the complete freesurfer segmentation 
        pipeline on a single subject, it will generate a shell file containing
        the information, execute it, and finally delete it.

    Args:
        freesurfer_home (path_like): Path to the freesurfer home
        subjects_dir (path_like): Path to the subjects foleder
        subject_name (str): Name of the subject to process
        mri_fname (path_like): Path to the .nii MRI file
        n_jobs (int): Number of threads to use, can be 1 to max(threads), 
            or -1 to consider all threads
    """
    # Define bash file name
    cmd_file = op.join(os.getcwd(), 'fs_launcher_{0}.sh'.format(subject_name))
    # Write commands
    with open(cmd_file, 'w') as f:
        f.writelines("#!/bin/bash\n")
        f.writelines('export SUBJECTS_DIR={0}\n'.format(subjects_dir))
        f.writelines('export FREESURFER_HOME={0}\n'.format(freesurfer_home))
        f.writelines('source $FREESURFER_HOME/SetUpFreeSurfer.sh\n')
        f.writelines('recon-all -subjid {0} -i {1} -all -parallel -openmp {2}'
                     .format(subject_name, mri_fname, n_jobs))
    # Change bash file rights for execution
    os.system('chmod +x {0}'.format(cmd_file))
    # Run the bash script
    # subprocess.run('source {0}'.format(cmd_file), shell=True, text=True, 
    #                executable='/bin/bash')
    subprocess.check_call('source {0}'.format(cmd_file), shell=True, text=True,
                          executable='/bin/bash')
    # Remove bash file
    os.remove(cmd_file)

    return


def compute_scalp_meshes(freesurfer_home, subjects_dir, subject_name):
    """This function allows to launch the complete mne pipeline for scalp 
        meshes reconstruction on a single subject, it will generate a shell 
        file containing the information, execute it, and finally delete it.

    Args:
        freesurfer_home (path_like): Path to the freesurfer home
        subjects_dir (path_like): Path to the subjects foleder
        subject_name (str): Name of the subject to process
    """
    
    # Define bash file name
    cmd_file = op.join(os.getcwd(), 'scalp_meshes_{0}.sh'.format(subject_name))
    # Write commands
    with open(cmd_file, 'w') as f:
        f.writelines('#!/bin/bash\n')
        f.writelines('source activate py310\n')
        f.writelines('export SUBJECTS_DIR={0}\n'.format(subjects_dir))
        f.writelines('export FREESURFER_HOME={0}\n'.format(freesurfer_home))
        f.writelines('source $FREESURFER_HOME/SetUpFreeSurfer.sh\n')
        f.writelines('mne make_scalp_surfaces -o' +
                     '-s {0}'.format(subject_name) +
                     '-d {0}'.format(subjects_dir))
    # Change bash file rights for execution
    os.system('chmod +x {0}'.format(cmd_file))
    # Run the bash script
    subprocess.check_call('source {0}'.format(cmd_file), shell=True, text=True,
                          executable='/bin/bash')
    # Remove bash file
    os.remove(cmd_file)

    return


if __name__ == '__main__':
    fs_home = '/usr/local/freesurfer/7.3.2'
    sbj_dir = '/home/jerry/freesurfer/TweakDreams'
    sbj = 'TD001'
    mri = '/media/jerry/ruggero/dataset_td02/mri/nifti/' + \
        'sub-td001_ses-d01_mri.nii'
    n_jobs = -1

    compute_freesurfer(fs_home, sbj_dir, sbj, mri, n_jobs)
    # compute_scalp_meshes(fs_home, sbj_dir, sbj)
