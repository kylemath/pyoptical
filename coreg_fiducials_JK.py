# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:30:07 2020

@author: spork
"""


from mne.channels import compute_native_head_t, read_custom_montage
from mne.channels.montage import  transform_to_head
from mne.viz import set_3d_title, set_3d_view
from mne.transforms import apply_trans
from mne.viz import plot_alignment
import os.path as op
import mne
import numpy as np
import pandas as pd
from mne.coreg import coregister_fiducials
from mne.io.meas_info import read_fiducials
from mne.datasets import fetch_fsaverage
from pyoptical.utils import boxy2mne


# from configparser import ConfigParser, RawConfigParser
# import glob as glob
# import re as re

# import numpy as np

# from ..base import BaseRaw
# from ..constants import FIFF
# from ..meas_info import create_info, _format_dig_points
# from ...annotations import Annotations
# from ...transforms import apply_trans, _get_trans
# from ...utils import logger, verbose, fill_doc
# import pdb
from mne.transforms import apply_trans, _get_trans

# boxy_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311a.001"
# mtg_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311_good.mtg"
coord_file = "C:\\Users\\spork\\pyoptical\\data\\emm0311.elp"

# boxy_file = "data/emm0311a.001"
# mtg_file = "data/emm0311_good.mtg"
# coord_file = "data/emm0311.elp"

srate = 39.0625

# =============================================================================
#     read source and electrode locations from .mtg and .tol/.elp files
#     taken from boxy2mne
# =============================================================================

###check if we are given a .tol or .elp file###
chan_label = []
coords = []
fiducial_coords = []
if coord_file[-3:] == 'elp':
    get_label = 0
    get_coords = 0
    ###load and read .elp file###
    with open(coord_file,'r') as data:
        for i_line in data:
            ###first let's get our fiducial coordinates###
            if '%F' in i_line:
                fiducial_coords.append(i_line.split()[1:])
            ###check where sensor info starts###
            if '//Sensor name' in i_line:
                get_label = 1
            elif get_label == 1:
                ###grab the part after '%N' for the label###
                label = i_line.split()[1]
                chan_label.append(label)
                get_label = 0
                get_coords = 1
            elif get_coords == 1:
                X, Y, Z = i_line.split()
                coords.append([float(X),float(Y),float(Z)])
                get_coords = 0
elif coord_file[-3:] == 'tol':
    ###load and read .tol file###
    with open(coord_file,'r') as data:
        for i_line in data:
            label, X, Y, Z = i_line.split()
            chan_label.append(label)
            ###convert coordinates from mm to m##
            coords.append([(float(X)*0.001),(float(Y)*0.001),(float(Z)*0.001)])
   
fiducial_coords[0] = np.asarray([float(x) for x in fiducial_coords[0]])
fiducial_coords[1] = np.asarray([float(x) for x in fiducial_coords[1]])
fiducial_coords[2] = np.asarray([float(x) for x in fiducial_coords[2]])

# =============================================================================
# METHOD 1
# =============================================================================
###put labels and coords in a dict###
all_chan = dict(zip(chan_label,coords))

###make our montage###
montage = mne.channels.make_dig_montage(ch_pos=all_chan,coord_frame='unknown',
                                        nasion = fiducial_coords[0],
                                        lpa = fiducial_coords[1], 
                                        rpa = fiducial_coords[2])

###create our info struct###
info = mne.create_info(chan_label,srate, 'eeg').set_montage(montage)

subjects_dir = op.dirname(fetch_fsaverage())

fiducials = read_fiducials(subjects_dir + '\\fsaverage\\bem\\fsaverage-fiducials.fif')
trans = coregister_fiducials(info, fiducials[0], tol=0.02)

fig = mne.viz.plot_alignment(
    # Plot options
    show_axes=True, dig='fiducials', surfaces='head', mri_fiducials=True,
    subject='fsaverage', subjects_dir=subjects_dir, info=info,
    coord_frame='mri',
    trans=trans,  # transform from head coords to fsaverage's MRI
    )
set_3d_view(figure=fig, azimuth=135, elevation=80)

# =============================================================================
# METHOD 2 (FROM nirx.py)
# =============================================================================
mri_head_t, _ = _get_trans('fsaverage', 'mri', 'head')
# src_locs = apply_trans(mri_head_t, src_locs)
# det_locs = apply_trans(mri_head_t, det_locs)
# ch_locs = apply_trans(mri_head_t, ch_locs)
coords = apply_trans(mri_head_t,coords)
fiducial_coords = apply_trans(mri_head_t,fiducial_coords)
# for chan in info['dig']:
#     chan['r'] = apply_trans(mri_head_t,chan['r'])

###put labels and coords in a dict###
all_chan = dict(zip(chan_label,coords))

###make our montage###
montage = mne.channels.make_dig_montage(ch_pos=all_chan,coord_frame='unknown',
                                        nasion = fiducial_coords[0],
                                        lpa = fiducial_coords[1], 
                                        rpa = fiducial_coords[2])

###create our info struct###
info = mne.create_info(chan_label,srate, ch_types='eeg').set_montage(montage)
# info.update(dig=montage.dig)

subjects_dir = op.dirname(fetch_fsaverage())

fig = mne.viz.plot_alignment(
    # Plot options
    show_axes=True, dig='fiducials', surfaces='head', mri_fiducials=True,
    subject='fsaverage', subjects_dir=subjects_dir, info=info,
    coord_frame='mri',
    trans='fsaverage',
    )
set_3d_view(figure=fig, azimuth=135, elevation=80)

# =============================================================================
# 
# =============================================================================