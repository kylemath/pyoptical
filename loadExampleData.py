import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import os
from itertools import compress
import mne

# Example from https://mne.tools/dev/auto_tutorials/preprocessing/plot_70_fnirs_processing.html

fnirs_data_folder = mne.datasets.fnirs_motor.data_path()
fnirs_raw_dir = os.path.join(fnirs_data_folder, 'Participant-1')

# MNE raw object - https://mne.tools/stable/generated/mne.io.Raw.html
raw_intensity = mne.io.read_raw_nirx(fnirs_raw_dir, verbose=True).load_data()
print("Raw imported data file: ", raw_intensity)
print("Example sensor name: ", raw_intensity.info.ch_names[1])
print("Example sensor information: ", raw_intensity.info['chs'][2])

# raw_intensity.plot_sensors()


## Selecting channels 

picks = mne.pick_types(raw_intensity.info, meg=False, fnirs=True)
print("Channels to pull out: ", picks)

dists = mne.preprocessing.nirs.source_detector_distances(
	raw_intensity.info, picks=picks)
print("Channel distances: ", dists)

raw_intensity.pick(picks[dists > 0.01])
print("Long enough channels: ", raw_intensity)

# raw_intensity.plot(n_channels=len(raw_intensity.ch_names), 
# 					duration=500, show_scrollbars=False)
# plt.show()

## Converting to optical density

raw_od = mne.preprocessing.nirs.optical_density(raw_intensity)
# raw_od.plot(n_channels=len(raw_od.ch_names),
# 			duration=500, show_scrollbars=False)
# plt.show()

## Evaluating the quality of the data

sci = mne.preprocessing.nirs.scalp_coupling_index(raw_od)
# fig, ax = plt.subplots()
# ax.hist(sci)
# ax.set(xlabel='Scalp Coupling Index', ylabel='Count', xlim=[0, 1])
# plt.show()

## Converting from optical density to haemoglobin

raw_haemo = mne.preprocessing.nirs.beer_lambert_law(raw_od)
# raw_haemo.plot(n_channels=len(raw_haemo.ch_names),
# 				duration=500, show_scrollbars=False)
# plt.show()

## Remove heart rate from signal

# fig = raw_haemo.plot_psd(average=True)
# fig.suptitle('Before filtering', weight='bold', size='x-large')
# fig.subplots_adjust(top=0.88)
raw_haemo = raw_haemo.filter(0.05, 0.7, h_trans_bandwidth=0.2, 
							l_trans_bandwidth=0.02)
# fig = raw_haemo.plot_psd(average=True)
# fig.suptitle('After filtering', weight='bold', size='x-large')
# fig.subplots_adjust(top=0.88)

## Extract Epochs

events, _ = mne.events_from_annotations(raw_haemo, event_id={'1.0': 1,
															 '2.0': 2,
															 '3.0': 3})
event_dict = {'Control': 1, 'Tapping/Left': 2, 'Tapping/Right': 3}
# fig = mne.viz.plot_events(events, event_id=event_dict, 
# 						sfreq=raw_haemo.info['sfreq'])
# fig.subplots_adjust(right=0.7)

reject_criteria = dict(hbo=80e-6)
tmin, tmax = -5, 15

epochs = mne.Epochs(raw_haemo, events, event_id=event_dict, 
					tmin=tmin, tmax=tmax, 
					reject=reject_criteria, reject_by_annotation=True, 
					proj=True, baseline=(None, 0), preload=True,
					detrend=None, verbose=True)

# plt.show()

# epochs.plot_drop_log()

## View consistency of responses over trials

# epochs['Tapping'].plot_image(combine='mean', vmin=-15, vmax=15,
# 				 			 ts_args=dict(ylim=dict(hbo=[-15, 15],
# 				 			 						hbr=[-15, 15])))

# epochs['Control'].plot_image(combine='mean', vmin=-15, vmax=15,
# 							ts_args=dict(ylim=dict(hbo=[-15, 15],
# 												   hbr=[-15, 15])))

## View consistency of response accross channels

# clims = dict(hbo=[-10, 10], hbr=[-10, 10])
# epochs['Control'].average().plot_image(clim=clims)
# epochs['Tapping'].average().plot_image(clim=clims)

## Plot standard fNIRS response image

# evoked_dict = {'Tapping/HbO': epochs['Tapping'].average(picks='hbo'),
# 			   'Tapping/HbR': epochs['Tapping'].average(picks='hbr'),
# 			   'Control/HbO': epochs['Control'].average(picks='hbo'),
# 			   'Control/HbR': epochs['Control'].average(picks='hbr')}

# for condition in evoked_dict: 
# 	evoked_dict[condition].rename_channels(lambda x: x[:-4])

# color_dict = dict(HbO='r', HbR='b')
# styles_dict = dict(Control=dict(linestyle='dashed'))

# mne.viz.plot_compare_evokeds(evoked_dict, combine="mean", ci=0.95,
# 							colors=color_dict, styles=styles_dict)

## View topographic representation of activity

# times = np.arange(-3.5, 13.2, 3.0)
# topomap_args = dict(extrapolate='local')
# epochs['Tapping'].average(picks='hbo').plot_joint(
# 	times=times, topomap_args=topomap_args)

## Comparing tapping of left and right hands

# topomap_args = dict(extrapolate='local')
# times = np.arange(4.0, 11.0, 1.0)
# epochs['Tapping/Left'].average(picks='hbo').plot_topomap(
# 		times=times, **topomap_args)
# epochs['Tapping/Right'].average(picks='hbo').plot_topomap(
# 		times=times, **topomap_args)

## Compare conditions

topomap_args = dict(extrapolate='local')

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(9, 5))
vmin, vmax, ts = -8, 8, 9.0

evoked_left = epochs['Tapping/Left'].average()
evoked_right = epochs['Tapping/Right'].average()

evoked_left.plot_topomap(ch_type='hbo', times=ts, axes=axes[0, 0],
						vmin=vmin, vmax=vmax, colorbar=False,
						**topomap_args)
evoked_left.plot_topomap(ch_type='hbr', times=ts, axes=axes[1, 0],
						vmin=vmin, vmax=vmax, colorbar=False,
						**topomap_args)
evoked_right.plot_topomap(ch_type='hbo', times=ts, axes=axes[0, 1], 
						vmin=vmin, vmax=vmax, colorbar=False,
						**topomap_args)
evoked_right.plot_topomap(ch_type='hbr', times=ts, axes=axes[1, 1], 
						vmin=vmin, vmax=vmax, colorbar=False,
						**topomap_args)

evoked_diff = mne.combine_evoked([evoked_left, -evoked_right], weights='equal')

evoked_diff.plot_topomap(ch_type='hbo', times=ts, axes=axes[0, 2],
						vmin=vmin, vmax=vmax,
						**topomap_args)
evoked_diff.plot_topomap(ch_type='hbr', times=ts, axes=axes[1, 2], 
						vmin=vmin, vmax=vmax, 
						**topomap_args)

for column, condition in enumerate(
		['Tapping Left', 'Tapping Right', 'Left-Right']):
	for row, chroma in enumerate(['HbO', 'HbR']):
		axes[row, column].set_title('{}: {}'.format(chroma, condition))

plt.show()