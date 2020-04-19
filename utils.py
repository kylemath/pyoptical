# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:46:32 2020

@author: spork
"""

# =============================================================================
# so channels in the mne example are source-detector pairs (similar to nomad)
# but I'm unclear what the coordinates refer to, maybe has coords for both
# =============================================================================
# =============================================================================
# so mne.create_info will create an info object for the optical data
# requires the following variables:
#     ch_names = list of strings containing channel names
#     sfreq = sample rate
#     ch_types = channel type, doesn't seem to support raw optical, leave empty
#     montage = can be a string or list containing channel positions
#     verbose = I assume for logging stuff
# =============================================================================
    
# =============================================================================
# so we currently load the participant montage and their tol info
# montage file contains (likely) a subset of the channels in the tol file
# so what we need to do if compare our montage channels and find the 
# coordinates from the tol
# =============================================================================

import mne

def boxy2mne(mtg_file,tol_file):
    ###load .mtg files###
    chan_num = []
    source_label = []
    detect_label = []
    chan_wavelength = []
    chan_modulation = []
    
    with open(mtg_file,'r') as data:
        for i_ignore in range(2):
            next(data)
        for i_line in data:
            chan1, chan2, source, detector, wavelength, modulation = i_line.split()
            chan_num.append(chan1)
            source_label.append(source)
            detect_label.append(detector)
            chan_wavelength.append(wavelength)
            chan_modulation.append(modulation)
    
    ###read .tol file###
    chan_label = []
    coords = []
    with open(tol_file,'r') as data:
        for i_line in data:
            label, X, Y, Z = i_line.split()
            chan_label.append(label)
            coords.append([X,Y,Z])
        
    # unique_wavelengths = set(chan_wavelength)
    source_coords = []
    for i_chan in source_label:
        if i_chan in chan_label:
            chan_index = chan_label.index(i_chan)
            source_coords.append(coords[chan_index])
            
    detect_coords = []
    for i_chan in detect_label:
        if i_chan in chan_label:
            chan_index = chan_label.index(i_chan)
            detect_coords.append(coords[chan_index])
        
    chan_coords = []
    chan_labels = []
    for i_coord in range(len(source_coords)):
        chan_coords.append(source_coords[i_coord] + detect_coords[i_coord])
        chan_labels.append(source_label[i_coord] + '-' + detect_label[i_coord])
        
    srate = 39.0625
    
    info = mne.create_info(chan_labels,srate)
    print(info)

    for i_chan in range(len(chan_labels)):
        for i_coord in range(3):
            info['chs'][i_chan]['loc'][3+i_coord] = float(chan_coords[i_chan][i_coord])
            info['chs'][i_chan]['loc'][6+i_coord] = float(chan_coords[i_chan][3 + i_coord])
            
    # test['chs'][0]['loc'][3]
    # chan_coords[0][0]
    picks = [x for x in range(len(chan_labels))]
    dists = mne.preprocessing.nirs.source_detector_distances(info, picks = picks)
    
    return dists
    