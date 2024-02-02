import mne
import yasa


def sleep_staging(raw, eeg_ch='Z6Z'):
    model = yasa.SleepStaging(raw=raw, eeg_name=eeg_ch, eog_name='HEOG', 
                              emg_name='EMG')
    stages = model.predict()
    proba = model.predict_proba()
    hypnogram = yasa.hypno_str_to_int(stages)
    hypnogram = yasa.hypno_upsample_to_data(hypnogram, sf_hypno=1/30, 
                                            data=raw)
    
    return stages, proba, hypnogram
    

def sw_detection(raw, hypno):
    sw = yasa.sw_detect(raw, sf=None, ch_names=None, hypno=hypno, include=(2),
                        freq_sw=(0.5, 2.), dur_neg=(0.25, 1.), 
                        dur_pos=(0.1, 1.), amp_neg=(40, 200), 
                        amp_pos=(10, 150), amp_ptp=(75, 350), 
                        coupling=False, remove_outliers=True)
    
    return sw.summary()
