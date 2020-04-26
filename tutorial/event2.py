import os 
import numpy as np 
import mne
import matplotlib.pyplot as plt 

plotAll = False

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
						'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file, verbose=False)
raw.crop(tmax=60).load_data()

events= mne.find_events(raw, stim_channel='STI 014')

sample_data_events_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
										'sample_audvis_raw-eve.fif')
events_from_file = mne.read_events(sample_data_events_file)
assert np.array_equal(events, events_from_file[:len(events)])

mne.find_events(raw, stim_channel='STI 014')
events_no_button = mne.pick_events(events, exclude=32)
merged_events = mne.merge_events(events, [1, 2, 3], 1)
print(np.unique(merged_events[:, -1]))


event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3, 
			  'visual/right': 4, 'smiley': 5, 'buttonpress': 32}


if plotAll:
	fig = mne.viz.plot_events(events, sfreq=raw.info['sfreq'], 
							  first_samp=raw.first_samp, event_id=event_dict)
	fig.subplots_adjust(right=0.7)

	raw.plot(events=events, start=5, duration=10, color='gray', 
	     event_color={1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'y', 32: 'k'})

	plt.show()

new_events = mne.make_fixed_length_events(raw, start=5, stop=50, duration=2.)
print(new_events)