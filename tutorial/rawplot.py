import os
import mne

import matplotlib.pyplot as plt 

plotAll = False

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
									'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(tmax=60).load_data()


if plotAll: 
	raw.plot()	

if plotAll:
	raw.plot_psd(average=True)

if plotAll:
	midline = ['EEG 002', 'EEG 012', 'EEG 030', 'EEG 048', 'EEG 049' 'EEG 058', 'EEG 060']
	raw.plot_psd(picks=midline)

if plotAll:
	raw.plot_psd_topo()

if plotAll:
	raw.copy().pick_types(meg=False, eeg=True).plot_psd_topo()	


if plotAll:
	raw.plot_sensors(ch_type='eeg')

raw.plot_projs_topomap(colorbar=True)
plt.show()