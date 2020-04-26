
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import mne
import numpy as np 
import os

allPlot = False

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
									'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=True)

montage_dir = os.path.join(os.path.dirname(mne.__file__), 
						   'channels', 'data', 'montages')

print('\nBUILT-IN MONTAGE FILES')
print('=======================')
print(sorted(os.listdir(montage_dir)))

ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
print(ten_twenty_montage)


if allPlot: 
	fig = ten_twenty_montage.plot(kind='3d')
	fig.gca().view_init(azim=70, elev=15)
	ten_twenty_montage.plot(kind='topomap', show_names=True)

# if allPlot: 
fig = plt.figure()
ax2d = fig.add_subplot(121)
ax3d = fig.add_subplot(122, projection='3d')
raw.plot_sensors(ch_type='eeg', axes=ax2d)
raw.plot_sensors(ch_type='eeg', axes=ax3d, kind='3d')
ax3d.view_init(azim=70, elev=15)


plt.show()

