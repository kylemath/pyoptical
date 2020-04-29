# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 10:19:03 2020

@author: spork
"""


from utils import boxy2mne
import numpy as np
import mne

import pandas as pd
from mne.coreg import coregister_fiducials
from mne.io.meas_info import read_fiducials
from mne.datasets import fetch_fsaverage
from mne.viz import set_3d_title, set_3d_view
import os.path as op
import os

path = os.getcwd()

boxy_file = os.path.join(path, 'data', 'emm0311a.001')
mtg_file = os.path.join(path, 'data', 'emm0311_good.mtg')
# coord_file = os.path.join(path, 'data', 'emm0311.tol') 
coord_file = os.path.join(path, 'data', 'emm0311.elp')  

raw_data = boxy2mne(boxy_file=boxy_file, mtg_file=mtg_file, coord_file=coord_file)

subjects_dir = op.dirname(fetch_fsaverage())

fig = mne.viz.plot_alignment(
    # Plot options
    show_axes=True, dig='fiducials', surfaces='head', mri_fiducials=True,
    subject='fsaverage', subjects_dir=subjects_dir, info=raw_data.info,
    coord_frame='mri',
    trans=raw_data.info['trans'],  # transform from head coords to fsaverage's MRI
    )
set_3d_view(figure=fig, azimuth=135, elevation=80)