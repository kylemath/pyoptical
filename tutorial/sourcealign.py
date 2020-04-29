import os.path as op 
import numpy as np 
import mne
from mne.datasets import sample

print(__doc__)

data_path = sample.data_path()
subjects_dir = op.join(data_path, 'subjects')
raw_fname = op.join(data_path, 'MEG', 'sample', 'sample_audvis_raw.fif')
trans_fname = op.join(data_path, 'MEG', 'sample', 
					  'sample_audvis_raw-trans.fif')
raw = mne.io.read_raw_fif(raw_fname)
trans = mne.read_trans(trans_fname)
src = mne.read_source_spaces(op.join(subjects_dir, 'sample', 'bem', 
									'sample-oct-6-src.fif'))


# fig = mne.viz.plot_alignment(raw.info, trans=trans, subject='sample', 
# 							subjects_dir=subjects_dir, surfaces='head-dense', 
# 							show_axes=True, dig=True, eeg=[], meg='sensors', 
# 							coord_frame='meg')
# mne.viz.set_3d_view(fig, 45, 90, distance=0.6, focalpoint=(0., 0., 0.))
print('Distance from head origin to MEG origin: %0.1f mm'
	% (1000 * np.linalg.norm(raw.info['dev_head_t']['trans'][:3, 3])))
print('Distance from head origin to MRI origin: %0.1f mm'
	% (1000 * np.linalg.norm(trans['trans'][:3, 3])))
dists = mne.dig_mri_distances(raw.info, trans, 'sample', 
							  subjects_dir=subjects_dir)
print('Distance from %s digitized points to head surface: %0.1f mm'
	% (len(dists), 1000 * np.mean(dists)))

# mne.viz.plot_alignment(raw.info, trans=trans, subject='sample', src=src,
# 					   subjects_dir=subjects_dir, dig=True, 
# 					   surfaces=['head-dense', 'white'], coord_frame='meg')


# mne.gui.coregistration(subject='sample', subjects_dir=subjects_dir)

sphere = mne.make_sphere_model(info=raw.info, r0='auto', head_radius='auto')
src = mne.setup_volume_source_space(sphere=sphere, pos=10)
mne.viz.plot_alignment(
	raw.info, eeg=False, meg=False, bem=sphere, src=src, dig=True,
	surfaces=['brain', 'outer_skin'], coord_frame='meg', show_axes=True)