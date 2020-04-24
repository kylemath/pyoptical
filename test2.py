import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne
import mne

boxy_file = "data/emm0311a.001"
mtg_file = "data/emm0311_good.mtg"
coord_file = "data/emm0311.tol"
coord_file = "data/emm0311.elp"

raw_data = boxy2mne(boxy_file=boxy_file, mtg_file=mtg_file, coord_file=coord_file)

###grab only channels for each data type###
ch_list_ac = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'AC ' in chan['ch_name']])
ch_list_dc = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'DC ' in chan['ch_name']])
ch_list_ph = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs'] if 'Ph ' in chan['ch_name']])
ch_list_all = np.asarray([chan['scanno']-1 for chan in raw_data.info['chs']])

###plot our data###
raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_ac)
raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_dc)
raw_data.plot(n_channels = 20,duration = 500, show_scrollbars = False, order = ch_list_ph)

###calculate our distances (should be the same across data types###)
dists_ac = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_ac)
dists_dc = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_dc)
dists_ph = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_ph)
dists_all = mne.preprocessing.nirs.source_detector_distances(raw_data.info, picks = ch_list_all)

###get our events###
events = mne.find_events(raw_data, stim_channel='Markers')