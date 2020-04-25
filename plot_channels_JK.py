# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:49:01 2020

@author: spork
"""

import matplotlib.pyplot as plt
from scipy.io import loadmat

from mne.viz import plot_alignment, snapshot_brain_montage
from pyoptical.utils import boxy2mne
import numpy as np
import mne

###data files###
boxy_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311a.001"
mtg_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311_good.mtg"
coord_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311.elp"

###process data###
raw_data = boxy2mne(boxy_file=boxy_file, mtg_file=mtg_file, coord_file=coord_file)

###get channel coordinates and labels for a few channels###
chan_coords = np.asarray([x['loc'][0:3] for x in raw_data.info['chs'][0:64]])
chan_names = raw_data.info['ch_names'][0:64]
ch_pos = dict(zip(chan_names,chan_coords))

###create our montage and info objects###
montage = mne.channels.make_dig_montage(ch_pos=ch_pos,coord_frame='head')
info = mne.create_info(chan_names,1000, 'eeg').set_montage(montage)

###plot the data###
###this bit is taken from the "working with ECoG Data' tutorial###
###but used our channels and coords from above###
subjects_dir = mne.datasets.sample.data_path() + '/subjects'
fig = plot_alignment(info, subject='sample', subjects_dir=subjects_dir,
                     surfaces=['pial'])
mne.viz.set_3d_view(fig, 200, 70)
