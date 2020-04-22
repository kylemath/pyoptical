# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:46:32 2020

@author: spork
"""

import mne
import numpy as np
import pandas as pd

def boxy2mne(boxy_file,mtg_file,tol_file):
    
# =============================================================================
#     ready raw data from boxy file
# =============================================================================
    ###this keeps track of the line we're on###
    ###mostly to know the start and stop of data (probably an easier way)###
    line_num = 0
    
    ###load and read data to get some meta information###
    ###there is alot of information at the beginning of a file###
    ###but this only grabs some of it###
    with open(boxy_file,'r') as data:
        for i_line in data:
            line_num += 1
            if '#DATA ENDS' in i_line:
                end_line = line_num - 1
                break
            if 'Detector Channels' in i_line:
                detect_num = int(i_line.rsplit(' ')[0])
            elif 'External MUX Channels' in i_line:
                mux_num = int(i_line.rsplit(' ')[0])
            elif 'Auxiliary Channels' in i_line:
                aux_num = int(i_line.rsplit(' ')[0])
            elif 'Waveform (CCF) Frequency (Hz)' in i_line:
                ccf_ha = float(i_line.rsplit(' ')[0])
            elif 'Update Rate (Hz)' in i_line:
                srate = float(i_line.rsplit(' ')[0])
            elif 'Updata Rate (Hz)' in i_line:
                srate = float(i_line.rsplit(' ')[0])
            elif '#DATA BEGINS' in i_line:
                start_line = line_num

    ###now let's go through and parse our raw data###  
    raw_data = pd.read_csv(boxy_file, skiprows=start_line, sep='\t')
    
    ###only go up to 'J' since that the max number of detectors we can have###
    ###for now anyway###
    detectors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z']
    data_types = ['AC','DC','Ph']
    sources = np.arange(1,mux_num+1,1)
    
    ###since we can save boxy files in two different styles###
    ###this will check to see which style the data is saved###
    ###seems to also work with older boxy files###
    if 'exmux' in raw_data.columns:
        filetype = 1
        
        ###drop the last line as this is just '#DATA ENDS'###
        raw_data = raw_data.drop([len(raw_data)-1])
        
        ###store some extra info###
        record = raw_data['record'].to_numpy()
        exmux = raw_data['exmux'].to_numpy()
        
        ###make some empty variables to store our data###
        raw_ac = np.zeros((detect_num*mux_num,int(len(raw_data)/mux_num)))
        raw_dc = np.zeros((detect_num*mux_num,int(len(raw_data)/mux_num)))
        raw_ph = np.zeros((detect_num*mux_num,int(len(raw_data)/mux_num)))
    else:
        filetype = 2
        
        ###drop the last line as this is just '#DATA ENDS'###
        ###also drop the first line since this is empty###
        raw_data = raw_data.drop([0,len(raw_data)-1])
        
        ###make some empty variables to store our data###
        raw_ac = np.zeros(((detect_num*mux_num),len(raw_data)))
        raw_dc = np.zeros(((detect_num*mux_num),len(raw_data)))
        raw_ph = np.zeros(((detect_num*mux_num),len(raw_data)))
    
    ###store some extra data, might not need these though###
    time = raw_data['time'].to_numpy()
    group = raw_data['group'].to_numpy()
    step = raw_data['step'].to_numpy()
    mark = raw_data['mark'].to_numpy()
    flag = raw_data['flag'].to_numpy()
    aux1 = raw_data['aux-1'].to_numpy()
    digaux = raw_data['digaux'].to_numpy()
    bias = np.zeros((detect_num,len(raw_data)))
    
    ###loop through detectors###
    for i_detect in detectors[0:detect_num]:
        
        ###older boxy files don't seem to keep track of detector bias###
        if 'bias-A' in raw_data.columns:
            bias[detectors.index(i_detect),:] = raw_data['bias-' + i_detect].to_numpy()
            
        ###loop through data types###
        for i_data in data_types:
            
            ###loop through sources###
            for i_source in sources:
                
                ###where to store our data###
                index_loc = detectors.index(i_detect)*mux_num + (i_source-1)
                
                ###need to treat our filetypes differently###
                if filetype == 1:
                    
                    ###filetype saves timepoints in groups###
                    ###this should account for that###
                    time_points = np.arange(i_source-1,int(record[-1])*mux_num,mux_num)
                    
                    ###determine which channel to look for###
                    channel = i_detect + '-' + i_data
                    
                    ###save our data based on data type###
                    if data_types.index(i_data) == 0:
                        raw_ac[index_loc,:] = raw_data[channel][time_points].to_numpy()
                    elif data_types.index(i_data) == 1:
                        raw_dc[index_loc,:] = raw_data[channel][time_points].to_numpy()
                    elif data_types.index(i_data) == 2:
                        raw_ph[index_loc,:] = raw_data[channel][time_points].to_numpy()
                else:
                    
                    ###determine which channel to look for###
                    channel = i_detect + '-' + i_data + str(i_source)
                    
                    ###save our data based on data type###
                    if data_types.index(i_data) == 0:
                        raw_ac[index_loc,:] = raw_data[channel].to_numpy()
                    elif data_types.index(i_data) == 1:
                        raw_dc[index_loc,:] = raw_data[channel].to_numpy()
                    elif data_types.index(i_data) == 2:
                        raw_ph[index_loc,:] = raw_data[channel].to_numpy()
    
# =============================================================================
#     read source and electrode locations from .mtg and .tol files
# =============================================================================
    
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
        
# =============================================================================
#     so this has been added because all the .mtg files I have contain
#     multiple blocks/data files, so a montage file then contains more channels 
#     than a single boxy data file. this function is only designed to take
#     a single boxy file. the below code is just a work around for testing.
# =============================================================================
    if len(chan_labels) != len(raw_ac):
        chan_labels = chan_labels[0:len(raw_ac)]  
# =============================================================================
#         
# =============================================================================
    
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
    
    ac = mne.io.RawArray(raw_ac, info)
    dc = mne.io.RawArray(raw_dc, info)
    ph = mne.io.RawArray(raw_ph, info)
    
    all_data = {'AC': ac, 'DC':dc, 'Ph':ph, 'Dist':dists}
    
    return all_data
    