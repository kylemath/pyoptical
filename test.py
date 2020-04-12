import pandas as pd 
import matplotlib.pyplot as plt

filename = "data/trigs001a.001"
data = pd.read_csv(filename, skiprows=188, sep='\t', index_col='time')
data[["A-Ph1", "A-Ph2", "A-Ph3", "A-Ph4", "A-Ph5"]].plot()
plt.show()

