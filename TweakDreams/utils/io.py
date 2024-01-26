import h5py
import glob
from scipy.io import loadmat


def open_matfile(mat_fname):
    try:
        mat = loadmat(mat_fname)
        print('Loaded mat file <= v7.3...\n')
    except:
        mat = h5py.File(mat_fname)
        print('Loaded mat file >= v7.3...\n')
    return mat


def fname_finder(pathname):
    return glob.glob(pathname)