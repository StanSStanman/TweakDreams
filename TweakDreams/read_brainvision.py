import os
import os.path as op
import mne
from utils.montage import read_elc


def brainvision_to_mne(vhdr_fnames, elc_fname, events_id, raw_dir, fif_fname):
    """Read and convert TweakDreams' brainvision raw files in mne fif files.
       The raw fif files are diveded by nights and awakenings and saved with 
       the correct references and names for the autonomic signals channels.
       A small event matrix is also saved with the raw file.

    Args:
        vhdr_fname (_type_): _description_
        elc_fname (_type_): _description_
        events_id (_type_): _description_
        raw_dir (_type_): _description_
        fif_fname (_type_): _description_

    Return:

    """
    # Setting counter for awakenings
    awakening = 0

    for vhdr_fname in vhdr_fnames:
        # Read brainvision raw (no memory loading)
        raw = mne.io.read_raw_brainvision(vhdr_fname, preload=False)
        # Reading the montage
        digi_mont = read_elc(elc_fname, head_size=None)
        # Extracting salient events
        events, event_dict = mne.events_from_annotations(raw, 
                                                         event_id=events_id)

        # Setting counters for events
        start, stop = False, False
        # For loop to cut raw in chunks
        for i, ev in enumerate(events):
            if ev[-1] == 20 and not start:
                start = True
                start_tp = ev[0]
                start_idx = i
            elif ev[-1] == 40 and not stop:
                stop = True
                stop_tp = ev[0]
                stop_idx = i

            # Once a chunk is detected, cut the raw file, load data, 
            # add montage, do some mumbojambos, and save as a mne .fif file
            if start and stop:
                # Define destination directory
                aw_raw_dir = op.join(raw_dir, 'aw_{0}'.format(awakening))
                # Create the whole paths tree
                os.makedirs(aw_raw_dir, exist_ok=True)

                # Cut the data chunk for this awakening
                tmin = raw.times[start_tp]
                tmax = raw.times[stop_tp]
                crop_raw = raw.copy().crop(tmin, tmax)
                # Load data in memory
                crop_raw.load_data()
                # Adding the reference channel
                crop_raw = crop_raw.add_reference_channels('Z12Z')
                # Renaming and assing a type to autonomic channels
                crop_raw = crop_raw.rename_channels(mapping={'BIP1': 'EMG',
                                                            'BIP2': 'ECG',
                                                            'BIP3': 'RES'})
                crop_raw = crop_raw.set_channel_types(mapping={'EMG': 'emg',
                                                            'ECG': 'ecg',
                                                            'RES': 'resp'})
                # Adding the montage after defining autonomic channels
                crop_raw = crop_raw.set_montage(digi_mont)
                # Referencing and renaming the vertical ocular channel
                crop_raw = mne.set_bipolar_reference(crop_raw, 'VEOGR', 'R1Z', 
                                                     ch_name='VEOG', 
                                                     drop_refs=False, 
                                                     copy='False')
                # Deleting the old unreferenced VEOGR channel
                crop_raw.drop_channels(ch_names=['VEOGR'])
                # Creating the horizontal ocular channel 
                crop_raw = mne.set_bipolar_reference(crop_raw, 'L1G', 'R1G', 
                                                     ch_name='HEOG', 
                                                     drop_refs=False, 
                                                     copy='False')
                # Assing type to ocular channels
                crop_raw = crop_raw.set_channel_types(mapping={'VEOG': 'eog',
                                                            'HEOG': 'eog'})
                # Saving the raw fif file
                crop_raw.save(op.join(aw_raw_dir, 
                                      '{0}-raw.fif'.format(fif_fname)),
                              overwrite=True)

                ev_chunk = events.copy()[start_idx:stop_idx, :]
                mne.write_events(op.join(aw_raw_dir, 
                                        '{0}-eve.fif'.format(fif_fname)), 
                                        ev_chunk, overwrite=True)

                start, stop = False, False
                awakening += 1
                del crop_raw

    return


if __name__ == '__main__':
    from utils.io import fname_finder
    data_dir = '/media/jerry/ruggero/tweakdreams'
    subjects = ['TD010']
    nights = ['N1']

    for sbj in subjects:
        for ngt in nights:
            _vhdr = op.join(data_dir, '{0}', '{0}_{1}', 'eeg',
                            '*', '*.vhdr').format(sbj, ngt)
            vhdr_fnames = fname_finder(_vhdr)
            _elc = op.join(data_dir, '{0}', '{0}_{1}', 'eeg', 
                           '{0}_{1}*.elc').format(sbj, ngt)
            elc_fname = fname_finder(_elc)[0]
            events_id = {'Stimulus/s20': 20,
                        'Stimulus/s30': 30,
                        'Stimulus/s40': 40,
                        'Stimulus/s22': 22,
                        'Stimulus/s24': 24,
                        'Stimulus/s26': 26,
                        'Stimulus/s28': 28}
            raw_dir = op.join(data_dir, 'mne', '{0}', '{1}', 
                              'raw').format(sbj, ngt)
            fif_fname = '{0}_{1}'.format(sbj, ngt)

            brainvision_to_mne(vhdr_fnames, elc_fname, events_id, 
                               raw_dir, fif_fname)
