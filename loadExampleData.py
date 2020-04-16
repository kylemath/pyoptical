import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import os
from itertools import compress
import mne

# Example from https://mne.tools/dev/auto_tutorials/preprocessing/plot_70_fnirs_processing.html

fnirs_data_folder = mne.datasets.fnirs_motor.data_path()
fnirs_raw_dir = os.path.join(fnirs_data_folder, 'Participant-1')

# MNE raw object - https://mne.tools/stable/generated/mne.io.Raw.html
raw_intensity = mne.io.read_raw_nirx(fnirs_raw_dir, verbose=True).load_data()
print("Raw imported data file: ", raw_intensity)

picks = mne.pick_types(raw_intensity.info, meg=False, fnirs=True)
print("Channels to pull out: ", picks)

dists = mne.preprocessing.nirs.source_detector_distances(
	raw_intensity.info, picks=picks)
print("Channel distances: ", dists)

raw_intensity.pick(picks[dists > 0.01])
print("Long enough channels: ", raw_intensity)

raw_intensity.plot(n_channels=len(raw_intensity.ch_names), 
					duration=500, show_scrollbars=False)

plt.show()