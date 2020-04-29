import os.path as op
import mne
from mne.datasets import sample
data_path = sample.data_path()

# the raw file containing the channel location + types
raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
# The paths to Freesurfer reconstructions
subjects_dir = data_path + '/subjects'
subject = 'sample'

# mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir, 
# 				brain_surfaces='white', orientation='coronal')


trans = data_path + '/MEG/sample/sample_audvis_raw-trans.fif'

info = mne.io.read_info(raw_fname)

# mne.viz.plot_alignment(info, trans, subject=subject, dig=True, 
# 						meg=['helmet', 'sensors'], subjects_dir=subjects_dir, 
# 						surfaces='brain')

src = mne.setup_source_space(subject, spacing='oct6', add_dist='patch',
							subjects_dir=subjects_dir)

fig = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir, 
							surfaces='white', coord_frame='head',
							src=src)
mne.viz.set_3d_view(fig, aximuth=173.78, elevation=101.75,
					distance=0.30, focalpoint=(-0.03, -0.01, 0.03))