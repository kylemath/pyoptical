import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne
import mne

boxy_file = "data/emm0311a.001"
mtg_file = "data/emm0311_good.mtg"
# coord_file = "data/emm0311.tol"
coord_file = "data/emm0311.elp"

raw_data = boxy2mne(boxy_file=boxy_file, mtg_file=mtg_file, coord_file=coord_file)


# fig = plt.figure()
# ax3d = fig.add_subplot(111, projection='3d')
# raw_data.plot_sensors(ch_type='eeg', axes=ax3d, kind='3d')
# ax3d.view_init(azim=70, elev=15)



###grab only channels for each data type###
ch_list_ac = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'AC ' in chan['ch_name']])
# ch_list_dc = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'DC ' in chan['ch_name']])
# ch_list_ph = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'Ph ' in chan['ch_name']])
# ch_list_all = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs']])

###plot our data###
# raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_ac)
# raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_dc)
# raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_ph)

# plt.show()
###calculate our distances (should be the same across data types###)
dists_ac = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_ac)
# dists_dc = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_dc)
# dists_ph = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_ph)
# dists_all = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_all)

for i in np.arange(24):
	print(raw_data.info['chs'][i]['loc'][3:6])


subjects_dir = mne.datasets.sample.data_path() + '/subjects'
data_path = mne.datasets.sample.data_path()
trans = mne.read_trans(data_path + '/MEG/sample/sample_audvis_raw-trans.fif')
raw = mne.io.read_raw_fif(data_path + '/MEG/sample/sample_audvis_raw.fif')
fig = mne.viz.plot_alignment(raw_data.info, trans, subject='sample',
							dig=False,
							eeg=['original', 'projected'], meg=[],
							coord_frame='head', subjects_dir=subjects_dir) 
mne.viz.set_3d_view(figure=fig, azimuth=135, elevation=80)

plt.show()
