import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 

filename = "data/trigs001a.001"
data = pd.read_csv(filename, skiprows=188, sep='\t', index_col='time')

# data[["A-Ph1", "A-Ph2", "A-Ph3", "A-Ph4", "A-Ph5"]].plot()
# plt.show()

detectors = ['A', 'B', 'C', 'D']
fig, ax = plt.subplots()


# Load distance file
# Find short channels

# Normalize each channel
for detector in detectors:
    for x in np.arange(32):
        thischan = detector + '-Ph' + str(x+1)
        tempchan = (data[thischan] - data[thischan].mean()) / data[thischan].std()

# Plot average of all channels
count_chan = 0
sumchan = pd.Series(np.arange(len(data)))
for detector in detectors:
    for x in np.arange(32):
        thischan = detector + '-Ph' + str(x+1)
        tempchan = (data[thischan] - data[thischan].mean()) / data[thischan].std()
        count_chan = count_chan + 1
        sumchan.add(tempchan)
tempchan = tempchan / count_chan
tempchan.plot(ax=ax)
plt.show()

# Unwrap Phase

# Remove pulse artifact


