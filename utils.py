# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 09:53:58 2020

@author: spork
"""

import mne
import numpy as np
import pandas as pd
from mne.coreg import coregister_fiducials
from mne.io.meas_info import read_fiducials
from mne.datasets import fetch_fsaverage
from mne.transforms import apply_trans
import os.path as op

def boxy2mne(*,boxy_file=None,mtg_file=None,coord_file=None):
    
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
                source_num = int(i_line.rsplit(' ')[0])
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
    
    ###detectors, sources, and data types###
    detectors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z']
    data_types = ['AC','DC','Ph']
    sources = np.arange(1,source_num+1,1)
    
    ###since we can save boxy files in two different styles###
    ###this will check to see which style the data is saved###
    ###seems to also work with older boxy files###
    if 'exmux' in raw_data.columns:
        filetype = 'non-parsed'
        
        ###drop the last line as this is just '#DATA ENDS'###
        raw_data = raw_data.drop([len(raw_data)-1])
        
        ###store some extra info###
        record = raw_data['record'].to_numpy()
        exmux = raw_data['exmux'].to_numpy()
        
        ###make some empty variables to store our data###
        raw_ac = np.zeros((detect_num*source_num,int(len(raw_data)/source_num)))
        raw_dc = np.zeros((detect_num*source_num,int(len(raw_data)/source_num)))
        raw_ph = np.zeros((detect_num*source_num,int(len(raw_data)/source_num)))
    else:
        filetype = 'parsed'
        
        ###drop the last line as this is just '#DATA ENDS'###
        ###also drop the first line since this is empty###
        raw_data = raw_data.drop([0,len(raw_data)-1])
        
        ###make some empty variables to store our data###
        raw_ac = np.zeros(((detect_num*source_num),len(raw_data)))
        raw_dc = np.zeros(((detect_num*source_num),len(raw_data)))
        raw_ph = np.zeros(((detect_num*source_num),len(raw_data)))
    
    ###store some extra data, might not need these though###
    time = raw_data['time'].to_numpy() if 'time' in raw_data.columns else []
    time = raw_data['time'].to_numpy() if 'time' in raw_data.columns else []
    group = raw_data['group'].to_numpy() if 'group' in raw_data.columns else []
    step = raw_data['step'].to_numpy() if 'step' in raw_data.columns else []
    mark = raw_data['mark'].to_numpy() if 'mark' in raw_data.columns else []
    flag = raw_data['flag'].to_numpy() if 'flag' in raw_data.columns else []
    aux1 = raw_data['aux-1'].to_numpy() if 'aux-1' in raw_data.columns else []
    digaux = raw_data['digaux'].to_numpy() if 'digaux' in raw_data.columns else []
    bias = np.zeros((detect_num,len(raw_data)))
    
    ###loop through detectors###
    for i_detect in detectors[0:detect_num]:
        
        ###older boxy files don't seem to keep track of detector bias###
        ###probably due to specific boxy settings actually###
        if 'bias-A' in raw_data.columns:
            bias[detectors.index(i_detect),:] = raw_data['bias-' + i_detect].to_numpy()
            
        ###loop through data types###
        for i_data in data_types:
            
            ###loop through sources###
            for i_source in sources:
                
                ###where to store our data###
                index_loc = detectors.index(i_detect)*source_num + (i_source-1)
                
                ###need to treat our filetypes differently###
                if filetype == 'non-parsed':
                    
                    ###filetype saves timepoints in groups###
                    ###this should account for that###
                    time_points = np.arange(i_source-1,int(record[-1])*source_num,source_num)
                    
                    ###determine which channel to look for###
                    channel = i_detect + '-' + i_data
                    
                    ###save our data based on data type###
                    if data_types.index(i_data) == 0:
                        raw_ac[index_loc,:] = raw_data[channel][time_points].to_numpy()
                    elif data_types.index(i_data) == 1:
                        raw_dc[index_loc,:] = raw_data[channel][time_points].to_numpy()
                    elif data_types.index(i_data) == 2:
                        raw_ph[index_loc,:] = raw_data[channel][time_points].to_numpy()
                elif filetype == 'parsed':
                    
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
#     read source and electrode locations from .mtg and .tol/.elp files
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
    
    ###check if we are given a .tol or .elp file###
    all_labels = []
    all_coords = []
    fiducial_coords = []
    if coord_file[-3:].lower() == 'elp'.lower():
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
                    all_labels.append(label)
                    get_label = 0
                    get_coords = 1
                elif get_coords == 1:
                    X, Y, Z = i_line.split()
                    all_coords.append([float(X),float(Y),float(Z)])
                    get_coords = 0
        for i_index in range(3):
            fiducial_coords[i_index] = np.asarray([float(x) for x in fiducial_coords[i_index]])
    elif coord_file[-3:] == 'tol':
        ###load and read .tol file###
        with open(coord_file,'r') as data:
            for i_line in data:
                label, X, Y, Z = i_line.split()
                all_labels.append(label)
                ###convert coordinates from mm to m##
                all_coords.append([(float(X)*0.001),(float(Y)*0.001),(float(Z)*0.001)])
        
    ###get coordinates for sources###
    source_coords = []
    for i_chan in source_label:
        if i_chan in all_labels:
            chan_index = all_labels.index(i_chan)
            source_coords.append(all_coords[chan_index])
            
    ###get coordinates for detectors###
    detect_coords = []
    for i_chan in detect_label:
        if i_chan in all_labels:
            chan_index = all_labels.index(i_chan)
            detect_coords.append(all_coords[chan_index])
            
    ###need to rename labels to make other functions happy###
    ###get our unique labels for sources and detectors###
    unique_source_labels = []
    unique_detect_labels = []
    [unique_source_labels.append(label) for label in source_label if label not in unique_source_labels]
    [unique_detect_labels.append(label) for label in detect_label if label not in unique_detect_labels]
    
    ###now let's label each channel in our data###
    ###data is channels X timepoint where the first source_num rows correspond to###
    ###the first detector, and each row within that group is a different source###
    ###should note that current .mtg files contain channels for multiple data files###
    ###going to move to have a single .mtg file per participant, condition, and montage###
    ###combine coordinates and label our channels###
    ###will label them based on ac, dc, and ph data###
    boxy_coords = []
    boxy_labels = []
    data_types = ['AC','DC','Ph']
    total_chans = detect_num*source_num
    for i_type in data_types:
        for i_coord in range(len(source_coords[0:total_chans])):
            boxy_coords.append(np.mean(
                np.vstack((source_coords[i_coord], detect_coords[i_coord])),
                axis=0).tolist() + source_coords[i_coord] + 
                detect_coords[i_coord] + [chan_wavelength[i_coord]] + [0] + [0])
            boxy_labels.append('S' + 
                                   str(unique_source_labels.index(source_label[i_coord])+1)
                                   + '_D' + 
                                   str(unique_detect_labels.index(detect_label[i_coord])+1) 
                                   + ' ' + chan_wavelength[i_coord] + ' ' + i_type)
    
    ###montage only wants channel coords, so need to grab those, convert to###
    ###array, then make a dict with labels###
    for i_chan in range(len(boxy_coords)):
        boxy_coords[i_chan] = np.asarray(boxy_coords[i_chan],dtype=np.float64) 
        
    for i_chan in range(len(all_coords)):
        all_coords[i_chan] = np.asarray(all_coords[i_chan],dtype=np.float64) 

    all_chan_dict = dict(zip(all_labels,all_coords))
    
    ###make our montage###
    montage_orig = mne.channels.make_dig_montage(ch_pos=all_chan_dict,coord_frame='head',
                                            nasion = fiducial_coords[0],
                                            lpa = fiducial_coords[1], 
                                            rpa = fiducial_coords[2])
    
    ###for some reason make_dig_montage put our channels in a different order than what we input###
    ###let's fix that. should be fine to just change coords and ch_names###
    for i_chan in range(len(all_coords)):
        montage_orig.dig[i_chan+3]['r'] = all_coords[i_chan]
        montage_orig.ch_names[i_chan] = all_labels[i_chan]
        
    ###add an extra channel for our triggers###
    boxy_labels.append('Markers')

    ###create info structure###
    info = mne.create_info(boxy_labels,srate,ch_types='fnirs_raw')
    info.update(dig=montage_orig.dig)
    
    ###get our fiducials and transform matrix from fsaverage###
    subjects_dir = op.dirname(fetch_fsaverage())
    fid_path = op.join(subjects_dir, 'fsaverage', 'bem', 'fsaverage-fiducials.fif')
    fiducials = read_fiducials(fid_path)
    trans = coregister_fiducials(info, fiducials[0], tol=0.02)
        
    ###remake montage using the transformed coordinates###
    all_coords_trans = apply_trans(trans,all_coords)
    all_chan_dict_trans = dict(zip(all_labels,all_coords_trans))
    fiducial_coords_trans = apply_trans(trans,fiducial_coords)
    
    ###make our montage###
    montage_trans = mne.channels.make_dig_montage(ch_pos=all_chan_dict_trans,coord_frame='head',
                                            nasion = fiducial_coords_trans[0],
                                            lpa = fiducial_coords_trans[1], 
                                            rpa = fiducial_coords_trans[2])
    
    ###let's fix montage order again###
    for i_chan in range(len(all_coords_trans)):
        montage_trans.dig[i_chan+3]['r'] = all_coords_trans[i_chan]
        montage_trans.ch_names[i_chan] = all_labels[i_chan]
    
    ###add data type and channel wavelength to info###
    info.update(dig=montage_trans.dig, trans=trans)

    ###place our coordinates and wavelengths for each channel###
    for i_chan in range(len(boxy_labels)-1):
        temp_chn = apply_trans(trans,boxy_coords[i_chan][0:3])
        temp_src = apply_trans(trans,boxy_coords[i_chan][3:6])
        temp_det = apply_trans(trans,boxy_coords[i_chan][6:9])
        temp_other = np.asarray(boxy_coords[i_chan][9:],dtype=np.float64)
        info['chs'][i_chan]['loc'] = test = np.concatenate((temp_chn, temp_src, 
                                                            temp_det, temp_other),axis=0)
    info['chs'][-1]['loc'] = np.zeros((12,))
    
    ###now combine our data types into a single array###
    all_data = np.append(raw_ac, np.append(raw_dc, raw_ph, axis=0),axis=0)
    
    ###add our markers to the data array based on filetype###
    if filetype == 'non-parsed':
        if type(digaux) is list and digaux != []:
            markers = digaux[np.arange(0,len(digaux),source_num)]
        else:
            markers = np.zeros(np.size(all_data,axis=1))
    elif filetype == 'parsed':
        markers = digaux  
    all_data = np.vstack((all_data, markers))
    
    ###create our raw data object###
    raw_data_obj = mne.io.RawArray(all_data, info)
    
    return raw_data_obj
    