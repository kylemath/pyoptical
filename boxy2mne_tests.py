# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 09:15:39 2020

@author: spork
"""


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne
import mne
from mne.datasets import fetch_fsaverage
from mne.viz import set_3d_title, set_3d_view
import os
import os.path as op

path = os.getcwd()

boxy_file = os.path.join(path, 'data', 'emm0311a.001')
mtg_file = os.path.join(path, 'data', 'emm0311_good.mtg')
coord_file = os.path.join(path, 'data', 'emm0311.elp')  

raw_data = boxy2mne(boxy_file=boxy_file, mtg_file=mtg_file, coord_file=coord_file)

###grab only channels for each data type###
###get indices and labels for ac, dc, and ph###
types = raw_data.info['chan_data_type']
ac_indices = [i_index for i_index, x in enumerate(types) if x == "AC"]
dc_indices = [i_index for i_index, x in enumerate(types) if x == "DC"]
ph_indices = [i_index for i_index, x in enumerate(types) if x == "Ph"]
mrk_index = types.index('Markers')
ac_labels = [raw_data.info['ch_names'][idx] for idx in ac_indices]
dc_labels = [raw_data.info['ch_names'][idx] for idx in dc_indices]
ph_labels = [raw_data.info['ch_names'][idx] for idx in ph_indices]

###grab our data###
###second may be better since it will return a raw object###
ac_data, ac_times = raw_data.get_data(ac_indices, return_times=True)
dc_data, dc_times = raw_data.get_data(dc_indices, return_times=True)
ph_data, ph_times = raw_data.get_data(ph_indices, return_times=True)

###also grab marker data in two ways###
mrk_data, mrk_times = raw_data.get_data(['Markers'], return_times=True)

###plot our data###
raw_data.plot(n_channels = 5,duration = 500, scalings='auto', order = ac_indices)
raw_data.plot(n_channels = 5,duration = 500, scalings='auto', order = dc_indices)
raw_data.plot(n_channels = 5,duration = 500, scalings='auto', order = ph_indices)
raw_data.plot(n_channels = 1,duration = 500, order = [mrk_index])

###calculate our distances (should be the same across data types###)
dists_ac = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ac_indices)
dists_dc = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = dc_indices)
dists_ph = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ph_indices)

###get our events###
events = mne.find_events(raw_data, stim_channel='Markers')

###plot our channel locations###
###NOTE###
###so it seems that when we create our info struct in boxy2mne
###if we specify ch_types as 'eeg', coord_frame in plot_alignment below can be set to mri or head
###if ch_types is fnirs_raw, coord_frame will have to be to head, else the channels 
###will be above the head and in the wrong orientation (almost like the transform is not applied)
###in short, ch_types(eeg) and coord_frame(mri/head) = ch_types(fnirs_raw) and coord_frame(head)
###not really sure why since the transformation matrix is the same either way
###maybe this is just because fnirs functionality isn't as extensive as eeg yet?
subjects_dir = op.dirname(fetch_fsaverage())

fig = mne.viz.plot_alignment(
    # Plot options
    show_axes=True, dig='fiducials', surfaces='head', mri_fiducials=True,
    subject='fsaverage', subjects_dir=subjects_dir, info=raw_data.info,
    coord_frame='head',
    trans=raw_data.info['trans'],  # transform from head coords to fsaverage's MRI
    )
set_3d_view(figure=fig, azimuth=135, elevation=80)
