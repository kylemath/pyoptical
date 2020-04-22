import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne

boxy_file = "data/emm0311a.001"
mtg_file = "data/emm0311_good.mtg"
tol_file = "data/emm0311.tol"

all_data = boxy2mne(boxy_file, mtg_file, tol_file)
print(all_data['AC'])
print(all_data['DC'])
print(all_data['Ph'])
print(all_data['Dist'])