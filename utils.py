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
    
    ###need to have function determine sampling rate automatically, eventually
    srate = 39.0625
    
    ###set up some variables###
    chan_num = []
    source_label = []
    detect_label = []
    chan_wavelength = []
    chan_modulation = []
    
    ###load and read each line of the .mtg file###
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
    
    ###load and read .tol file###
    chan_label = []
    coords = []
    with open(tol_file,'r') as data:
        for i_line in data:
            label, X, Y, Z = i_line.split()
            chan_label.append(label)
            ###convert coordinates from mm to m##
            coords.append([(float(X)*0.001),(float(Y)*0.001),(float(Z)*0.001)])
        
    ###get coordinates for sources###
    source_coords = []
    for i_chan in source_label:
        if i_chan in chan_label:
            chan_index = chan_label.index(i_chan)
            source_coords.append(coords[chan_index])
            
    ###get coordinates for detectors###
    detect_coords = []
    for i_chan in detect_label:
        if i_chan in chan_label:
            chan_index = chan_label.index(i_chan)
            detect_coords.append(coords[chan_index])
        
    ###combine coordinates and label our channels###
    chan_coords = []
    chan_labels = []
    for i_coord in range(len(source_coords)):
        chan_coords.append(source_coords[i_coord] + detect_coords[i_coord])
        chan_labels.append(source_label[i_coord] + '_' + detect_label[i_coord]
                           + ' ' + chan_wavelength[i_coord])
    
    ###create info structure###
    info = mne.create_info(chan_labels,srate)

    ###place out coordinates and wavelengths for each channel###
    for i_chan in range(len(chan_labels)):
        for i_coord in range(3):
            info['chs'][i_chan]['loc'][3+i_coord] = float(chan_coords[i_chan][i_coord])
            info['chs'][i_chan]['loc'][6+i_coord] = float(chan_coords[i_chan][3 + i_coord])
        info['chs'][i_chan]['loc'][9] = float(chan_wavelength[i_coord])
            
    ###use all channels and get our source-detector distances###
    picks = [x for x in range(len(chan_labels))]
    dists = mne.preprocessing.nirs.source_detector_distances(info, picks = picks)
    
    return info, dists
    