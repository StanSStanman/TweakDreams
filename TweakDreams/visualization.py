import mne


def visualize_alignment(subject, sbj_dir, info_fname, trans_fname, 
                        src_fname, fwd_fname, surfaces=None):
    mne.viz.set_3d_backend('notebook')
    
    if surfaces is None:
        surfaces = {'outer_skin': .2, 'inner_skull': .4, 'white': 1.}
    
    src = mne.read_source_spaces(src_fname)
    info = mne.read_epochs(info_fname, preload=False).info
    fwd = mne.read_forward_solution(fwd_fname)
    fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
                                            force_fixed=False,
                                            use_cps=True)

    fig = mne.viz.plot_alignment(
        info=info,
        subject=subject,
        trans=trans_fname,
        subjects_dir=sbj_dir,
        surfaces=surfaces,
        coord_frame="mri",
        src=src,
        fwd=fwd,
        meg=False,
        eeg='projected',
        show_axes=False, fig=None, interaction='terrain'
    )
    mne.viz.set_3d_view(
        fig,
        azimuth=173.78,
        elevation=101.75,
        distance=0.30,
        focalpoint=(-0.03, -0.01, 0.03),
    )
    return 


def visualize_sensitivity(subject, sbj_dir, fwd_fname):
    # mne.viz.set_3d_backend('notebook')
    # import pyvista
    # pyvista.set_jupyter_backend('none')
    fwd = mne.read_forward_solution(fwd_fname)
    fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True,
                                               force_fixed=False,
                                               use_cps=True)
    fig = mne.viz.create_3d_figure((1080, 1080), show=True)
    eeg_sens = mne.sensitivity_map(fwd, ch_type="eeg", mode="free")
    eeg_sens.plot(subject=subject, subjects_dir=sbj_dir, surface='pial',
                  hemi='both', clim=dict(lims=[0, 50, 100]), figure=fig)

    return


if __name__ == '__main__':
    subject = 'TD001'
    subjects_dir = '/home/jerry/freesurfer/TweakDreams'
    info_fname = '/media/jerry/ruggero/dataset_td02/mne/TD001/n1/prep/aw0/TD001-epo.fif'
    trans_fname = '/media/jerry/ruggero/dataset_td02/mne/TD001/n1/trans/TD001-trans.fif'
    src_fname = '/media/jerry/ruggero/dataset_td02/mne/TD001/n1/src/TD001-src.fif'
    fwd_fname = '/media/jerry/ruggero/dataset_td02/mne/TD001/n1/fwd/TD001-fwd.fif'
    
    visualize_alignment(subject, subjects_dir, info_fname, trans_fname, 
                        src_fname, fwd_fname)
    visualize_sensitivity(subject, subjects_dir, fwd_fname)
