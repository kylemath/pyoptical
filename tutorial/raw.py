import os
import numpy as np 
import matplotlib.pyplot as plt 
import mne

plotAll = False

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
									'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)

print(raw)

raw.crop(tmax=60)
raw.load_data()

n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
n_chan = len(ch_names)

print('the (cropped) sample data object has {} time samples and {} channels.'
	.format(n_time_samps, n_chan))
print('The last time sample is at {} seconds.'.format(time_secs[-1]))
print('The first few channel names are {}.'.format(', '.join(ch_names[:3])))
print()

print('bad channels:', raw.info['bads'])
print(raw.info['sfreq'], 'Hz')
print(raw.info['description'], '\n')

print(raw.info)

print(raw.time_as_index(20.0001))
print(raw.time_as_index([20, 30, 40]), '\n')
print(np.diff(raw.time_as_index([1, 2, 3, 4, 5, 6, 7])))

eeg_and_eog = raw.copy().pick_types(meg=False, eeg=True, eog=True)
print(len(raw.ch_names), '->', len(eeg_and_eog.ch_names))

raw_temp = raw.copy()
print('Number of channels in raw_temp:')
print(len(raw_temp.ch_names), end=' -> drop two -> ')
raw_temp.drop_channels(['EEG 037', 'EEG 059'])
print(len(raw_temp.ch_names), end=' -> pick three -> ')
raw_temp.pick_channels(['MEG 1811', 'EEG 017', 'EOG 061'])
print(len(raw_temp.ch_names))


channel_names = ['EOG 061', 'EEG 003', 'EEG 002', 'EEG 001']
eog_and_frontal_eeg = raw.copy().reorder_channels(channel_names)
print(eog_and_frontal_eeg.ch_names)

raw.rename_channels({'EOG 061': 'blink detector'})

print(raw.ch_names[-3:])
channel_renaming_dict = {name: name.replace(' ', '_') for name in raw.ch_names}
raw.rename_channels(channel_renaming_dict)
print(raw.ch_names[-3:])

raw.set_channel_types({'EEG_001': 'eog'})
print(raw.copy().pick_types(meg=False, eog=True).ch_names)

raw_selection = raw.copy().crop(tmin=10, tmax=12.5)
print(raw_selection)
print(raw_selection.times[:3])

print(raw_selection.times.min(), raw_selection.times.max())
raw_selection.crop(tmin=1)
print(raw_selection.times.min(), raw_selection.times.max())


raw_selection1 = raw.copy().crop(tmin=30, tmax=30.1)
raw_selection2 = raw.copy().crop(tmin=40, tmax=41.1)
raw_selection3 = raw.copy().crop(tmin=50, tmax=51.3)
raw_selection1.append([raw_selection2, raw_selection3])
print(raw_selection1.times.min(), raw_selection1.times.max())




print('----------------')

sampling_freq = raw.info['sfreq']
start_stop_seconds = np.array([11, 13])
start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
channel_index = 0
raw_selection = raw[channel_index, start_sample:stop_sample]
print(raw_selection)


if plotAll: 
	x = raw_selection[1]
	y = raw_selection[0].T 
	plt.plot(x,y)

channel_names = ['MEG_0712', 'MEG_1022']
two_meg_chans = raw[channel_names, start_sample:stop_sample]

if plotAll:
	y_offset = np.array([5e-11, 0])
	x = two_meg_chans[1]
	y = two_meg_chans[0].T + y_offset
	lines = plt.plot(x, y)
	plt.legend(lines, channel_names)

eeg_channel_indices = mne.pick_types(raw.info, meg=False, eeg=True)
eeg_data, times = raw[eeg_channel_indices]
print(eeg_data.shape)

data = raw.get_data()
print(data.shape)

data, times = raw.get_data(return_times=True)
print(data.shape)
print(times.shape)

first_channel_data = raw.get_data(picks=0)
eeg_and_eog_data = raw.get_data(picks=['eeg', 'eog'])
two_meg_chans_data = raw.get_data(picks=['MEG_0712', 'MEG_1022'], 
								start=1000, stop=2000)

print(first_channel_data.shape)
print(eeg_and_eog_data.shape)
print(two_meg_chans_data.shape)

data = raw.get_data()
np.save(file='my_data.npy', arr=data)


print('-----------')
start_sample, stop_sample = raw.time_as_index([10, 13])
df = raw.to_data_frame(picks=['eeg'], start=start_sample, stop=stop_sample)
print(df.head())






plt.show()