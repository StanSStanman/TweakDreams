import mne
from TweakDreams.utils.montage import read_elc


def set_eeglab_montage(eegl_fname, elc_fname):

    eegl_epo = mne.io.read_epochs_eeglab(eegl_fname, montage_units='mm')
    eegl_epo.set_channel_types({'EMG': 'emg',
                                'ECG': 'ecg',
                                'VEOGR': 'eog',
                                'RES': 'resp'})
    digi_mont = read_elc(elc_fname, head_size=None)
    eegl_epo = eegl_epo.set_montage(digi_mont)
    return eegl_epo


if __name__ == '__main__':
    eegl_epo.save(mne_epo_fname, fmt='single', overwrite=True)