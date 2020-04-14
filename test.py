import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 

filename = "data/trigs001a.001"
data = pd.read_csv(filename, skiprows=188, sep='\t', index_col='time')

# data[["A-Ph1", "A-Ph2", "A-Ph3", "A-Ph4", "A-Ph5"]].plot()
# plt.show()

detectors = ['A', 'B', 'C', 'D']
fig, ax = plt.subplots()

count_chan = 0
sumchan = pd.Series(np.arange(len(data)))

# Load distance file
# Find short channels

for detector in detectors:
    for x in np.arange(32):
        thischan = detector + '-Ph' + str(x+1)
        # Normalize each channel
        tempchan = (data[thischan] - data[thischan].mean()) / data[thischan].std()
        count_chan = count_chan + 1
        sumchan.add(tempchan)
        # tempchan = data[thischan]

# Plot average of all channels

tempchan = tempchan / count_chan
tempchan.plot(ax=ax)
plt.show()

