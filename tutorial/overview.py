import os
import numpy as np 
import mne
import matplotlib.pyplot as plt 



sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 
									'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
print(raw.info)

plotAll = True

# raw.plot_psd(fmax=50)
# plt.show(block=True)
# raw.plot(duration=5, n_channels=30)
# plt.show()

ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)
ica.exclude = [1, 2]
if plotAll:
	ica.plot_properties(raw, picks=ica.exclude)

orig_raw = raw.copy()
raw.load_data()
ica.apply(raw)

# show some frontal channels to clearly illustrate the artifact removal
chs = ['MEG 0111', 'MEG 0121', 'MEG 0131', 'MEG 0211', 'MEG 0221', 'MEG 0231',
       'MEG 0311', 'MEG 0321', 'MEG 0331', 'MEG 1511', 'MEG 1521', 'MEG 1531',
       'EEG 001', 'EEG 002', 'EEG 003', 'EEG 004', 'EEG 005', 'EEG 006',
       'EEG 007', 'EEG 008']
chan_idxs = [raw.ch_names.index(ch) for ch in chs]

if plotAll: 
	orig_raw.plot(order=chan_idxs, start=12, duration=10)
	raw.plot(order=chan_idxs, start=12, duration=10)

events = mne.find_events(raw, stim_channel='STI 014')
print(events[:5])

event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3, 
			'visual/right': 4, 'smiley': 5, 'buttonpress': 32}

if plotAll:
	fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info['sfreq'],
						first_samp=raw.first_samp)

reject_criteria = dict(mag=4000e-15,
					   grad=4000e-13,
					   eeg=150e-6,
					   eog=250e-6)
epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax= 0.5,
					reject=reject_criteria, preload=True)

conds_we_care_about = ['auditory/left', 'auditory/right', 
						'visual/left', 'visual/right']
epochs.equalize_event_counts(conds_we_care_about)
aud_epochs = epochs['auditory']
vis_epochs = epochs['visual']
del raw, epochs

if plotAll:
	aud_epochs.plot_image(picks=['MEG 1332', 'EEG 021'])

frequencies = np.arange(7, 30, 3)
power = mne.time_frequency.tfr_morlet(aud_epochs, n_cycles=2, return_itc=False, 
									  freqs=frequencies, decim=3)
if plotAll: 
	power.plot(['EEG 021'])	
	print(power)						

aud_evoked = aud_epochs.average()
vis_evoked = vis_epochs.average()

if plotAll: 
	mne.viz.plot_compare_evokeds(dict(auditory=aud_evoked, visual=vis_evoked), 
							legend='upper left', show_sensors='upper right')
	aud_evoked.plot_joint(picks='meg')
	aud_evoked.plot_topomap(times=[0., 0.08, 0.1, 0.12, 0.2], ch_type='eeg')

evoked_diff = mne.combine_evoked([aud_evoked, -vis_evoked], weights='equal')

if plotAll:
	evoked_diff.pick_types('mag').plot_topo(color='r', legend=False)


# load inverse operator
inverse_operator_file = os.path.join(sample_data_folder, 'MEG', 'sample',
									'sample_audvis-meg-oct-6-meg-inv.fif')
inv_operator = mne.minimum_norm.read_inverse_operator(inverse_operator_file)
# set signal-to-noise ratio (SNR) to compute regularization parameter (λ²)	
snr = 3.
lambda2 = 1. / snr ** 2
# generate the source time course (STC)
stc = mne.minimum_norm.apply_inverse(vis_evoked, inv_operator, 
									lambda2=lambda2, 
									method='MNE')

# path to subject's MRI files
subjects_dir = os.path.join(sample_data_folder, 'subjects')
# plot
print(subjects_dir)
if plotAll: 
	stc.plot(initial_time=0.1, hemi='split', views=['lat', 'med'], 
			subjects_dir=subjects_dir)







plt.show()