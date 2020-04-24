import os
import numpy as np 
import mne
import matplotlib.pyplot as plt 

plotAll = False;

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
									'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(tmax=60).load_data()

if plotAll: 
	raw.copy().pick_types(meg=False, stim=True).plot(start=3, duration=6)

events = mne.find_events(raw, stim_channel='STI 014')
print(events[:5])

testing_data_folder = mne.datasets.testing.data_path()
eeglab_raw_file = os.path.join(testing_data_folder, 'EEGLAB', 'test_raw.set')
eeglab_raw = mne.io.read_raw_eeglab(eeglab_raw_file)
print(eeglab_raw.annotations)
print(set(eeglab_raw.annotations.description))

custom_mapping = {'rt': 77, 'square': 42}
events_from_annot, event_dict = mne.events_from_annotations(eeglab_raw, event_id=custom_mapping)
print(event_dict)
print(events_from_annot[:5])

mapping = {1: 'auditory/left', 2: 'auditory/right', 3: 'visual/left', 
		   4: 'visual/right', 5: 'smiley', 32: 'buttonpress'}
onsets = events[:, 0] / raw.info['sfreq']
durations = np.zeros_like(onsets)
descriptions = [mapping[event_id] for event_id in events[:, 2]]
annot_from_events = mne.Annotations(onset=onsets, duration=durations, 
								   description=descriptions, 
								   orig_time=raw.info['meas_date'])
raw.set_annotations(annot_from_events)
raw.plot(start=5, duration=5)


plt.show()
