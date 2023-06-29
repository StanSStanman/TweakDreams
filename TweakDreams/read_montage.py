import numpy as np
# from collections import OrderedDict
from mne.channels.montage import make_dig_montage
# from warnings import warn


def read_elc(fname, head_size):
    """Read .elc files.

    Parameters
    ----------
    fname : str
        File extension is expected to be '.elc'.
    head_size : float | None
        The size of the head in [m]. If none, returns the values read from the
        file with no modification.

    Returns
    -------
    montage : instance of DigMontage
        The montage in [m].
    """
    fid_names = ('Nz', 'LPA', 'RPA')

    # ch_names_, pos = [], []
    with open(fname) as fid:
        # _read_elc does require to detect the units. (see _mgh_or_standard)
        for line in fid:
            if 'UnitPosition' in line:
                units = line.split()[-1]
                scale = dict(m=1., mm=1e-3)[units]
                break
        else:
            raise RuntimeError('Could not detect units in file %s' % fname)
        for line in fid:
            if 'Positions\n' in line:
                break
        pos = []
        for line in fid:
            if 'Labels\n' in line:
                break
            pos.append(list(map(float, line.split()[-3:])))
        for line in fid:
            # if not line or not set(line) - {' '}:
            #     break
            if 'NumberHeadShapePoints' in line:
                break
            # ch_names_.append(line.strip('\n').split())
            ch_names_ = line.strip('\n').split()
        for line in fid:
            if 'UnitHeadShapePoints' in line:
                hs_units = line.split()[-1]
                hs_scale = dict(m=1., mm=1e-3)[hs_units]
                break
        hs_pos = []
        for line in fid:
            if 'HeadShapePoints' in line:
                continue
            hs_pos.append(list(map(float, line.split())))

    pos = np.array(pos) * scale
    hs_pos = np.array(hs_pos) * hs_scale
    if head_size is not None:
        pos *= head_size / np.median(np.linalg.norm(pos, axis=1))

    # ch_pos = _check_dupes_odict(ch_names_, pos)
    # nasion, lpa, rpa = [hs_pos.pop(n, None) for n in fid_names]
    nasion, lpa, rpa = tuple(hs_pos[-3:])
    hs_pos = hs_pos[:-3, :]

    ch_pos = {ch_names_[i]: pos[i] for i in range(len(ch_names_))}

    return make_dig_montage(ch_pos=ch_pos, nasion=nasion, lpa=lpa, rpa=rpa, 
                            hsp=hs_pos, coord_frame='unknown')


if __name__ == '__main__':
    mont_fname = '/media/jerry/ruggero/dataset_td02/brainvision' +  \
        '/TD001_N1/eeg/TD001_N1.elc'
    
    dig_mont = read_elc(mont_fname, head_size=None)
    0/0
