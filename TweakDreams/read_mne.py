import mne
import os
import os.path as op
from utils.io import fname_finder


def read_raw(raw_dir):
    raw_file = fname_finder(op.join(raw_dir, '*-raw.fif'))[0]
    eve_file = fname_finder(op.join(raw_dir, '*-eve.fif'))[0]

    raw = mne.io.read_raw_fif(raw_file, allow_maxshield=False, preload=False)
    eve = mne.read_events(eve_file)

    return raw, eve


if __name__ == "__main__":
    from utils.globals import prj_data

    data_dir = prj_data
    subjects = ['TD001']
    nights = ['N1']
    # awakenings = ['aw_4','aw_5']
    # awakenings = ['aw_5'] # TODO: change with a dir finder

    for sbj in subjects:
        for n in nights:
            raw_dir = op.join(prj_data, 'mne', '{0}', '{1}', 
                                'raw').format(sbj, n)
            
            raw = read_raw(raw_dir)
    