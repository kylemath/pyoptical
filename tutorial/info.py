import os
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
									'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
print(raw.info)

info = mne.io.read_info(sample_data_raw_file)
# print(info)

# print(info.keys())

# print(
# 	mne.pick_channels(info['ch_names'], include=['MEG 0312', 'EEG 005'])
# 	)	
# print(
# 	mne.pick_channels(info['ch_names'], include=[],
# 					  exclude=['MEG 0312', 'EEG 005'])
# 	)

# print(mne.pick_types(info, meg=False, eeg=True, exclude=[]))

picks = (25, 76, 77, 319)
print([mne.channel_type(info, x) for x in picks])

ch_idx_by_type = mne.channel_indices_by_type(info)
print(ch_idx_by_type)
print(ch_idx_by_type['eog'])